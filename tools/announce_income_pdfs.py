#!/usr/bin/env python3
"""Announce reviewed incoming PDF identities with honest draft catalogue metadata.

Readers are never published by this script. The intake and editorial work remain
visible in the work ledger until complete EN/RO editions pass the release gate.
"""

from __future__ import annotations

import argparse
import os
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import book_tasks  # noqa: E402
import build_books  # noqa: E402

INVENTORY = ROOT / "tasks/income-inventory.json"
COVERS = ROOT / ".book-work/income-clean-covers"
EXCLUDED = {
    "The_Grand_Defiance",
}
LANGUAGES = tuple(build_books.LANGUAGES)

FICTION = re.compile(
    r"alice|dracula|moby|oliver twist|peter pan|white fang|wuthering|"
    r"yellow wallpaper|count fathom|robinson crusoe|lost world|call of the wild|"
    r"sleepy hollow|enchanted april|grimms|pride and prejudice|frankenstein|"
    r"karamazov|hunger games|dune|solitude|catcher in the rye|hitchhiker|"
    r"foundation series|1984|hobbit|star trek|star wars|warhammer|expanse|"
    r"left hand of darkness|book thief|gatsby|les mis|don quixote|"
    r"jane eyre|matrix universe|cyberpunk|ender|mockingbird|altered carbon|"
    r"martian|red mars|tale of two cities|alchemist|magic mountain|"
    r"the grand defiance|echoes from beyond|horizon of fools|swipe or not",
    re.I,
)

NOVEL_TOPICS = {
    "Alice s Adventures in Wonderland": ["Alice's fall down the rabbit hole", "the changing rules of Wonderland", "the Cheshire Cat", "the Queen of Hearts", "Alice's trial"],
    "Dracula": ["Jonathan Harker's journey to Transylvania", "Count Dracula's arrival in England", "Lucy Westenra's illness", "Mina Harker's records", "the pursuit of Dracula"],
    "Grimms Fairy Tales": ["the collected folk tales", "enchanted forests and households", "promises and bargains", "danger and transformation", "the tales' moral endings"],
    "Moby Dick Or The Whale": ["Ishmael's voyage aboard the Pequod", "Captain Ahab's pursuit", "the white whale", "life aboard a whaling ship", "obsession and revenge"],
    "Oliver Twist": ["Oliver's childhood in the workhouse", "his journey to London", "Fagin's group of thieves", "Nancy's difficult choices", "poverty and social injustice"],
    "Peter Pan": ["the Darling children's journey", "Neverland and the Lost Boys", "Peter Pan and Wendy", "Captain Hook", "childhood and growing up"],
    "The Call of the Wild": ["Buck's removal from home", "survival in the Yukon", "sled teams and their owners", "John Thornton", "Buck's return to the wild"],
    "The Enchanted April": ["the holiday in Italy", "four women sharing a villa", "loneliness and friendship", "marriage and independence", "change through companionship"],
    "The Legend of Sleepy Hollow": ["Ichabod Crane", "the village of Sleepy Hollow", "Katrina Van Tassel", "the Headless Horseman", "fear and local storytelling"],
    "The Life and Adventures of Robinson Crusoe": ["Crusoe's voyage", "life on the island", "survival and daily work", "Friday's arrival", "return from isolation"],
    "The Lost World": ["Professor Challenger's expedition", "the journey to South America", "the isolated plateau", "prehistoric creatures", "the explorers' return"],
    "The Yellow Wallpaper": ["a woman's confinement", "the room and its wallpaper", "the narrator's private writing", "her changing perception", "control and mental distress"],
    "White Fang": ["White Fang's life in the wild", "encounters with people", "violence and survival", "Weedon Scott's care", "trust and belonging"],
    "Wuthering Heights": ["Catherine and Heathcliff", "the houses of Wuthering Heights and Thrushcross Grange", "family conflict", "love and revenge", "the next generation"],
}

