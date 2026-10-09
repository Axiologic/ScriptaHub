import json
from pathlib import Path

cache_path = Path('tools/keyword-translations.generated.json')
cache = json.loads(cache_path.read_text())
languages = ('fr', 'de', 'es', 'pt', 'it', 'ro', 'pl')
replacements = {
    'football era': ("ère du football", 'Fußballära', 'era del fútbol', 'era do futebol', 'epoca del calcio', 'era fotbalului', 'epoka futbolu'),
    'goals': ('buts', 'Tore', 'goles', 'golos', 'gol', 'goluri', 'bramki'),
    'honours': ('distinctions', 'Auszeichnungen', 'títulos', 'títulos', 'titoli', 'distincții', 'wyróżnienia'),
    'training': ('entraînement', 'Training', 'entrenamiento', 'treino', 'allenamento', 'antrenament', 'trening'),
    'early talent': ('talent précoce', 'frühes Talent', 'talento temprano', 'talento precoce', 'talento precoce', 'talent timpuriu', 'wczesny talent'),
    'Sporting Lisbon': ('Sporting Lisbonne', 'Sporting Lissabon', 'Sporting de Lisboa', 'Sporting Lisboa', 'Sporting Lisbona', 'Sporting Lisabona', 'Sporting Lizbona'),
    'Manchester United': ('Manchester United', 'Manchester United', 'Manchester United', 'Manchester United', 'Manchester United', 'Manchester United', 'Manchester United'),
    'physical training': ('préparation physique', 'körperliches Training', 'preparación física', 'preparação física', 'preparazione fisica', 'pregătire fizică', 'trening fizyczny'),
    'self-made athlete': ('athlète formé par ses efforts', 'selbst geformter Athlet', 'atleta formado por esfuerzo propio', 'atleta formado pelo próprio esforço', 'atleta formato con le proprie forze', 'sportiv format prin propriile eforturi', 'sportowiec ukształtowany własną pracą'),
    'dribbling': ('dribble', 'Dribbling', 'regate', 'drible', 'dribbling', 'dribling', 'drybling'),
    'passing': ('passes', 'Passspiel', 'pases', 'passes', 'passaggi', 'pase', 'podania'),
    'vision': ('vision du jeu', 'Spielübersicht', 'visión de juego', 'visão de jogo', 'visione di gioco', 'viziune de joc', 'wizja gry'),
    'playmaking': ('création du jeu', 'Spielgestaltung', 'creación de juego', 'criação de jogo', 'creazione del gioco', 'construcția jocului', 'kreowanie gry'),
    'young winger': ('jeune ailier', 'junger Flügelspieler', 'joven extremo', 'jovem extremo', 'giovane ala', 'extremă tânără', 'młody skrzydłowy'),
    'pace': ('vitesse', 'Schnelligkeit', 'velocidad', 'velocidade', 'velocità', 'viteză', 'szybkość'),
    'footwork': ('jeu de jambes', 'Fußarbeit', 'juego de pies', 'jogo de pés', 'gioco di piedi', 'joc de picioare', 'praca nóg'),
    'finishing': ('finition devant le but', 'Torabschluss', 'definición ante el gol', 'finalização', 'finalizzazione', 'finalizare', 'wykończenie akcji'),
    'headers': ('buts de la tête', 'Kopfbälle', 'remates de cabeza', 'cabeceamentos', 'colpi di testa', 'lovituri de cap', 'strzały głową'),
    'Italy': ('Italie', 'Italien', 'Italia', 'Itália', 'Italia', 'Italia', 'Włochy'),
    'attacking football': ('football offensif', 'Angriffsfußball', 'fútbol ofensivo', 'futebol ofensivo', 'calcio offensivo', 'fotbal ofensiv', 'ofensywny futbol'),
    'train': ('s’entraîner', 'trainieren', 'entrenar', 'treinar', 'allenarsi', 'a se antrena', 'trenować'),
    'compete': ('concourir', 'konkurrieren', 'competir', 'competir', 'competere', 'a concura', 'rywalizować'),
    'La Liga': ('La Liga', 'La Liga', 'La Liga', 'La Liga', 'La Liga', 'La Liga', 'La Liga'),
    'Real Madrid': ('Real Madrid', 'Real Madrid', 'Real Madrid', 'Real Madrid', 'Real Madrid', 'Real Madrid', 'Real Madryt'),
    'league records': ('records de championnat', 'Ligarekorde', 'récords de liga', 'recordes da liga', 'record di campionato', 'recorduri de campionat', 'rekordy ligowe'),
    'sustained expectation': ('attentes constantes', 'anhaltende Erwartungen', 'expectativas constantes', 'expectativas constantes', 'aspettative costanti', 'așteptări constante', 'stałe oczekiwania'),
    'modern football': ('football moderne', 'moderner Fußball', 'fútbol moderno', 'futebol moderno', 'calcio moderno', 'fotbal modern', 'współczesny futbol'),
    'assists': ('passes décisives', 'Torvorlagen', 'asistencias', 'assistências', 'assist', 'pase decisive', 'asysty'),
    'global figures': ('figures mondiales', 'globale Persönlichkeiten', 'figuras mundiales', 'figuras globais', 'figure globali', 'figuri globale', 'postacie światowe'),
    'fitness': ('condition physique', 'körperliche Fitness', 'condición física', 'condição física', 'forma fisica', 'condiție fizică', 'sprawność fizyczna'),
    'personal branding': ('image de marque personnelle', 'persönliche Markenbildung', 'marca personal', 'marca pessoal', 'marchio personale', 'brand personal', 'marka osobista'),
    'charitable work': ('action caritative', 'Wohltätigkeitsarbeit', 'labor benéfica', 'trabalho solidário', 'attività benefica', 'activitate caritabilă', 'działalność dobroczynna'),
    'persistence': ('persévérance', 'Beharrlichkeit', 'perseverancia', 'persistência', 'perseveranza', 'perseverență', 'wytrwałość'),
    'pressure': ('pression', 'Druck', 'presión', 'pressão', 'pressione', 'presiune', 'presja'),
    'close control': ('contrôle rapproché du ballon', 'enge Ballführung', 'control cercano del balón', 'controlo próximo da bola', 'controllo ravvicinato della palla', 'control apropiat al mingii', 'bliska kontrola piłki'),
    'contrasting players': ('joueurs aux styles opposés', 'Spieler mit gegensätzlichen Stilen', 'jugadores de estilos opuestos', 'jogadores de estilos contrastantes', 'giocatori dagli stili opposti', 'jucători cu stiluri contrastante', 'zawodnicy o odmiennych stylach'),
    'shared legacy': ('héritage commun', 'gemeinsames Erbe', 'legado compartido', 'legado partilhado', 'eredità condivisa', 'moștenire comună', 'wspólne dziedzictwo'),
    'chance': ('occasion de but', 'Torchance', 'ocasión de gol', 'ocasião de golo', 'occasione da gol', 'ocazie de gol', 'szansa na gola'),
}
for phrase, labels in replacements.items():
    assert len(labels) == len(languages)
    for language, label in zip(languages, labels):
        assert phrase in cache['translations'][language]
        cache['translations'][language][phrase] = label
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
print('curated', len(replacements), 'phrases')
