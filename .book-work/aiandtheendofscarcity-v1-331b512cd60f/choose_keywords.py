import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('builder', 'tools/build_books.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
w = Path(__file__).resolve().parent
reader = w / 'book/en/short_content.html'
p = w / 'book/manifest.json'
m = json.loads(p.read_text())
source = b.keyword_source_text(reader)
candidates = b.extract_keyword_candidates(m['title']['en'], m['shortDescription']['en'], source, 200)
excluded = {3,6,7,11,13,16,17,25,27,29,30,33,34,38,40,43,45,47,48,52,53,54,59,61,70,71,72,75,79,80,87,89,93,97,109,112,114,116,124,125,126,128,129}
phrases = [v for i,v in enumerate(candidates,1) if i not in excluded]
phrases += ['predict demand', 'retraining', 'accountability', 'unequal access to essential goods']
assert len(phrases) == len(set(phrases)) == 90
assert all(b.keyword_normalise(x) in b.keyword_normalise(source) for x in phrases)
m['keywordReview'] = {'sourceHash': hashlib.sha256(reader.read_bytes()).hexdigest(), 'phrases': phrases, 'reviewedOn': '2026-10-09', 'method': 'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
