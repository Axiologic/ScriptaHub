import hashlib,importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
w=Path(__file__).resolve().parent;reader=w/'book/en/short_content.html';p=w/'book/manifest.json';m=json.loads(p.read_text());source=b.keyword_source_text(reader)
c=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,180)
indices=[1,2,3,6,8,9,10,11,12,13,17,19,21,23,24,27,30,31,33,34,36,37,39,40,41,43,44,46,53,54,57,58,59,63,65,68,69,70,71,72,73,74,76,77,79,80,81,82,83,84,85,86,88,89,90,91,94,95,97,98,99,100,101,102,105,106,108,110,111,112,113,114,115,118,120,121,124,127,128,133,134,135,136,137,143,149,151,152,153,154]
phrases=[c[i-1] for i in indices]
assert len(phrases)==len(set(phrases))==90
shelf={b.keyword_normalise(x).strip() for v in b.SHELF_CATEGORIES.values() for x in v['en'].split('|')}
assert all(b.keyword_normalise(x) in b.keyword_normalise(source) and b.keyword_normalise(x).strip() not in shelf and b.keyword_normalise(x)!=b.keyword_normalise(m['title']['en']) for x in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
