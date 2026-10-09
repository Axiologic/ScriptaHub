#!/usr/bin/env python3
"""Source-grounded editorial metadata for this staged release."""
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "book/manifest.json"
m = json.loads(p.read_text(encoding="utf-8"))

copy = {
"en": (
"Was the 2008 Crash Planned for Bitcoin?",
"Cryptographic precursors, financial collapse, and a speculative question",
"The book traces technical ideas that preceded Bitcoin. It describes the 2008 banking and housing collapse. It connects the crisis to a loss of trust in established finance. Events from 2000 to 2008 provide context for the world economy. A later chapter considers a theory of deliberate orchestration. The conclusion distinguishes that theory from proven evidence.",
"The opening chapter follows cryptography, digital money and proof of work before Bitcoin. The next chapter examines the housing and banking crisis and asks why a currency outside conventional institutions might appeal at that moment. A third chapter relates earlier geopolitical events and monetary policy to the financial setting.",
"The fourth chapter explores a possible deliberate collapse, but the book's conclusion states that no concrete evidence establishes such a plan. The reader can follow the author's question while keeping the documented sequence of events separate from the speculative explanation. The bibliography names Satoshi Nakamoto's Bitcoin paper and Adam Back's Hashcash paper."),
"ro": (
"A fost planificată criza din 2008 pentru Bitcoin?",
"Precursorii criptografici, criza financiară și o întrebare speculativă",
"Cartea urmărește ideile tehnice care au precedat Bitcoin. Descrie prăbușirea băncilor și a pieței imobiliare în 2008. Leagă criza de pierderea încrederii în finanțele tradiționale. Evenimentele dintre 2000 și 2008 oferă context istoric. Un capitol examinează teoria unei orchestrări deliberate. Concluzia deosebește această teorie de dovezile demonstrate.",
"Primul capitol urmărește criptografia, banii digitali și dovada muncii înainte de Bitcoin. Următorul examinează criza imobiliară și bancară și întreabă de ce ar deveni atractivă o monedă independentă de instituțiile obișnuite. Al treilea pune evenimentele geopolitice și politica monetară în contextul financiar.",
"Al patrulea capitol explorează posibilitatea unui colaps deliberat, însă concluzia afirmă că nu există dovezi concrete pentru un asemenea plan. Cititorul poate urmări întrebarea autorului și poate separa evenimentele prezentate de explicația speculativă. Bibliografia menționează lucrările despre Bitcoin ale lui Satoshi Nakamoto și Hashcash ale lui Adam Back."),
"fr": (
"Le krach de 2008 a-t-il été planifié pour Bitcoin ?",
"Précurseurs cryptographiques, crise financière et hypothèse spéculative",
"Le livre retrace des idées techniques antérieures à Bitcoin. Il décrit l'effondrement bancaire et immobilier de 2008. Il relie cette crise à la défiance envers la finance traditionnelle. Les événements de 2000 à 2008 fournissent un contexte historique. Un chapitre examine la théorie d'une orchestration délibérée. La conclusion distingue cette hypothèse des faits établis.",
"Le premier chapitre suit la cryptographie, la monnaie numérique et la preuve de travail avant Bitcoin. Le suivant examine la crise immobilière et bancaire et demande pourquoi une monnaie indépendante des institutions habituelles pouvait séduire. Un troisième chapitre situe les événements géopolitiques et la politique monétaire dans ce contexte financier.",
"Le quatrième chapitre explore la possibilité d'un effondrement organisé, mais la conclusion affirme qu'aucune preuve concrète ne démontre un tel plan. Le lecteur peut suivre la question de l'auteur tout en séparant la chronologie des événements de son interprétation spéculative. La bibliographie cite les textes de Satoshi Nakamoto sur Bitcoin et d'Adam Back sur Hashcash."),
"de": (
"War der Crash von 2008 für Bitcoin geplant?",
"Kryptografische Vorläufer, Finanzkrise und eine spekulative Frage",
"Das Buch verfolgt technische Ideen vor Bitcoin. Es beschreibt den Banken- und Immobilienkollaps von 2008. Es verbindet die Krise mit schwindendem Vertrauen in traditionelle Finanzinstitutionen. Ereignisse von 2000 bis 2008 liefern historischen Kontext. Ein Kapitel prüft die Theorie einer bewussten Inszenierung. Das Fazit trennt diese Theorie von belegten Erkenntnissen.",
"Das erste Kapitel behandelt Kryptografie, digitales Geld und Proof of Work vor Bitcoin. Danach untersucht das Buch die Immobilien- und Bankenkrise und fragt, warum eine Währung außerhalb üblicher Institutionen damals anziehend sein konnte. Ein drittes Kapitel ordnet geopolitische Ereignisse und Geldpolitik in das finanzielle Umfeld ein.",
"Das vierte Kapitel erörtert einen möglicherweise absichtlich herbeigeführten Zusammenbruch; das Fazit betont jedoch, dass konkrete Beweise für einen solchen Plan fehlen. Leser können der Frage des Autors folgen und zugleich die dargestellten Ereignisse von ihrer spekulativen Deutung trennen. Die Bibliografie nennt Arbeiten von Satoshi Nakamoto über Bitcoin und Adam Back über Hashcash."),
"es": (
"¿Se planeó la crisis de 2008 para Bitcoin?",
"Antecedentes criptográficos, crisis financiera y una pregunta especulativa",
"El libro recorre ideas técnicas anteriores a Bitcoin. Describe el colapso bancario e inmobiliario de 2008. Vincula la crisis con la pérdida de confianza en las finanzas tradicionales. Los sucesos de 2000 a 2008 aportan contexto histórico. Un capítulo examina la teoría de una orquestación deliberada. La conclusión distingue esa teoría de los hechos demostrados.",
"El primer capítulo sigue la criptografía, el dinero digital y la prueba de trabajo antes de Bitcoin. El siguiente examina la crisis inmobiliaria y bancaria y pregunta por qué podía atraer una moneda ajena a las instituciones habituales. Un tercer capítulo sitúa los sucesos geopolíticos y la política monetaria en ese entorno financiero.",
"El cuarto capítulo explora un posible colapso deliberado, pero la conclusión afirma que no hay pruebas concretas de tal plan. El lector puede seguir la pregunta del autor mientras separa la secuencia de hechos de su explicación especulativa. La bibliografía cita los trabajos de Satoshi Nakamoto sobre Bitcoin y de Adam Back sobre Hashcash."),
"pt": (
"A crise de 2008 foi planeada para o Bitcoin?",
"Precursores criptográficos, crise financeira e uma questão especulativa",
"O livro acompanha ideias técnicas anteriores ao Bitcoin. Descreve o colapso bancário e imobiliário de 2008. Relaciona a crise com a perda de confiança nas finanças tradicionais. Os acontecimentos de 2000 a 2008 fornecem contexto histórico. Um capítulo examina a teoria de uma orquestração deliberada. A conclusão distingue essa hipótese dos factos comprovados.",
"O primeiro capítulo aborda criptografia, dinheiro digital e prova de trabalho antes do Bitcoin. O seguinte examina a crise imobiliária e bancária e pergunta por que uma moeda independente das instituições habituais poderia atrair interesse. Um terceiro capítulo situa acontecimentos geopolíticos e política monetária nesse contexto financeiro.",
"O quarto capítulo explora a possibilidade de um colapso deliberado, mas a conclusão afirma que não existem provas concretas de tal plano. O leitor pode acompanhar a pergunta do autor e separar a sequência dos acontecimentos da interpretação especulativa. A bibliografia cita os trabalhos de Satoshi Nakamoto sobre Bitcoin e de Adam Back sobre Hashcash."),
"it": (
"Il crollo del 2008 fu pianificato per Bitcoin?",
"Precursori crittografici, crisi finanziaria e un'ipotesi speculativa",
"Il libro ripercorre idee tecniche anteriori a Bitcoin. Descrive il crollo bancario e immobiliare del 2008. Collega la crisi alla perdita di fiducia nella finanza tradizionale. Gli eventi dal 2000 al 2008 offrono il contesto storico. Un capitolo esamina la teoria di un'orchestrazione deliberata. La conclusione distingue tale teoria dai fatti dimostrati.",
"Il primo capitolo segue crittografia, denaro digitale e proof of work prima di Bitcoin. Il successivo esamina la crisi immobiliare e bancaria e chiede perché una moneta esterna alle istituzioni consuete potesse attrarre. Un terzo capitolo colloca eventi geopolitici e politica monetaria nel relativo contesto finanziario.",
"Il quarto capitolo esplora un possibile crollo deliberato, ma la conclusione afferma che non esistono prove concrete di un simile piano. Il lettore può seguire la domanda dell'autore separando la sequenza degli eventi dalla sua spiegazione speculativa. La bibliografia cita gli scritti di Satoshi Nakamoto su Bitcoin e di Adam Back su Hashcash."),
"pl": (
"Czy krach w 2008 roku zaplanowano dla Bitcoina?",
"Kryptograficzni poprzednicy, kryzys finansowy i spekulacyjne pytanie",
"Książka opisuje idee techniczne poprzedzające Bitcoin. Przedstawia załamanie banków i rynku nieruchomości w 2008 roku. Łączy kryzys z utratą zaufania do tradycyjnych finansów. Wydarzenia z lat 2000–2008 tworzą kontekst historyczny. Jeden rozdział rozważa teorię celowej koordynacji. Zakończenie oddziela tę teorię od udowodnionych faktów.",
"Pierwszy rozdział omawia kryptografię, pieniądz cyfrowy i dowód pracy przed Bitcoinem. Następny analizuje kryzys bankowy i mieszkaniowy oraz pyta, dlaczego waluta niezależna od zwykłych instytucji mogła wtedy przyciągać uwagę. Trzeci rozdział umieszcza wydarzenia geopolityczne i politykę pieniężną w kontekście finansowym.",
"Czwarty rozdział rozważa możliwość celowo wywołanego załamania, lecz zakończenie stwierdza, że brak konkretnych dowodów na taki plan. Czytelnik może śledzić pytanie autora, oddzielając przedstawione wydarzenia od spekulacyjnej interpretacji. Bibliografia wymienia prace Satoshiego Nakamoto o Bitcoinie i Adama Backa o Hashcash."),
}

for lang, (title, subtitle, short, first, second) in copy.items():
    m["title"][lang] = title
    m["subtitle"][lang] = subtitle
    m["shortDescription"][lang] = short
    m["aboutBook"][lang] = [first, second]
m["shortDescriptionEditorial"] = {
    "method": "active-LLM authored and translated; source chapters and conclusion reviewed",
    "sourceSha256": "45859534d7ccbbf3ac4ce5f8b359ba2e94420e6b0d39e629678a14afb7ca557b",
    "sentencesPerLanguage": 6,
    "status": "reviewed",
}
m.pop("metadataDraft", None)
p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for lang, (_, _, short, first, second) in copy.items():
    assert len([s for s in short.split(". ") if s]) == 6, lang
    assert all(len(s.split()) <= 22 for s in short.split(". ")), lang
    assert 60 <= len((first + " " + second).split()) <= 250, lang
