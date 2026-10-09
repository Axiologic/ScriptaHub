import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, 'tools')
from build_books import keyword_normalise, keyword_source_text, SHELF_CATEGORIES

root = Path('.book-work/charlesdarwinarevolutionaryforceinscienceandsociety-v1-412e39743f82/book')
source = root / 'en/short_content.html'
path = root / 'manifest.json'
manifest = json.loads(path.read_text())
phrases = [
    'Darwin', 'evolution by natural selection', 'diversity of life',
    'Beagle voyage', 'genetics', 'disputes about science and religion', 'evolutionary language',
    'practical applications', "Darwin's method", 'compare evidence',
    'revise explanations', 'present-day biology', 'DNA',
    'physical account of inheritance', 'mutations', 'population genetics',
    'genetic drift', 'evolutionary developmental biology',
    'variation and selection', 'neutral mutations', 'speculation',
    'biological evolution', 'technology and culture', 'scientific interests',
    'observing nature', 'classical curriculum', 'medical training',
    'Edinburgh', 'Cambridge', 'clergy', 'beetles',
    'John Stevens Henslow', 'HMS Beagle', 'early habit of observation',
    'naturalist', 'specimens and notes', 'South America',
    'geological layers', 'Cape Verde', 'slow change',
    'vast time', 'fossils', 'living animals', 'Galápagos Islands',
    'closely related forms', 'fixity of species', 'collections',
    'transformation of species', 'John Gould', 'Galápagos finches',
    'geographical distribution', 'Thomas Malthus', 'limited resources',
    'inherited traits', 'advantageous traits', 'descendants',
    'populations', 'On the Origin of Species', 'Mendel',
    'heredity', 'natural selection', 'acquired traits',
    'directed evolution', 'Modern Synthesis', 'molecular biology',
    'measurement', 'separately created species',
    "humanity's place in nature", 'theological and philosophical debates',
    'philosophical debates', 'political uses', 'Social Darwinism',
    'eugenics', 'hierarchy and coercion', 'human behavior',
    'morality', 'cultural influences', 'artificial selection',
    'crop and animal breeding', 'genetic diversity', 'seed preservation',
    'conservation', 'bacteria and viruses', 'antibiotic resistance',
    'vaccine development', 'genetic algorithms', 'swarm intelligence',
    'synthetic biology', 'adaptation', 'model of inquiry',
]
text = keyword_normalise(keyword_source_text(source))
shelf = {keyword_normalise(label).strip() for localized in SHELF_CATEGORIES.values() for label in localized['en'].split('|')}
missing = [phrase for phrase in phrases if keyword_normalise(phrase) not in text]
collisions = [phrase for phrase in phrases if keyword_normalise(phrase).strip() in shelf]
print('count', len(phrases), 'distinct', len(set(phrases)), 'missing', missing, 'shelf', collisions)
if len(phrases) != 90 or len(set(phrases)) != 90 or missing or collisions:
    raise SystemExit(1)
manifest['keywordReview'] = {'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(), 'phrases': phrases}
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
