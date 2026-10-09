from bs4 import BeautifulSoup
from pathlib import Path
import re
w=Path(__file__).resolve().parents[1]
for lang in ('en','ro'):
 p=w/f'book/{lang}/full_content.html'
 s=BeautifulSoup(p.read_text(),'html.parser')
 refs=s.select('ol li')
 assert len(refs)==5
 for item in refs:
  item.string=re.sub(r'^\d+\.\s*','',item.get_text(' ',strip=True))
 p.write_text(str(s)+'\n')
