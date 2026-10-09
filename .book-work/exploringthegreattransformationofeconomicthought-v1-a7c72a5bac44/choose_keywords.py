import hashlib
import importlib.util
import json
from pathlib import Path

s = importlib.util.spec_from_file_location('b', 'tools/build_books.py')
b = importlib.util.module_from_spec(s)
s.loader.exec_module(b)
w = Path(__file__).resolve().parent
reader = w/'book/en/short_content.html'
p = w/'book/manifest.json'
m = json.loads(p.read_text())
text = b.keyword_source_text(reader)
candidates = b.extract_keyword_candidates(m['title']['en'], m['shortDescription']['en'], text, 180)
indices = [1,2,3,4,5,8,9,11,13,18,21,22,25,28,29,31,32,33,34,37,40,41,42,44,45,46,48,49,50,51,52,55,56,57,58,59,61,63,64,65,69,70,72,74,76,77,79,85,86,87,88,89,90,91,92,93,94,96,97,98,99,100,101,102,103,105,106,107,109,110,112,113,115,116,118,119,120,121,122,123,124,125,126,127,128,131,134,140,141,142]
phrases = [candidates[i-1] for i in indices]
assert len(phrases) == len(set(phrases)) == 90
shelf = {b.keyword_normalise(x).strip() for v in b.SHELF_CATEGORIES.values() for x in v['en'].split('|')}
assert all(b.keyword_normalise(x) in b.keyword_normalise(text) and b.keyword_normalise(x).strip() not in shelf for x in phrases)
m['keywordReview'] = {'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(), 'phrases':phrases, 'reviewedOn':'2026-10-09', 'method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
