import json
from pathlib import Path

workspace = Path(__file__).parent
manifest_path = workspace / 'book/manifest.json'
manifest = json.loads(manifest_path.read_text())
manifest['title'] = {
    'en': 'Mary Shelley’s Frankenstein',
    'fr': 'Frankenstein de Mary Shelley',
    'de': 'Mary Shelleys Frankenstein',
    'es': 'Frankenstein de Mary Shelley',
    'pt': 'Frankenstein de Mary Shelley',
    'it': 'Frankenstein di Mary Shelley',
    'ro': 'Frankenstein de Mary Shelley',
    'pl': 'Frankenstein Mary Shelley',
}
manifest['subtitle'] = {
    'en': 'A humorous retelling about creation, abandonment, and responsibility',
    'fr': 'Un récit plein d’humour sur la création, l’abandon et la responsabilité',
    'de': 'Eine humorvolle Nacherzählung über Schöpfung, Verlassenwerden und Verantwortung',
    'es': 'Un relato con humor sobre creación, abandono y responsabilidad',
    'pt': 'Uma narrativa com humor sobre criação, abandono e responsabilidade',
    'it': 'Un racconto ironico su creazione, abbandono e responsabilità',
    'ro': 'O repovestire cu umor despre creație, abandon și responsabilitate',
    'pl': 'Opowieść z humorem o stworzeniu, porzuceniu i odpowiedzialności',
}
sentences = {
    'en': [
        'Victor Frankenstein creates life and abandons the being he has made.',
        'Rejection leaves the creature searching for language, belonging, and companionship.',
        'William and Justine reveal the cost of Victor’s silence.',
        'A destroyed second creation turns a promise into revenge.',
        'The wedding night and Arctic pursuit bring creator and creature to ruin.',
        'Humour sharpens a question about scientific power and responsibility.',
    ],
    'fr': [
        'Victor Frankenstein crée la vie puis abandonne l’être qu’il a fabriqué.',
        'Le rejet pousse la créature à chercher langage, appartenance et compagnie.',
        'William et Justine révèlent le prix du silence de Victor.',
        'Une seconde création détruite transforme une promesse en vengeance.',
        'La nuit de noces et la poursuite arctique conduisent les deux êtres à la ruine.',
        'L’humour aiguise la question du pouvoir scientifique et de la responsabilité.',
    ],
    'de': [
        'Victor Frankenstein erschafft Leben und verlässt das Wesen sofort.',
        'Ablehnung lässt die Kreatur nach Sprache, Zugehörigkeit und Gesellschaft suchen.',
        'William und Justine zeigen den Preis von Victors Schweigen.',
        'Eine zerstörte zweite Schöpfung verwandelt ein Versprechen in Rache.',
        'Hochzeitsnacht und arktische Verfolgung führen Schöpfer und Geschöpf ins Verderben.',
        'Humor schärft die Frage nach wissenschaftlicher Macht und Verantwortung.',
    ],
    'es': [
        'Victor Frankenstein crea vida y abandona al ser que ha formado.',
        'El rechazo lleva a la criatura a buscar lenguaje, pertenencia y compañía.',
        'William y Justine muestran el precio del silencio de Victor.',
        'Una segunda creación destruida convierte una promesa en venganza.',
        'La noche de bodas y la persecución ártica arruinan a creador y criatura.',
        'El humor agudiza la pregunta sobre poder científico y responsabilidad.',
    ],
    'pt': [
        'Victor Frankenstein cria vida e abandona o ser que fez.',
        'A rejeição leva a criatura a procurar linguagem, pertença e companhia.',
        'William e Justine mostram o custo do silêncio de Victor.',
        'Uma segunda criação destruída transforma uma promessa em vingança.',
        'A noite de núpcias e a perseguição ártica arruínam criador e criatura.',
        'O humor acentua a questão do poder científico e da responsabilidade.',
    ],
    'it': [
        'Victor Frankenstein crea la vita e abbandona l’essere che ha fatto.',
        'Il rifiuto spinge la creatura a cercare lingua, appartenenza e compagnia.',
        'William e Justine mostrano il costo del silenzio di Victor.',
        'Una seconda creazione distrutta trasforma una promessa in vendetta.',
        'La notte di nozze e l’inseguimento artico portano creatore e creatura alla rovina.',
        'L’ironia rende più acuta la domanda sul potere scientifico e la responsabilità.',
    ],
    'ro': [
        'Victor Frankenstein creează viață și abandonează ființa pe care a făcut-o.',
        'Respingerea împinge creatura să caute limbaj, apartenență și tovărășie.',
        'William și Justine arată prețul tăcerii lui Victor.',
        'O a doua creație distrusă transformă o promisiune în răzbunare.',
        'Noaptea nunții și urmărirea arctică îi duc la ruină pe creator și creatură.',
        'Umorul face mai ascuțită întrebarea despre puterea științei și responsabilitate.',
    ],
    'pl': [
        'Victor Frankenstein tworzy życie i porzuca stworzoną istotę.',
        'Odrzucenie każe stworzeniu szukać języka, przynależności i towarzystwa.',
        'William i Justine ukazują cenę milczenia Victora.',
        'Zniszczenie drugiej istoty zmienia obietnicę w zemstę.',
        'Noc poślubna i arktyczny pościg prowadzą twórcę i stworzenie do zguby.',
        'Humor wyostrza pytanie o władzę nauki i odpowiedzialność.',
    ],
}
manifest['shortDescription'] = {language: ' '.join(lines) for language, lines in sentences.items()}
manifest['aboutBook'] = {
    'en': [
        'This humorous 2024 retelling follows Victor Frankenstein from his early fascination with alchemy to the creation of a living being at Ingolstadt. Frightened by his success, Victor abandons the creature. The account follows the resulting deaths of William and Justine, the creature’s experience of rejection, and its demand for a companion.',
        'Victor’s destruction of the second creation leads to threats, the death of Elizabeth, and a pursuit into the Arctic. Final reflections connect the story’s ambition and abandonment to questions about artificial intelligence, biotechnology, and the duties attached to new powers. This is a reading of Shelley’s novel, not the original 1818 novel itself.',
    ],
    'fr': [
        'Cette reprise humoristique de 2024 suit Victor Frankenstein de son intérêt pour l’alchimie à la création d’un être vivant à Ingolstadt. Effrayé par sa réussite, Victor abandonne la créature. Le récit suit alors les morts de William et Justine, le rejet subi par la créature et sa demande d’une compagne.',
        'La destruction de la seconde création mène aux menaces, à la mort d’Elizabeth et à une poursuite dans l’Arctique. Les réflexions finales relient ambition et abandon aux questions d’intelligence artificielle, de biotechnologie et de responsabilité. Il s’agit d’une lecture du roman de Shelley, non du roman original de 1818.',
    ],
    'de': [
        'Diese humorvolle Nacherzählung von 2024 begleitet Victor Frankenstein von seiner frühen Begeisterung für Alchemie bis zur Erschaffung eines lebenden Wesens in Ingolstadt. Aus Angst vor seinem Erfolg verlässt Victor die Kreatur. Der Text verfolgt Williams und Justines Tod, die Ablehnung der Kreatur und ihre Forderung nach einer Gefährtin.',
        'Die Zerstörung der zweiten Schöpfung führt zu Drohungen, Elizabeths Tod und einer Verfolgung in der Arktis. Abschließende Gedanken verbinden Ehrgeiz und Verlassenwerden mit Fragen zu künstlicher Intelligenz, Biotechnologie und Verantwortung. Dies ist eine Deutung von Shelleys Roman, nicht der Originalroman von 1818.',
    ],
    'es': [
        'Esta narración humorística de 2024 sigue a Victor Frankenstein desde su interés por la alquimia hasta la creación de un ser vivo en Ingolstadt. Asustado por su éxito, Victor abandona a la criatura. El relato sigue las muertes de William y Justine, el rechazo sufrido por la criatura y su petición de una compañera.',
        'La destrucción de la segunda creación conduce a amenazas, la muerte de Elizabeth y una persecución en el Ártico. Las reflexiones finales vinculan ambición y abandono con la inteligencia artificial, la biotecnología y la responsabilidad. Es una lectura de la novela de Shelley, no la novela original de 1818.',
    ],
    'pt': [
        'Esta narrativa humorística de 2024 acompanha Victor Frankenstein desde o interesse pela alquimia até à criação de um ser vivo em Ingolstadt. Assustado pelo próprio êxito, Victor abandona a criatura. O texto segue as mortes de William e Justine, a rejeição sofrida pela criatura e o seu pedido de uma companheira.',
        'A destruição da segunda criação leva a ameaças, à morte de Elizabeth e a uma perseguição no Ártico. As reflexões finais ligam ambição e abandono à inteligência artificial, à biotecnologia e à responsabilidade. É uma leitura do romance de Shelley, não o romance original de 1818.',
    ],
    'it': [
        'Questa narrazione ironica del 2024 segue Victor Frankenstein dall’interesse per l’alchimia alla creazione di un essere vivente a Ingolstadt. Spaventato dal proprio successo, Victor abbandona la creatura. Il testo segue le morti di William e Justine, il rifiuto subito dalla creatura e la sua richiesta di una compagna.',
        'La distruzione della seconda creazione porta a minacce, alla morte di Elizabeth e a un inseguimento nell’Artico. Le riflessioni finali collegano ambizione e abbandono a intelligenza artificiale, biotecnologia e responsabilità. È una lettura del romanzo di Shelley, non il romanzo originale del 1818.',
    ],
    'ro': [
        'Această repovestire cu umor din 2024 îl urmărește pe Victor Frankenstein de la interesul pentru alchimie până la crearea unei ființe vii la Ingolstadt. Speriat de reușită, Victor abandonează creatura. Eseul prezintă apoi morțile lui William și Justine, respingerea ființei și cererea ei de a avea o însoțitoare.',
        'Distrugerea celei de-a doua creații aduce amenințări, moartea lui Elizabeth și urmărirea prin Arctica. Reflecțiile finale leagă ambiția și abandonul de inteligența artificială, biotehnologie și responsabilitate. Aceasta este o interpretare a romanului lui Shelley, nu romanul original din 1818.',
    ],
    'pl': [
        'Ta humorystyczna opowieść z 2024 roku śledzi Victora Frankensteina od zainteresowania alchemią po stworzenie żywej istoty w Ingolstadt. Przerażony sukcesem Victor porzuca stworzenie. Tekst opisuje śmierć Williama i Justine, odrzucenie stworzenia oraz jego prośbę o towarzyszkę.',
        'Zniszczenie drugiej istoty prowadzi do gróźb, śmierci Elizabeth i pościgu przez Arktykę. Końcowe refleksje łączą ambicję i porzucenie z pytaniami o sztuczną inteligencję, biotechnologię i odpowiedzialność. Jest to interpretacja powieści Shelley, a nie jej oryginalny tekst z 1818 roku.',
    ],
}
release_path = workspace / 'release.json'
release = json.loads(release_path.read_text())
manifest['shortDescriptionEditorial'] = {
    'method': 'active-LLM-authored',
    'sourceSha256': release['sha256'],
    'sentencesPerLanguage': 6,
    'status': 'reviewed-intake',
}
manifest.pop('metadataDraft', None)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
release['changes'] = {
    'en': 'Cleaned source retelling with complete and ten-minute English and Romanian readers, a new English PDF, preserved cover and reviewed discovery metadata.',
    'ro': 'Repovestire sursă curățată, cu lecturi integrale și de zece minute în engleză și română, PDF nou în engleză, copertă păstrată și metadate revizuite.',
}
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n')
