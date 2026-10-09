"""Review ninety source-occurring search phrases from the English short reader."""
import hashlib
import importlib.util
import json
from pathlib import Path

spec=importlib.util.spec_from_file_location('build_books','tools/build_books.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
root=Path(__file__).resolve().parents[1]
reader=root/'book/en/short_content.html'
mp=root/'book/manifest.json'
m=json.loads(mp.read_text())
source=b.keyword_source_text(reader)
candidates=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,120)
excluded={1,3,4,5,6,13,15,22,24,31,33,39,40,42,45,46,48,49,50,56,62,67,71,72,77,86,88,91,95,97}
phrases=[phrase for i,phrase in enumerate(candidates,1) if i not in excluded]
assert len(phrases)==90
assert len(set(phrases))==90
assert all(b.keyword_normalise(p) in b.keyword_normalise(source) for p in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-08','method':'editorial source-occurrence review of English ten-minute reader'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('selected',len(phrases))
