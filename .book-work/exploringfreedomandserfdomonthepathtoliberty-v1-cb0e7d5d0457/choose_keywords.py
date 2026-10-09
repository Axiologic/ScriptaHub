import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parent;reader=w/'book/en/short_content.html';mp=w/'book/manifest.json';m=json.loads(mp.read_text())
source=b.keyword_source_text(reader)
candidates=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,120)
excluded={2,3,4,6,12,13,16,18,21,26,34,39,40,43,47,51,52,57,66,72,78,85,91,93,97,99,100}
phrases=[p for i,p in enumerate(candidates,1) if i not in excluded]
assert len(phrases)==90 and len(set(phrases))==90
assert all(b.keyword_normalise(p) in b.keyword_normalise(source) for p in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
