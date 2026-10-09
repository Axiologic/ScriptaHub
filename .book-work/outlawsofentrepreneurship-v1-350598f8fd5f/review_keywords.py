import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, 'tools')
from build_books import keyword_normalise, keyword_source_text, SHELF_CATEGORIES

root = Path('.book-work/outlawsofentrepreneurship-v1-350598f8fd5f/book')
source = root / 'en/short_content.html'
path = root / 'manifest.json'
manifest = json.loads(path.read_text())
phrases = [
    'enterprise', 'accepted rules', 'pirates', 'smugglers',
    'fraudsters', 'political rebels', 'innovators', 'business failures',
    'gaps in a system', 'ambition', 'sound judgment',
    'possibility and harm', 'useful disruption', 'exploitation',
    'shadow entrepreneurs', 'lawful founder', 'building a company',
    'organize people', 'assess risk', 'move goods', 'find customers',
    'formal rules', 'actual demand', 'adaptability', 'fraud',
    'coercion', 'trade', 'community', 'action under uncertainty',
    'large institutions', 'narrow interests', 'routes and markets',
    'lawbreaking', 'subversive enterprise',
    'established order', 'political and industrial figures',
    'existing institutions', 'French revolutionary tradition',
    'steel production', 'vertical integration',
    'assemble resources', 'alter production', 'new model',
    'industrial power', 'exploit workers', 'narrow competition',
    'stagnant system', 'who benefits', 'who bears the cost',
    'quiet innovators', 'agricultural work',
    'practical knowledge', 'farmers', 'improved crops', 'soil care',
    'Gordon Moore', 'technical work', 'microprocessors',
    'teaching', 'designing', 'organizing', 'solving a problem',
    'economic system', 'small decisions', 'public triumph',
    'comeback and collapse', 'South Sea Company', 'speculation',
    'productive activity', 'trading venture', 'investors',
    'share price', 'bubble', 'WeWork', 'rapid growth',
    'valuation', 'founder’s vision', 'recovery',
    'failure', 'risk', 'leader’s assumptions',
    'create value', 'resilience', 'oversight', 'evidence',
    'accountability', 'workers', 'customers', 'creative destruction', 'debt',
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
