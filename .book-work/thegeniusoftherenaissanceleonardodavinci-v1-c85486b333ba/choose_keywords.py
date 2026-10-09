import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parent;reader=w/'book/en/short_content.html';p=w/'book/manifest.json';m=json.loads(p.read_text());source=b.keyword_source_text(reader)
candidates=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,140)
excluded={11,12,16,22,25,26,31,42,45,49,53,63,65,67,68,81,85,93,97,106}
phrases=[v for i,v in enumerate(candidates,1) if i not in excluded]
assert len(phrases)==len(set(phrases))==90
assert all(b.keyword_normalise(v) in b.keyword_normalise(source) for v in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
