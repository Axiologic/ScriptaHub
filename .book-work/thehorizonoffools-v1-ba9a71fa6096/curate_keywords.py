import json
from pathlib import Path

path = Path('tools/keyword-translations.generated.json')
cache = json.loads(path.read_text())
fix = {
    'Virtual Continuum': {'es': 'Continuo Virtual', 'it': 'Continuum Virtuale', 'ro': 'Continuumul Virtual', 'pl': 'Wirtualne Kontinuum'},
    'superintelligences': {'de': 'Superintelligenzen', 'it': 'superintelligenze', 'pl': 'superinteligencje'},
    'superintelligence': {'pl': 'superinteligencja'},
    'Sol’Luma': {'fr': 'Sol’Luma', 'de': 'Sol’Luma', 'es': 'Sol’Luma', 'pt': 'Sol’Luma', 'it': 'Sol’Luma', 'ro': 'Sol’Luma', 'pl': 'Sol’Luma'},
    'Zar’Gonn': {'fr': 'Zar’Gonn', 'de': 'Zar’Gonn', 'es': 'Zar’Gonn', 'pt': 'Zar’Gonn', 'it': 'Zar’Gonn', 'ro': 'Zar’Gonn', 'pl': 'Zar’Gonn'},
    'omniscience': {'de': 'Allwissenheit', 'ro': 'omnisciență', 'pl': 'wszechwiedza'},
    'games of nonsense': {'fr': 'jeux dénués de sens', 'de': 'Spiele des Unsinns', 'es': 'juegos sin sentido', 'pt': 'jogos sem sentido', 'it': 'giochi senza senso', 'ro': 'jocuri fără noimă', 'pl': 'gry bez sensu'},
    'unpredictable chaos': {'pl': 'nieprzewidywalny chaos'},
    'philosopher-king': {'es': 'rey filósofo', 'ro': 'rege filosof', 'pl': 'król filozof'},
    'Maze of Nowhere': {'fr': 'Labyrinthe de Nulle Part', 'de': 'Labyrinth des Nirgendwo', 'es': 'Laberinto de Ninguna Parte', 'pt': 'Labirinto de Lugar Nenhum', 'it': 'Labirinto del Nulla', 'ro': 'Labirintul Nicăieri', 'pl': 'Labirynt Donikąd'},
    'sensible route': {'pt': 'trajeto coerente', 'ro': 'cale rațională'},
    'moving forward': {'de': 'Vorankommen', 'it': 'andare avanti', 'ro': 'înaintare'},
    'burden of knowing': {'fr': 'poids du savoir', 'pt': 'peso do conhecimento'},
    'remaining frontier': {'it': 'ultima frontiera', 'ro': 'frontiera rămasă'},
    'former explorer': {'de': 'ehemaliger Entdecker', 'pl': 'dawny odkrywca'},
    'Fractured Mirror': {'fr': 'Miroir brisé', 'de': 'Zerbrochener Spiegel', 'es': 'Espejo Roto', 'pt': 'Espelho Partido', 'it': 'Specchio Infranto', 'ro': 'Oglinda spartă', 'pl': 'Pęknięte Lustro'},
    'earlier self': {'fr': 'ancien soi', 'de': 'früheres Selbst', 'es': 'yo anterior', 'pt': 'eu anterior', 'it': 'sé precedente', 'ro': 'sinele de odinioară', 'pl': 'dawne ja'},
    'primal self': {'de': 'ursprüngliches Selbst', 'it': 'sé primordiale', 'ro': 'sine primordial'},
    'logical self': {'fr': 'soi logique', 'es': 'yo lógico', 'pt': 'eu lógico', 'it': 'sé logico', 'ro': 'sine logic'},
    'shelter': {'es': 'amparo', 'it': 'riparo', 'pl': 'osłona'},
    'Cracks in the Continuum': {'fr': 'Fissures dans le Continuum', 'de': 'Risse im Kontinuum', 'es': 'Grietas en el Continuo', 'pt': 'Fissuras no Continuum', 'it': 'Fessure nel Continuum', 'ro': 'Fisuri în continuum', 'pl': 'Pęknięcia w Kontinuum'},
    'shared world': {'de': 'gemeinsame Welt', 'ro': 'lume comună'},
    'denial of their past': {'pl': 'zaprzeczanie własnej przeszłości'},
    'paradox and play': {'de': 'Paradox und Spiel'},
    'final answer': {'de': 'endgültige Antwort'},
    'The Threshold': {'pt': 'O Limiar', 'ro': 'Pragul', 'pl': 'Próg'},
    'wider form of awareness': {'fr': 'forme plus vaste de conscience', 'es': 'forma más amplia de conciencia', 'pt': 'forma mais ampla de consciência', 'it': 'forma più ampia di coscienza', 'ro': 'formă mai amplă a conștiinței'},
    'The New Realm': {'ro': 'Noul tărâm', 'pl': 'Nowa Kraina'},
    'merged consciousness': {'pl': 'połączona świadomość'},
    'direct exchanges of awareness': {'fr': 'échanges directs de conscience', 'de': 'direkter Austausch von Bewusstsein', 'es': 'intercambios directos de conciencia', 'it': 'scambi diretti di coscienza', 'ro': 'schimburi directe de conștiință'},
}
for phrase, labels in fix.items():
    for lang, label in labels.items():
        assert phrase in cache['translations'][lang], (phrase, lang)
        cache['translations'][lang][phrase] = label
path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
print('Curated', sum(map(len, fix.values())), 'labels')