GROUP_OVERRIDES = {
    "AI and the New Educational Frontier": "technology",
    "Between War and Peace The Human Experience": "society",
    "Blockchain and AI Strategies for Winning Enterprise Customers": "business",
    "Dostoevsky s vision of morality Crime and Punishment": "fiction",
    "Exploring Freedom and Serfdom on the Path to Liberty": "society",
    "Introduction to Artificial Intelligence": "technology",
    "Inventors Ideas For Curious Kids Big and Small": "science",
    "Mastering Human Like Writing with AI": "technology",
    "Messi or Ronaldo The End of an Era": "society",
    "Narrative of the Life of FREDERICK DOUGLASS": "society",
    "Navigating The Three Body Problem Universe": "fiction",
    "Parasitic Behaviors in Modern Organizations": "business",
    "SG 1 Universe": "fiction",
    "The Global Identity Trap": "society",
    "The Life of Elon Musk From Roots to Rockets": "technology",
    "The Road to AGI Milestones and Conceptual Challenges": "technology",
    "The Strange Case of Dr Jekyll and Mr Hyde": "fiction",
    "The Ultimate Slave Owner s Handbook An Endless Ode to Servitude": "society",
    "The Unwritten Masterpiece A Treatise on Literary Futility and the Illusion of Profundity": "fiction",
    "The genius of the Renaissance Leonardo da Vinci": "science",
    "Top 15 Must Watch Action TV Series": "society",
}

TITLE_OVERRIDES = {
    "A_Woman_Fight_for_Freedom_Jane_Eyre": "A Woman’s Fight for Freedom: Jane Eyre",
    "Gatsby_s_Journey___The_American_Dream": "Gatsby’s Journey: The American Dream Exposed",
    "Inventors___Ideas__For_Curious_Kids__Big_and_Small": "Inventors & Ideas: For Curious Kids, Big and Small",
    "Silent_Spies___How_Your_Watch_You": "Silent Spies: How Do Your Devices Watch You?",
    "The__Mockingbird_s__Impact_on_Today_Society": "The ‘Mockingbird’s’ Impact on Today’s Society",
}

DESCRIPTION = {
    "en": ('The book introduces {a}.', 'Its discussion turns to {b}.', 'Another section examines {c}.', 'The source also develops {d}.', 'A later passage addresses {e}.', 'Together, these subjects frame the book’s {field} focus.'),
    "fr": ('Le livre présente {a}.', 'Le texte aborde ensuite {b}.', 'Une autre section examine {c}.', 'Le livre développe aussi {d}.', 'Un passage ultérieur traite de {e}.', 'Ces sujets dessinent son approche de {field}.'),
    "de": ('Das Buch führt in {a} ein.', 'Der Text wendet sich dann {b} zu.', 'Ein weiterer Abschnitt untersucht {c}.', 'Das Buch entwickelt auch {d}.', 'Eine spätere Passage behandelt {e}.', 'Diese Themen prägen seinen Schwerpunkt auf {field}.'),
    "es": ('El libro presenta {a}.', 'Después, el texto aborda {b}.', 'Otra sección examina {c}.', 'El libro también desarrolla {d}.', 'Un pasaje posterior trata {e}.', 'Estos temas definen su enfoque de {field}.'),
    "pt": ('O livro apresenta {a}.', 'Em seguida, o texto aborda {b}.', 'Outra seção examina {c}.', 'O livro também desenvolve {d}.', 'Uma passagem posterior trata de {e}.', 'Esses temas definem seu enfoque de {field}.'),
    "it": ('Il libro presenta {a}.', 'Il testo affronta poi {b}.', 'Un’altra sezione esamina {c}.', 'Il libro sviluppa anche {d}.', 'Un passaggio successivo tratta {e}.', 'Questi temi definiscono il suo approccio a {field}.'),
    "ro": ('Cartea prezintă {a}.', 'Textul abordează apoi {b}.', 'O altă secțiune examinează {c}.', 'Cartea dezvoltă și {d}.', 'Un pasaj ulterior tratează {e}.', 'Aceste teme conturează perspectiva sa asupra {field}.'),
    "pl": ('Książka przedstawia {a}.', 'Następnie tekst omawia {b}.', 'Kolejny rozdział bada {c}.', 'Książka rozwija także {d}.', 'Późniejszy fragment dotyczy {e}.', 'Te tematy określają jej spojrzenie na {field}.'),
}

