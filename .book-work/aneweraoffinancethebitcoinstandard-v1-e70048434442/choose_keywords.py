import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('builder', 'tools/build_books.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
work = Path(__file__).resolve().parent
reader = work / 'book/en/short_content.html'
manifest_path = work / 'book/manifest.json'
manifest = json.loads(manifest_path.read_text())
text = builder.keyword_source_text(reader)
candidates = builder.extract_keyword_candidates(manifest['title']['en'], manifest['shortDescription']['en'], text, 180)
excluded = {3,5,9,10,16,20,26,27,29,31,32,36,42,43,48,49,52,57,61,64,65,69,72,75,86,87,89,90,92,95,97,98,107,112,114,117,119,120}
selected = [phrase for i, phrase in enumerate(candidates[:120], 1) if i not in excluded]
selected += [candidates[i-1] for i in (123,125,127,128,130,132,133,134)]
assert len(selected) == len(set(selected)) == 90
assert all(builder.keyword_normalise(phrase) in builder.keyword_normalise(text) for phrase in selected)
manifest['keywordReview'] = {'sourceHash': hashlib.sha256(reader.read_bytes()).hexdigest(), 'phrases': selected, 'reviewedOn': '2026-10-09', 'method': 'editorial source-occurrence review of English ten-minute reader'}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
