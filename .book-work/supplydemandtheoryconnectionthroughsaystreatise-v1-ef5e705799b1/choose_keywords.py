import hashlib,importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
w=Path(__file__).resolve().parent;reader=w/'book/en/short_content.html';p=w/'book/manifest.json';m=json.loads(p.read_text());source=b.keyword_source_text(reader)
c=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,200)
indices=[3,4,9,10,11,12,15,17,19,20,24,25,26,27,30,31,33,34,37,38,39,40,41,43,44,45,46,48,51,53,56,57,58,60,64,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,83,132,85,87,89,90,91,93,94,95,96,97,98,99,101,103,104,105,106,107,108,131,110,123,113,114,117,119,135,122,124,125,126,127,128,129,133,136,138]
phrases=[c[i-1] for i in indices]
assert len(phrases)==len(set(phrases))==90
shelf={b.keyword_normalise(x).strip() for v in b.SHELF_CATEGORIES.values() for x in v['en'].split('|')}
assert all(b.keyword_normalise(x) in b.keyword_normalise(source) and b.keyword_normalise(x).strip() not in shelf and b.keyword_normalise(x)!=b.keyword_normalise(m['title']['en']) for x in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
