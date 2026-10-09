import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parent;p=w/'book/manifest.json';m=json.loads(p.read_text());reader=w/'book/en/short_content.html';source=b.keyword_source_text(reader)
v=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,160)
keep='1,2,3,5,7,8,9,11,12,13,14,15,16,18,20,22,23,24,25,26,27,29,30,31,32,33,35,36,37,38,39,41,42,43,45,46,47,48,50,52,53,54,55,56,57,58,60,62,64,66,68,69,70,71,72,73,74,75,76,77,78,79,81,82,85,87,89,90,91,93,94,95,96,97,98,99,100,101,103,106,108,109,110,111,112,113,115,123,125,126'
indices=[int(x) for x in keep.split(',')]
phrases=[v[i-1] for i in indices]
phrases=[{'federal reserve':'2008 financial crisis','murray rothbard':'liquidity','creating money':'accountability','prices and distribute benefits':'benefits unevenly','crisis support work':'stimulus','created money enters':'newly created money','different routes':'households, firms','way expectations':'expectations','examines inflation':'production','constraints on money':'credit','spending power expands':'demand','spending power':'savers','free-banking proposal and commodity-backed money':'depositors'}.get(x,x) for x in phrases]
assert len(phrases)==len(set(phrases))==90
assert all(b.keyword_normalise(x) in b.keyword_normalise(source) for x in phrases)
shelf={b.keyword_normalise(x).strip() for e in b.SHELF_CATEGORIES.values() for x in e['en'].split('|')}
assert all(b.keyword_normalise(x).strip() not in shelf for x in phrases)
assert all(b.keyword_normalise(x)!=b.keyword_normalise(m['title']['en']) for x in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print(len(phrases),'source-grounded phrases')
