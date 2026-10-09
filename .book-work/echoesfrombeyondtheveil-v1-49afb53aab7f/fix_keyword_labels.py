import json
from pathlib import Path

cache_path = Path('tools/keyword-translations.generated.json')
cache = json.loads(cache_path.read_text(encoding='utf-8'))
langs = ('fr', 'de', 'es', 'pt', 'it', 'ro', 'pl')
fixes = {
    'Administrator Thorne': ('Administrateur Thorne', 'Administrator Thorne', 'Administrador Thorne', 'Administrador Thorne', 'Amministratore Thorne', 'Administratorul Thorne', 'Administrator Thorne'),
    'ARIA': ('ARIA', 'ARIA', 'ARIA', 'ARIA', 'ARIA', 'ARIA', 'ARIA'),
    'Cosmic Wardens': ('Gardiens cosmiques', 'Kosmische Wächter', 'Guardianes Cósmicos', 'Guardiões Cósmicos', 'Custodi Cosmici', 'Străjerii Cosmici', 'Kosmiczni Strażnicy'),
    'Sumerian tablets': ('tablettes sumériennes', 'sumerische Tontafeln', 'tablillas sumerias', 'tabuletas sumérias', 'tavolette sumere', 'tăblițe sumeriene', 'tabliczki sumeryjskie'),
    'Gnostic gospels': ('évangiles gnostiques', 'gnostische Evangelien', 'evangelios gnósticos', 'evangelhos gnósticos', 'vangeli gnostici', 'evanghelii gnostice', 'ewangelie gnostyckie'),
    'quantum entanglement': ('intrication quantique', 'Quantenverschränkung', 'entrelazamiento cuántico', 'emaranhamento quântico', 'entanglement quantistico', 'încurcare cuantică', 'splątanie kwantowe'),
    'quantum entanglement simulation': ('simulation d’intrication quantique', 'Simulation der Quantenverschränkung', 'simulación de entrelazamiento cuántico', 'simulação de emaranhamento quântico', 'simulazione dell’entanglement quantistico', 'simulare de încurcare cuantică', 'symulacja splątania kwantowego'),
    'quantum fluctuations': ('fluctuations quantiques', 'Quantenschwankungen', 'fluctuaciones cuánticas', 'flutuações quânticas', 'fluttuazioni quantistiche', 'fluctuații cuantice', 'fluktuacje kwantowe'),
    'multiversal rebellion': ('rébellion multiverselle', 'multiverselle Rebellion', 'rebelión multiversal', 'rebelião multiversal', 'ribellione multiversale', 'rebeliune multiversală', 'bunt wieloświatów'),
    'collective resistance': ('résistance collective', 'kollektiver Widerstand', 'resistencia colectiva', 'resistência coletiva', 'resistenza collettiva', 'rezistență colectivă', 'zbiorowy opór'),
    'utopia': ('utopie', 'Utopie', 'utopía', 'utopia', 'utopia', 'utopie', 'utopia'),
    'perfect morning': ('matin parfait', 'perfekter Morgen', 'mañana perfecta', 'manhã perfeita', 'mattina perfetta', 'dimineață perfectă', 'idealny poranek'),
    'maglevs': ('trains à sustentation magnétique', 'Magnetschwebebahnen', 'trenes de levitación magnética', 'comboios de levitação magnética', 'treni a levitazione magnetica', 'trenuri maglev', 'koleje magnetyczne'),
    'unstated consequence': ('conséquence implicite', 'unausgesprochene Konsequenz', 'consecuencia no expresada', 'consequência não declarada', 'conseguenza sottintesa', 'consecință nerostită', 'niewypowiedziana konsekwencja'),
    'rehearsed assurances': ('assurances répétées', 'eingeübte Beteuerungen', 'garantías ensayadas', 'garantias ensaiadas', 'rassicurazioni preparate', 'asigurări exersate', 'wyuczone zapewnienia'),
    'practiced smiles': ('sourires de façade', 'eingeübtes Lächeln', 'sonrisas ensayadas', 'sorrisos ensaiados', 'sorrisi studiati', 'zâmbete exersate', 'wyćwiczone uśmiechy'),
    'fractured mirror': ('miroir brisé', 'zerbrochener Spiegel', 'espejo fracturado', 'espelho fraturado', 'specchio infranto', 'oglindă spartă', 'pęknięte lustro'),
    'timelines': ('lignes temporelles', 'Zeitlinien', 'líneas temporales', 'linhas temporais', 'linee temporali', 'linii temporale', 'linie czasowe'),
    'shifting entities': ('entités changeantes', 'wandelnde Wesen', 'entidades cambiantes', 'entidades mutáveis', 'entità mutevoli', 'entități schimbătoare', 'zmienne istoty'),
    'neural assistant ARIA': ('assistante neurale ARIA', 'neuronale Assistentin ARIA', 'asistente neuronal ARIA', 'assistente neural ARIA', 'assistente neurale ARIA', 'asistenta neuronală ARIA', 'asystentka neuronowa ARIA'),
    'distortions in the sky': ('distorsions dans le ciel', 'Verzerrungen am Himmel', 'distorsiones en el cielo', 'distorções no céu', 'distorsioni nel cielo', 'distorsiuni pe cer', 'zniekształcenia na niebie'),
    'supposed safety': ('sécurité supposée', 'vermeintliche Sicherheit', 'supuesta seguridad', 'suposta segurança', 'presunta sicurezza', 'presupusă siguranță', 'rzekome bezpieczeństwo'),
    'Wardens’ power': ('pouvoir des Gardiens', 'Macht der Wächter', 'poder de los Guardianes', 'poder dos Guardiões', 'potere dei Custodi', 'puterea Străjerilor', 'moc Strażników'),
    'crystal shatters': ('le cristal se brise', 'Kristall zerbricht', 'el cristal se rompe', 'o cristal se parte', 'il cristallo si frantuma', 'cristalul se sparge', 'kryształ pęka'),
    'apparent order': ('ordre apparent', 'scheinbare Ordnung', 'orden aparente', 'ordem aparente', 'ordine apparente', 'ordine aparentă', 'pozorny porządek'),
    "Wardens' forms": ('formes des Gardiens', 'Gestalten der Wächter', 'formas de los Guardianes', 'formas dos Guardiões', 'forme dei Custodi', 'formele Străjerilor', 'postacie Strażników'),
    'comfort of New Athens’ illusion': ('confort de l’illusion de la Nouvelle Athènes', 'Trost der Illusion von Neu-Athen', 'consuelo de la ilusión de Nueva Atenas', 'conforto da ilusão de Nova Atenas', 'conforto dell’illusione di Nuova Atene', 'confortul iluziei Noii Atene', 'pociecha złudzenia Nowych Aten'),
}

for phrase, labels in fixes.items():
    assert len(labels) == len(langs), phrase
    for language, label in zip(langs, labels):
        assert phrase in cache['translations'][language], (language, phrase)
        cache['translations'][language][phrase] = label
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Corrected {len(fixes)} discovery phrases across {len(langs)} languages')
