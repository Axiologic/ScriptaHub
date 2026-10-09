import hashlib
import importlib.util
import json
from pathlib import Path

s=importlib.util.spec_from_file_location('b','tools/build_books.py')
b=importlib.util.module_from_spec(s)
s.loader.exec_module(b)
w=Path(__file__).resolve().parent
reader=w/'book/en/short_content.html'
p=w/'book/manifest.json'
m=json.loads(p.read_text())
source=b.keyword_source_text(reader)
candidates=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,180)
excluded={5,15,16,18,31,33,36,41,43,44,49,50,57,64,68,70,74,78,79,84,86,87,89,91,97,98,99,101,104,107,108,110,111,112}
phrases=[x for i,x in enumerate(candidates,1) if i not in excluded]
phrases+=['smartphones','televisions','thermostat','camera','advertisement after a conversation','data use','deletion of their data','access to audio','router and a phone','microphone and location permissions','data is shared','location and other data']
assert len(phrases)==len(set(phrases))==90
shelf={b.keyword_normalise(x).strip() for v in b.SHELF_CATEGORIES.values() for x in v['en'].split('|')}
assert all(b.keyword_normalise(x) in b.keyword_normalise(source) and b.keyword_normalise(x).strip() not in shelf and b.keyword_normalise(x)!=b.keyword_normalise(m['title']['en']) for x in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
