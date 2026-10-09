import json
from pathlib import Path

cache_path = Path('tools/keyword-translations.generated.json')
cache = json.loads(cache_path.read_text())
languages = ('fr', 'de', 'es', 'pt', 'it', 'ro', 'pl')
replacements = {
    'living being': ('être vivant', 'lebendes Wesen', 'ser vivo', 'ser vivo', 'essere vivente', 'ființă vie', 'żywa istota'),
    'maker': ('créateur', 'Erschaffer', 'creador', 'criador', 'creatore', 'creator', 'twórca'),
    'alchemical writing': ('écrits alchimiques', 'alchemistische Schriften', 'escritos alquímicos', 'escritos alquímicos', 'scritti alchemici', 'scrieri alchimice', 'pisma alchemiczne'),
    'experiment': ('expérience scientifique', 'Experiment', 'experimento', 'experiência científica', 'esperimento', 'experiment', 'eksperyment'),
    'human customs': ('coutumes humaines', 'menschliche Bräuche', 'costumbres humanas', 'costumes humanos', 'usanze umane', 'obiceiuri omenești', 'ludzkie zwyczaje'),
    'William': ('William', 'William', 'William', 'William', 'William', 'William', 'William'),
    'silence': ('silence', 'Schweigen', 'silencio', 'silêncio', 'silenzio', 'tăcere', 'milczenie'),
    'companion': ('compagnon', 'Gefährte', 'compañero', 'companheiro', 'compagno', 'tovarăș', 'towarzysz'),
    'need for care': ('besoin de soins', 'Bedürfnis nach Fürsorge', 'necesidad de cuidado', 'necessidade de cuidados', 'bisogno di cure', 'nevoie de grijă', 'potrzeba opieki'),
    'possible harm': ('dommage possible', 'möglicher Schaden', 'posible daño', 'possível dano', 'possibile danno', 'posibil rău', 'możliwa szkoda'),
    'Elizabeth': ('Elizabeth', 'Elizabeth', 'Elizabeth', 'Elizabeth', 'Elizabeth', 'Elizabeth', 'Elizabeth'),
    'chain of loss': ('suite de pertes', 'Kette von Verlusten', 'cadena de pérdidas', 'cadeia de perdas', 'catena di perdite', 'șir de pierderi', 'łańcuch strat'),
    'duties': ('devoirs', 'Pflichten', 'deberes', 'deveres', 'doveri', 'îndatoriri', 'obowiązki'),
    'making life': ('donner la vie', 'Leben hervorbringen', 'dar vida', 'dar vida', 'dare la vita', 'a da viață', 'dawanie życia'),
    'powerful technologies': ('technologies puissantes', 'mächtige Technologien', 'tecnologías poderosas', 'tecnologias poderosas', 'tecnologie potenti', 'tehnologii puternice', 'potężne technologie'),
    'people affected': ('personnes concernées', 'betroffene Menschen', 'personas afectadas', 'pessoas afetadas', 'persone coinvolte', 'oameni afectați', 'osoby dotknięte skutkami'),
    'learn': ('apprendre', 'lernen', 'aprender', 'aprender', 'imparare', 'a învăța', 'uczyć się'),
    'protect': ('protéger', 'schützen', 'proteger', 'proteger', 'proteggere', 'a proteja', 'chronić'),
    'teach': ('enseigner', 'lehren', 'enseñar', 'ensinar', 'insegnare', 'a învăța pe cineva', 'nauczać'),
    'boundary': ('frontière', 'Grenze', 'frontera', 'fronteira', 'confine', 'graniță', 'granica'),
}
for phrase, labels in replacements.items():
    assert len(labels) == len(languages)
    for language, label in zip(languages, labels):
        assert phrase in cache['translations'][language]
        cache['translations'][language][phrase] = label
cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
print('curated', len(replacements), 'phrases')
