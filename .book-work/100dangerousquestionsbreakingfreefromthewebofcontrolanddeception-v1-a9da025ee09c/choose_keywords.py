import hashlib,importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('b','tools/build_books.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
w=Path(__file__).resolve().parent;p=w/'book/manifest.json';m=json.loads(p.read_text());reader=w/'book/en/short_content.html';source=b.keyword_source_text(reader)
candidates=b.extract_keyword_candidates(m['title']['en'],m['shortDescription']['en'],source,160)
excluded={13,16,26,49,98,29,43,59,68,77,78,82,83,88,95,99,102,103,106,107,110}
phrases=[v for i,v in enumerate(candidates,1) if i not in excluded]
revisions={
 'artificial intelligence':'algorithms',
 'challenge familiar ideals':'customs',
 'work offers flexibility':'celebrity',
 'ideals of impartiality':'nationalism',
 'precarious work offers':'marriage',
 'provocative possibilities':'forgiveness',
 'standard of normality':'self-worth',
 'language and support':'poverty',
 'people conceal parts':'risk to workers',
 'economic and social expectations':'afterlife',
 'come under scrutiny':'free will',
 'communication challenge':'consciousness',
 'stability and care':'policing',
 'guarantees advancement':'meritocracy',
 'automation complicate':'conformity',
 'pursuit of meaning anchor':'friendship',
 'creating contentment':'privilege',
 'people and widen access':'human judgment',
 'offers flexibility':'elections',
 'official decision':'representation',
 'choices people':'traditions',
 'stated purpose':'manipulation',
 'conceal parts':'intimacy',
 'hidden actor':'productivity',
 'widen access':'suffering',
}
phrases=[revisions.get(v,v) for v in phrases]
assert len(phrases)==len(set(phrases))==90
assert all(b.keyword_normalise(v) in b.keyword_normalise(source) for v in phrases)
assert all(b.keyword_normalise(v).strip() not in {b.keyword_normalise(x).strip() for entry in b.SHELF_CATEGORIES.values() for x in entry['en'].split('|')} for v in phrases)
m['keywordReview']={'sourceHash':hashlib.sha256(reader.read_bytes()).hexdigest(),'phrases':phrases,'reviewedOn':'2026-10-09','method':'editorial source-occurrence review of English ten-minute reader'}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
