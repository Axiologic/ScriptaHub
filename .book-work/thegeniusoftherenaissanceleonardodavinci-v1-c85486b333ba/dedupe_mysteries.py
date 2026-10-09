from bs4 import BeautifulSoup
from pathlib import Path
import json

work=Path(__file__).resolve().parent
markers={'en':' Many myths and conspiracy theories have emerged over the years','ro':' De-a lungul anilor au apărut numeroase mituri și teorii ale conspirației'}
for language,marker in markers.items():
 p=work/'book'/language/'full_content.html'
 s=BeautifulSoup(p.read_text(),'html.parser')
 paragraphs=s.find('section',id='mysteries').find_all('p')
 assert len(paragraphs)==10 and marker in paragraphs[2].get_text()
 paragraphs[2].string.replace_with(paragraphs[2].string.split(marker,1)[0])
 paragraphs[3].decompose()
 p.write_text(str(s))
qa=work/'qa/source-selection.json';d=json.loads(qa.read_text());d['editorialCleanup']='Chapter Four repeated two near-identical passages on secret messages, The Da Vinci Code, and the Mona Lisa. Kept first occurrence and all unique material; removed repetitions in both EN and RO readers.';qa.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
