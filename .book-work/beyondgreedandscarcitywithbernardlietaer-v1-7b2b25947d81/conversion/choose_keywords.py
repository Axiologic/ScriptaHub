import hashlib,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
w=Path(__file__).resolve().parents[1];reader=w/'book/en/short_content.html';mp=w/'book/manifest.json';m=json.loads(mp.read_text())
source=b.keyword_source_text(reader)
candidates=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,120)
excluded={3,4,6,9,10,11,18,19,20,24,25,29,30,39,42,46,47,58,59,60,63,68,70,71,72,74,83,91,93,96}
phrases=[p for i,p in enumerate(candidates,1) if i not in excluded]
replacements={
 'stewardship alongside conventional market activity':'demurrage',
 'held cultural stories':'caregiving',
 'money through psychological archetypes':'psychological archetypes',
 'bitcoin shows demand':'Bitcoin',
 'designed for different needs':'interoperable',
 'qualities of care':'volunteering',
 'particular function':'speculative and competitive use',
 'systems circulate':'accountability',
 'historical model':"Bali's water and rice systems",
 'interprets money':'ancient Egypt',
 'artificial intelligence':'Yang qualities',
 'digital technology':'Yin qualities',
}
phrases=[replacements.get(p,p) for p in phrases]
assert len(phrases)==90,len(phrases)
assert len(set(phrases))==90
missing=[p for p in phrases if b.keyword_normalise(p) not in b.keyword_normalise(source)]
assert not missing,missing
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
