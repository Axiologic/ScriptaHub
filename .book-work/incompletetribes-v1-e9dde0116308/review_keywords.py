import hashlib
import importlib.util
import json
from pathlib import Path

w = Path(__file__).parent
source = w / 'book/en/short_content.html'
manifest_path = w / 'book/manifest.json'
spec = importlib.util.spec_from_file_location('build_books', 'tools/build_books.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
phrases = '''peaceful civilization|design of belonging|close groups|total authority|source of meaning|other loyalties|human psychology|institutional design|overlapping communities|community models|utopian promises|cynical resignation|historical variation|human biology|bounded community|loyalty|shared norms|memory|cooperation|group identities|trust and sacrifice|insiders and outsiders|multiple affiliations|layered reality|inconsistent people|fairness and advantage|intimacy and privacy|independence and recognition|internal conflict|total identity|absence of aggression|rivalry|negotiated settlements|restrained sanctions|survivable|idealism|sophisticated despair|world-sized community|criticism|complete tribe|jurisdiction|facts|friendships|private doubts|independent judgment|universal rights|equal legal standing|plural society|common civic floor|strong commitments|inherited communities|digital platforms|political movements|isolated people|synthetic intimacy|healthy groups|craft|service|form of care|corruption|routes for correction|constitutional|strong cooperation|knowledge is partial|jurisdiction limited|sovereignty should remain divided|overlapping loyalties|social divisions|shared institutions|mixed memberships|divided loyalty|voluntary departure|exit|dissent|trust and rules|leaders|sanctions|polycentric order|decision-making and failure|shared problems|legitimate opposition|rules of conflict|bridges across divisions|emotional synchronization|audit|outside comparisons|personalization|law of history|archipelago|imperfect people'''.split('|')
norm = b.keyword_normalise(b.keyword_source_text(source))
shelf = {b.keyword_normalise(label).strip() for localized in b.SHELF_CATEGORIES.values() for label in localized['en'].split('|')}
missing = [p for p in phrases if b.keyword_normalise(p) not in norm]
invalid = [p for p in phrases if b.keyword_normalise(p).strip() in shelf]
print('count', len(phrases), 'distinct', len(set(phrases)), 'missing', missing, 'shelf', invalid)
if len(phrases) != 90 or len(set(phrases)) != 90 or missing or invalid:
    raise SystemExit(1)
m = json.loads(manifest_path.read_text())
m['keywordReview'] = {'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(), 'phrases': phrases, 'status': 'reviewed-source-grounded'}
manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
