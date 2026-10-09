import hashlib,importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
w=Path(__file__).resolve().parent;reader=w/'book/en/short_content.html';p=w/'book/manifest.json';m=json.loads(p.read_text());source=b.keyword_source_text(reader)
c=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,200)
indices=[1,2,3,5,6,7,9,10,11,12,13,14,15,17,18,19,20,22,23,25,26,27,28,29,30,31,32,33,34,35,36,37,40,41,42,43,44,45,47,48,49,50,52,53,54,55,60,61,63,64,65,66,67,69,70,71,74,78,79,81,83,59]
custom=['the One Ring','Bilbo Baggins','the Shire','Middle-earth','servants of Sauron attack','threatened by Sauron’s darkness','bring Frodo and Sam','ancient maps and artifacts','Bilbo discovers an old map','toward a concealed realm','ancient source of light','ring represents','new adventure in Middle-earth','fellowship as a union','rough terrain, storms','shared courage and trust','Gandalf’s guidance','Aragorn’s steadiness','Legolas’s observation','Gimli’s determination','hobbits’ persistence','inside the hidden realm','light within him','servants of Sauron','trust, sacrifice','trust, loyalty','loyalty and the readiness','stronger sense of purpose']
phrases=[c[i-1] for i in indices]+custom
assert len(phrases)==len(set(phrases))==90
shelf={b.keyword_normalise(x).strip() for v in b.SHELF_CATEGORIES.values() for x in v['en'].split('|')}
bad=[x for x in phrases if b.keyword_normalise(x) not in b.keyword_normalise(source) or b.keyword_normalise(x).strip() in shelf or b.keyword_normalise(x)==b.keyword_normalise(m['title']['en'])]
assert not bad,bad
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
