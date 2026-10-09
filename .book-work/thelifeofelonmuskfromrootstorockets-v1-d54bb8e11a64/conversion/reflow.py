"""Join sentences broken solely by source PDF page boundaries."""
from bs4 import BeautifulSoup
from pathlib import Path
import re
w=Path(__file__).resolve().parents[1]
for lang,ends in {'en':('U.S. reliance on',"The company's"),'ro':('navele spațiale','Unitățile companiei')}.items():
 p=w/f'book/{lang}/full_content.html'
 soup=BeautifulSoup(p.read_text(),'html.parser')
 for ending in ends:
  first=next(x for x in soup.select('p') if x.get_text(' ',strip=True).endswith(ending))
  second=first.find_next_sibling('p')
  assert second is not None
  first.append(' '+second.get_text(' ',strip=True))
  second.decompose()
 p.write_text(str(soup)+'\n')
 print(lang,'merged',len(ends),'page continuations')