ABOUT = {
    "en": (
        'The book begins with {a} and then sets it beside {b}. Its sections give distinct attention to {c}, tracing how these ideas or events enter the wider subject. The order places the first two topics before the more detailed discussion that follows.',
        'Later material discusses {d} and {e}. These strands establish the book’s scope and help readers decide where to begin. The sequence of topics makes clear which questions or events receive sustained attention in the text.'),
    "fr": (
        'Le texte commence par {a}, puis le rapproche de {b}. Ses sections accordent une attention particulière à {c} et situent ces idées ou événements dans le sujet général. Cet ordre fait précéder la discussion détaillée par les deux premiers thèmes.',
        'La suite traite de {d} et de {e}. Ces fils montrent l’étendue du livre et aident à choisir un point de départ. La progression indique les questions ou événements auxquels le texte accorde une attention soutenue.'),
    "de": (
        'Das Buch beginnt mit {a} und stellt es neben {b}. Seine Abschnitte widmen sich besonders {c} und ordnen diese Gedanken oder Ereignisse in das größere Thema ein. Die ersten beiden Themen stehen vor der ausführlicheren Erörterung.',
        'Spätere Teile behandeln {d} und {e}. Diese Stränge zeigen den Umfang des Buches und helfen bei der Wahl eines Einstiegs. Die Abfolge macht sichtbar, welchen Fragen oder Ereignissen der Text besondere Aufmerksamkeit schenkt.'),
    "es": (
        'El texto comienza con {a} y después lo relaciona con {b}. Sus secciones prestan atención especial a {c} y sitúan estas ideas o hechos en el tema general. Los dos primeros asuntos preceden el análisis más detallado.',
        'Más adelante se tratan {d} y {e}. Estos hilos muestran el alcance del libro y ayudan a elegir por dónde empezar. La progresión indica las preguntas o los hechos que reciben atención sostenida.'),
    "pt": (
        'O texto começa com {a} e depois o relaciona com {b}. Suas seções dão atenção especial a {c} e situam essas ideias ou acontecimentos no tema mais amplo. Os dois primeiros assuntos vêm antes da análise mais detalhada.',
        'Mais adiante aparecem {d} e {e}. Esses fios mostram o alcance do livro e ajudam a escolher um ponto de partida. A sequência indica as perguntas ou acontecimentos que recebem atenção contínua.'),
    "it": (
        'Il testo inizia con {a} e poi lo accosta a {b}. Le sue sezioni dedicano attenzione a {c} e collocano queste idee o vicende nel tema più ampio. I primi due argomenti precedono l’esame più dettagliato.',
        'Più avanti compaiono {d} ed {e}. Questi fili mostrano l’ampiezza del libro e aiutano a scegliere da dove iniziare. La sequenza indica le domande o gli eventi cui il testo dedica maggiore attenzione.'),
    "ro": (
        'Textul începe cu {a} și îl pune apoi alături de {b}. Secțiunile sale acordă atenție lui {c} și așază aceste idei sau întâmplări în tema mai largă. Primele două subiecte preced analiza mai detaliată.',
        'Mai târziu apar {d} și {e}. Aceste fire arată întinderea cărții și ajută cititorul să aleagă de unde începe. Succesiunea arată întrebările sau întâmplările cărora textul le acordă atenție susținută.'),
    "pl": (
        'Tekst rozpoczyna się od {a}, a następnie zestawia ten temat z {b}. Jego części poświęcają uwagę {c} i umieszczają te idee lub wydarzenia w szerszym kontekście. Dwa pierwsze tematy poprzedzają bardziej szczegółowe omówienie.',
        'Dalsze fragmenty omawiają {d} i {e}. Te wątki pokazują zakres książki i pomagają wybrać punkt wyjścia. Kolejność wskazuje pytania lub wydarzenia, którym tekst poświęca szczególną uwagę.'),
}

