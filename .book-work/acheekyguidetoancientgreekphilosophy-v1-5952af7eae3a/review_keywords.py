import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, 'tools')
from build_books import keyword_normalise, keyword_source_text, SHELF_CATEGORIES

root = Path('.book-work/acheekyguidetoancientgreekphilosophy-v1-5952af7eae3a/book')
source = root / 'en/short_content.html'
manifest_path = root / 'manifest.json'
manifest = json.loads(manifest_path.read_text())
phrases = [
    'Greek philosophy', 'Pre-Socratics', 'Hellenistic schools',
    'European thought', 'historical evidence', 'philosophical questions',
    'old arguments', 'teaching style', 'early thinkers', 'inherited stories',
    'Thales', 'water as a basic element', 'Anaximander', 'apeiron',
    'boundless source', 'familiar material', 'Heraclitus', 'change',
    'river', 'constant change', 'proposed substances', 'competing proposals',
    'basic observation', 'continuing conversation', 'Socrates', 'Plato',
    'Aristotle', 'relentless questioner', 'confidence', 'method',
    'conversation', 'examination', 'easy answers', 'stable reality',
    'Forms', 'cave image', 'education', 'familiar appearances',
    'shadows', 'observable world', 'natural inquiry', 'politics',
    'Golden Mean', 'proportion', 'extremes', 'questioning',
    'abstract explanation', 'observation', 'Alexander', 'living well',
    'Cynics', 'convention', 'radical simplicity', 'Diogenes',
    'Stoics', 'events beyond one’s control', 'Epicureans', 'pleasure',
    'moderation', 'Skeptics', 'certainty', 'inquiry', 'freedom',
    'social expectations', 'disciplining judgment', 'modest satisfactions',
    'premature conclusions', 'Renaissance', 'ancient texts',
    'Scientific Revolution', 'mathematical form', 'Descartes',
    'Spinoza', 'Leibniz', 'Locke', 'Hume', 'mind', 'experience',
    'substance', 'knowledge', 'Nietzsche', 'existentialism',
    'phenomenology', 'analytic philosophy', 'postmodernism',
    'contemporary debates', 'language', 'identity', 'technology',
    'sense of humor',
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
