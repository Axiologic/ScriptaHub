import json
from pathlib import Path

path = Path('tools/keyword-translations.generated.json')
data = json.loads(path.read_text())
fix = {
    'the Belt': {'pt': 'o Cinturão', 'pl': 'Pas Asteroidów'},
    'Belters': {'fr': 'habitants de la Ceinture', 'de': 'Bewohner des Gürtels', 'es': 'habitantes del Cinturón', 'pt': 'habitantes do Cinturão', 'it': 'abitanti della Cintura', 'ro': 'locuitori ai Centurii', 'pl': 'mieszkańcy Pasa'},
    'Rocinante': {'ro': 'Rocinante', 'pl': 'Rocinante'},
    'protomolecule': {'de': 'Protomolekül'},
    'alien technology': {'fr': 'technologie extraterrestre', 'es': 'tecnología extraterrestre', 'pl': 'technologia pozaziemska'},
    'philosophical interest': {'ro': 'interes filosofic', 'pl': 'zainteresowanie filozoficzne'},
    'transform matter': {'pl': 'przekształcanie materii'},
    'living systems': {'ro': 'sisteme vii', 'pl': 'żywe systemy'},
    'human-scale refuge': {'de': 'Zuflucht im menschlichen Maßstab'},
    'crew': {'es': 'tripulación'},
    'conflicting loyalties': {'de': 'widersprüchliche Loyalitäten'},
    'substitute for ethics': {'fr': 'substitut à l’éthique', 'it': 'sostituto dell’etica', 'ro': 'substitut pentru etică', 'pl': 'substytut etyki'},
    'environmentally strained': {'es': 'bajo presión ambiental', 'pt': 'sob pressão ambiental', 'it': 'sotto pressione ambientale', 'pl': 'obciążony środowiskowo'},
    'stations and ships': {'de': 'Raumstationen und Schiffe'},
    'resentment': {'pl': 'uraza'},
    'settlement': {'fr': 'colonisation', 'de': 'Besiedlung', 'es': 'asentamiento', 'pt': 'assentamento', 'it': 'insediamento', 'ro': 'colonizare', 'pl': 'osadnictwo'},
    'different gravities': {'de': 'unterschiedliche Schwerkraft', 'es': 'distintas fuerzas de gravedad', 'pl': 'różne siły grawitacji'},
    'search for purpose': {'de': 'Suche nach Sinn', 'pl': 'poszukiwanie celu'},
    'intelligence': {'fr': 'intelligence', 'it': 'intelligenza', 'ro': 'inteligență'},
    'vulnerability and inquiry': {'de': 'Verletzlichkeit und Forschung', 'es': 'vulnerabilidad e indagación', 'pt': 'vulnerabilidade e investigação', 'it': 'vulnerabilità e ricerca', 'ro': 'vulnerabilitate și cercetare', 'pl': 'wrażliwość i dociekanie'},
    'scarce resources': {'ro': 'resurse limitate'},
    'minerals and labor': {'pt': 'minerais e trabalho'},
    'statecraft': {'fr': 'art de gouverner', 'de': 'Staatskunst', 'es': 'arte de gobernar', 'pt': 'arte de governar', 'it': 'arte di governare', 'ro': 'arta guvernării', 'pl': 'sztuka rządzenia'},
    'negotiate power': {'ro': 'negocierea puterii', 'pl': 'negocjowanie władzy'},
    'alien structures': {'fr': 'structures extraterrestres', 'it': 'strutture extraterrestri', 'pl': 'struktury pozaziemskie'},
    'ring gates': {'fr': 'portes des anneaux', 'de': 'Ringportale', 'es': 'puertas de los anillos', 'pt': 'portais dos anéis', 'it': 'portali degli anelli', 'ro': 'porțile inelare', 'pl': 'bramy pierścieniowe'},
    'scientific learning': {'pl': 'uczenie się przez naukę'},
}
for phrase, labels in fix.items():
    for language, label in labels.items():
        assert phrase in data['translations'][language], (phrase, language)
        data['translations'][language][phrase] = label
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Curated', sum(map(len, fix.values())), 'keyword labels')
