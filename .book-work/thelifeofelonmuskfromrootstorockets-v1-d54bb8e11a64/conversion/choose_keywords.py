import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parents[1];reader=w/'book/en/short_content.html';mp=w/'book/manifest.json';m=json.loads(mp.read_text())
source=b.keyword_source_text(reader)
candidates=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,120)
excluded={1,3,5,6,7,11,12,13,16,17,18,20,27,28,29,30,35,36,38,39,42,43,49,55,56,59,62,66,78,86}
phrases=[p for i,p in enumerate(candidates,1) if i not in excluded]
replacements={
 'electronic payments convenient':'online commerce',
 'settlement on mars':'self-sustaining settlement on Mars',
 'travel through low-resistance':'orbital debris',
 'international space':'Dragon capsule',
 'narrative separates':'NASA contracts',
 'surrounding privacy':'space technology',
 'serving newspapers':'online finance',
 'proceeds in x.com':'X.com merged with Confinity',
 'defining product':'eBay bought PayPal',
 'promising access':'solar power',
}
phrases=[replacements.get(p,p) for p in phrases]
assert len(phrases)==90 and len(set(phrases))==90
assert all(b.keyword_normalise(p) in b.keyword_normalise(source) for p in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-08','method':'editorial source-occurrence review of English ten-minute reader'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
