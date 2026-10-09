import json
from pathlib import Path

root = Path('.book-work/echoesfrombeyondtheveil-v1-49afb53aab7f')
path = root / 'book/manifest.json'
book = json.loads(path.read_text(encoding='utf-8'))

titles = {
    'en': 'Echoes from Beyond the Veil',
    'fr': 'Échos d’au-delà du voile',
    'de': 'Echos jenseits des Schleiers',
    'es': 'Ecos del otro lado del velo',
    'pt': 'Ecos para além do véu',
    'it': 'Echi oltre il velo',
    'ro': 'Ecouri de dincolo de văl',
    'pl': 'Echa zza zasłony',
}
subtitles = {
    'en': 'A speculative journey through a manufactured utopia',
    'fr': 'Un voyage spéculatif dans une utopie fabriquée',
    'de': 'Eine spekulative Reise durch eine künstliche Utopie',
    'es': 'Un viaje especulativo por una utopía fabricada',
    'pt': 'Uma viagem especulativa por uma utopia fabricada',
    'it': 'Un viaggio speculativo in un’utopia costruita',
    'ro': 'O călătorie speculativă printr-o utopie construită',
    'pl': 'Spekulacyjna podróż przez stworzoną utopię',
}
sentences = {
    'en': [
        'Physicist Elara Venn lives in a seemingly perfect New Athens.',
        'An anomaly in her quantum research unsettles its orderly surface.',
        'Zephyr Kane suspects that familiar reality has been constructed.',
        'Their inquiry leads through surveillance, ancient records and a crystalline device.',
        'The novella joins scientific speculation with cosmic horror.',
        'Its four chapters ask what people risk when they question a comforting world.',
    ],
    'fr': [
        'La physicienne Elara Venn vit dans une Nouvelle Athènes apparemment parfaite.',
        'Une anomalie dans ses recherches quantiques trouble cette harmonie.',
        'Zephyr Kane soupçonne que la réalité familière est une construction.',
        'Leur enquête traverse la surveillance, des archives anciennes et un dispositif cristallin.',
        'Cette nouvelle mêle spéculation scientifique et horreur cosmique.',
        'Ses quatre chapitres interrogent les risques de mettre en doute un monde rassurant.',
    ],
    'de': [
        'Die Physikerin Elara Venn lebt in einem scheinbar perfekten Neu-Athen.',
        'Eine Anomalie in ihrer Quantenforschung stört die geordnete Oberfläche.',
        'Zephyr Kane vermutet, dass die vertraute Wirklichkeit konstruiert wurde.',
        'Ihre Suche führt durch Überwachung, alte Archive und ein kristallines Gerät.',
        'Die Novelle verbindet wissenschaftliche Spekulation mit kosmischem Horror.',
        'Vier Kapitel fragen nach dem Risiko, eine tröstliche Welt zu hinterfragen.',
    ],
    'es': [
        'La física Elara Venn vive en una Nueva Atenas aparentemente perfecta.',
        'Una anomalía en su investigación cuántica altera esa apariencia ordenada.',
        'Zephyr Kane sospecha que la realidad familiar ha sido construida.',
        'Su búsqueda atraviesa vigilancia, archivos antiguos y un dispositivo cristalino.',
        'La novela corta une especulación científica y terror cósmico.',
        'Sus cuatro capítulos preguntan qué arriesga quien cuestiona un mundo tranquilizador.',
    ],
    'pt': [
        'A física Elara Venn vive numa Nova Atenas aparentemente perfeita.',
        'Uma anomalia na sua investigação quântica perturba essa superfície ordenada.',
        'Zephyr Kane suspeita que a realidade familiar foi construída.',
        'A investigação atravessa vigilância, arquivos antigos e um dispositivo cristalino.',
        'A novela combina especulação científica com horror cósmico.',
        'Os quatro capítulos perguntam quais riscos surgem ao questionar um mundo reconfortante.',
    ],
    'it': [
        'La fisica Elara Venn vive in una Nuova Atene apparentemente perfetta.',
        'Un’anomalia nella sua ricerca quantistica incrina quella superficie ordinata.',
        'Zephyr Kane sospetta che la realtà familiare sia stata costruita.',
        'La loro indagine passa per sorveglianza, antichi archivi e un dispositivo cristallino.',
        'Il racconto unisce speculazione scientifica e orrore cosmico.',
        'I quattro capitoli chiedono cosa rischia chi mette in dubbio un mondo rassicurante.',
    ],
    'ro': [
        'Fiziciana Elara Venn trăiește într-o Nouă Atenă aparent perfectă.',
        'O anomalie din cercetarea sa cuantică tulbură această ordine.',
        'Zephyr Kane bănuiește că realitatea familiară a fost construită.',
        'Cercetarea lor trece prin supraveghere, arhive străvechi și un dispozitiv cristalin.',
        'Nuvela îmbină speculația științifică și groaza cosmică.',
        'Cele patru capitole întreabă ce riscă oamenii când contestă o lume liniștitoare.',
    ],
    'pl': [
        'Fizyczka Elara Venn żyje w pozornie doskonałych Nowych Atenach.',
        'Anomalia w jej badaniach kwantowych narusza ten uporządkowany obraz.',
        'Zephyr Kane podejrzewa, że znajoma rzeczywistość została skonstruowana.',
        'Ich śledztwo prowadzi przez nadzór, dawne archiwa i kryształowe urządzenie.',
        'Nowela łączy spekulację naukową z kosmiczną grozą.',
        'Cztery rozdziały pytają o ryzyko podważenia świata, który daje poczucie bezpieczeństwa.',
    ],
}
about = {
    'en': [
        'Elara Venn begins with a small discrepancy in quantum data and finds a city whose flawless manners conceal unease. With Zephyr Kane, she tests the limits of New Athens and searches records that suggest a reality shaped from outside.',
        'The story follows their movement from scientific doubt to a confrontation with the Cosmic Wardens. Its four chapters combine surveillance, invented mythology and multiversal science fiction while keeping the human choice to ask questions at the center.',
    ],
    'fr': [
        'Elara Venn part d’un faible écart dans des données quantiques et découvre une ville dont les manières impeccables cachent un malaise. Avec Zephyr Kane, elle éprouve les limites de la Nouvelle Athènes et consulte des archives suggérant une réalité façonnée de l’extérieur.',
        'Le récit va du doute scientifique à la confrontation avec les Gardiens cosmiques. Ses quatre chapitres mêlent surveillance, mythologie inventée et science-fiction multiverselle autour du choix humain de poser des questions.',
    ],
    'de': [
        'Elara Venn entdeckt eine kleine Abweichung in Quantendaten und eine Stadt, deren tadellose Umgangsformen Unruhe verbergen. Mit Zephyr Kane prüft sie Neu-Athens Grenzen und sucht in Archiven nach Spuren einer von außen geformten Wirklichkeit.',
        'Die Geschichte führt vom wissenschaftlichen Zweifel zur Begegnung mit den Kosmischen Wächtern. Vier Kapitel verbinden Überwachung, erfundene Mythologie und Multiversums-Fiktion mit der menschlichen Entscheidung, Fragen zu stellen.',
    ],
    'es': [
        'Elara Venn parte de una pequeña discrepancia en datos cuánticos y descubre una ciudad cuya cortesía impecable oculta inquietud. Junto a Zephyr Kane, pone a prueba Nueva Atenas y consulta archivos que sugieren una realidad moldeada desde fuera.',
        'La historia pasa de la duda científica al encuentro con los Guardianes Cósmicos. Sus cuatro capítulos combinan vigilancia, mitología inventada y ficción multiversal, con la decisión humana de preguntar en el centro.',
    ],
    'pt': [
        'Elara Venn parte de uma pequena discrepância em dados quânticos e encontra uma cidade cuja cordialidade impecável esconde inquietação. Com Zephyr Kane, testa os limites de Nova Atenas e consulta arquivos que sugerem uma realidade moldada de fora.',
        'A narrativa passa da dúvida científica ao confronto com os Guardiões Cósmicos. Os quatro capítulos juntam vigilância, mitologia inventada e ficção multiversal, mantendo no centro a escolha humana de fazer perguntas.',
    ],
    'it': [
        'Elara Venn parte da una piccola discrepanza nei dati quantistici e scopre una città la cui cortesia impeccabile nasconde inquietudine. Con Zephyr Kane mette alla prova Nuova Atene e cerca negli archivi tracce di una realtà plasmata dall’esterno.',
        'Il racconto passa dal dubbio scientifico al confronto con i Custodi Cosmici. Quattro capitoli intrecciano sorveglianza, mitologia inventata e fantascienza multiversale, ponendo al centro la scelta umana di fare domande.',
    ],
    'ro': [
        'Elara Venn pornește de la o mică abatere în datele cuantice și descoperă un oraș ale cărui maniere impecabile ascund neliniște. Alături de Zephyr Kane, testează limitele Noii Atene și caută în arhive urmele unei realități modelate din afară.',
        'Povestea trece de la îndoiala științifică la confruntarea cu Străjerii Cosmici. Cele patru capitole îmbină supravegherea, mitologia inventată și science-fictionul multiversal, păstrând în centru alegerea umană de a pune întrebări.',
    ],
    'pl': [
        'Elara Venn zaczyna od małej rozbieżności w danych kwantowych i odkrywa miasto, którego nienaganne obyczaje skrywają niepokój. Razem z Zephyrem Kane’em bada granice Nowych Aten i szuka w archiwach śladów rzeczywistości kształtowanej z zewnątrz.',
        'Opowieść przechodzi od naukowych wątpliwości do spotkania z Kosmicznymi Strażnikami. Cztery rozdziały łączą nadzór, wymyśloną mitologię i fantastykę wieloświata wokół ludzkiej decyzji, by zadawać pytania. To pytanie pozostaje w centrum opowieści.',
    ],
}

for language in titles:
    assert len(sentences[language]) == 6
    assert all(len(s.split()) <= 22 for s in sentences[language]), language
book['title'] = titles
book['subtitle'] = subtitles
book['shortDescription'] = {k: ' '.join(v) for k, v in sentences.items()}
book['aboutBook'] = about
book['shortDescriptionEditorial'] = {
    'source': 'editorial', 'status': 'reviewed',
    'basis': 'Four complete source fiction chapters on PDF pages 8–38; former project preface and annexes excluded.',
}
book['metadataDraft']['reviewRequired'] = False
path.write_text(json.dumps(book, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Authored metadata in 8 languages')
