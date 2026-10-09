import json
import re
from pathlib import Path

path = Path('.book-work/charlesdarwinarevolutionaryforceinscienceandsociety-v1-412e39743f82/book/manifest.json')
m = json.loads(path.read_text())
data = {
 'en': {
  'title': 'Charles Darwin A Revolutionary Force in Science and Society',
  'subtitle': 'From the Beagle voyage to genetics, public debate, and evolutionary applications',
  'short': [
   'Darwin’s theory of natural selection changed how scientists explain the diversity of life.',
   'The book follows his early studies and the observations gathered aboard HMS Beagle.',
   'It traces how Darwin developed his theory and how later genetics refined it.',
   'One chapter imagines his response to modern biology while identifying that exercise as speculation.',
   'The social chapters examine religious debate and the misuse of evolutionary language to justify inequality.',
   'The final chapter connects evolutionary principles with breeding, medicine, conservation, and technology.',
  ],
  'about': [
   'This book follows Charles Darwin from his formative studies through the Beagle expedition and the development of natural selection. It shows how field observations, specimens, correspondence, and reading helped turn a question about species into an explanatory theory. Its opening thought experiment considers modern genetics from Darwin’s imagined perspective, without presenting those reactions as historical testimony.',
   'Later chapters follow the theory through Mendelian inheritance, population genetics, and the Modern Synthesis. They examine religious and philosophical debate, distinguish Darwin’s science from Social Darwinist and eugenic misuse, and survey applications in breeding, medicine, conservation, and computing. The bibliography preserves the source’s cited works.',
  ],
 },
 'fr': {
  'title': 'Charles Darwin : une force révolutionnaire dans la science et la société',
  'subtitle': 'Du voyage du Beagle à la génétique et aux débats sociaux',
  'short': [
   'La sélection naturelle de Darwin a transformé l’explication scientifique de la diversité du vivant.',
   'Le livre suit sa formation et les observations recueillies à bord du Beagle.',
   'Il retrace la naissance de sa théorie et son évolution grâce à la génétique.',
   'Un chapitre imagine sa réaction à la biologie moderne en présentant cet exercice comme une hypothèse.',
   'Les chapitres sociaux étudient les débats religieux et les usages abusifs de l’évolution pour justifier les inégalités.',
   'Le dernier chapitre relie les principes évolutifs à l’élevage, la médecine, la conservation et la technologie.',
  ],
  'about': [
   'Ce livre suit Charles Darwin depuis ses études jusqu’au voyage du Beagle et à la formulation de la sélection naturelle. Il montre comment les observations de terrain, les spécimens, la correspondance et ses lectures ont transformé une question sur les espèces en théorie explicative. Son ouverture imagine ce que Darwin aurait pu penser de la génétique moderne, sans présenter cette réaction comme un témoignage historique.',
   'Les chapitres suivants suivent la théorie à travers l’hérédité mendélienne, la génétique des populations et la synthèse moderne. Ils examinent les débats religieux et philosophiques, distinguent la science de Darwin des détournements sociaux et eugénistes, puis présentent des applications en élevage, médecine, conservation et informatique. La bibliographie conserve les références de la source.',
  ],
 },
 'de': {
  'title': 'Charles Darwin: Eine revolutionäre Kraft in Wissenschaft und Gesellschaft',
  'subtitle': 'Von der Beagle-Reise zur Genetik und gesellschaftlichen Debatte',
  'short': [
   'Darwins natürliche Selektion veränderte die wissenschaftliche Erklärung der Vielfalt des Lebens.',
   'Das Buch verfolgt seine Ausbildung und die Beobachtungen an Bord der Beagle.',
   'Es beschreibt die Entstehung seiner Theorie und ihre spätere Weiterentwicklung durch die Genetik.',
   'Ein Kapitel stellt sich seine Reaktion auf moderne Biologie vor und kennzeichnet dies als Spekulation.',
   'Die gesellschaftlichen Kapitel behandeln religiöse Debatten und den Missbrauch evolutionärer Sprache zur Rechtfertigung von Ungleichheit.',
   'Das letzte Kapitel verbindet evolutionäre Prinzipien mit Züchtung, Medizin, Naturschutz und Technik.',
  ],
  'about': [
   'Dieses Buch begleitet Charles Darwin von seiner Ausbildung über die Reise der Beagle bis zur Entwicklung der natürlichen Selektion. Es zeigt, wie Feldbeobachtungen, gesammelte Exemplare, Briefe und Lektüre aus Fragen über Arten eine erklärende Theorie entstehen ließen. Der Einstieg stellt sich Darwins Reaktion auf moderne Genetik vor, ohne diese Gedanken als historische Aussagen auszugeben.',
   'Spätere Kapitel verfolgen die Theorie durch Mendels Vererbungslehre, Populationsgenetik und die Moderne Synthese. Sie behandeln religiöse und philosophische Debatten, unterscheiden Darwins Wissenschaft vom Missbrauch durch Sozialdarwinismus und Eugenik und betrachten Anwendungen in Züchtung, Medizin, Naturschutz und Informatik. Die Bibliografie bewahrt die Quellenangaben des Ausgangstextes.',
  ],
 },
 'es': {
  'title': 'Charles Darwin: una fuerza revolucionaria en la ciencia y la sociedad',
  'subtitle': 'Del viaje del Beagle a la genética y el debate social',
  'short': [
   'La selección natural de Darwin transformó la explicación científica de la diversidad de la vida.',
   'El libro sigue sus estudios y las observaciones reunidas a bordo del Beagle.',
   'Explica cómo desarrolló su teoría y cómo la genética la refinó después.',
   'Un capítulo imagina su reacción ante la biología moderna y presenta ese ejercicio como especulación.',
   'Los capítulos sociales examinan el debate religioso y el uso indebido del lenguaje evolutivo para justificar desigualdades.',
   'El último capítulo relaciona los principios evolutivos con la cría, la medicina, la conservación y la tecnología.',
  ],
  'about': [
   'Este libro acompaña a Charles Darwin desde sus estudios iniciales hasta el viaje del Beagle y la formulación de la selección natural. Muestra cómo las observaciones de campo, los especímenes, las cartas y las lecturas convirtieron una pregunta sobre las especies en una teoría explicativa. Su comienzo imagina la respuesta de Darwin a la genética moderna sin presentar esa reacción como testimonio histórico.',
   'Los capítulos posteriores siguen la teoría a través de la herencia mendeliana, la genética de poblaciones y la Síntesis Moderna. Examinan debates religiosos y filosóficos, distinguen la ciencia de Darwin de los abusos del darwinismo social y la eugenesia, y presentan aplicaciones en cría, medicina, conservación e informática. La bibliografía conserva las obras citadas por la fuente.',
  ],
 },
 'pt': {
  'title': 'Charles Darwin: uma força revolucionária na ciência e na sociedade',
  'subtitle': 'Da viagem do Beagle à genética e ao debate social',
  'short': [
   'A seleção natural de Darwin transformou a explicação científica da diversidade da vida.',
   'O livro acompanha a formação e as observações feitas a bordo do Beagle.',
   'Mostra como a teoria surgiu e como a genética a refinou posteriormente.',
   'Um capítulo imagina a reação de Darwin à biologia moderna e identifica esse exercício como especulação.',
   'Os capítulos sociais examinam debates religiosos e o abuso da linguagem evolutiva para justificar desigualdades.',
   'O capítulo final liga princípios evolutivos à criação, medicina, conservação e tecnologia.',
  ],
  'about': [
   'Este livro acompanha Charles Darwin desde os primeiros estudos até à viagem do Beagle e à formulação da seleção natural. Mostra como observações de campo, espécimes, correspondência e leituras transformaram uma pergunta sobre espécies numa teoria explicativa. A abertura imagina a reação de Darwin à genética moderna sem apresentar essa hipótese como testemunho histórico.',
   'Os capítulos seguintes acompanham a teoria pela hereditariedade mendeliana, genética das populações e Síntese Moderna. Examinam debates religiosos e filosóficos, distinguem a ciência de Darwin dos abusos do darwinismo social e da eugenia, e apresentam aplicações na criação, medicina, conservação e informática. A bibliografia preserva as obras citadas na fonte.',
  ],
 },
 'it': {
  'title': 'Charles Darwin: una forza rivoluzionaria nella scienza e nella società',
  'subtitle': 'Dal viaggio del Beagle alla genetica e al dibattito sociale',
  'short': [
   'La selezione naturale di Darwin cambiò la spiegazione scientifica della diversità della vita.',
   'Il libro segue la sua formazione e le osservazioni raccolte a bordo del Beagle.',
   'Ricostruisce lo sviluppo della teoria e i successivi contributi della genetica.',
   'Un capitolo immagina la sua reazione alla biologia moderna e dichiara il carattere ipotetico dell’esercizio.',
   'I capitoli sociali esaminano il dibattito religioso e l’abuso del linguaggio evolutivo per giustificare le disuguaglianze.',
   'L’ultimo capitolo collega i principi evolutivi ad allevamento, medicina, conservazione e tecnologia.',
  ],
  'about': [
   'Questo libro segue Charles Darwin dagli studi giovanili al viaggio del Beagle e alla formulazione della selezione naturale. Mostra come osservazioni sul campo, campioni, corrispondenza e letture trasformarono una domanda sulle specie in una teoria esplicativa. L’apertura immagina la sua risposta alla genetica moderna senza presentare tali reazioni come testimonianze storiche.',
   'I capitoli successivi seguono la teoria attraverso l’ereditarietà mendeliana, la genetica delle popolazioni e la Sintesi Moderna. Esaminano il dibattito religioso e filosofico, distinguono la scienza di Darwin dagli abusi del darwinismo sociale e dell’eugenetica e descrivono applicazioni nell’allevamento, nella medicina, nella conservazione e nell’informatica. La bibliografia conserva le opere citate dalla fonte.',
  ],
 },
 'ro': {
  'title': 'Charles Darwin: o forță revoluționară în știință și societate',
  'subtitle': 'De la călătoria pe Beagle la genetică și dezbaterea socială',
  'short': [
   'Selecția naturală formulată de Darwin a schimbat explicația științifică a diversității vieții.',
   'Cartea urmărește formarea sa și observațiile adunate la bordul navei Beagle.',
   'Arată cum a dezvoltat teoria și cum genetica a rafinat-o ulterior.',
   'Un capitol imaginează reacția sa la biologia modernă și precizează caracterul speculativ al exercițiului.',
   'Capitolele sociale examinează dezbaterea religioasă și folosirea abuzivă a limbajului evoluționist pentru justificarea inegalității.',
   'Ultimul capitol leagă principiile evolutive de ameliorare, medicină, conservare și tehnologie.',
  ],
  'about': [
   'Cartea îl urmărește pe Charles Darwin de la studiile timpurii la călătoria pe Beagle și formularea selecției naturale. Arată cum observațiile pe teren, specimenele, corespondența și lecturile au transformat o întrebare despre specii într-o teorie explicativă. Deschiderea își imaginează răspunsul lui Darwin la genetica modernă, fără a prezenta acea reacție drept mărturie istorică.',
   'Capitolele următoare urmăresc teoria prin ereditatea mendeliană, genetica populațiilor și sinteza modernă. Ele examinează dezbaterile religioase și filosofice, deosebesc știința lui Darwin de abuzurile darwinismului social și eugeniei și prezintă aplicații în ameliorare, medicină, conservare și informatică. Bibliografia păstrează lucrările citate în sursă.',
  ],
 },
 'pl': {
  'title': 'Charles Darwin: rewolucyjna siła w nauce i społeczeństwie',
  'subtitle': 'Od podróży Beagle do genetyki i debaty społecznej',
  'short': [
   'Dobór naturalny Darwina zmienił naukowe wyjaśnienie różnorodności życia.',
   'Książka opisuje jego edukację i obserwacje zebrane na pokładzie Beagle.',
   'Pokazuje rozwój jego teorii oraz późniejsze uzupełnienia wniesione przez genetykę.',
   'Jeden rozdział wyobraża sobie reakcję Darwina na współczesną biologię i zaznacza spekulacyjny charakter tego zabiegu.',
   'Rozdziały społeczne badają debatę religijną i nadużywanie języka ewolucji do usprawiedliwiania nierówności.',
   'Ostatni rozdział łączy zasady ewolucji z hodowlą, medycyną, ochroną przyrody i technologią.',
  ],
  'about': [
   'Książka prowadzi czytelnika od wczesnych studiów Charlesa Darwina przez podróż Beagle do sformułowania doboru naturalnego. Pokazuje, jak obserwacje terenowe, okazy, korespondencja i lektury zamieniły pytanie o gatunki w teorię wyjaśniającą. Początek wyobraża sobie reakcję Darwina na współczesną genetykę, ale nie przedstawia tych przypuszczeń jako świadectwa historycznego.',
   'Dalsze rozdziały śledzą teorię przez dziedziczenie mendlowskie, genetykę populacji i nowoczesną syntezę. Analizują spory religijne i filozoficzne, odróżniają naukę Darwina od nadużyć darwinizmu społecznego i eugeniki oraz omawiają zastosowania w hodowli, medycynie, ochronie przyrody i informatyce. Bibliografia zachowuje dzieła wymienione w źródle.',
  ],
 },
}
for lang, item in data.items():
    assert len(item['short']) == 6
    assert all(len(sentence.split()) <= 22 for sentence in item['short']), (lang, [len(s.split()) for s in item['short']])
    count = sum(len(paragraph.split()) for paragraph in item['about'])
    assert 60 <= count <= 250, (lang, count)
    m['title'][lang] = item['title']
    m['subtitle'][lang] = item['subtitle']
    m['shortDescription'][lang] = ' '.join(item['short'])
    m['aboutBook'][lang] = item['about']
m['shortDescriptionEditorial'] = {
    'source': 'editorial', 'status': 'reviewed',
    'basis': 'Seven original chapters, complete conclusion and bibliography, and the English ten-minute edition; six source-grounded sentences per interface language.',
}
path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
print('Reviewed metadata in', len(data), 'languages')
