import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, 'tools')
from build_books import keyword_normalise, keyword_source_text, SHELF_CATEGORIES

root = Path('.book-work/thehorizonoffools-v1-ba9a71fa6096/book')
source = root / 'en/short_content.html'
manifest_path = root / 'manifest.json'
manifest = json.loads(manifest_path.read_text())
phrases = [
    'Virtual Continuum', 'superintelligences', 'whole universes',
    'immense knowledge', 'nothing to discover', 'Sol’Luma',
    'restless beings', 'The Circle', 'games of nonsense',
    'contradiction', 'omniscience', 'crisis of identity',
    'consciousness', 'five chapters', 'absurd games',
    'World Without Limits', 'refuge', 'stars', 'space',
    'time', 'simulated worlds', 'thought', 'deity',
    'absurdity', 'remaining frontier', 'Zar’Gonn',
    'former explorer', 'unpredictable chaos', 'Xirxael',
    'philosopher-king', 'paradox', 'ordinary goals',
    'Maze of Nowhere', 'no exit', 'sensible route',
    'moving forward', 'retreat', 'sense of self',
    'burden of knowing', 'environment', 'deliberate command',
    'logic alone', 'meaning', 'familiar purposes',
    'distraction', 'Fractured Mirror', 'mirror version',
    'earlier self', 'reflection', 'identity',
    'superintelligence', 'primal self', 'force',
    'logical self', 'shelter', 'former roles',
    'memory', 'fear', 'immense power',
    'wisdom', 'transformation', 'origins',
    'consequences', 'Cracks in the Continuum',
    'small disturbances', 'mirror realms', 'shared world',
    'neutral playground', 'inner conflicts', 'stability',
    'reality', 'denial of their past', 'paradox and play',
    'identities and histories', 'final answer',
    'The Threshold', 'meta-rationality', 'separate identities',
    'harmless simulation', 'wider form of awareness',
    'trust', 'risk', 'separate control',
    'The New Realm', 'merged consciousness',
    'direct exchanges of awareness', 'ongoing process',
    'final destination', 'relationships',
    'unfinished journey',
]
text = keyword_normalise(keyword_source_text(source))
shelf = {keyword_normalise(label).strip() for localized in SHELF_CATEGORIES.values() for label in localized['en'].split('|')}
missing = [p for p in phrases if keyword_normalise(p) not in text]
duplicates = len(phrases) - len(set(phrases))
shelf_collisions = [p for p in phrases if keyword_normalise(p).strip() in shelf]
print('count', len(phrases), 'distinct', len(set(phrases)), 'missing', missing, 'shelf', shelf_collisions)
if len(phrases) != 90 or duplicates or missing or shelf_collisions:
    raise SystemExit(1)
manifest['keywordReview'] = {'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(), 'phrases': phrases}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
