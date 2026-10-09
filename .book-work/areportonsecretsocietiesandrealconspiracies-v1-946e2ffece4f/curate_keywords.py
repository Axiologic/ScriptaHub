import json
from pathlib import Path

cache_path = Path('tools/keyword-translations.generated.json')
cache = json.loads(cache_path.read_text())
overrides = {
    'Edward Snowden’s disclosures': {'fr': 'révélations d’Edward Snowden', 'de': 'Enthüllungen von Edward Snowden', 'es': 'revelaciones de Edward Snowden', 'pt': 'revelações de Edward Snowden', 'it': 'rivelazioni di Edward Snowden', 'ro': 'dezvăluirile lui Edward Snowden', 'pl': 'ujawnienia Edwarda Snowdena'},
    'USS Liberty': {'fr': 'USS Liberty', 'de': 'USS Liberty', 'es': 'USS Liberty', 'pt': 'USS Liberty', 'it': 'USS Liberty', 'ro': 'USS Liberty', 'pl': 'USS Liberty'},
    'Watergate': {'fr': 'Watergate', 'de': 'Watergate', 'es': 'Watergate', 'pt': 'Watergate', 'it': 'Watergate', 'ro': 'Watergate', 'pl': 'Watergate'},
    'Cambridge Analytica': {'pl': 'Cambridge Analytica'},
    'personal information': {'pl': 'informacje osobiste'},
    'Fellowship': {'fr': 'The Fellowship', 'de': 'The Fellowship', 'es': 'The Fellowship', 'pt': 'The Fellowship', 'it': 'The Fellowship', 'ro': 'The Fellowship', 'pl': 'The Fellowship'},
    'Freemasonry': {'pl': 'wolnomularstwo'},
    'Skull and Bones': {'fr': 'Skull and Bones', 'de': 'Skull and Bones', 'es': 'Skull and Bones', 'pt': 'Skull and Bones', 'it': 'Skull and Bones', 'ro': 'Skull and Bones', 'pl': 'Skull and Bones'},
    'Operation Snow White': {'fr': 'opération Snow White', 'de': 'Operation Snow White', 'es': 'operación Snow White', 'pt': 'operação Snow White', 'it': 'operazione Snow White', 'ro': 'Operațiunea Snow White', 'pl': 'operacja Snow White'},
    'Project Sunshine': {'de': 'Projekt Sunshine'},
    'infiltration': {'pl': 'infiltracja'},
    'recorded event': {'pl': 'udokumentowane zdarzenie'},
    'political figures': {'de': 'politische Persönlichkeiten', 'ro': 'personalități politice', 'pl': 'postacie polityczne'},
    'intelligence tests': {'fr': 'tests d’intelligence', 'it': 'test di intelligenza', 'ro': 'teste de inteligență', 'pl': 'testy inteligencji'},
    'online quizzes': {'es': 'cuestionarios en línea'},
    'target messages': {'fr': 'messages ciblés', 'de': 'gezielte Botschaften', 'es': 'mensajes dirigidos', 'pt': 'mensagens direcionadas', 'it': 'messaggi mirati', 'ro': 'mesaje direcționate', 'pl': 'ukierunkowane komunikaty'},
    'official cover-ups': {'fr': 'dissimulation officielle', 'de': 'amtliche Vertuschungen', 'it': 'insabbiamenti ufficiali', 'ro': 'mușamalizări oficiale', 'pl': 'oficjalne tuszowanie'},
    'political deception': {'fr': 'tromperie politique', 'pt': 'engano político'},
    'biological weapons testing': {'fr': 'essais d’armes biologiques'},
    'reported meeting': {'fr': 'réunion rapportée', 'es': 'reunión documentada', 'it': 'riunione riferita', 'pl': 'relacjonowane spotkanie'},
    'public record': {'it': 'documentazione pubblica'},
    'membership list': {'it': 'elenco dei membri'},
    'coordinated plot': {'fr': 'complot coordonné', 'pt': 'conspiração coordenada', 'pl': 'skoordynowany spisek'},
    'fraternal network': {'ro': 'rețea fraternă'},
    'official explanations': {'de': 'offizielle Erklärungen'},
}
for phrase, labels in overrides.items():
    for language, label in labels.items():
        if phrase not in cache['translations'][language]:
            raise ValueError((phrase, language))
        cache['translations'][language][phrase] = label
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
print(f'Curated {sum(len(values) for values in overrides.values())} local keyword labels')
