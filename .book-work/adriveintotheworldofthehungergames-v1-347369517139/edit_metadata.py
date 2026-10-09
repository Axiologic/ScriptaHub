import json
from pathlib import Path

workspace = Path(__file__).parent
manifest_path = workspace / 'book/manifest.json'
manifest = json.loads(manifest_path.read_text())
manifest['title'] = {
    'en': 'A Drive into the World of the Hunger Games',
    'fr': 'Une plongée dans le monde de Hunger Games',
    'de': 'Eine Reise in die Welt der Hunger Games',
    'es': 'Un recorrido por el mundo de Los juegos del hambre',
    'pt': 'Uma viagem pelo mundo de Jogos da Fome',
    'it': 'Un viaggio nel mondo di Hunger Games',
    'ro': 'O călătorie în lumea Jocurilor foamei',
    'pl': 'Podróż do świata Igrzysk śmierci',
}
manifest['subtitle'] = {
    'en': 'Power, survival, technology, and resistance in Panem',
    'fr': 'Pouvoir, survie, technologie et résistance à Panem',
    'de': 'Macht, Überleben, Technik und Widerstand in Panem',
    'es': 'Poder, supervivencia, tecnología y resistencia en Panem',
    'pt': 'Poder, sobrevivência, tecnologia e resistência em Panem',
    'it': 'Potere, sopravvivenza, tecnologia e resistenza a Panem',
    'ro': 'Putere, supraviețuire, tehnologie și rezistență în Panem',
    'pl': 'Władza, przetrwanie, technologia i opór w Panem',
}
sentences = {
    'en': [
        'The Capitol keeps Panem’s districts divided through scarcity and fear.',
        'Annual televised Games turn children’s survival into political spectacle.',
        'Katniss’s sacrifice for Prim opens a path toward resistance.',
        'District industries and controlled history reveal the design of power.',
        'Arena surveillance and engineered creatures show technology serving oppression.',
        'The Mockingjay symbol carries hope across books, films, and audiences.',
    ],
    'fr': [
        'Le Capitole divise les districts de Panem par la pénurie et la peur.',
        'Les Jeux télévisés transforment la survie des enfants en spectacle politique.',
        'Le sacrifice de Katniss pour Prim ouvre une voie de résistance.',
        'Industries des districts et histoire contrôlée révèlent l’architecture du pouvoir.',
        'Surveillance de l’arène et créatures modifiées montrent une technologie oppressive.',
        'Le geai moqueur porte l’espoir dans les livres, les films et le public.',
    ],
    'de': [
        'Das Kapitol hält Panems Distrikte durch Mangel und Angst getrennt.',
        'Die jährlichen Fernsehspiele machen das Überleben von Kindern zum politischen Spektakel.',
        'Katniss’ Opfer für Prim eröffnet einen Weg zum Widerstand.',
        'Distriktindustrien und gelenkte Geschichte zeigen den Aufbau der Macht.',
        'Überwachung der Arena und gezüchtete Wesen zeigen Technik als Unterdrückungsmittel.',
        'Der Spotttölpel trägt Hoffnung durch Bücher, Filme und Publikum.',
    ],
    'es': [
        'El Capitolio divide los distritos de Panem mediante escasez y miedo.',
        'Los Juegos televisados convierten la supervivencia infantil en espectáculo político.',
        'El sacrificio de Katniss por Prim abre un camino de resistencia.',
        'Las industrias distritales y la historia controlada revelan el diseño del poder.',
        'La vigilancia de la arena y criaturas modificadas muestran tecnología opresiva.',
        'El sinsajo lleva esperanza entre libros, películas y públicos.',
    ],
    'pt': [
        'O Capitólio divide os distritos de Panem através da escassez e do medo.',
        'Os Jogos televisivos transformam a sobrevivência infantil em espetáculo político.',
        'O sacrifício de Katniss por Prim abre caminho à resistência.',
        'Indústrias distritais e história controlada revelam o desenho do poder.',
        'Vigilância da arena e criaturas modificadas mostram tecnologia ao serviço da opressão.',
        'O símbolo do tordo leva esperança pelos livros, filmes e públicos.',
    ],
    'it': [
        'Capitol City divide i distretti di Panem con scarsità e paura.',
        'Gli annuali Giochi televisivi trasformano la sopravvivenza dei bambini in spettacolo politico.',
        'Il sacrificio di Katniss per Prim apre una strada alla resistenza.',
        'Industrie distrettuali e storia controllata svelano la struttura del potere.',
        'Sorveglianza dell’arena e creature modificate mostrano una tecnologia oppressiva.',
        'La ghiandaia imitatrice porta speranza tra libri, film e pubblico.',
    ],
    'ro': [
        'Capitoliul ține districtele Panemului dezbinate prin lipsuri și frică.',
        'Jocurile televizate transformă supraviețuirea copiilor în spectacol politic.',
        'Sacrificiul lui Katniss pentru Prim deschide un drum al rezistenței.',
        'Industriile districtelor și istoria controlată dezvăluie construcția puterii.',
        'Supravegherea arenei și ființele modificate arată tehnologia pusă în slujba opresiunii.',
        'Gaița Zeflemitoare poartă speranța prin cărți, filme și comunități de cititori.',
    ],
    'pl': [
        'Kapitol dzieli dystrykty Panem przez niedostatek i strach.',
        'Coroczne telewizyjne Igrzyska czynią przetrwanie dzieci politycznym widowiskiem.',
        'Poświęcenie Katniss dla Prim otwiera drogę oporu.',
        'Przemysł dystryktów i kontrolowana historia odsłaniają budowę władzy.',
        'Nadzór nad areną i zmienione stworzenia pokazują technologię służącą uciskowi.',
        'Kosogłos niesie nadzieję przez książki, filmy i publiczność.',
    ],
}
manifest['shortDescription'] = {language: ' '.join(lines) for language, lines in sentences.items()}
manifest['aboutBook'] = {
    'en': [
        'This essay explores Suzanne Collins’s Hunger Games world through the Capitol’s control of Panem, the industries and history of its districts, and the annual arena. It examines the connected themes of power, oppression, sacrifice, and survival, with Katniss Everdeen’s choices as a route into the wider political system.',
        'Further chapters consider identity under broadcast spectacle, the Mockingjay as a symbol of resistance, and unequal access to surveillance, medicine, and engineered creatures. A brief plot guide covers the original trilogy and its film adaptations. The essay ends by asking who controls technology and how solidarity can resist fear.',
    ],
    'fr': [
        'Cet essai explore l’univers de Hunger Games de Suzanne Collins à travers le contrôle du Capitole sur Panem, les industries et l’histoire des districts ainsi que l’arène annuelle. Il relie pouvoir, oppression, sacrifice et survie, en partant des choix de Katniss Everdeen pour comprendre le système politique.',
        'D’autres chapitres examinent l’identité sous le spectacle télévisé, le geai moqueur comme symbole de résistance et l’accès inégal à la surveillance, aux soins et aux créatures modifiées. Un court guide suit la trilogie et ses adaptations. L’essai demande enfin qui contrôle la technologie et comment la solidarité résiste à la peur.',
    ],
    'de': [
        'Dieser Essay untersucht Suzanne Collins’ Hunger-Games-Welt anhand der Herrschaft des Kapitols über Panem, der Geschichte und Industrien der Distrikte sowie der jährlichen Arena. Er verbindet Macht, Unterdrückung, Opfer und Überleben; Katniss Everdeens Entscheidungen führen in das politische System ein.',
        'Weitere Kapitel behandeln Identität im Fernseh-Spektakel, den Spotttölpel als Widerstandssymbol und ungleichen Zugang zu Überwachung, Medizin und gezüchteten Wesen. Ein kurzer Handlungsführer umfasst Trilogie und Verfilmungen. Zum Schluss fragt der Essay, wer Technik kontrolliert und wie Solidarität der Angst widerstehen kann.',
    ],
    'es': [
        'Este ensayo explora el mundo de Los juegos del hambre de Suzanne Collins mediante el control del Capitolio sobre Panem, la historia y las industrias distritales y la arena anual. Relaciona poder, opresión, sacrificio y supervivencia, usando las decisiones de Katniss Everdeen para explicar el sistema político.',
        'Otros capítulos examinan la identidad en el espectáculo televisivo, el sinsajo como símbolo de resistencia y el acceso desigual a vigilancia, medicina y criaturas modificadas. Una guía breve recorre la trilogía y sus películas. El ensayo pregunta quién controla la tecnología y cómo la solidaridad resiste el miedo.',
    ],
    'pt': [
        'Este ensaio explora o universo de Jogos da Fome de Suzanne Collins através do controlo do Capitólio sobre Panem, da história e das indústrias dos distritos e da arena anual. Relaciona poder, opressão, sacrifício e sobrevivência, partindo das escolhas de Katniss Everdeen para compreender o sistema político.',
        'Outros capítulos analisam identidade no espetáculo televisivo, o tordo como símbolo de resistência e o acesso desigual a vigilância, medicina e criaturas modificadas. Um guia breve percorre a trilogia e os filmes. O ensaio pergunta quem controla a tecnologia e como a solidariedade resiste ao medo.',
    ],
    'it': [
        'Questo saggio esplora il mondo di Hunger Games di Suzanne Collins attraverso il controllo di Capitol City su Panem, la storia e le industrie dei distretti e l’arena annuale. Collega potere, oppressione, sacrificio e sopravvivenza, partendo dalle scelte di Katniss Everdeen per comprendere il sistema politico.',
        'Altri capitoli esaminano identità nello spettacolo televisivo, la ghiandaia imitatrice come simbolo di resistenza e l’accesso diseguale a sorveglianza, medicina e creature modificate. Una breve guida segue trilogia e film. Il saggio chiede chi controlli la tecnologia e come la solidarietà resista alla paura.',
    ],
    'ro': [
        'Eseul explorează lumea Jocurilor foamei de Suzanne Collins prin controlul Capitoliului asupra Panemului, istoria și industriile districtelor și arena anuală. Leagă puterea, opresiunea, sacrificiul și supraviețuirea, pornind de la alegerile lui Katniss Everdeen pentru a înțelege sistemul politic.',
        'Alte capitole examinează identitatea în spectacolul televizat, Gaița Zeflemitoare ca simbol al rezistenței și accesul inegal la supraveghere, medicină și ființe modificate. Un scurt ghid urmărește trilogia și adaptările ei cinematografice. Eseul întreabă cine controlează tehnologia și cum poate solidaritatea să reziste fricii.',
    ],
    'pl': [
        'Esej bada świat Igrzysk śmierci Suzanne Collins przez władzę Kapitolu nad Panem, dzieje i przemysł dystryktów oraz coroczną arenę. Łączy władzę, ucisk, poświęcenie i przetrwanie, wychodząc od wyborów Katniss Everdeen, aby wyjaśnić system polityczny.',
        'Dalsze rozdziały omawiają tożsamość w telewizyjnym widowisku, Kosogłosa jako znak oporu i nierówny dostęp do nadzoru, medycyny oraz zmodyfikowanych stworzeń. Krótki przewodnik opisuje trylogię i filmy. Esej pyta, kto kontroluje technologię i jak solidarność może przeciwstawić się strachowi.',
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
    'en': 'Cleaned source essay with complete and ten-minute English and Romanian readers, a new English PDF, preserved cover and reviewed discovery metadata.',
    'ro': 'Eseu sursă curățat, cu lecturi integrale și de zece minute în engleză și română, PDF nou în engleză, copertă păstrată și metadate revizuite.',
}
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n')
