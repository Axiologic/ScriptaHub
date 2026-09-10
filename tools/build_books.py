#!/usr/bin/env python3
"""Migrate the legacy book library into the prebuilt ``docs/books`` catalogue.

The migration deliberately has no network dependency.  It preserves every
published edition already available in ``old_content`` and creates localised
catalogue metadata for every supported interface language.  Run it from the
repository root:

    python3 tools/build_books.py build --source old_content
    python3 tools/build_books.py check

``build`` moves published files, so a successful run makes ``old_content``
obsolete.  The generated ``docs/collection.json`` is the canonical aggregate
for the browser catalogue; ``collection.js`` is a local-file-friendly mirror.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata
import uuid
from urllib.parse import unquote, urlencode
from urllib.request import Request, urlopen
import time


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BOOKS = DOCS / "books"
COLLECTION = DOCS / "collection.json"
COLLECTION_SCRIPT = DOCS / "collection.js"
LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "pt": "Português",
    "it": "Italiano",
    "ro": "Română",
    "pl": "Polski",
}
SOURCE_LANGUAGE_CODES = {code.upper(): code for code in LANGUAGES}


# The only authored keyword vocabulary: ten real-world shelf categories for
# each broad section. All remaining terms are extracted from each short read.
SHELF_CATEGORIES = {
    "technology": {
        "en": "artificial intelligence|machine learning|computer science|software engineering|information systems|data science|automation|software architecture|language models|digital technology",
        "fr": "intelligence artificielle|apprentissage automatique|informatique|génie logiciel|systèmes d’information|science des données|automatisation|architecture logicielle|modèles de langage|technologie numérique",
        "de": "künstliche Intelligenz|maschinelles Lernen|Informatik|Softwaretechnik|Informationssysteme|Datenwissenschaft|Automatisierung|Softwarearchitektur|Sprachmodelle|digitale Technologie",
        "es": "inteligencia artificial|aprendizaje automático|informática|ingeniería de software|sistemas de información|ciencia de datos|automatización|arquitectura de software|modelos de lenguaje|tecnología digital",
        "pt": "inteligência artificial|aprendizado de máquina|ciência da computação|engenharia de software|sistemas de informação|ciência de dados|automação|arquitetura de software|modelos de linguagem|tecnologia digital",
        "it": "intelligenza artificiale|apprendimento automatico|informatica|ingegneria del software|sistemi informativi|scienza dei dati|automazione|architettura software|modelli linguistici|tecnologia digitale",
        "ro": "inteligență artificială|învățare automată|informatică|inginerie software|sisteme informaționale|știința datelor|automatizare|arhitectură software|modele de limbaj|tehnologie digitală",
        "pl": "sztuczna inteligencja|uczenie maszynowe|informatyka|inżynieria oprogramowania|systemy informacyjne|nauka o danych|automatyzacja|architektura oprogramowania|modele językowe|technologia cyfrowa",
    },
    "science": {
        "en": "scientific research|research methods|scientific method|reproducibility|computational science|formal sciences|research infrastructure|knowledge engineering|scientific publishing|philosophy of science",
        "fr": "recherche scientifique|méthodes de recherche|méthode scientifique|reproductibilité|science informatique|sciences formelles|infrastructure de recherche|ingénierie des connaissances|édition scientifique|philosophie des sciences",
        "de": "wissenschaftliche Forschung|Forschungsmethoden|wissenschaftliche Methode|Reproduzierbarkeit|Computational Science|formale Wissenschaften|Forschungsinfrastruktur|Wissensengineering|wissenschaftliches Publizieren|Wissenschaftsphilosophie",
        "es": "investigación científica|métodos de investigación|método científico|reproducibilidad|ciencia computacional|ciencias formales|infraestructura de investigación|ingeniería del conocimiento|publicación científica|filosofía de la ciencia",
        "pt": "pesquisa científica|métodos de pesquisa|método científico|reprodutibilidade|ciência computacional|ciências formais|infraestrutura de pesquisa|engenharia do conhecimento|publicação científica|filosofia da ciência",
        "it": "ricerca scientifica|metodi di ricerca|metodo scientifico|riproducibilità|scienza computazionale|scienze formali|infrastruttura di ricerca|ingegneria della conoscenza|editoria scientifica|filosofia della scienza",
        "ro": "cercetare științifică|metode de cercetare|metodă științifică|reproductibilitate|știință computațională|științe formale|infrastructură de cercetare|ingineria cunoașterii|publicare științifică|filosofia științei",
        "pl": "badania naukowe|metody badawcze|metoda naukowa|odtwarzalność|nauka obliczeniowa|nauki formalne|infrastruktura badawcza|inżynieria wiedzy|publikowanie naukowe|filozofia nauki",
    },
    "fiction": {
        "en": "fiction|literature|science fiction|speculative fiction|philosophical fiction|literary fiction|future fiction|social fiction|technology fiction|idea-driven fiction",
        "fr": "fiction|littérature|science-fiction|fiction spéculative|fiction philosophique|fiction littéraire|fiction du futur|fiction sociale|fiction technologique|fiction d’idées",
        "de": "Fiktion|Literatur|Science-Fiction|spekulative Fiktion|philosophische Fiktion|literarische Fiktion|Zukunftsfiktion|soziale Fiktion|Technologiefiktion|Ideenroman",
        "es": "ficción|literatura|ciencia ficción|ficción especulativa|ficción filosófica|ficción literaria|ficción del futuro|ficción social|ficción tecnológica|ficción de ideas",
        "pt": "ficção|literatura|ficção científica|ficção especulativa|ficção filosófica|ficção literária|ficção do futuro|ficção social|ficção tecnológica|ficção de ideias",
        "it": "narrativa|letteratura|fantascienza|narrativa speculativa|narrativa filosofica|narrativa letteraria|narrativa del futuro|narrativa sociale|narrativa tecnologica|narrativa di idee",
        "ro": "ficțiune|literatură|science-fiction|ficțiune speculativă|ficțiune filosofică|ficțiune literară|ficțiune despre viitor|ficțiune socială|ficțiune tehnologică|ficțiune de idei",
        "pl": "fikcja|literatura|science fiction|fikcja spekulatywna|fikcja filozoficzna|fikcja literacka|fikcja przyszłości|fikcja społeczna|fikcja technologiczna|fikcja idei",
    },
    "philosophy": {
        "en": "philosophy|epistemology|ontology|logic|metaphysics|ethics|philosophy of science|philosophy of mind|political philosophy|social philosophy",
        "fr": "philosophie|épistémologie|ontologie|logique|métaphysique|éthique|philosophie des sciences|philosophie de l’esprit|philosophie politique|philosophie sociale",
        "de": "Philosophie|Erkenntnistheorie|Ontologie|Logik|Metaphysik|Ethik|Wissenschaftsphilosophie|Philosophie des Geistes|politische Philosophie|Sozialphilosophie",
        "es": "filosofía|epistemología|ontología|lógica|metafísica|ética|filosofía de la ciencia|filosofía de la mente|filosofía política|filosofía social",
        "pt": "filosofia|epistemologia|ontologia|lógica|metafísica|ética|filosofia da ciência|filosofia da mente|filosofia política|filosofia social",
        "it": "filosofia|epistemologia|ontologia|logica|metafisica|etica|filosofia della scienza|filosofia della mente|filosofia politica|filosofia sociale",
        "ro": "filosofie|epistemologie|ontologie|logică|metafizică|etică|filosofia științei|filosofia minții|filosofie politică|filosofie socială",
        "pl": "filozofia|epistemologia|ontologia|logika|metafizyka|etyka|filozofia nauki|filozofia umysłu|filozofia polityczna|filozofia społeczna",
    },
    "business": {
        "en": "business|management|entrepreneurship|innovation|economics|strategy|investment|digital business|organizational studies|technology management",
        "fr": "entreprise|gestion|entrepreneuriat|innovation|économie|stratégie|investissement|entreprise numérique|études organisationnelles|gestion technologique",
        "de": "Wirtschaft|Management|Unternehmertum|Innovation|Ökonomie|Strategie|Investition|digitales Geschäft|Organisationsforschung|Technologiemanagement",
        "es": "empresa|gestión|emprendimiento|innovación|economía|estrategia|inversión|negocio digital|estudios organizativos|gestión tecnológica",
        "pt": "negócios|gestão|empreendedorismo|inovação|economia|estratégia|investimento|negócios digitais|estudos organizacionais|gestão de tecnologia",
        "it": "impresa|gestione|imprenditorialità|innovazione|economia|strategia|investimento|impresa digitale|studi organizzativi|gestione della tecnologia",
        "ro": "afaceri|management|antreprenoriat|inovare|economie|strategie|investiții|afaceri digitale|studii organizaționale|managementul tehnologiei",
        "pl": "biznes|zarządzanie|przedsiębiorczość|innowacja|ekonomia|strategia|inwestowanie|biznes cyfrowy|studia organizacyjne|zarządzanie technologią",
    },
    "society": {
        "en": "social sciences|political science|sociology|governance|public policy|political economy|social theory|institutional studies|democracy|ethics",
        "fr": "sciences sociales|science politique|sociologie|gouvernance|politique publique|économie politique|théorie sociale|études institutionnelles|démocratie|éthique",
        "de": "Sozialwissenschaften|Politikwissenschaft|Soziologie|Governance|öffentliche Politik|politische Ökonomie|Sozialtheorie|Institutionenforschung|Demokratie|Ethik",
        "es": "ciencias sociales|ciencia política|sociología|gobernanza|política pública|economía política|teoría social|estudios institucionales|democracia|ética",
        "pt": "ciências sociais|ciência política|sociologia|governança|política pública|economia política|teoria social|estudos institucionais|democracia|ética",
        "it": "scienze sociali|scienza politica|sociologia|governance|politica pubblica|economia politica|teoria sociale|studi istituzionali|democrazia|etica",
        "ro": "științe sociale|științe politice|sociologie|guvernanță|politici publice|economie politică|teorie socială|studii instituționale|democrație|etică",
        "pl": "nauki społeczne|politologia|socjologia|zarządzanie publiczne|polityka publiczna|ekonomia polityczna|teoria społeczna|studia instytucjonalne|demokracja|etyka",
    },
}

SUBJECT_TAGS = {
    group: {
        language: {
            f"category-{index:02d}": label
            for index, label in enumerate(labels.split("|"), start=1)
        }
        for language, labels in localized.items()
    }
    for group, localized in SHELF_CATEGORIES.items()
}

# These are discovery domains, not site-administration labels.  Together with
# the ten subject tags above they produce 25 terms readers actually use to find
# a field, a method, a literary mode, or a societal problem.
TOPICS = {
    "en": {"technology": "intelligent and trustworthy technologies", "science": "research, evidence, and the systems that make knowledge usable", "fiction": "speculative futures, human choices, and technological change", "philosophy": "foundations, limits, and the conditions of reasoning", "business": "innovation, organizations, and economic change", "society": "institutions, freedom, power, and collective life"},
    "fr": {"technology": "les technologies intelligentes et dignes de confiance", "science": "la recherche, les preuves et les systèmes qui rendent le savoir utilisable", "fiction": "les futurs spéculatifs, les choix humains et le changement technologique", "philosophy": "les fondements, les limites et les conditions du raisonnement", "business": "l’innovation, les organisations et le changement économique", "society": "les institutions, la liberté, le pouvoir et la vie collective"},
    "de": {"technology": "intelligente und vertrauenswürdige Technologien", "science": "Forschung, Evidenz und Systeme für nutzbares Wissen", "fiction": "spekulative Zukünfte, menschliche Entscheidungen und technologischen Wandel", "philosophy": "Grundlagen, Grenzen und Bedingungen des Denkens", "business": "Innovation, Organisationen und wirtschaftlichen Wandel", "society": "Institutionen, Freiheit, Macht und gemeinschaftliches Leben"},
    "es": {"technology": "tecnologías inteligentes y fiables", "science": "investigación, evidencia y sistemas que hacen utilizable el conocimiento", "fiction": "futuros especulativos, decisiones humanas y cambio tecnológico", "philosophy": "fundamentos, límites y condiciones del razonamiento", "business": "innovación, organizaciones y cambio económico", "society": "instituciones, libertad, poder y vida colectiva"},
    "pt": {"technology": "tecnologias inteligentes e confiáveis", "science": "pesquisa, evidências e sistemas que tornam o conhecimento utilizável", "fiction": "futuros especulativos, escolhas humanas e mudança tecnológica", "philosophy": "fundamentos, limites e condições do raciocínio", "business": "inovação, organizações e mudança econômica", "society": "instituições, liberdade, poder e vida coletiva"},
    "it": {"technology": "tecnologie intelligenti e affidabili", "science": "ricerca, evidenza e sistemi che rendono utilizzabile la conoscenza", "fiction": "futuri speculativi, scelte umane e cambiamento tecnologico", "philosophy": "fondamenti, limiti e condizioni del ragionamento", "business": "innovazione, organizzazioni e cambiamento economico", "society": "istituzioni, libertà, potere e vita collettiva"},
    "ro": {"technology": "tehnologii inteligente și de încredere", "science": "cercetare, dovezi și sisteme care fac cunoașterea utilizabilă", "fiction": "viitoruri speculative, alegeri umane și schimbare tehnologică", "philosophy": "fundamente, limite și condițiile raționării", "business": "inovare, organizații și schimbare economică", "society": "instituții, libertate, putere și viață colectivă"},
    "pl": {"technology": "inteligentne i godne zaufania technologie", "science": "badania, dowody i systemy czyniące wiedzę użyteczną", "fiction": "spekulatywne przyszłości, ludzkie wybory i zmianę technologiczną", "philosophy": "podstawy, granice i warunki rozumowania", "business": "innowacje, organizacje i zmianę gospodarczą", "society": "instytucje, wolność, władzę i życie zbiorowe"},
}

ABOUT_BOOK_TITLES = {
    "en": "About Book",
    "fr": "À propos du livre",
    "de": "Über das Buch",
    "es": "Sobre el libro",
    "pt": "Sobre o livro",
    "it": "Il libro",
    "ro": "Despre carte",
    "pl": "O książce",
}

COPY = {
    "en": {"home": "Library", "description": "{title} is an Axiologic Research book about {topic}, made for readers who want to examine an idea rather than merely consume a summary.", "read": "Read Online", "short": "Read in 10 Min", "download": "Download PDF", "unavailable": "This reading edition is not yet available in {language}.", "available": "Available in", "keywords": "Keywords", "keywordCloudNote": "Larger terms occur in more books across the library.", "back": "Back to library"},
    "fr": {"home": "Bibliothèque", "description": "{title} est un livre d’Axiologic Research sur {topic}, conçu pour les lecteurs qui veulent examiner une idée plutôt que consommer un simple résumé.", "read": "Lire en ligne", "short": "Lire en 10 min", "download": "Télécharger le PDF", "unavailable": "Cette édition de lecture n’est pas encore disponible en {language}.", "available": "Disponible en", "keywords": "Mots-clés", "keywordCloudNote": "Les termes plus grands apparaissent dans davantage de livres de la bibliothèque.", "back": "Retour à la bibliothèque"},
    "de": {"home": "Bibliothek", "description": "{title} ist ein Buch von Axiologic Research über {topic}, für Leserinnen und Leser, die eine Idee prüfen statt nur eine Zusammenfassung zu konsumieren.", "read": "Online lesen", "short": "In 10 Min. lesen", "download": "PDF herunterladen", "unavailable": "Diese Leseausgabe ist noch nicht auf {language} verfügbar.", "available": "Verfügbar in", "keywords": "Schlagwörter", "keywordCloudNote": "Größere Begriffe kommen in mehr Büchern der Bibliothek vor.", "back": "Zur Bibliothek"},
    "es": {"home": "Biblioteca", "description": "{title} es un libro de Axiologic Research sobre {topic}, pensado para lectores que quieren examinar una idea y no solo consumir un resumen.", "read": "Leer en línea", "short": "Leer en 10 min", "download": "Descargar PDF", "unavailable": "Esta edición de lectura todavía no está disponible en {language}.", "available": "Disponible en", "keywords": "Palabras clave", "keywordCloudNote": "Los términos más grandes aparecen en más libros de la biblioteca.", "back": "Volver a la biblioteca"},
    "pt": {"home": "Biblioteca", "description": "{title} é um livro da Axiologic Research sobre {topic}, feito para leitores que querem examinar uma ideia em vez de apenas consumir um resumo.", "read": "Ler online", "short": "Ler em 10 min", "download": "Baixar PDF", "unavailable": "Esta edição de leitura ainda não está disponível em {language}.", "available": "Disponível em", "keywords": "Palavras-chave", "keywordCloudNote": "Termos maiores aparecem em mais livros da biblioteca.", "back": "Voltar à biblioteca"},
    "it": {"home": "Biblioteca", "description": "{title} è un libro di Axiologic Research su {topic}, pensato per chi vuole esaminare un’idea anziché consumare solo un riassunto.", "read": "Leggi online", "short": "Leggi in 10 min", "download": "Scarica il PDF", "unavailable": "Questa edizione di lettura non è ancora disponibile in {language}.", "available": "Disponibile in", "keywords": "Parole chiave", "keywordCloudNote": "I termini più grandi compaiono in più libri della biblioteca.", "back": "Torna alla biblioteca"},
    "ro": {"home": "Bibliotecă", "description": "{title} este o carte Axiologic Research despre {topic}, pentru cititori care vor să examineze o idee, nu doar să consume un rezumat.", "read": "Citește online", "short": "Citește în 10 min", "download": "Descarcă PDF", "unavailable": "Această ediție de lectură nu este încă disponibilă în {language}.", "available": "Disponibil în", "keywords": "Cuvinte-cheie", "keywordCloudNote": "Termenii mai mari apar în mai multe cărți din bibliotecă.", "back": "Înapoi la bibliotecă"},
    "pl": {"home": "Biblioteka", "description": "{title} to książka Axiologic Research o {topic}, dla czytelników, którzy chcą zbadać ideę, a nie tylko przeczytać streszczenie.", "read": "Czytaj online", "short": "Czytaj w 10 min", "download": "Pobierz PDF", "unavailable": "To wydanie do czytania nie jest jeszcze dostępne po {language}.", "available": "Dostępne w", "keywords": "Słowa kluczowe", "keywordCloudNote": "Większe terminy występują w większej liczbie książek w bibliotece.", "back": "Wróć do biblioteki"},
}

# Keep the compact book-page widget descriptive without stealing attention from
# the book itself.  The visual size already communicates the same idea.
for _language, _note in {
    "en": "Size follows global frequency.",
    "fr": "La taille suit l’usage.",
    "de": "Größe folgt globaler Häufigkeit.",
    "es": "El tamaño sigue frecuencia.",
    "pt": "Tamanho segue frequência global.",
    "it": "Dimensione segue frequenza globale.",
    "ro": "Mărimea urmează frecvența globală.",
    "pl": "Rozmiar odzwierciedla częstotliwość.",
}.items():
    COPY[_language]["keywordCloudNote"] = _note

for _language in COPY:
    COPY[_language]["description"] = COPY[_language]["description"].replace("Axiologic Research", "ScriptaHub")

CLOUD_INSTRUCTIONS = {
    "en": "drag to rotate · Ctrl-drag to move · scroll to zoom", "fr": "glisser pour tourner · Ctrl-glisser pour déplacer · défiler pour zoomer",
    "de": "ziehen zum Drehen · Strg-Ziehen zum Verschieben · scrollen zum Zoomen", "es": "arrastra para girar · Ctrl-arrastrar para mover · desplázate para ampliar",
    "pt": "arraste para girar · Ctrl-arraste para mover · role para ampliar", "it": "trascina per ruotare · Ctrl-trascina per spostare · scorri per ingrandire",
    "ro": "trage pentru rotire · Ctrl-trage pentru deplasare · derulează pentru zoom", "pl": "przeciągnij, aby obrócić · Ctrl-przeciągnij, aby przesunąć · przewiń, aby przybliżyć",
}

CLOUD_PREVIEW_INSTRUCTIONS = {
    "en": "click to enlarge", "fr": "cliquez pour agrandir", "de": "zum Vergrößern klicken", "es": "haz clic para ampliar",
    "pt": "clique para ampliar", "it": "clicca per ingrandire", "ro": "apasă pentru mărire", "pl": "kliknij, aby powiększyć",
}

CLOUD_CLOSE_LABELS = {
    "en": "Close keyword cloud", "fr": "Fermer le nuage de mots-clés", "de": "Schlagwortwolke schließen", "es": "Cerrar nube de palabras clave",
    "pt": "Fechar nuvem de palavras-chave", "it": "Chiudi nuvola di parole chiave", "ro": "Închide norul de cuvinte-cheie", "pl": "Zamknij chmurę słów kluczowych",
}

BOOK_ACTIONS = {
    "en": {"create": "Create", "feedback": "Suggest An Edit", "editions": "Editions", "initial": "Initial ScriptaHub edition.", "editionLabel": "Edition 1"},
    "fr": {"create": "Créer", "feedback": "Proposer une modification", "editions": "Éditions", "initial": "Première édition ScriptaHub.", "editionLabel": "Édition 1"},
    "de": {"create": "Erstellen", "feedback": "Änderung vorschlagen", "editions": "Ausgaben", "initial": "Erste ScriptaHub-Ausgabe.", "editionLabel": "Ausgabe 1"},
    "es": {"create": "Crear", "feedback": "Proponer un cambio", "editions": "Ediciones", "initial": "Primera edición de ScriptaHub.", "editionLabel": "Edición 1"},
    "pt": {"create": "Criar", "feedback": "Sugerir alteração", "editions": "Edições", "initial": "Primeira edição ScriptaHub.", "editionLabel": "Edição 1"},
    "it": {"create": "Crea", "feedback": "Proponi una modifica", "editions": "Edizioni", "initial": "Prima edizione ScriptaHub.", "editionLabel": "Edizione 1"},
    "ro": {"create": "Creează", "feedback": "Propune o modificare", "editions": "Ediții", "initial": "Ediția inițială ScriptaHub.", "editionLabel": "Ediția 1"},
    "pl": {"create": "Utwórz", "feedback": "Zaproponuj zmianę", "editions": "Wydania", "initial": "Pierwsze wydanie ScriptaHub.", "editionLabel": "Wydanie 1"},
}


def theme_switcher() -> str:
    """Compact shared control: symbols avoid taking header space in any locale."""
    return '<div class="theme-switcher"><button type="button" data-theme-toggle aria-label="Switch to dark appearance">☼</button></div>'


def site_footer(start: Path, language: str) -> str:
    legal = relpath(DOCS / "legal", start)
    links = (
        ("terms.html", "terms", "Terms"),
        ("privacy.html", "privacy", "Privacy"),
        ("cookies.html", "cookies", "Cookies & local storage"),
        ("notice.html", "notice", "Legal notice"),
        ("ai.html", "ai", "AI transparency"),
    )
    navigation = "".join(
        f'<a data-footer-{key} data-legal-link href="{html.escape(f"{legal}/{page}?lang={language}", quote=True)}">{html.escape(label)}</a>'
        for page, key, label in links
    )
    return f'<footer class="site-footer"><a class="footer-wordmark" href="{html.escape(relpath(DOCS / "index.html", start))}">ScriptaHub.com</a><nav aria-label="Legal">{navigation}</nav><span class="footer-status">© 2026 ScriptaHub</span></footer>'


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", normalized)) or "keyword"


def relpath(target: Path, start: Path) -> str:
    return Path(os.path.relpath(target, start)).as_posix()


def clean_fragment(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def keyword_source_text(page: Path) -> str:
    """Extract a reader for keyword scoring and give section headings weight."""
    source = page.read_text(encoding="utf-8", errors="ignore")
    source = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.IGNORECASE | re.DOTALL)
    main_match = re.search(r"<main\b[^>]*>(.*?)</main>", source, flags=re.IGNORECASE | re.DOTALL)
    source = main_match.group(1) if main_match else source
    source = re.sub(r"<figure\b[^>]*>.*?</figure>", " ", source, flags=re.IGNORECASE | re.DOTALL)
    source = re.sub(
        r"<p\b[^>]*>(?:(?!</p>).)*(?:KDP|publishing rights|Author(?:&#x27;|&apos;|’|')s Note|available for free|ScriptaHub|all (?:the )?free books|Venture Studio)(?:(?!</p>).)*</p>",
        " ", source, flags=re.IGNORECASE | re.DOTALL,
    )
    source = re.sub(
        r"<section\b[^>]*>\s*<h[1-4]\b[^>]*>\s*(?:why\s+read|reading\s+the\s+complete)[^<]*</h[1-4]>.*?</section>",
        " ", source, flags=re.IGNORECASE | re.DOTALL,
    )
    headings = [clean_fragment(value) for value in re.findall(r"<h[1-4]\b[^>]*>(.*?)</h[1-4]>", source, flags=re.IGNORECASE | re.DOTALL)]
    headings = [
        value for value in headings
        if keyword_normalise(value).strip() not in {
            "content", "contents", "copyright", "author notes", "authors notes",
            "references", "bibliography", "selective bibliography",
        }
        and not keyword_normalise(value).strip().startswith("copyright ")
    ]
    # Preserve semantic boundaries.  Without punctuation, a heading followed
    # by a table cell could become a fabricated phrase such as
    # ``content methodological`` even though it never occurs in the book.
    source = re.sub(
        r"</(?:address|article|aside|blockquote|caption|dd|div|dl|dt|figcaption|footer|h[1-6]|header|li|main|nav|p|section|td|th|tr)\s*>",
        ". ", source, flags=re.IGNORECASE,
    )
    # Repetition is deliberate: headings usually name the question a reader
    # would search, while navigation/footer boilerplate should not outrank it.
    return ". ".join([*(headings * 5), clean_fragment(source)])


def one(pattern: str, source: str, label: str, page: Path) -> str:
    match = re.search(pattern, source, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError(f"Missing {label} in {page}")
    return clean_fragment(match.group(1))


def parse_book_page(page: Path) -> dict[str, str]:
    source = page.read_text(encoding="utf-8")
    cover = unquote(one(r'class="[^"]*\bedition-cover\b[^"]*"[^>]*\bsrc="[^"]*/([^/"\s]+)"', source, "cover", page))
    description = one(r'<p\s+class="edition-why"[^>]*>(.*?)</p>', source, "description", page)
    subtitle_match = re.search(r'<p\s+class="edition-subtitle"[^>]*>(.*?)</p>', source, flags=re.IGNORECASE | re.DOTALL)
    return {
        "title": one(r"<h1[^>]*>(.*?)</h1>", source, "title", page),
        # A few legacy editions deliberately have no marketing subtitle. Keep
        # a meaningful record rather than dropping the book from the catalogue.
        "subtitle": clean_fragment(subtitle_match.group(1)) if subtitle_match else "Axiologic Research Edition",
        "description": description,
        "category": one(r'<p\s+class="eyebrow edition-kicker"[^>]*>(.*?)</p>', source, "category", page).replace(" · Axiologic Research Editions", ""),
        "cover": cover,
    }


def subject_group(category: str, title: str, description: str = "") -> str:
    """Classify the subject, using the editorial synopsis when a category is broad."""
    sample = f"{category} {title} {description}".lower()
    if any(token in sample for token in ("literature", "literary", "science fiction", "cosmic", "political & social sf", "human & philosophical sf", "philosophical fiction", "speculative fiction")):
        return "fiction"
    if any(token in sample for token in ("business", "startups", "investment", "economy")):
        return "business"
    if category.lower() == "essay" and any(token in sample for token in ("market", "profitable", "subscription", "willingness to pay")):
        return "business"
    if any(token in sample for token in ("outfinit", "mathematics", "meta-rational", "philosophy", "meaning")):
        return "philosophy"
    if any(token in sample for token in ("power", "institutions", "society", "civilization", "civilisation", "social", "anthropology", "emotion")):
        return "society"
    if any(token in sample for token in ("research", "science", "executable", "experiments")):
        return "science"
    return "technology"


def keyword_normalise(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold()).encode("ascii", "ignore").decode("ascii")
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value)).strip() + " "


def keyword_identifier(label: str) -> str:
    normalized = keyword_normalise(label).strip()
    return "term:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:20]


ENGLISH_STOP_WORDS = frozenset("""
a about above across after afterwards again against all almost alone along already also although always am among
an and another any anyone anything are around as at be became because become becomes been before behind being below
beside between beyond both but by can cannot could did do does doing done down during each either else enough even ever
every everyone everything few first for from further get gets getting give given gives go goes had has have having he
hence her here hers herself him himself his how however i if in indeed into is it its itself just keep kind last least
less like made make makes many may me might mine more most mostly much must my myself neither never no nobody none nor
not nothing now of off often on once one only or other others otherwise our ours ourselves out over own perhaps rather
same second several she should since so some someone something still such than that the their theirs them themselves
then there therefore these they thing things this those though through throughout thus to together too toward under
unless until up upon us use used using very via was we well were what whatever when where whether which while who whom
whose why will with within without would yet you your yours yourself yourselves
""".split())

KEYWORD_NOISE_WORDS = frozenset("""
acknowledgements appendix author book chapter conclusion contents copyright edition example examples figure figures
footnote introduction note notes page pages part preface reader readers reading references section sections scripta
scriptahub summary table text volume complete minute minutes online original opening synthesis publishing website kdp
alboaie sinica
""".split())


def keyword_catalog(group: str) -> list[tuple[str, str, dict[str, str]]]:
    """Return the ten deliberately broad, library-shelf categories."""
    return [
        (
            keyword_identifier(SUBJECT_TAGS[group]["en"][key]),
            key,
            {language: SUBJECT_TAGS[group][language][key] for language in LANGUAGES},
        )
        for key in SUBJECT_TAGS[group]["en"]
    ]


def _keyword_tokens(value: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9]*(?:[-’'][A-Za-z0-9]+)*|[A-Z]{2,8}", value)


def _keyword_label(tokens: list[str]) -> str:
    acronyms = {"ai", "agi", "api", "cpu", "gpu", "llm", "ml", "nlp", "rag", "rl", "ui", "ux"}
    words = []
    for token in tokens:
        if token.lower() in acronyms:
            words.append(token.upper())
        else:
            words.append(token.lower())
    return " ".join(words)


def extract_keyword_candidates(
    title: str, description: str, source_text: str, limit: int = 140,
) -> list[str]:
    """Rank noun phrases found verbatim in a book's short edition.

    Only grammar, stop words, and document structure live in code. Subject
    vocabulary comes from the edition itself. Headings are weighted by
    keyword_source_text; the synopsis can boost existing phrases, not add them.
    """
    try:
        import nltk
    except ImportError as error:
        raise RuntimeError(
            "Keyword extraction needs NLTK; install tools/requirements-keywords.txt"
        ) from error

    weighted = source_text
    title_key = keyword_normalise(title).strip()
    title_terms = {
        token for token in title_key.split()
        if token not in ENGLISH_STOP_WORDS and len(token) > 2
    }
    counts: Counter[str] = Counter()
    surfaces: dict[str, Counter[str]] = {}
    connectors = {"and", "of", "for", "in", "on", "with", "without", "between", "under", "after", "before", "through"}
    sentences = [sentence for sentence in nltk.sent_tokenize(weighted) if sentence.strip()]
    tagged_sentences = nltk.pos_tag_sents([nltk.word_tokenize(sentence) for sentence in sentences])

    def content_token(token: str, tag: str) -> bool:
        lower = keyword_normalise(token).strip()
        return (
            bool(lower)
            and lower not in ENGLISH_STOP_WORDS
            and lower not in KEYWORD_NOISE_WORDS
            and not lower.startswith(("scriptahub", "axiologic", "achilles"))
            and (
                tag.startswith("NN")
                or tag.startswith("JJ")
                or tag in {"VBG", "VBN", "FW"}
                or (token.isupper() and 2 <= len(token) <= 8)
            )
        )

    for tagged in tagged_sentences:
        for start, (token, tag) in enumerate(tagged):
            if not content_token(token, tag):
                continue
            chunk: list[str] = []
            noun_count = 0
            content_count = 0
            for end in range(start, min(len(tagged), start + 7)):
                current, current_tag = tagged[end]
                lower = keyword_normalise(current).strip()
                if content_token(current, current_tag):
                    chunk.append(current)
                    content_count += 1
                    if current_tag.startswith("NN") or (current.isupper() and len(current) >= 2):
                        noun_count += 1
                elif (
                    lower in connectors
                    and chunk
                    and end + 1 < len(tagged)
                    and content_token(*tagged[end + 1])
                ):
                    chunk.append(lower)
                else:
                    break
                if len(chunk) > 5:
                    break
                if content_count < 2 or noun_count < 1:
                    continue
                gerund_noun = current_tag == "VBG" and len(chunk) >= 2 and chunk[-2].casefold() not in connectors
                if not (
                    current_tag.startswith("NN")
                    or current_tag == "FW"
                    or gerund_noun
                    or (current.isupper() and len(current) >= 2)
                ):
                    continue
                label = _keyword_label(chunk)
                key = keyword_normalise(label).strip()
                if key == title_key or len(label) < 5 or len(label) > 68:
                    continue
                key_terms = {
                    item for item in key.split()
                    if item not in ENGLISH_STOP_WORDS and len(item) > 2
                }
                if key_terms and key_terms <= title_terms:
                    continue
                counts[key] += 1
                surfaces.setdefault(key, Counter())[label] += 1

    scored = []
    synopsis_key = keyword_normalise(description)
    for key, frequency in counts.items():
        tokens = key.split()
        length = len(tokens)
        phrase = surfaces[key].most_common(1)[0][0]
        synopsis_boost = 18 if keyword_normalise(phrase) in synopsis_key else 0
        acronym_boost = 5 if any(part.casefold() in {"ai", "agi", "api", "cpu", "gpu", "llm", "ml", "nlp", "rag", "rl"} for part in phrase.split()) else 0
        length_boost = {2: 13, 3: 18, 4: 16, 5: 10}.get(min(length, 5), 4)
        repetition = min(frequency, 12) * (3.4 + length * .62)
        specificity = sum(min(len(token), 13) for token in tokens) / max(length, 1)
        score = repetition + length_boost + synopsis_boost + acronym_boost + specificity
        scored.append((score, frequency, length, key, phrase))

    selected: list[str] = []
    selected_token_sets: list[set[str]] = []
    prefix_counts: Counter[tuple[str, ...]] = Counter()
    for _, _, _, key, phrase in sorted(scored, key=lambda row: (-row[0], -row[1], -row[2], row[3])):
        token_set = set(key.split())
        if any(len(token_set & prior) / max(len(token_set | prior), 1) > .72 for prior in selected_token_sets):
            continue
        prefix = tuple(key.split()[:2])
        if prefix_counts[prefix] >= 2:
            continue
        selected.append(phrase)
        selected_token_sets.append(token_set)
        prefix_counts[prefix] += 1
        if len(selected) >= limit:
            break

    if len(selected) < min(90, limit):
        present = {keyword_normalise(item).strip() for item in selected}
        for _, _, _, key, phrase in sorted(scored, key=lambda row: (-row[0], -row[1], -row[2], row[3])):
            if key in present:
                continue
            selected.append(phrase)
            present.add(key)
            if len(selected) >= limit:
                break
    return selected


def keyword_data(
    group: str, title: str = "", description: str = "", source_text: str = "",
) -> tuple[list[str], dict[str, list[str]]]:
    """Create 10 broad shelf labels plus 90 phrases extracted from the book."""
    broad = keyword_catalog(group)
    shelf_terms = {
        keyword_normalise(label).strip()
        for localized in SHELF_CATEGORIES.values()
        for label in localized["en"].split("|")
    }
    phrases = [
        phrase for phrase in extract_keyword_candidates(title, description, source_text, 140)
        if keyword_normalise(phrase).strip() not in shelf_terms
    ][:90]
    if len(phrases) < 90:
        raise ValueError(f"{title or group} yielded only {len(phrases)} source-derived keywords")
    identifiers = [identifier for identifier, _, _ in broad]
    identifiers.extend(
        keyword_identifier(phrase)
        for phrase in phrases
    )
    localized = {
        language: [labels[language] for _, _, labels in broad] + phrases
        for language in LANGUAGES
    }
    return identifiers, localized


def title_route(title: str) -> tuple[str, ...]:
    """One lower-case folder per title word; never use taxonomy as a path."""
    return tuple(slugify(title).split("-"))


def random_book_id() -> str:
    """Create the actual random postfix that keeps equally named books apart."""
    return "bk-" + uuid.uuid4().hex[:16]


def transfer(source: Path, destination: Path) -> bool:
    """Move one known source safely; permit an idempotent rerun."""
    if destination.exists():
        return False
    if not source.exists():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    return True


def hardlink_or_copy(source: Path, destination: Path) -> None:
    if destination.exists():
        return
    try:
        os.link(source, destination)
    except OSError:
        shutil.copy2(source, destination)


def create_display_cover(source: Path, destination: Path) -> None:
    """Create the portrait cover used by the catalogue and book page.

    Legacy ``cover.png`` files are source artwork, not consistently shaped web
    covers: several include an empty transparent/white/black canvas beside the
    actual cover.  Keeping that canvas and fitting it into a 2:3 slot makes the
    book look like a tiny icon.  The derived WebP trims the outer canvas and
    makes a portrait crop once, during generation.  Thumbnails remain the
    lightweight image used only in catalogue lists.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [
                "convert", str(source), "-fuzz", "3%", "-trim", "+repage",
                "-resize", "640x960^", "-gravity", "center", "-extent", "640x960",
                "-quality", "90", str(destination),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        # A useful cover is more important than an optional conversion tool.
        # The catalogue CSS still treats this fallback as a portrait object.
        shutil.copy2(source, destination)


def create_thumbnail(source: Path, destination: Path) -> None:
    """Create the exact 2:3 WebP used by catalogue cards.

    Card artwork must not inherit a legacy export canvas or a near-portrait
    ratio that leaves pale seams around the image.  It is derived from the
    already-normalised display cover, never directly from a PDF page.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [
                "convert", str(source), "-resize", "320x480!", "-strip",
                "-quality", "84", str(destination),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        shutil.copy2(source, destination)


def set_html_language_and_paths(path: Path, language: str, pdf_name: str | None) -> None:
    """Repair old relative reader/PDF links after relocating an edition."""
    source = path.read_text(encoding="utf-8")
    reader_path = relpath(DOCS / "reader", path.parent)
    source = re.sub(
        r'(["\'])(?:\.\./)+reader/',
        lambda match: f'{match.group(1)}{reader_path}/',
        source,
    )
    if pdf_name:
        source = re.sub(r'(["\'])(?:\.\./)+EN/[^"\']+\.pdf', lambda match: f'{match.group(1)}{pdf_name}', source)
    if re.search(r"<html\b[^>]*\blang=", source, re.IGNORECASE):
        source = re.sub(r'(<html\b[^>]*\blang=["\'])[^"\']*', rf'\g<1>{language}', source, count=1, flags=re.IGNORECASE)
    else:
        source = re.sub(r"<html\b", f'<html lang="{language}"', source, count=1, flags=re.IGNORECASE)
    path.write_text(source, encoding="utf-8")


LEGACY_READER_HTML = re.compile(
    r'(?P<quote>["\'])(?P<path>[^"\']*htmls/[A-Za-z]{2}/[^"\']+\.html)(?P=quote)',
    flags=re.IGNORECASE,
)
LEGACY_READER_ASSET = re.compile(
    r'(?P<quote>["\'])(?P<path>[^"\']*(?:(?:htmls/[A-Za-z]{2}/)|(?:[./]+(?:EN|FR|DE|ES|PT|IT|RO|PL)/))[^"\']+\.assets/(?P<filename>[^/"\']+))(?P=quote)',
    flags=re.IGNORECASE,
)


def repair_reader_links() -> int:
    """Replace legacy reader targets with their files in the migrated book tree.

    Old short editions point at ``content/htmls/<language>/…`` and some PDF
    figures use the same prefix.  Both are invalid once an edition lives beside
    its own full HTML and assets.  This intentionally handles only those known
    migration patterns; the separate link auditor catches every other problem.
    """
    changed = 0
    for page in sorted(BOOKS.glob("**/*.html")):
        if page.name not in {"full_content.html", "short_content.html"} and not page.name.endswith(".previous.html"):
            continue
        source = page.read_text(encoding="utf-8")
        book_root = page.parent.parent

        def replace_html(match: re.Match[str]) -> str:
            target = "full_content.html" if (page.parent / "full_content.html").is_file() else "book.html"
            return f'{match.group("quote")}{target}{match.group("quote")}'

        def replace_asset(match: re.Match[str]) -> str:
            legacy_path = match.group("path")
            filename = match.group("filename")
            language_match = re.search(r'(?:htmls/|/)(EN|FR|DE|ES|PT|IT|RO|PL)/', legacy_path, flags=re.IGNORECASE)
            preferred = book_root / language_match.group(1).lower() if language_match else page.parent
            candidates = sorted(preferred.rglob(filename)) if preferred.is_dir() else []
            if not candidates:
                candidates = sorted(book_root.rglob(filename))
            if not candidates:
                return match.group(0)
            return f'{match.group("quote")}{relpath(candidates[0], page.parent)}{match.group("quote")}'

        repaired = LEGACY_READER_HTML.sub(replace_html, source)
        repaired = LEGACY_READER_ASSET.sub(replace_asset, repaired)
        if repaired != source:
            page.write_text(repaired, encoding="utf-8")
            changed += 1
    return changed


def edition_record(book_root: Path, language: str) -> dict[str, str]:
    folder = book_root / language
    display_cover = "cover.webp" if (folder / "cover.webp").is_file() else "cover.png"
    record = {"book": (Path(language) / "book.html").as_posix(), "cover": (Path(language) / display_cover).as_posix(), "sourceCover": (Path(language) / "cover.png").as_posix(), "thumbnail": (Path(language) / "thumbnail.webp").as_posix()}
    for filename, key in (("full_content.html", "fullContent"), ("short_content.html", "shortContent"), ("book.pdf", "pdf")):
        if (folder / filename).is_file():
            record[key] = (Path(language) / filename).as_posix()
    return record


def snapshot_edition_covers(book_root: Path, edition: dict, source_root: Path | None = None, refresh_pending: bool = False) -> None:
    """Give each edition independent artwork paths; published snapshots are immutable."""
    source_root = source_root or book_root
    replace = refresh_pending and edition.get("status") == "preparing"
    covers = edition.setdefault("covers", {})
    for language in LANGUAGES:
        source = next((source_root / language / name for name in ("cover.webp", "cover.png") if (source_root / language / name).is_file()), None)
        if source is None or (language in covers and not replace):
            continue
        destination = book_root / "edition-files" / edition["id"] / "covers" / f"{language}{source.suffix}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        if replace or not destination.exists():
            shutil.copy2(source, destination)
        covers[language] = destination.relative_to(book_root).as_posix()


def ensure_editions_file(book_root: Path, manifest: dict[str, object]) -> None:
    """Create or gently extend a book's durable edition history.

    Existing edition entries are never removed or rewritten here. Future
    publishing code must archive a replaced PDF and add a new record; this
    helper only establishes the initial edition and fills absent current PDF
    language links.
    """
    path = book_root / "editions.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        payload = {}
    records = payload.get("editions") if isinstance(payload.get("editions"), list) else []
    if manifest.get("publicationStatus") == "preparing" and records and not payload.get("currentEdition"):
        return
    current_id = str(payload.get("currentEdition") or "edition-1")
    current = next((entry for entry in records if isinstance(entry, dict) and entry.get("id") == current_id), None)
    if current is None:
        manifest_mtime = (book_root / "manifest.json").stat().st_mtime if (book_root / "manifest.json").is_file() else time.time()
        current = {
            "id": current_id,
            "number": 1,
            "label": {language: BOOK_ACTIONS[language]["editionLabel"] for language in LANGUAGES},
            "publishedAt": datetime.fromtimestamp(manifest_mtime, timezone.utc).date().isoformat(),
            "changes": {language: BOOK_ACTIONS[language]["initial"] for language in LANGUAGES},
            "pdf": {},
        }
        records.append(current)
    current.setdefault("pdf", {})
    for language, edition in manifest.get("editions", {}).items():
        if isinstance(edition, dict) and edition.get("pdf") and language not in current["pdf"]:
            current["pdf"][language] = edition["pdf"]
    snapshot_edition_covers(book_root, current)
    payload.update({
        "schemaVersion": 1,
        "bookId": manifest.get("id"),
        "currentEdition": current_id,
        "editions": records,
    })
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reader_href(book: dict[str, object], language: str, page_path: Path, format_name: str, ui_language: str | None = None) -> str:
    """Build a local-reader URL with a stable progress identity and locale."""
    ui_language = ui_language or language
    edition = book["editions"][language]
    content_key = "shortContent" if format_name == "short" else "fullContent"
    if content_key not in edition:
        raise ValueError(f"{book['id']} has no {format_name} reader edition in {language}")
    reader_directory = DOCS / "reader"
    book_directory = DOCS / str(book["directory"])
    params = {
        "id": f"{book['id']}:{book.get('currentEdition', 'edition-1')}:{language}:{format_name}",
        "title": f"{book['title'][language]} · {COPY[ui_language][format_name]}",
        "html": relpath(book_directory / str(edition[content_key]), reader_directory),
        "mode": "ten-minute" if format_name == "short" else "full",
        "back": relpath(page_path, reader_directory) + "?" + urlencode({"lang": ui_language}),
        "book": str(book["directory"]),
        "language": language,
        "lang": ui_language,
        "format": format_name,
    }
    english_pdf = book["editions"].get("en", {}).get("pdf")
    if english_pdf:
        params["pdf"] = relpath(book_directory / str(english_pdf), reader_directory)
    return f'{relpath(reader_directory / "index.html", page_path.parent)}?{urlencode(params)}'


PREPARATION_LABELS = {
    "en": ("In preparation", "A new edition is in preparation. The published edition remains available."),
    "fr": ("En préparation", "Une nouvelle édition est en préparation. L’édition publiée reste disponible."),
    "de": ("In Vorbereitung", "Eine neue Ausgabe wird vorbereitet. Die veröffentlichte Ausgabe bleibt verfügbar."),
    "es": ("En preparación", "Se está preparando una nueva edición. La edición publicada sigue disponible."),
    "pt": ("Em preparação", "Uma nova edição está em preparação. A edição publicada continua disponível."),
    "it": ("In preparazione", "Una nuova edizione è in preparazione. L’edizione pubblicata resta disponibile."),
    "ro": ("În lucru", "O ediție nouă este în lucru. Ediția publicată rămâne disponibilă."),
    "pl": ("W przygotowaniu", "Nowe wydanie jest w przygotowaniu. Opublikowane wydanie pozostaje dostępne."),
}


def translation_href(book: dict[str, object], language: str, page_path: Path, format_name: str) -> str:
    query = urlencode({"book": book["directory"], "target": language, "format": format_name, "lang": language})
    return f'{relpath(DOCS / "translate" / "index.html", page_path.parent)}?{query}'


def about_book_section(book: dict[str, object], language: str) -> str:
    """Render the authored landing-page copy; reader editions are separate."""
    localized = book.get("aboutBook")
    paragraphs = localized.get(language) if isinstance(localized, dict) else None
    if (
        not isinstance(paragraphs, list) or not 2 <= len(paragraphs) <= 4
        or any(not isinstance(text, str) or not text.strip() for text in paragraphs)
    ):
        raise ValueError(f"{book['id']} {language}: aboutBook needs 2–4 authored paragraphs")
    word_count = len(" ".join(paragraphs).split())
    if not 60 <= word_count <= 250:
        raise ValueError(f"{book['id']} {language}: aboutBook must contain 60–250 words, got {word_count}")
    body = "".join(f"<p>{html.escape(text)}</p>" for text in paragraphs)
    return (
        '<section class="book-introduction" id="about-book" aria-labelledby="about-book-title">'
        '<div><p class="eyebrow">ScriptaHub</p>'
        f'<h2 id="about-book-title">{html.escape(ABOUT_BOOK_TITLES[language])}</h2>'
        f'{body}</div></section>'
    )


def animation_record(book: dict[str, object]) -> dict[str, object] | None:
    """Resolve optional animation assets inside docs, preserving their source edition."""
    animation = book.get("animation")
    if not animation:
        return None
    if not isinstance(animation, dict):
        raise ValueError(f"{book['id']}: animation must be an object")
    if animation.get("language") not in LANGUAGES or animation.get("status") not in ("preview", "published"):
        raise ValueError(f"{book['id']}: invalid animation language or status")
    duration = animation.get("durationMs")
    if not isinstance(duration, int) or not 0 < duration <= 14400000:
        raise ValueError(f"{book['id']}: invalid animation duration")
    if not animation.get("edition"):
        raise ValueError(f"{book['id']}: animation needs its source edition")
    result = {key: value for key, value in animation.items() if key not in ("standalone", "poster", "featured")}
    book_root = (DOCS / str(book["directory"])).resolve()
    animation_root = book_root / "Animation"
    for key, extension in (("page", ".html"), ("shf", ".shf")):
        value = animation.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"{book['id']}: missing animation {key}")
        target = (book_root / value).resolve()
        if target.parent != animation_root or target.suffix != extension or (key == "shf" and not target.is_file()):
            raise ValueError(f"{book['id']}: animation {key} must be inside this book's Animation folder: {value}")
        if key == "page" and target.name != "index.html":
            raise ValueError(f"{book['id']}: animation page must be Animation/index.html")
        result[key] = target.relative_to(DOCS.resolve()).as_posix()
    return result


def animation_page(book: dict[str, object]) -> str:
    """A generated content identifier and shared asset references, never a copied player."""
    folder = DOCS / str(book["directory"]) / "Animation"
    asset = lambda name: html.escape(relpath(DOCS / name, folder), quote=True)
    title = html.escape(str(book["title"]["en"]))
    identifier = html.escape(str(book["id"]), quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Animation · ScriptaHub</title>
<link rel="stylesheet" href="{asset('assets/site.css')}">
<link rel="stylesheet" href="{asset('assets/animation.css')}">
</head>
<body data-app-page="true" data-animation-book="{identifier}">
<script src="{asset('collection.js')}"></script>
<script src="{asset('assets/shf/shf-player.js')}"></script>
<script src="{asset('assets/animation.js')}"></script>
<script src="{asset('assets/site.js')}"></script>
<script src="{asset('assets/reading.js')}"></script>
<script src="{asset('assets/text-show.js')}"></script>
<script src="{asset('assets/book-view.js')}"></script>
<script src="{asset('assets/workflow.js')}"></script>
</body>
</html>
'''


def book_page(
    book: dict[str, object], language: str, page_path: Path, has_content: bool,
) -> str:
    words = COPY[language]
    title = str(book["title"][language])
    subtitle = str(book["subtitle"][language])
    topic = TOPICS[language][str(book["group"])]
    description = str(book["descriptions"][language]).replace("Axiologic Research", "ScriptaHub")
    edition = book["editions"][language]
    page_dir = page_path.parent
    home = relpath(DOCS / "index.html", page_dir)
    css = relpath(DOCS / "assets" / "site.css", page_dir)
    collection_script = relpath(COLLECTION_SCRIPT, page_dir)
    site_script = relpath(DOCS / "assets" / "site.js", page_dir)
    create_page = relpath(DOCS / "create" / "index.html", page_dir)
    feedback_page = relpath(DOCS / "feedback" / "index.html", page_dir)
    editions_page = relpath(DOCS / "editions" / "index.html", page_dir)
    language_options = "\n".join(
        f'<option value="../{code}/book.html?lang={code}"{" selected" if code == language else ""}>{html.escape(name)}</option>'
        for code, name in LANGUAGES.items()
    )
    actions = []
    for format_name, content_key in (("short", "shortContent"), ("read", "fullContent")):
        target = language if content_key in edition else "en"
        if content_key in book["editions"].get(target, {}):
            href = reader_href(book, target, page_path, format_name, ui_language=language)
            actions.append(f'<a class="button button-quiet" data-reading-format="{format_name}" data-reading-label="{html.escape(words[format_name], quote=True)}" href="{html.escape(href, quote=True)}">{html.escape(words[format_name])}</a>')
        else:
            actions.append(f'<span class="button button-quiet" aria-disabled="true">{html.escape(words[format_name])}</span>')
    english_pdf = book["editions"].get("en", {}).get("pdf")
    if english_pdf:
        pdf_href = relpath(DOCS / str(book["directory"]) / english_pdf, page_dir)
        actions.append(f'<a class="button button-quiet" data-download-pdf href="{html.escape(pdf_href, quote=True)}" download>{html.escape(words["download"])}</a>')
    animation = animation_record(book)
    workflow_query = urlencode({"book": str(book["directory"]), "lang": language})
    animation_url = (relpath(DOCS / animation["page"], page_dir) + "?" + urlencode({"lang": language})) if animation else (relpath(DOCS / "animation-request/index.html", page_dir) + "?" + workflow_query)
    actions.insert(0, f'<a class="button button-quiet" data-animation-link href="{html.escape(animation_url, quote=True)}">Animation</a>')
    side_actions = []
    fork_url = relpath(DOCS / "fork/index.html", page_dir) + "?" + workflow_query
    side_actions.append(f'<a class="button button-quiet" data-fork-link href="{html.escape(fork_url, quote=True)}">Fork</a>')
    side_actions.append(f'<a class="button button-quiet" data-book-feedback href="{html.escape(f"{feedback_page}?{workflow_query}", quote=True)}">{html.escape(BOOK_ACTIONS[language]["feedback"])}</a>')
    side_actions.append(f'<a class="button button-quiet" data-book-editions href="{html.escape(f"{editions_page}?{workflow_query}", quote=True)}">{html.escape(BOOK_ACTIONS[language]["editions"])}</a>')
    missing_format = next((name for name, key in (("read", "fullContent"), ("short", "shortContent")) if key not in edition), None)
    availability = ""
    if missing_format:
        request_href = translation_href(book, language, page_path, missing_format)
        availability = f'<p class="edition-unavailable"><a data-translation-notice href="{html.escape(request_href, quote=True)}">{html.escape(words["unavailable"].format(language=LANGUAGES[language]))}</a></p>'
    status_note = ""
    if book.get("publicationStatus") == "preparing":
        label = PREPARATION_LABELS[language][0]
        status_note = f'<p class="publication-status" role="status">{html.escape(label)}</p>'
    keyword_entries = []
    for source_rank, (identifier, label) in enumerate(zip(book["keywordIds"], book["keywords"][language], strict=True)):
        stats = book["keywordStats"][language][identifier]
        keyword_entries.append((source_rank, identifier, label, stats))
    shelf_ids = {identifier for identifier, _, _ in keyword_catalog(str(book["group"]))}
    # The compact preview should introduce this particular book, not repeat
    # its broad shelf.  Niche terms are ranked first by their global weight and
    # then by their source-derived relevance; the ten shelf terms remain
    # available in the complete fullscreen cloud.
    contextual_entries = [entry for entry in keyword_entries if entry[1] not in shelf_ids]
    shelf_entries = [entry for entry in keyword_entries if entry[1] in shelf_ids]
    contextual_entries.sort(key=lambda entry: (-int(entry[3]["count"]), entry[0]))
    shelf_entries.sort(key=lambda entry: (-int(entry[3]["count"]), entry[0]))
    keyword_entries = contextual_entries + shelf_entries
    keyword_items = [
        {
            "label": str(label),
            "count": int(stats["count"]),
            "href": f'{home}?{urlencode({"lang": language, "keyword": identifier})}',
        }
        for _, identifier, label, stats in keyword_entries
    ]
    keyword_data = json.dumps(keyword_items, ensure_ascii=False).replace("</", "<\\/")
    keyword_options = json.dumps({"ariaLabel": words["keywords"], "instruction": CLOUD_PREVIEW_INSTRUCTIONS[language], "modalInstruction": CLOUD_INSTRUCTIONS[language], "closeLabel": CLOUD_CLOSE_LABELS[language], "showInstruction": False}, ensure_ascii=False).replace("</", "<\\/")
    cloud_script = relpath(DOCS / "assets" / "keyword-cloud.js", page_dir)
    return f"""<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · ScriptaHub</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta property="og:type" content="book">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:image" content="cover.webp">
  <link rel="stylesheet" href="{html.escape(css)}">
  <link rel="stylesheet" href="{relpath(DOCS / 'assets' / 'text-show.css', page_dir)}">
</head>
<body data-book-page="true" data-book-language="{language}" data-book-id="{book['id']}">
  <main class="site-shell book-page">
    <header class="site-header"><a class="wordmark" href="{html.escape(home)}">ScriptaHub<span>.com</span></a><div class="header-tools"><a class="header-create" data-create-link href="{html.escape(create_page, quote=True)}?lang={language}">{html.escape(BOOK_ACTIONS[language]["create"])}</a><div class="site-scale" aria-label="Site text size"><button type="button" data-site-smaller aria-label="Decrease site size">A−</button><button type="button" data-site-size aria-label="Reset site size">100%</button><button type="button" data-site-larger aria-label="Increase site size">A+</button></div>{theme_switcher()}<label class="language-picker"><span class="sr-only">Language</span><select onchange="location.href=this.value">{language_options}</select></label></div></header>
    {status_note}<article class="book-hero">
      <button class="cover-link" type="button" data-cover-preview aria-label="{html.escape(title, quote=True)}"><img src="cover.webp" alt="{html.escape(title)}"></button>
      <div class="book-details"><div class="book-copy"><p class="eyebrow">{html.escape(topic)} · ScriptaHub</p><h1>{html.escape(title)}</h1><p class="book-subtitle">{html.escape(subtitle)}</p><p class="lead" data-text-show>{html.escape(description)}</p>{availability}</div><div class="book-actions">{"".join(actions)}</div></div>
      <nav class="book-side-actions">{"".join(side_actions)}</nav>
      <aside class="book-keyword-widget" aria-label="{html.escape(words['keywords'], quote=True)}"><div class="keyword-cloud book-keyword-cloud" data-book-keyword-cloud></div></aside>
    </article>
    {about_book_section(book, language)}{site_footer(page_dir, language)}
  </main>
  <script src="{html.escape(cloud_script)}"></script><script>globalThis.ScriptaKeywordCloud.mount(document.querySelector('[data-book-keyword-cloud]'), {keyword_data}, {keyword_options});</script><script src="{html.escape(collection_script)}"></script><script src="{relpath(DOCS / 'assets' / 'reading.js', page_dir)}"></script><script src="{relpath(DOCS / 'assets' / 'text-show.js', page_dir)}"></script><script src="{relpath(DOCS / 'assets' / 'book-view.js', page_dir)}"></script><script src="{html.escape(site_script)}"></script>
</body>
</html>
"""


def build(source_root: Path) -> dict[str, object]:
    content = source_root / "content"
    source_index = json.loads((content / "index.json").read_text(encoding="utf-8"))
    source_books = {book["id"]: book for book in source_index["books"]}
    BOOKS.mkdir(parents=True, exist_ok=True)
    manifests = []
    moved = 0

    for source_id, source_book in sorted(source_books.items(), key=lambda item: item[1]["slug"]):
        legacy_page = source_root / "books" / source_book["slug"] / "index.html"
        metadata = parse_book_page(legacy_page)
        group = subject_group(metadata["category"], metadata["title"], metadata["description"])
        uid = random_book_id()
        route = title_route(metadata["title"])
        book_root = BOOKS.joinpath(*route, uid)
        descriptions = {
            language: COPY[language]["description"].format(title=metadata["title"], topic=TOPICS[language][group])
            for language in LANGUAGES
        }
        for language in LANGUAGES:
            (book_root / language).mkdir(parents=True, exist_ok=True)

        # Move content readers first.  Assets retain their original sibling
        # names so all figure references inside the edition remain valid.
        edition_sources = {SOURCE_LANGUAGE_CODES[edition["language"]]: edition for edition in source_book["editions"]}
        for language, edition in edition_sources.items():
            target = book_root / language
            # Move the canonical PDF before its reader so a legacy in-reader
            # download link can be repaired to the sibling ``book.pdf``.
            for source_key, filename in (("pdf", "book.pdf"), ("html", "full_content.html"), ("tenMinuteHtml", "short_content.html")):
                if source_key not in edition:
                    continue
                old = content / edition[source_key]
                new = target / filename
                if transfer(old, new):
                    moved += 1
                assets = old.with_name(f"{old.stem}.assets")
                if assets.exists():
                    target_assets = new.with_name(f"{old.stem}.assets")
                    if transfer(assets, target_assets):
                        moved += 1
                if new.suffix == ".html":
                    set_html_language_and_paths(new, language, "book.pdf" if (target / "book.pdf").is_file() else None)

        # Every language directory gets a cover and thumbnail.  Hard links keep
        # the static tree portable without multiplying the image payload.
        cover_source = content / "covers" / metadata["cover"]
        english_cover = book_root / "en" / "cover.png"
        if transfer(cover_source, english_cover):
            moved += 1
        create_display_cover(english_cover, book_root / "en" / "cover.webp")
        thumbnail_source = content / "thumbnails" / (Path(metadata["cover"]).stem + ".webp")
        english_thumb = book_root / "en" / "thumbnail.webp"
        if transfer(thumbnail_source, english_thumb):
            moved += 1
        create_thumbnail(book_root / "en" / "cover.webp", english_thumb)
        for language in LANGUAGES:
            if language == "en":
                continue
            hardlink_or_copy(english_cover, book_root / language / "cover.png")
            hardlink_or_copy(book_root / "en" / "cover.webp", book_root / language / "cover.webp")
            hardlink_or_copy(english_thumb, book_root / language / "thumbnail.webp")

        editions = {language: edition_record(book_root, language) for language in LANGUAGES}
        english_source = editions["en"].get("shortContent") or editions["en"].get("fullContent")
        source_text = keyword_source_text(book_root / english_source) if english_source else ""
        keyword_ids, keywords = keyword_data(group, metadata["title"], metadata["description"], source_text)
        available_languages = [LANGUAGES[language] for language, edition in editions.items() if "fullContent" in edition or "shortContent" in edition]
        manifest = {
            "schemaVersion": 1,
            "id": uid,
            "sourceId": source_id,
            "route": list(route),
            "category": metadata["category"],
            "group": group,
            "title": {language: metadata["title"] for language in LANGUAGES},
            "subtitle": {language: metadata["subtitle"] for language in LANGUAGES},
            "shortDescription": descriptions,
            "keywords": keywords,
            "keywordIds": keyword_ids,
            "coverUrl": {language: editions[language]["cover"] for language in LANGUAGES},
            "thumbnailUrl": {language: editions[language]["thumbnail"] for language in LANGUAGES},
            "editions": editions,
            "availableLanguages": available_languages,
        }
        manifest_path = book_root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ensure_editions_file(book_root, manifest)
        manifests.append({**manifest, "directory": book_root.relative_to(DOCS).as_posix()})

    collection = make_collection(manifests)
    COLLECTION.write_text(json.dumps(collection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    COLLECTION_SCRIPT.write_text("globalThis.SCRIPTA_COLLECTION = " + json.dumps(collection, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    repair_reader_links()
    rebuild_keywords()
    return {"books": len(manifests), "moved": moved, "keywords": sum(len(values) for values in collection["keywords"].values())}



HOME_LABELS = {"en": "Home", "fr": "Accueil", "de": "Startseite", "es": "Inicio", "pt": "Início", "it": "Home", "ro": "Acasă", "pl": "Strona główna"}
HOME_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5M5.5 9v11h5v-6h3v6h5V9"/></svg>'


def install_site_branding(source: str, page_dir: Path) -> str:
    """Share the mascot favicon and deterministic header navigation across shells."""
    if 'site-header' in source or 'data-animation-book' in source or 'data-reader-app' in source:
        source = re.sub(r'[ \t]*<script>try\{if\(localStorage.getItem\("scripta-site-theme"\).*?</script>', '', source)
        bootstrap = '<script data-site-theme-bootstrap>try{const t=localStorage.getItem("scripta-site-theme");document.documentElement.dataset.theme=["light","orange","nord","dark","dark-orange"].includes(t)?t:"dark-orange"}catch{document.documentElement.dataset.theme="dark-orange"}</script>'
        source = re.sub(r'<script data-site-theme-bootstrap>.*?</script>', bootstrap, source)
        if 'data-site-theme-bootstrap' not in source:
            source = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n  ' + bootstrap, source, count=1)
    icon = html.escape(relpath(DOCS / "assets" / "librarian-icon.svg", page_dir), quote=True)
    if '<head' in source and 'rel="icon"' not in source:
        favicon = html.escape(relpath(DOCS / "favicon.ico", page_dir), quote=True)
        source = source.replace('</head>', f'  <link rel="icon" href="{favicon}" sizes="16x16 32x32 48x48">\n  <link rel="icon" type="image/svg+xml" href="{icon}">\n</head>', 1)
    language_match = re.search(r'<html\b[^>]* lang="([a-z]+)"', source)
    language = language_match.group(1) if language_match else "en"
    if language not in HOME_LABELS:
        language = "en"
    def header(match: re.Match) -> str:
        markup = match.group(0)
        if 'class="brand-icon"' not in markup:
            markup = re.sub(r'(<a\b[^>]*class="wordmark"[^>]*>)', lambda m: m.group(1) + f'<img class="brand-icon" src="{icon}" width="34" height="34" alt="">', markup, count=1)
        if 'data-home-link' not in markup:
            home = html.escape(relpath(DOCS / "index.html", page_dir) + f'?lang={language}', quote=True)
            label = HOME_LABELS[language]
            link = f'<a class="header-home" data-home-link href="{home}" aria-label="{label}" title="{label}">{HOME_ICON}<span>{label}</span></a>'
            markup = re.sub(r'(?=<a\b[^>]*data-create-link)', lambda _: link, markup, count=1)
        return markup
    return re.sub(r'<header\b[^>]*class="site-header"[^>]*>.*?</header>', header, source, flags=re.S)


def version_shared_assets(source: str, page_dir: Path, versions: dict[Path, str]) -> str:
    """Keep new HTML and its shared component code in the same browser revision."""
    source = install_site_branding(source, page_dir)
    def replace(match: re.Match) -> str:
        attribute, value = match.groups()
        plain = html.unescape(value).split("?", 1)[0]
        if ":" in plain or plain.startswith("//"):
            return match.group(0)
        target = (page_dir / plain).resolve()
        digest = versions.get(target)
        return f'{attribute}="{plain}?v={digest}"' if digest else match.group(0)
    return re.sub(r'(src|href)="([^"#]+)"', replace, source)


def shared_asset_versions() -> dict[Path, str]:
    paths = [COLLECTION_SCRIPT, DOCS / "favicon.ico", DOCS / "reader/reader.css", DOCS / "reader/reader.js", *[DOCS / "assets" / name for name in (
        "site.js", "site.css", "text-show.js", "text-show.css", "book-view.js",
        "librarian.js", "workflow.js", "reading.js", "home-librarian.css",
        "home-librarian.js", "dictation.js", "keyword-cloud.js", "librarian-icon-orange.svg", "librarian-icon-nord.svg", "librarian-mascot.js", "librarian-icon.svg", "librarian-icon.png", "shf/shf-player.js")]]
    return {path.resolve(): hashlib.sha256(path.read_bytes()).hexdigest()[:12] for path in paths if path.is_file()}


def refresh_pages() -> dict[str, int]:
    """Recreate generated catalogue pages from already-migrated manifests."""
    collection = rebuild_collection_from_manifests()
    versions = shared_asset_versions()
    for listing in collection["books"]:
        root = DOCS / listing["directory"]
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        ensure_editions_file(root, manifest)
        keyword_stats = {
            language: {keyword["id"]: {"count": keyword["count"]} for keyword in collection["keywords"][language]}
            for language in LANGUAGES
        }
        page_book = {**manifest, "directory": listing["directory"], "descriptions": manifest["shortDescription"], "keywordStats": keyword_stats}
        if manifest.get("animation"):
            page = root / "Animation" / "index.html"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(version_shared_assets(animation_page(page_book), page.parent, versions), encoding="utf-8")
        for language in LANGUAGES:
            edition = manifest["editions"][language]
            has_content = "fullContent" in edition or "shortContent" in edition
            page = root / language / "book.html"
            page.write_text(version_shared_assets(book_page(page_book, language, page, has_content), page.parent, versions), encoding="utf-8")
    for shell in [DOCS / "index.html", *DOCS.glob("*/*.html")]:
        source = shell.read_text(encoding="utf-8")
        updated = version_shared_assets(source, shell.parent, versions)
        if updated != source:
            shell.write_text(updated, encoding="utf-8")
    # Discovery is rendered from collection data in the browser. Remove pages
    # produced by older builds so per-keyword routes cannot return by accident.
    if (DOCS / "keywords").exists():
        shutil.rmtree(DOCS / "keywords")
    return {"books": len(collection["books"])}


def rebuild_collection_from_manifests() -> dict[str, object]:
    """Regenerate the aggregate after an edition is recovered or amended."""
    manifests = []
    for path in sorted(BOOKS.glob("**/manifest.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifests.append({**manifest, "directory": path.parent.relative_to(DOCS).as_posix()})
    collection = make_collection(manifests)
    COLLECTION.write_text(json.dumps(collection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    COLLECTION_SCRIPT.write_text("globalThis.SCRIPTA_COLLECTION = " + json.dumps(collection, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    return collection


def refresh_display_covers() -> int:
    """Derive consistent 2:3 WebP covers for every existing migrated book."""
    changed = 0
    for manifest_path in sorted(BOOKS.glob("**/manifest.json")):
        root = manifest_path.parent
        english_source = root / "en" / "cover.png"
        if not english_source.is_file():
            continue
        english_display = root / "en" / "cover.webp"
        create_display_cover(english_source, english_display)
        english_thumbnail = root / "en" / "thumbnail.webp"
        create_thumbnail(english_display, english_thumbnail)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for language in LANGUAGES:
            display = root / language / "cover.webp"
            thumbnail = root / language / "thumbnail.webp"
            if language != "en":
                if display.exists():
                    display.unlink()
                hardlink_or_copy(english_display, display)
                if thumbnail.exists():
                    thumbnail.unlink()
                hardlink_or_copy(english_thumbnail, thumbnail)
            edition = edition_record(root, language)
            if manifest["editions"].get(language) != edition or manifest["coverUrl"].get(language) != edition["cover"]:
                manifest["editions"][language] = edition
                manifest["coverUrl"][language] = edition["cover"]
                changed += 1
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rebuild_collection_from_manifests()
    refresh_pages()
    return changed


def reorganize_book_routes() -> int:
    """Move books to ``books/<title-word>/…/<random-id>/`` and repair readers."""
    collection = json.loads(COLLECTION.read_text(encoding="utf-8"))
    moved = 0
    for listing in collection["books"]:
        old_root = DOCS / listing["directory"]
        manifest_path = old_root / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        route = title_route(str(manifest["title"]["en"]))
        identifier = random_book_id()
        new_root = BOOKS.joinpath(*route, identifier)
        if new_root.exists():
            raise FileExistsError(new_root)
        new_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old_root), str(new_root))
        manifest_path = new_root / "manifest.json"
        manifest["id"] = identifier
        manifest["route"] = list(route)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for language in LANGUAGES:
            edition_dir = new_root / language
            for reader in edition_dir.glob("*.html"):
                if reader.name != "book.html":
                    set_html_language_and_paths(reader, language, "book.pdf" if (edition_dir / "book.pdf").is_file() else None)
        moved += 1
    # The former taxonomy is now empty. Remove only empty directories, from the
    # deepest level upward, so no title-based route can be touched accidentally.
    for directory in sorted((path for path in BOOKS.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass
    rebuild_collection_from_manifests()
    refresh_pages()
    return moved


def recover_leftovers(source_root: Path) -> int:
    """Attach recognizable editions that were intentionally absent from the old index.

    These are legacy alternatives, archive PDFs, or translations whose names did
    not match the previous discovery convention.  Unknown draft manuscripts are
    deliberately *not* published by this function.
    """
    collection = json.loads(COLLECTION.read_text(encoding="utf-8"))
    roots = {book["sourceId"]: DOCS / book["directory"] for book in collection["books"]}
    moved = 0

    def update_manifest(source_id: str, language: str, field: str, filename: str) -> None:
        manifest_path = roots[source_id] / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["editions"][language][field] = f"{language}/{filename}"
        manifest["availableLanguages"] = [
            LANGUAGES[code] for code, edition in manifest["editions"].items()
            if "fullContent" in edition or "shortContent" in edition
        ]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def move_edition(source: Path, source_id: str, language: str, filename: str, field: str | None = None) -> None:
        nonlocal moved
        destination = roots[source_id] / language / filename
        if transfer(source, destination):
            moved += 1
        assets = source.with_name(f"{source.stem}.assets")
        if assets.exists() and transfer(assets, destination.with_name(f"{source.stem}.assets")):
            moved += 1
        if destination.suffix == ".html":
            set_html_language_and_paths(destination, language, "book.pdf" if (destination.parent / "book.pdf").is_file() else None)
        if field:
            update_manifest(source_id, language, field, filename)

    content = source_root / "content"
    move_edition(content / "htmls" / "ES" / "The_Thousand_Handed_Devil_ES.html", "The_Thousand_Handed_Devil", "es", "full_content.html", "fullContent")
    move_edition(content / "10minutes" / "The_Schizoid_and_the_Oracle.html", "The_Schizoid_and_the_Oracle", "en", "short_content.html", "shortContent")
    move_edition(content / "10minutes" / "PL" / "EXPLAINABLE_PL.html", "EXPLAINABLE_AI", "pl", "short_content.html", "shortContent")
    # The remaining three are historical alternatives, retained alongside the
    # current editions without silently replacing a reviewed one.
    move_edition(content / "htmls" / "FR" / "The_Fragmented_Future_FR(1).html", "The_Fragmented_Future", "fr", "full_content.previous.html")
    move_edition(content / "10minutes" / "ES" / "EXPLAINABLE_ES.html", "EXPLAINABLE_AI", "es", "short_content.previous.html")
    move_edition(content / "10minutes" / "IT" / "EXPLAINABLE_IT.html", "EXPLAINABLE_AI", "it", "short_content.previous.html")
    move_edition(content / "EN" / "The_Future_of_Research_Infrastructure.pdf", "FUTURE_RESEARCH_INFRASTRUCTURE", "en", "book.previous-edition.pdf")

    # Preserve distinctive legacy art instead of discarding it.  The Romanian
    # Schizoid artwork is made the active Romanian cover; the older Outfinitism
    # cover remains an explicit historical asset.
    schizoid = roots["The_Schizoid_and_the_Oracle"] / "ro"
    for old_name, new_name in (("The_Schizoid_and_the_Oracle_RO.png", "cover.png"),):
        old = content / "covers" / old_name
        if old.exists():
            target = schizoid / new_name
            if target.exists():
                target.unlink()
            transfer(old, target)
            moved += 1
    old_thumb = content / "thumbnails" / "The_Schizoid_and_the_Oracle_RO.webp"
    if old_thumb.exists():
        target = schizoid / "thumbnail.webp"
        if target.exists():
            target.unlink()
        transfer(old_thumb, target)
        moved += 1
    move_edition(content / "covers" / "Outfinitism_Third_Edition.png", "Outfinitism_Meta_Rationality", "en", "cover.previous-edition.png")
    move_edition(content / "thumbnails" / "Outfinitism_Third_Edition.webp", "Outfinitism_Meta_Rationality", "en", "thumbnail.previous-edition.webp")

    rebuild_collection_from_manifests()
    refresh_pages()
    return moved


def introductory_description(path: Path) -> str | None:
    """Extract a reader's first useful paragraph for catalogue metadata."""
    source = path.read_text(encoding="utf-8")
    # Brand names and KDP occur only in imported front matter, in every
    # language.  Filtering them is more reliable than maintaining eight lists
    # of translated copyright phrases.
    ignored = (
        "conversion notice", "copyright", "publishing rights",
        "available for free", "author's note", "all rights reserved",
        "kdp", "scriptahub", "axiologic", "achilles", "outfinity",
    )
    for fragment in re.findall(r"<p\b[^>]*>(.*?)</p>", source, flags=re.IGNORECASE | re.DOTALL):
        text = clean_fragment(fragment)
        compact = text.casefold()
        if len(text) < 110 or any(marker in compact for marker in ignored):
            continue
        if len(text) > 430:
            stop = max(text.rfind(mark, 0, 430) for mark in (". ", "! ", "? ", "… "))
            text = text[:stop + 1] if stop > 160 else text[:427].rstrip() + "…"
        return text
    return None


def enrich_metadata() -> int:
    """Use the actual reader editions for specific localised short descriptions."""
    changed = 0
    for manifest_path in sorted(BOOKS.glob("**/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("shortDescriptionEditorial"):
            continue
        for language, edition in manifest["editions"].items():
            candidate = edition.get("shortContent") or edition.get("fullContent")
            if not candidate:
                continue
            description = introductory_description(manifest_path.parent / candidate)
            if description and manifest["shortDescription"].get(language) != description:
                manifest["shortDescription"][language] = description
                changed += 1
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rebuild_collection_from_manifests()
    refresh_pages()
    return changed


KEYWORD_TRANSLATION_CACHE = ROOT / "tools" / "keyword-translations.generated.json"


def translate_keyword_phrases(phrases: set[str]) -> dict[str, dict[str, str]]:
    """Translate extracted phrases locally and cache the generated metadata.

    No remote translation API is used.  Marian models are downloaded from
    their public model repository on first use and then run locally.  The cache
    is generated data, not an authored keyword taxonomy.
    """
    try:
        import torch
        from transformers import MarianMTModel, MarianTokenizer
    except ImportError as error:
        raise RuntimeError(
            "Keyword localisation needs tools/requirements-keywords.txt"
        ) from error

    translations: dict[str, dict[str, str]] = {"en": {phrase: phrase for phrase in phrases}}
    if KEYWORD_TRANSLATION_CACHE.is_file():
        cached = json.loads(KEYWORD_TRANSLATION_CACHE.read_text(encoding="utf-8"))
        for language, values in cached.get("translations", {}).items():
            if language in LANGUAGES and isinstance(values, dict):
                translations[language] = {str(key): str(value) for key, value in values.items()}
    for language in LANGUAGES:
        translations.setdefault(language, {})

    model_groups = (
        ("Helsinki-NLP/opus-mt-en-ROMANCE", (("fr", ">>fr<< "), ("es", ">>es<< "), ("pt", ">>pt<< "), ("it", ">>it<< "), ("ro", ">>ro<< "))),
        ("Helsinki-NLP/opus-mt-en-de", (("de", ""),)),
        ("Helsinki-NLP/opus-mt-en-zlw", (("pl", ">>pol<< "),)),
    )
    torch.set_num_threads(max(1, min(8, os.cpu_count() or 1)))
    ordered_phrases = sorted(phrases, key=lambda value: (value.casefold(), value))

    for model_name, targets in model_groups:
        pending_targets = [
            (language, prefix, [phrase for phrase in ordered_phrases if phrase not in translations[language]])
            for language, prefix in targets
        ]
        pending_targets = [target for target in pending_targets if target[2]]
        if not pending_targets:
            continue
        print(f"Loading local keyword translator {model_name}...", flush=True)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        model.eval()
        for language, prefix, pending in pending_targets:
            print(f"Translating {len(pending)} extracted phrases to {language}...", flush=True)
            for offset in range(0, len(pending), 128):
                batch_phrases = pending[offset:offset + 128]
                encoded = tokenizer(
                    [prefix + phrase for phrase in batch_phrases], return_tensors="pt",
                    padding=True, truncation=True, max_length=64,
                )
                with torch.inference_mode():
                    generated = model.generate(**encoded, max_new_tokens=48, num_beams=1)
                outputs = tokenizer.batch_decode(generated, skip_special_tokens=True)
                for phrase, output in zip(batch_phrases, outputs, strict=True):
                    output = re.sub(r"\s+", " ", output).strip(" \t\r\n•–—;,")
                    if not output:
                        raise ValueError(f"Empty {language} translation for {phrase!r}")
                    translations[language][phrase] = output
                if offset and offset % 1280 == 0:
                    print(f"  {language}: {min(offset + 128, len(pending))}/{len(pending)}", flush=True)
            KEYWORD_TRANSLATION_CACHE.write_text(
                json.dumps({"schemaVersion": 1, "translations": {code: translations[code] for code in LANGUAGES if code != "en"}}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        del model, tokenizer
    return translations


def rebuild_keywords(manifest_paths: list[Path] | None = None) -> int:
    """Extract and localise 90 niche phrases per book from its short read."""
    records = []
    all_phrases: set[str] = set()
    shelf_terms = {
        keyword_normalise(label).strip()
        for localized in SHELF_CATEGORIES.values()
        for label in localized["en"].split("|")
    }
    for manifest_path in sorted(manifest_paths if manifest_paths is not None else BOOKS.glob("**/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        root = manifest_path.parent
        english_edition = manifest["editions"].get("en", {})
        source_name = english_edition.get("shortContent") or english_edition.get("fullContent")
        if (root / "en/short_content.html").is_file():
            source_name = "en/short_content.html"
        elif not source_name and (root / "en/full_content.html").is_file():
            source_name = "en/full_content.html"
        source_text = ""
        source_hash = ""
        if source_name and (root / str(source_name)).is_file():
            source_text = keyword_source_text(root / str(source_name))
            source_hash = hashlib.sha256((root / str(source_name)).read_bytes()).hexdigest()
        title = str(manifest["title"]["en"])
        description = str(manifest["shortDescription"].get("en", ""))
        group = subject_group(str(manifest["category"]), title, description)
        candidates = [
            phrase for phrase in extract_keyword_candidates(title, description, source_text, 120)
            if keyword_normalise(phrase).strip() not in shelf_terms
        ]
        reviewed = manifest.get("keywordReview", {})
        if reviewed.get("sourceHash") == source_hash and reviewed.get("phrases"):
            candidates = reviewed["phrases"]
            if len(candidates) != 90 or len(set(candidates)) != 90 or any(
                keyword_normalise(phrase) not in keyword_normalise(source_text)
                or keyword_normalise(phrase).strip() in shelf_terms
                or keyword_normalise(phrase) == keyword_normalise(title)
                for phrase in candidates
            ):
                raise ValueError(f"{title}: reviewed keywords must be 90 distinct phrases from the current English reader")
        if len(candidates) < 90:
            raise ValueError(f"{title} yielded only {len(candidates)} source-derived keywords")
        records.append((manifest_path, manifest, group, candidates, source_hash))
        all_phrases.update(candidates)

    translations = translate_keyword_phrases(all_phrases)
    changed = 0
    for manifest_path, manifest, group, candidates, source_hash in records:
        broad = keyword_catalog(group)
        localized = {
            language: [labels[language] for _, _, labels in broad]
            for language in LANGUAGES
        }
        identifiers = [identifier for identifier, _, _ in broad]
        seen = {
            language: {keyword_normalise(label) for label in localized[language]}
            for language in LANGUAGES
        }
        for phrase in candidates:
            labels = {language: translations[language][phrase] for language in LANGUAGES}
            if any(keyword_normalise(labels[language]) in seen[language] for language in LANGUAGES):
                continue
            identifiers.append(keyword_identifier(phrase))
            for language in LANGUAGES:
                localized[language].append(labels[language])
                seen[language].add(keyword_normalise(labels[language]))
            if len(identifiers) == 100:
                break
        if len(identifiers) != 100:
            raise ValueError(f"{manifest['title']['en']} has only {len(identifiers)} distinct translated keywords")
        if manifest.get("group") != group or manifest.get("keywordIds") != identifiers or manifest.get("keywords") != localized or manifest.get("keywordSourceHash") != source_hash:
            manifest["group"] = group
            manifest["keywordIds"] = identifiers
            manifest["keywords"] = localized
            manifest["keywordSourceHash"] = source_hash
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    if manifest_paths is None or any(path.resolve().is_relative_to(BOOKS.resolve()) for path in manifest_paths):
        rebuild_collection_from_manifests()
        refresh_pages()
    return changed


def rebrand_metadata() -> int:
    """Replace retired public-brand labels in metadata and reader HTML."""
    def replace_public_brand(value: object) -> object:
        if isinstance(value, str):
            value = re.sub(r"www\\.axiologic\\.net", "ScriptaHub.com", value, flags=re.IGNORECASE)
            value = re.sub(r"Axiologic Research", "ScriptaHub", value, flags=re.IGNORECASE)
            value = re.sub(r"Recherche Axiologique|Investigação Axiológica|Investigación Axiológica|Badania Aksjologiczne", "ScriptaHub", value, flags=re.IGNORECASE)
            value = re.sub(r"Axiologic", "ScriptaHub", value, flags=re.IGNORECASE)
            return re.sub(r"\b(?:Achilles|Achille|Aquiles)\b", "ScriptaHub", value, flags=re.IGNORECASE)
        if isinstance(value, list):
            return [replace_public_brand(item) for item in value]
        if isinstance(value, dict):
            return {key: replace_public_brand(item) for key, item in value.items()}
        return value

    changed = 0
    for manifest_path in sorted(BOOKS.glob("**/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        updated = replace_public_brand(manifest)
        if updated != manifest:
            manifest_path.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    for reader_path in sorted(BOOKS.glob("**/*.html")):
        source = reader_path.read_text(encoding="utf-8", errors="ignore")
        updated_source = re.sub(r"https?://(?:www\.)?axiologic\.net", "https://ScriptaHub.com", source, flags=re.IGNORECASE)
        updated_source = re.sub(r"www\.axiologic\.net", "ScriptaHub.com", updated_source, flags=re.IGNORECASE)
        updated_source = re.sub(r"Axiologic Research", "ScriptaHub", updated_source, flags=re.IGNORECASE)
        updated_source = re.sub(r"Recherche Axiologique|Investigação Axiológica|Investigación Axiológica|Badania Aksjologiczne", "ScriptaHub", updated_source, flags=re.IGNORECASE)
        updated_source = re.sub(r"Axiologic", "ScriptaHub", updated_source, flags=re.IGNORECASE)
        updated_source = re.sub(r"\b(?:Achilles|Achille|Aquiles)\b", "ScriptaHub", updated_source, flags=re.IGNORECASE)
        if updated_source != source:
            reader_path.write_text(updated_source, encoding="utf-8")
            changed += 1
    rebuild_collection_from_manifests()
    refresh_pages()
    return changed


EDITORIAL_SLUG_ALIASES = {
    "OpenDSU_Essential_Philosophy": "opendsu",
    "Trustworthy_AI_Engineering_Course": "trustworthy-ai",
    "The_Basilisk_Internal_Critique_of_Outfinitism": "the-basilisks-internal-critique-of-outfinitism",
    "FUTURE_RESEARCH_INFRASTRUCTURE": "future-research-infrastructure",
}


def recover_editorial_descriptions() -> tuple[int, list[str]]:
    """Restore the concise original editorial descriptions from their public pages.

    The legacy HTML shells were intentionally retired after migration, while the
    public Axiologic book pages still expose their author-written
    ``edition-why`` paragraphs.  This restores only that metadata; it never
    replaces a reader edition or uses a translation service.
    """
    recovered = 0
    missing = []
    for manifest_path in sorted(BOOKS.glob("**/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("shortDescriptionEditorial"):
            continue
        source_id = str(manifest["sourceId"])
        candidates = [
            EDITORIAL_SLUG_ALIASES.get(source_id),
            slugify(str(manifest["title"]["en"])),
            slugify(source_id),
        ]
        description = None
        for slug in dict.fromkeys(candidate for candidate in candidates if candidate):
            request = Request(
                f"https://www.axiologic.net/books/{slug}/",
                headers={"User-Agent": "ScriptaHub catalogue migration/1.0 (+https://www.axiologic.net)"},
            )
            try:
                with urlopen(request, timeout=12) as response:
                    source = response.read().decode("utf-8", errors="replace")
            except OSError:
                continue
            match = re.search(r'<p\s+class="edition-why"[^>]*>(.*?)</p>', source, flags=re.IGNORECASE | re.DOTALL)
            if match:
                description = clean_fragment(match.group(1))
                break
        if description:
            if manifest["shortDescription"].get("en") != description:
                manifest["shortDescription"]["en"] = description
                manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                recovered += 1
        else:
            missing.append(source_id)
        time.sleep(.08)
    rebuild_collection_from_manifests()
    refresh_pages()
    return recovered, missing


def retire_source(source_root: Path) -> int:
    """Remove processed legacy material but preserve genuinely unclassified drafts."""
    expected = (ROOT / "old_content").resolve()
    source_root = source_root.resolve()
    if source_root != expected:
        raise ValueError(f"Refusing to retire anything except {expected}")
    problems = check()
    if problems:
        raise ValueError("Cannot retire source while the new collection is invalid:\n" + "\n".join(problems))
    keep = source_root / "unclassified"
    keep.mkdir(parents=True, exist_ok=True)
    drafts = (
        source_root / "content" / "htmls" / "RO" / "Idei_putine_si_fixe_RO_Draft_0_1.html",
        source_root / "content" / "htmls" / "RO" / "The Deep Canopy.html",
        source_root / "content" / "htmls" / "RO" / "Fortati_sa_Performam_RO_Draft_0_3.html",
    )
    retained = 0
    for draft in drafts:
        if draft.exists():
            transfer(draft, keep / draft.name)
            retained += 1
    for child in source_root.iterdir():
        if child == keep:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    return retained


def make_collection(manifests: list[dict[str, object]]) -> dict[str, object]:
    keyword_counts: dict[str, dict[str, dict[str, object]]] = {language: {} for language in LANGUAGES}
    books = []
    for manifest in manifests:
        directory = manifest["directory"]
        compact_editions = {
            language: {key: f"{directory}/{value}" for key, value in edition.items()}
            for language, edition in manifest["editions"].items()
        }
        book = {
            "id": manifest["id"], "sourceId": manifest["sourceId"], "directory": directory, "route": manifest["route"],
            "category": manifest["category"], "group": manifest["group"], "title": manifest["title"], "subtitle": manifest["subtitle"],
            "shortDescription": manifest["shortDescription"], "keywords": manifest["keywords"], "keywordIds": manifest["keywordIds"],
            "coverUrl": {language: f"{directory}/{value}" for language, value in manifest["coverUrl"].items()},
            "thumbnailUrl": {language: f"{directory}/{value}" for language, value in manifest["thumbnailUrl"].items()},
            "editions": compact_editions, "availableLanguages": manifest["availableLanguages"],
            "currentEdition": manifest.get("currentEdition", "edition-1"),
            "publicationStatus": manifest.get("publicationStatus", "published"),
            "pendingEdition": manifest.get("pendingEdition"),
            "sourceAliases": manifest.get("sourceAliases", []),
            "publicationLabel": {code: PREPARATION_LABELS[code][0] for code in LANGUAGES} if manifest.get("publicationStatus") == "preparing" else {},
        }
        animation = animation_record(manifest)
        if animation:
            book["animation"] = animation
        books.append(book)
        for language in LANGUAGES:
            for identifier, label in zip(manifest["keywordIds"], manifest["keywords"][language], strict=True):
                entry = keyword_counts[language].setdefault(identifier, {"id": identifier, "label": label, "slug": slugify(label), "count": 0})
                entry["count"] += 1
    keyword_lists = {}
    for language, entries in keyword_counts.items():
        used_slugs: set[str] = set()
        words = sorted(entries.values(), key=lambda entry: (-entry["count"], entry["label"].casefold(), entry["id"]))
        for entry in words:
            candidate = str(entry["slug"])
            if candidate in used_slugs:
                candidate = f"{candidate}--{slugify(str(entry['id']))}"
            entry["slug"] = candidate
            used_slugs.add(candidate)
        keyword_lists[language] = words
    return {
        "schemaVersion": 1,
        "supportedLanguages": [{"code": code, "name": name} for code, name in LANGUAGES.items()],
        "bookCount": len(books),
        "books": books,
        "keywords": keyword_lists,
    }


def editorial_description_problems(manifest: dict) -> list[str]:
    """Keep reviewed descriptions as six short, complete, authored sentences."""
    if not manifest.get("shortDescriptionEditorial"):
        return []
    problems = []
    descriptions = manifest.get("shortDescription", {})
    if set(descriptions) != set(LANGUAGES):
        problems.append(f"{manifest['id']}: editorial descriptions need all eight languages")
    for language, value in descriptions.items():
        sentences = re.split(r"(?<=[.!?])\s+", str(value).strip())
        if len(sentences) != 6 or any(not re.search(r"[.!?]$", sentence) for sentence in sentences):
            problems.append(f"{manifest['id']} {language}: description must have six complete sentences")
        if any(len(sentence.split()) > 22 for sentence in sentences):
            problems.append(f"{manifest['id']} {language}: description sentence exceeds 22 words")
        if re.search(r"(?:^|\s)\d+\.\d+\s|<[^>]+>|…|\.\.\.", str(value)):
            problems.append(f"{manifest['id']} {language}: description contains an outline, markup or truncated prose")
    return problems


def check() -> list[str]:
    problems = []
    if not COLLECTION.is_file():
        return [f"missing {COLLECTION.relative_to(ROOT)}"]
    collection = json.loads(COLLECTION.read_text(encoding="utf-8"))
    if collection.get("bookCount") != len(collection.get("books", [])):
        problems.append("collection bookCount does not match books")
    book_keyword_counts = Counter(
        identifier
        for book in collection.get("books", [])
        for identifier in book.get("keywordIds", [])
    )
    keyword_id_sets: dict[str, set[str]] = {}
    for language in LANGUAGES:
        keyword_entries = collection.get("keywords", {}).get(language, [])
        keyword_ids = [str(entry.get("id", "")) for entry in keyword_entries]
        keyword_id_sets[language] = set(keyword_ids)
        if len(keyword_ids) != len(keyword_id_sets[language]):
            problems.append(f"{language}: duplicate keyword IDs in collection")
        for entry in keyword_entries:
            identifier = str(entry.get("id", ""))
            if int(entry.get("count", 0)) != book_keyword_counts[identifier]:
                problems.append(f"{language}: keyword count mismatch for {identifier}")
    english_keyword_ids = keyword_id_sets.get("en", set())
    for language, identifiers in keyword_id_sets.items():
        if identifiers != english_keyword_ids:
            problems.append(f"{language}: keyword IDs do not match the language-independent English set")
    for book in collection.get("books", []):
        root = DOCS / book["directory"]
        manifest_path = root / "manifest.json"
        if not manifest_path.is_file():
            problems.append(f"missing manifest: {manifest_path.relative_to(ROOT)}")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        problems.extend(editorial_description_problems(manifest))
        if book.get("shortDescription") != manifest.get("shortDescription"):
            problems.append(f"{book['id']}: catalogue descriptions differ from manifest; run refresh")
        try:
            expected_animation = animation_record({**manifest, "directory": book["directory"]})
            if expected_animation != book.get("animation"):
                problems.append(f"{book['id']}: animation differs from manifest; run refresh")
            if expected_animation:
                animation_folder = DOCS / book["directory"] / "Animation"
                expected_files = {"index.html", Path(expected_animation["shf"]).name}
                if not animation_folder.is_dir() or {p.name for p in animation_folder.iterdir()} != expected_files:
                    problems.append(f"{book['id']}: Animation must contain only its SHF content and generated entry page")
                elif (animation_folder / "index.html").read_text(encoding="utf-8") != version_shared_assets(animation_page({**manifest, "directory": book["directory"]}), animation_folder, shared_asset_versions()):
                    problems.append(f"{book['id']}: animation entry differs from shared template; run refresh")
                history = json.loads((root / "editions.json").read_text(encoding="utf-8"))
                if expected_animation["edition"] not in {entry["id"] for entry in history.get("editions", [])}:
                    problems.append(f"{book['id']}: animation source edition is missing")
        except (ValueError, OSError) as error:
            problems.append(str(error))
        editions_path = root / "editions.json"
        if not editions_path.is_file():
            problems.append(f"{book['id']}: missing editions.json")
        else:
            try:
                history = json.loads(editions_path.read_text(encoding="utf-8"))
                history_records = history.get("editions", [])
                history_ids = {entry.get("id") for entry in history_records if isinstance(entry, dict)}
                if history.get("bookId") != book.get("id"):
                    problems.append(f"{book['id']}: editions.json bookId mismatch")
                if history.get("currentEdition") not in history_ids and manifest.get("publicationStatus") != "preparing":
                    problems.append(f"{book['id']}: editions.json current edition is missing")
                for history_entry in history_records:
                    if not isinstance(history_entry, dict) or not (history_entry.get("publishedAt") or (history_entry.get("status") == "preparing" and history_entry.get("startedAt"))) or not isinstance(history_entry.get("changes"), dict):
                        problems.append(f"{book['id']}: malformed edition history entry")
                        continue
                    for pdf_path in history_entry.get("pdf", {}).values():
                        target = (root / str(pdf_path)).resolve()
                        if root.resolve() not in target.parents or not target.is_file():
                            problems.append(f"{book['id']}: missing or unsafe historical PDF: {pdf_path}")
                    for cover_path in history_entry.get("covers", {}).values():
                        target = (root / str(cover_path)).resolve()
                        if root.resolve() not in target.parents or not target.is_file():
                            problems.append(f"{book['id']}: missing or unsafe edition cover: {cover_path}")
                    for formats in history_entry.get("readers", {}).values():
                        for reader_path in formats.values():
                            target = (root / str(reader_path)).resolve()
                            if root.resolve() not in target.parents or not target.is_file():
                                problems.append(f"{book['id']}: missing or unsafe historical reader: {reader_path}")
                if manifest.get("currentEdition") and manifest["currentEdition"] != history.get("currentEdition"):
                    problems.append(f"{book['id']}: current edition differs between manifest and history")
                if manifest.get("currentEdition") and manifest.get("releasePolicy") == "en-ro-on-request":
                    for required_language in ("en", "ro"):
                        if any(key not in manifest.get("editions", {}).get(required_language, {}) for key in ("fullContent", "shortContent")):
                            problems.append(f"{book['id']}: new releases require complete and short {required_language} readers")
            except (json.JSONDecodeError, OSError):
                problems.append(f"{book['id']}: invalid editions.json")
        expected_route = list(title_route(str(manifest.get("title", {}).get("en", ""))))
        if manifest.get("route") != expected_route:
            problems.append(f"{book['id']}: route does not match English title words")
        expected_directory = (Path("books").joinpath(*expected_route, str(manifest.get("id", "")))).as_posix()
        if book.get("directory") != expected_directory:
            problems.append(f"{book['id']}: directory does not match title route and random ID")
        identifiers = manifest.get("keywordIds", [])
        expected_count = len(identifiers) if manifest.get("publicationStatus") == "preparing" else 100
        if not 10 <= expected_count <= 100 or len(identifiers) != expected_count or len(set(identifiers)) != expected_count:
            problems.append(f"{book['id']}: expected 100 distinct keyword IDs, got {len(identifiers)}")
        missing_keyword_ids = set(identifiers) - english_keyword_ids
        if missing_keyword_ids:
            problems.append(f"{book['id']}: keyword IDs missing from collection: {', '.join(sorted(missing_keyword_ids))}")
        for language in LANGUAGES:
            keywords = manifest.get("keywords", {}).get(language, [])
            normalized_keywords = [keyword_normalise(str(keyword)) for keyword in keywords]
            if len(keywords) != expected_count or len(set(normalized_keywords)) != expected_count:
                problems.append(f"{book['id']} {language}: expected 100 distinct keywords, got {len(keywords)}")
            if keyword_normalise(str(manifest.get("title", {}).get(language, ""))) in normalized_keywords:
                problems.append(f"{book['id']} {language}: book title used as a keyword")
            for required in ("title", "subtitle", "shortDescription", "coverUrl"):
                if language not in manifest.get(required, {}):
                    problems.append(f"{book['id']} {language}: missing {required}")
            book_page_path = root / language / "book.html"
            if not book_page_path.is_file():
                problems.append(f"{book['id']} {language}: missing book page")
            else:
                page_source = book_page_path.read_text(encoding="utf-8")
                if 'data-text-show' not in page_source or not re.search(r'assets/book-view\.js(?:\?v=[^"<>]+)?"', page_source):
                    problems.append(f"{book['id']} {language}: missing shared book view/textShow")
                if manifest.get("shortDescriptionEditorial"):
                    expected_description = html.escape(manifest["shortDescription"][language])
                    if expected_description not in page_source:
                        problems.append(f"{book['id']} {language}: description differs from reviewed manifest; run refresh")
                if 'data-animation-link' not in page_source or 'data-fork-link' not in page_source:
                    problems.append(f"{book['id']} {language}: missing Animation or Fork action")
                try:
                    expected_about = about_book_section(manifest, language)
                    if expected_about not in page_source:
                        problems.append(f"{book['id']} {language}: book presentation differs from manifest; run refresh")
                except ValueError as error:
                    problems.append(str(error))
                page_keyword_ids = [
                    unquote(match)
                    for match in re.findall(r"(?:&|&amp;)keyword=([^\"&<\s]+)", page_source)
                ]
                if len(page_keyword_ids) != len(identifiers) or set(page_keyword_ids) != set(identifiers):
                    problems.append(f"{book['id']} {language}: book-page keyword links do not match the manifest")
        for language, edition in book.get("editions", {}).items():
            for path in edition.values():
                if not (DOCS / path).is_file():
                    problems.append(f"missing edition asset: {path}")
    if (DOCS / "keywords").exists():
        problems.append("legacy per-keyword pages exist; discovery must use the client-side catalogue filter")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "reorganize-routes", "rebuild-keywords", "refresh-covers", "enrich", "recover", "recover-editorial-descriptions", "rebrand", "retire-source", "repair-reader-links", "refresh", "check"))
    parser.add_argument("--source", type=Path, default=ROOT / "old_content", help="legacy source root")
    parser.add_argument("--manifest", action="append", type=Path, help="rebuild keywords for these manifests only, including staged releases")
    args = parser.parse_args(argv)
    if args.manifest and args.command != "rebuild-keywords":
        parser.error("--manifest is only supported by rebuild-keywords")
    if args.command == "build":
        result = build(args.source.resolve())
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Built {result['books']} books, moved {result['moved']} source entries, and indexed {result['keywords']} localised discovery terms.")
        return 0
    if args.command == "refresh":
        result = refresh_pages()
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Refreshed {result['books']} book roots; keyword discovery remains client-side.")
        return 0
    if args.command == "refresh-covers":
        changed = refresh_display_covers()
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Regenerated portrait display covers for {changed} edition records.")
        return 0
    if args.command == "recover":
        moved = recover_leftovers(args.source.resolve())
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Recovered {moved} legacy source entries.")
        return 0
    if args.command == "enrich":
        changed = enrich_metadata()
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Enriched {changed} manifest values from published reader editions.")
        return 0
    if args.command == "rebuild-keywords":
        changed = rebuild_keywords(args.manifest)
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Rebuilt editorial discovery keywords for {changed} books.")
        return 0
    if args.command == "rebrand":
        changed = rebrand_metadata()
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Rebranded public metadata or reader content in {changed} files.")
        return 0
    if args.command == "reorganize-routes":
        moved = reorganize_book_routes()
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Reorganized {moved} books into title-word routes with random IDs.")
        return 0
    if args.command == "repair-reader-links":
        repaired = repair_reader_links()
        print(f"Repaired legacy reader links in {repaired} edition file(s).")
        return 0
    if args.command == "recover-editorial-descriptions":
        recovered, missing = recover_editorial_descriptions()
        problems = check()
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return 1
        print(f"Recovered {recovered} editorial descriptions; {len(missing)} were unavailable.")
        if missing:
            print("Unavailable: " + ", ".join(missing))
        return 0
    if args.command == "retire-source":
        retained = retire_source(args.source)
        print(f"Retired processed legacy files; retained {retained} unclassified Romanian drafts in old_content/unclassified/.")
        return 0
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print("ScriptaHub collection is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
