import json
from pathlib import Path

workspace = Path(__file__).parent
manifest_path = workspace / 'book/manifest.json'
manifest = json.loads(manifest_path.read_text())
manifest['title'] = {
    'en': 'Messi or Ronaldo? The End of an Era',
    'fr': 'Messi ou Ronaldo ? La fin d’une époque',
    'de': 'Messi oder Ronaldo? Das Ende einer Ära',
    'es': '¿Messi o Ronaldo? El fin de una era',
    'pt': 'Messi ou Ronaldo? O fim de uma era',
    'it': 'Messi o Ronaldo? La fine di un’era',
    'ro': 'Messi sau Ronaldo? Sfârșitul unei ere',
    'pl': 'Messi czy Ronaldo? Koniec pewnej ery',
}
manifest['subtitle'] = {
    'en': 'Two careers, contrasting styles, and a lasting football rivalry',
    'fr': 'Deux carrières, des styles opposés et une rivalité durable',
    'de': 'Zwei Karrieren, gegensätzliche Spielweisen und eine bleibende Rivalität',
    'es': 'Dos carreras, estilos opuestos y una rivalidad duradera',
    'pt': 'Duas carreiras, estilos contrastantes e uma rivalidade duradoura',
    'it': 'Due carriere, stili opposti e una rivalità duratura',
    'ro': 'Două cariere, stiluri contrastante și o rivalitate durabilă',
    'pl': 'Dwie kariery, odmienne style i trwała rywalizacja',
}
sentences = {
    'en': [
        'Messi and Ronaldo reached football’s summit by markedly different paths.',
        'Rosario, Madeira, La Masia, and Sporting shaped their early careers.',
        'Playmaking and close control meet athletic power and varied finishing.',
        'El Clásico, La Liga, and Champions League records intensified the rivalry.',
        'Their influence extends into media, philanthropy, and younger players’ ambitions.',
        'The final debate asks which qualities should define football greatness.',
    ],
    'fr': [
        'Messi et Ronaldo ont atteint le sommet du football par des chemins différents.',
        'Rosario, Madère, La Masia et le Sporting ont marqué leurs débuts.',
        'Création et contrôle du ballon rencontrent puissance athlétique et finition variée.',
        'El Clásico, la Liga et les records européens ont intensifié leur rivalité.',
        'Leur influence touche les médias, la philanthropie et les jeunes joueurs.',
        'Le débat final demande quelles qualités définissent la grandeur footballistique.',
    ],
    'de': [
        'Messi und Ronaldo erreichten die Spitze des Fußballs auf sehr verschiedenen Wegen.',
        'Rosario, Madeira, La Masia und Sporting prägten ihre Anfänge.',
        'Spielgestaltung und Ballkontrolle treffen auf Athletik und vielseitigen Torabschluss.',
        'El Clásico, La Liga und europäische Rekorde verschärften die Rivalität.',
        'Ihr Einfluss reicht zu Medien, Wohltätigkeit und jungen Spielern.',
        'Die Schlussdebatte fragt, welche Eigenschaften fußballerische Größe bestimmen.',
    ],
    'es': [
        'Messi y Ronaldo alcanzaron la cima del fútbol por caminos distintos.',
        'Rosario, Madeira, La Masia y el Sporting marcaron sus comienzos.',
        'La creación y el control cercano contrastan con potencia y remates variados.',
        'El Clásico, La Liga y los récords europeos intensificaron la rivalidad.',
        'Su influencia alcanza medios, filantropía y aspiraciones de jóvenes futbolistas.',
        'El debate final pregunta qué cualidades definen la grandeza futbolística.',
    ],
    'pt': [
        'Messi e Ronaldo chegaram ao topo do futebol por caminhos diferentes.',
        'Rosário, Madeira, La Masia e Sporting marcaram os seus começos.',
        'Criação e controlo próximo contrastam com força e finalização variada.',
        'El Clásico, La Liga e recordes europeus intensificaram a rivalidade.',
        'A influência de ambos alcança meios de comunicação, filantropia e jovens jogadores.',
        'O debate final pergunta que qualidades definem a grandeza no futebol.',
    ],
    'it': [
        'Messi e Ronaldo hanno raggiunto il vertice del calcio per vie diverse.',
        'Rosario, Madeira, La Masia e Sporting hanno segnato i loro inizi.',
        'Regia e controllo ravvicinato incontrano atletismo e finalizzazioni diverse.',
        'El Clásico, Liga e record europei hanno intensificato la rivalità.',
        'La loro influenza riguarda media, filantropia e giovani calciatori.',
        'Il dibattito finale chiede quali qualità definiscano la grandezza calcistica.',
    ],
    'ro': [
        'Messi și Ronaldo au ajuns în vârful fotbalului pe drumuri diferite.',
        'Rosario, Madeira, La Masia și Sporting le-au marcat începuturile.',
        'Construcția jocului și controlul apropiat întâlnesc forța și finalizarea variată.',
        'El Clásico, La Liga și recordurile europene au intensificat rivalitatea.',
        'Influența lor atinge presa, filantropia și aspirațiile tinerilor fotbaliști.',
        'Dezbaterea finală întreabă ce calități definesc măreția în fotbal.',
    ],
    'pl': [
        'Messi i Ronaldo dotarli na szczyt futbolu różnymi drogami.',
        'Rosario, Madera, La Masia i Sporting ukształtowały ich początki.',
        'Kreowanie gry i kontrola piłki spotykają siłę oraz różnorodne wykończenie.',
        'El Clásico, La Liga i europejskie rekordy zaostrzyły rywalizację.',
        'Ich wpływ obejmuje media, dobroczynność i ambicje młodych piłkarzy.',
        'Końcowa debata pyta, jakie cechy określają piłkarską wielkość.',
    ],
}
manifest['shortDescription'] = {language: ' '.join(lines) for language, lines in sentences.items()}
manifest['aboutBook'] = {
    'en': [
        'This 2024 essay follows Lionel Messi and Cristiano Ronaldo from contrasting beginnings to sustained dominance in modern football. It compares Messi’s movement from winger to playmaker with Ronaldo’s development into a versatile scorer, then examines their Barcelona–Real Madrid rivalry, major records, and achievements for club and country.',
        'The book also considers their public reach, charitable work, and influence on aspiring players. Its final chapter weighs technique, athleticism, trophies, and individual preference without requiring a single winner. Statistics and career-stage descriptions reflect the source’s 2024 perspective.',
    ],
    'fr': [
        'Cet essai de 2024 suit Lionel Messi et Cristiano Ronaldo de leurs débuts contrastés à leur domination durable du football moderne. Il compare le passage de Messi de l’aile à la création du jeu avec l’évolution de Ronaldo en buteur polyvalent, puis examine leur rivalité entre Barcelone et le Real Madrid, leurs records et leurs succès en club et en sélection.',
        'Le livre aborde également leur visibilité publique, leurs actions caritatives et leur influence sur les jeunes joueurs. Le dernier chapitre confronte technique, athlétisme, trophées et préférences personnelles sans imposer un seul vainqueur. Les chiffres reflètent la perspective de la source en 2024.',
    ],
    'de': [
        'Dieser Essay von 2024 begleitet Lionel Messi und Cristiano Ronaldo von unterschiedlichen Anfängen bis zu ihrer langen Dominanz im modernen Fußball. Er vergleicht Messis Wandel vom Flügelspieler zum Spielgestalter mit Ronaldos Entwicklung zum vielseitigen Torjäger und behandelt danach die Rivalität zwischen Barcelona und Real Madrid, Rekorde sowie Erfolge im Verein und in der Nationalmannschaft.',
        'Das Buch betrachtet auch ihre öffentliche Reichweite, wohltätige Arbeit und Wirkung auf junge Spieler. Das letzte Kapitel wägt Technik, Athletik, Titel und persönliche Vorlieben ab, ohne einen einzigen Sieger festzulegen. Zahlen und Karrierebeschreibungen entsprechen dem Standpunkt der Quelle von 2024.',
    ],
    'es': [
        'Este ensayo de 2024 sigue a Lionel Messi y Cristiano Ronaldo desde comienzos opuestos hasta su prolongado dominio del fútbol moderno. Compara la transición de Messi del extremo al creador de juego con la evolución de Ronaldo como goleador versátil, y examina la rivalidad Barcelona–Real Madrid, los récords y los logros con clubes y selecciones.',
        'También considera su alcance público, labor benéfica e influencia sobre jóvenes futbolistas. El capítulo final sopesa técnica, atletismo, trofeos y preferencias personales sin exigir un único vencedor. Las cifras y etapas de sus carreras reflejan la perspectiva de la fuente de 2024.',
    ],
    'pt': [
        'Este ensaio de 2024 acompanha Lionel Messi e Cristiano Ronaldo desde começos contrastantes até ao domínio prolongado no futebol moderno. Compara a passagem de Messi de extremo a criador de jogo com a evolução de Ronaldo em goleador versátil, examinando depois a rivalidade Barcelona–Real Madrid, recordes e conquistas em clubes e seleções.',
        'O livro aborda também a projeção pública, a atividade solidária e a influência sobre jovens futebolistas. O último capítulo pondera técnica, atletismo, troféus e preferências pessoais sem exigir um único vencedor. Os números e fases de carreira refletem a perspetiva da fonte em 2024.',
    ],
    'it': [
        'Questo saggio del 2024 segue Lionel Messi e Cristiano Ronaldo dagli inizi diversi al lungo dominio nel calcio moderno. Confronta il passaggio di Messi da ala a regista con l’evoluzione di Ronaldo in marcatore versatile, poi esamina la rivalità Barcellona–Real Madrid, i record e i successi nei club e in nazionale.',
        'Considera inoltre la loro presenza pubblica, l’attività benefica e l’influenza sui giovani calciatori. Il capitolo finale valuta tecnica, atletismo, trofei e preferenze personali senza imporre un unico vincitore. Numeri e fasi di carriera rispecchiano la prospettiva della fonte del 2024.',
    ],
    'ro': [
        'Acest eseu din 2024 îi urmărește pe Lionel Messi și Cristiano Ronaldo de la începuturi contrastante la dominația îndelungată în fotbalul modern. Compară trecerea lui Messi de la extremă la coordonator de joc cu evoluția lui Ronaldo într-un marcator versatil, apoi discută rivalitatea Barcelona–Real Madrid, recordurile și realizările la club și națională.',
        'Cartea examinează și vizibilitatea publică, activitatea caritabilă și influența asupra tinerilor fotbaliști. Capitolul final cântărește tehnica, atletismul, trofeele și preferințele personale fără să impună un singur câștigător. Cifrele și etapele carierei reflectă perspectiva sursei din 2024.',
    ],
    'pl': [
        'Ten esej z 2024 roku śledzi Lionela Messiego i Cristiano Ronaldo od odmiennych początków po długą dominację we współczesnym futbolu. Porównuje przemianę Messiego ze skrzydłowego w rozgrywającego z rozwojem Ronaldo jako wszechstronnego strzelca, a następnie omawia rywalizację Barcelony z Realem Madryt, rekordy oraz sukcesy klubowe i reprezentacyjne.',
        'Książka opisuje także ich rozpoznawalność, działalność dobroczynną i wpływ na młodych piłkarzy. Ostatni rozdział waży technikę, atletyzm, trofea i osobiste preferencje bez wskazywania jednego zwycięzcy. Liczby i opisy etapów kariery odzwierciedlają perspektywę źródła z 2024 roku.',
    ],
}
manifest['shortDescriptionEditorial'] = {
    'method': 'active-LLM-authored',
    'sourceSha256': json.loads((workspace / 'release.json').read_text())['sha256'],
    'sentencesPerLanguage': 6,
    'status': 'reviewed-intake',
}
manifest.pop('metadataDraft', None)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
release_path = workspace / 'release.json'
release = json.loads(release_path.read_text())
release['changes'] = {
    'en': 'Cleaned source essay with complete and ten-minute English and Romanian readers, a new English PDF, preserved cover and reviewed discovery metadata.',
    'ro': 'Eseu sursă curățat, cu lecturi integrale și de zece minute în engleză și română, PDF nou în engleză, copertă păstrată și metadate revizuite.',
}
release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n')
