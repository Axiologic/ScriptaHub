from pathlib import Path
from bs4 import BeautifulSoup
import json

work=Path(__file__).parent
path=work/'book/en/full_content.html'
soup=BeautifulSoup(path.read_text(),'html.parser')
article=soup.select_one('article[data-reader-content]')
assert article
paragraphs=article.find_all('p',recursive=False)
assert len(paragraphs)==350,len(paragraphs)
assert paragraphs[9].get_text(' ',strip=True)=='Contents'
assert paragraphs[38].get_text(' ',strip=True)=='INTRODUCTION'
assert paragraphs[321].get_text(' ',strip=True)=='Selected References'

def heading(index,label,level,id=None,drop_next=None):
    old=paragraphs[index]
    new=soup.new_tag(level)
    new.string=label
    if id:new['id']=id
    old.replace_with(new)
    if drop_next is not None:paragraphs[drop_next].decompose()

heading(0,'Two Ways to Build a World','h1','book-title')
heading(5,'Note to the Reader','h2','reader-note')
heading(38,'Introduction: The Question After the Myth','h2','introduction',39)
for part,start in enumerate((47,88,138,191,245),1):
    title=paragraphs[start+1].get_text(' ',strip=True)
    heading(start,f'Part {part}: {title}','h2',f'part_{part:02}',start+1)
for number,start in enumerate((50,62,74,91,103,114,126,141,154,166,179,194,207,219,231,248,262,275),1):
    title=paragraphs[start+1].get_text(' ',strip=True)
    heading(start,f'Chapter {number}: {title}','h2',f'chapter_{number:02}',start+1)
heading(295,'Conclusion: The Choice Is an Architecture','h2','conclusion',296)
heading(305,'Appendix A: The Partnership-Domination Scorecard','h2','appendix_a',306)
heading(309,'Appendix B: A Research Agenda','h2','appendix_b',310)
heading(321,'Selected References','h2','references')
heading(348,'Source note','h2','source-note')
for i in (73,87,153,206,261,294,308):
    heading(i,paragraphs[i].get_text(' ',strip=True),'h3')
for i in range(9,38):paragraphs[i].decompose()
path.write_text(str(soup)+'\n')
(work/'qa').mkdir(exist_ok=True)
(work/'qa/source-selection.json').write_text(json.dumps({
    'source':'income/two_ways_to_build_a_world.docx',
    'retained':'Original title and Note to Reader, Introduction, eighteen chapters in five parts, Conclusion, Appendices A/B, selected references and source note.',
    'excluded':'Only the duplicated page-numbered contents list. No OutfinityGift brand or unrelated promotional appendix found.',
    'structure':'Converted plain paragraph headings to semantic h1/h2/h3 and stable chapter anchors before Romanian chunk translation.',
},indent=2)+'\n')
print('prepared',path)
