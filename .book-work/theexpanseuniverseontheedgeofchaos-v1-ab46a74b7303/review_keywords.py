import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, 'tools')
from build_books import keyword_normalise, keyword_source_text, subject_group, keyword_catalog

root = Path('.book-work/theexpanseuniverseontheedgeofchaos-v1-ab46a74b7303/book')
source = root / 'en/short_content.html'
manifest_path = root / 'manifest.json'
manifest = json.loads(manifest_path.read_text())
phrases = [
    'populated solar system', 'struggles over resources', 'Earth', 'Mars', 'the Belt',
    'control', 'protomolecule', 'alien technology', 'biology and physics',
    'human relationships', 'divided societies', 'philosophical interest', 'politics',
    'Rocinante', 'technological expansion', 'moral and social growth',
    'transform matter', 'living systems', 'capability',
    'human-scale refuge', 'crew', 'conflicting loyalties', 'mutual care',
    'powerful discovery', 'substitute for ethics', 'guarantee of progress', 'trust',
    'repeated choices', 'pressure', 'environmentally strained',
    'terraforming', 'Belters', 'stations and ships', 'extracting resources',
    'inner planets', 'low gravity', 'air', 'water', 'food',
    'bodily development', 'economic interdependence', 'resentment',
    'resistance', 'old inequalities', 'settlement', 'new hierarchies',
    'inherited suspicion', 'material inequalities', 'geography',
    'different gravities', 'migrations and crises', 'identities',
    'Julie Mao', 'search for purpose', 'loyalty to a community',
    'forms of life', 'intelligence', 'scientific curiosity', 'Prax Meng',
    'Elvi Okoye', 'strange phenomena', 'disciplined way to learn',
    'vulnerability and inquiry', 'meaning', 'scarce resources',
    'military and technological strength', 'trade', 'minerals and labor',
    'basic necessities', 'statecraft',
    'competing factions', 'transport', 'new technologies',
    'new discoveries', 'alliances', 'practical systems',
    'exploitation', 'negotiate power', 'missions', 'investigations',
    'battles', 'first contact', 'alien structures', 'ring gates',
    'uncertainty', 'adaptation', 'scientific learning', 'empathy',
    'political boundaries', 'institutions',
]
source_text = keyword_source_text(source)
group = subject_group(manifest['category'], manifest['title']['en'], manifest['shortDescription']['en'])
shelf = {keyword_normalise(v['en']) for _, _, v in keyword_catalog(group)}
missing = [p for p in phrases if keyword_normalise(p) not in keyword_normalise(source_text)]
duplicates = len(phrases) - len(set(phrases))
shelf_collisions = [p for p in phrases if keyword_normalise(p) in shelf]
print('phrases', len(phrases), 'distinct', len(set(phrases)), 'missing', missing, 'shelf', shelf_collisions)
if len(phrases) != 90 or duplicates or missing or shelf_collisions:
    raise SystemExit(1)
manifest['keywordReview'] = {
    'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(),
    'phrases': phrases,
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