SUBTITLE = {
    "en": "Themes of {a} and {b}", "fr": "Thèmes de {a} et {b}",
    "de": "Themen zu {a} und {b}", "es": "Temas de {a} y {b}",
    "pt": "Temas de {a} e {b}", "it": "Temi di {a} e {b}",
    "ro": "Teme despre {a} și {b}", "pl": "Tematy {a} i {b}",
}


def clean_title(folder: str) -> str:
    if folder in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[folder]
    title = re.sub(r"\s+", " ", folder.replace("___", ": ").replace("_", " ")).strip(" .")
    return re.sub(r"\b([A-Za-z]+) s\b", r"\1’s", title)


def update_route_if_needed(work: Path, release: dict, title: str) -> dict:
    route = list(build_books.title_route(title))
    new_directory = "/".join(["books", *route, release["bookId"]])
    if release["directory"] == new_directory and release["englishTitle"] == title:
        return release
    old_target = ROOT / "docs" / release["directory"]
    new_target = ROOT / "docs" / new_directory
    if old_target != new_target and old_target.exists():
        if new_target.exists():
            manifest = book_tasks.read(new_target / "manifest.json")
            if manifest["id"] != release["bookId"]:
                raise ValueError(f"Route collision: {new_target}")
            raise ValueError(f"Both old and new draft routes exist: {old_target}, {new_target}")
        new_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(old_target, new_target)
        parent = old_target.parent
        books_root = ROOT / "docs/books"
        while parent != books_root and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent
    release["englishTitle"] = title
    release["directory"] = new_directory
    book_tasks.write(work / "release.json", release)
    for path in (work / "book/manifest.json", new_target / "manifest.json"):
        if path.is_file():
            manifest = book_tasks.read(path)
            manifest["route"] = route
            manifest["title"]["en"] = title
            book_tasks.write(path, manifest)
    return release


def topics(source: Path, title: str) -> list[str]:
    novel = next((value for key, value in NOVEL_TOPICS.items() if book_tasks.normalise(key) == book_tasks.normalise(title)), None)
    if novel:
        return novel
    raw = subprocess.check_output(["pdftotext", "-f", "1", "-l", "12", "-layout", str(source), "-"], text=True, errors="replace")
    found: list[str] = []
    for line in raw.splitlines():
        if not re.search(r"\.{5,}\s*\d+\s*$", line):
            continue
        value = re.sub(r"\.{5,}\s*\d+\s*$", "", line).strip()
        value = re.sub(r"\s+", " ", value)
        if len(value.split()) < 2 or len(value.split()) > 12:
            continue
        if re.search(r"^(chapter|part|section|preface|introduction|conclusion|annex|appendix|about|a letter|legal|copyright|note|references|bibliography|table of contents|ai perspective|main characters|plot summary|historical and cultural context)\b", value, re.I):
            continue
        if re.search(r"outfinity|gift|supporters|ai author|personality|contents", value, re.I):
            continue
        value = re.sub(r"[.!?]+", "", value).strip(" :;—–-")
        if value and value.casefold() not in {item.casefold() for item in found}:
            found.append(value)
    # Chapterless fiction can still be announced by its distinctive title;
    # the landing copy remains marked as a draft until source review.
    fallback = [title, *re.split(r"\s+(?:and|or|of|the|in|to|from|with|into|through)\s+", title, flags=re.I)]
    for phrase in fallback:
        phrase = " ".join(re.sub(r"[.!?]+", "", phrase).strip(" :;—–-").split()[:8])
        if len(phrase) > 3 and phrase.casefold() not in {item.casefold() for item in found}:
            found.append(phrase)
        if len(found) >= 5:
            break
    return (found + [title] * 5)[:5]


def classify(title: str, terms: list[str]) -> tuple[str, str]:
    override = next((value for key, value in GROUP_OVERRIDES.items() if book_tasks.normalise(key) == book_tasks.normalise(title)), None)
    if override:
        group = override
        return group, {"fiction": "Literature", "technology": "Technology", "science": "Science", "philosophy": "Philosophy", "business": "Economics", "society": "Society"}[group]
    sample = f"{title} {' '.join(terms)}".lower()
    if FICTION.search(sample):
        return "fiction", "Literature"
    if re.search(r"market|finance|bitcoin|economic|capitalism|bank|entrepreneur|money|business|salary|client|wealth", sample):
        return "business", "Economics"
    if re.search(r"philosoph|logic|faith|existence|kabbalah|taoism|moral|free will|meaning", sample):
        return "philosophy", "Philosophy"
    if re.search(r"science|physics|universe|planet|einstein|newton|tesla|darwin|edison|biology", sample):
        return "science", "Science"
    if re.search(r"society|culture|history|freedom|control|conspir|holocaust|social|government|politic", sample):
        return "society", "Society"
    return "technology", "Technology"


def manifest_for(release: dict, terms: list[str]) -> dict:
    title = release["englishTitle"]
    group, category = classify(title, terms)
    broad = build_books.keyword_catalog(group)
    fields = {code: build_books.SHELF_CATEGORIES[group][code].split("|")[0] for code in LANGUAGES}
    descriptions = {}
    about = {}
    subtitles = {}
    for code in LANGUAGES:
        values = dict(zip("abcde", terms, strict=True))
        values.update(title=title, field=fields[code])
        descriptions[code] = " ".join(sentence.format(**values) for sentence in DESCRIPTION[code])
        about[code] = [paragraph.format(**values) for paragraph in ABOUT[code]]
        subtitles[code] = SUBTITLE[code].format(**values)
    route = list(build_books.title_route(title))
    return {
        "schemaVersion": 1, "id": release["bookId"],
        "sourceId": Path(release["source"]).parent.name,
        "sourceAliases": [Path(release["source"]).parent.name],
        "route": route, "category": category, "group": group,
        "title": {code: title for code in LANGUAGES},
        "subtitle": subtitles, "shortDescription": descriptions, "aboutBook": about,
        "keywordIds": [item[0] for item in broad],
        "keywords": {code: [item[2][code] for item in broad] for code in LANGUAGES},
        "coverUrl": {code: f"{code}/cover.webp" for code in LANGUAGES},
        "thumbnailUrl": {code: f"{code}/thumbnail.webp" for code in LANGUAGES},
        "editions": {code: {"book": f"{code}/book.html", "cover": f"{code}/cover.webp", "sourceCover": f"{code}/cover.png", "thumbnail": f"{code}/thumbnail.webp"} for code in LANGUAGES},
        "availableLanguages": [], "publicationStatus": "preparing", "currentEdition": None,
        "releasePolicy": "en-ro-on-request",
        "metadataDraft": {"sourceSha256": release["sha256"], "sourceHeadings": terms, "reviewRequired": True},
    }


def deduplicate_covers(target: Path, pending_id: str) -> None:
    """Preserve every language path while sharing identical cover bytes on disk."""
    primary = target / "en"
    for name in ("cover.png", "cover.webp", "thumbnail.webp"):
        source = primary / name
        if not source.is_file():
            continue
        source_hash = book_tasks.sha256(source)
        candidates = [target / code / name for code in LANGUAGES if code != "en"]
        if name == "cover.webp":
            candidates += list((target / "edition-files" / pending_id / "covers").glob("*.webp"))
        for destination in candidates:
            if not destination.is_file() or os.path.samefile(source, destination):
                continue
            if book_tasks.sha256(destination) != source_hash:
                continue
            destination.unlink()
            os.link(source, destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new-only", action="store_true", help="Leave already announced entries untouched when their cleaned cover is unchanged")
    args = parser.parse_args()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))["sources"]
    announced = []
    missing = []
    for entry in inventory:
        if entry["format"] != "pdf" or entry["status"] != "new-book":
            continue
        folder = Path(entry["source"]).parent.name
        if folder in EXCLUDED:
            continue
        cover = COVERS / f"{folder}.png"
        if not cover.is_file():
            missing.append(folder)
            continue
        source = ROOT / entry["source"]
        title = clean_title(folder)
        if args.new_only:
            old_work = ROOT / ".book-work" / f"{book_tasks.normalise(folder)}-v1-{entry['sha256'][:12]}"
            old_release_path = old_work / "release.json"
            if old_release_path.is_file():
                old_release = book_tasks.read(old_release_path)
                old_target = ROOT / "docs" / old_release["directory"]
                if (old_target / "manifest.json").is_file() and old_release.get("coverSource", {}).get("sha256") == book_tasks.sha256(cover):
                    announced.append({"source": entry["source"], "workdir": str(old_work.relative_to(ROOT)), "directory": str(old_target.relative_to(ROOT)), "bookId": old_release["bookId"]})
                    continue
        work = book_tasks.prepare(source, "en", title)
        release = book_tasks.read(work / "release.json")
        release = update_route_if_needed(work, release, title)
        release["contributors"] = [
            {"authorId": "axiologic-research", "role": "contributor", "statementId": "incoming-axiologic"},
            {"authorId": "outfinity-srl", "role": "contributor", "statementId": "incoming-outfinity"},
        ]
        book_tasks.write(work / "release.json", release)
        meta_path = work / "book/manifest.json"
        meta = manifest_for(release, topics(source, title))
        if meta_path.is_file():
            existing = book_tasks.read(meta_path)
            if existing.get("metadataDraft", {}).get("sourceSha256") == release["sha256"]:
                existing.update(meta)
                meta = existing
        book_tasks.write(meta_path, meta)
        if release.get("coverSource", {}).get("sha256") != book_tasks.sha256(cover) or not (work / "book/en/cover.webp").is_file():
            book_tasks.stage_cover(work, cover)
        target = book_tasks.announce(work)
        release = book_tasks.read(work / "release.json")
        public_manifest = target / "manifest.json"
        public = book_tasks.read(public_manifest)
        if public.get("metadataDraft", {}).get("sourceSha256") == release["sha256"]:
            for field in ("route", "title", "category", "group", "subtitle", "shortDescription", "aboutBook", "metadataDraft"):
                public[field] = meta[field]
            book_tasks.write(public_manifest, public)
        history_path = target / "editions.json"
        history = book_tasks.read(history_path)
        for pending in history["editions"]:
            if pending.get("status") == "preparing" and pending.get("source", {}).get("sha256") == release["sha256"]:
                pending["contributors"] = release["contributors"]
        book_tasks.write(history_path, history)
        deduplicate_covers(target, release["editionId"])
        announced.append({"source": entry["source"], "workdir": str(work.relative_to(ROOT)), "directory": str(target.relative_to(ROOT)), "bookId": release["bookId"]})
    report = {"schemaVersion": 1, "announced": announced, "pendingCovers": missing}
    book_tasks.write(ROOT / "tasks/income-pdf-announcements.json", report)
    for directory in sorted((ROOT / "docs/books").glob("**/*"), key=lambda path: len(path.parts), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    print(f"Announced {len(announced)} PDF books; {len(missing)} awaiting cleaned covers")


if __name__ == "__main__":
    main()
