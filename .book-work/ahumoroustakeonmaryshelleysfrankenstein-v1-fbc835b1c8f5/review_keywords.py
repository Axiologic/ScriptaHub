import hashlib
import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, 'tools')
from build_books import keyword_normalise

root=Path(__file__).parent
p=root/'book/manifest.json'
d=json.loads(p.read_text())
source=root/'book/en/short_content.html'
text=keyword_normalise(BeautifulSoup(source.read_text(),'html.parser').get_text(' ',strip=True))
phrases=[
 'Shelley’s novel', 'Victor Frankenstein', 'William Frankenstein', 'Justine', 'Henry Clerval',
 'Robert Walton', 'De Lacey cottage', 'Felix', 'Agatha', 'Safie',
 'University of Ingolstadt', 'Geneva', 'Alps', 'Scottish island', 'Arctic',
 'gothic novel', 'comic voice', 'comic narration', 'comic comparisons', 'humor',
 'underlying pattern', 'gothic', 'television, pop culture', 'pop culture', 'macabre arts and crafts',
 'creation', 'abandonment', 'responsibility', 'scientific ambition', 'scientific hubris',
 'secret of life', 'laboratory', 'body parts', 'electrical contraption', 'animate them',
 'yellow eyes', 'sentient creation', 'newborn mind', 'adult body', 'creator',
 'duty', 'younger brother William', 'family servant Justine', 'moral silence', 'wrongly accused',
 'wrongly accused and executed', 'female companion', 'away from humanity', 'rejection', 'rage',
 'creature’s experience', 'human feeling', 'language', 'appearance', 'attempts to belong',
 'companionship', 'blind father', 'saves a girl', 'frightened father', 'framing of an innocent woman',
 'innocent woman', 'moral problem', 'independent being', 'unfinished work', 'wedding night',
 'revenge', 'grief', 'pursuit', 'remorse', 'explorer Robert Walton',
 'lives lost', 'harmful choices', 'evil monster', 'final encounter', 'ethical relevance',
 'unchecked scientific ambition', 'loneliness', 'capacity to feel', 'seek connection', 'understanding an injury',
 'genetic engineering', 'serious questions', 'ethical prompts', 'far-reaching effects', 'moment of invention',
 'experiments and creations', 'analogies', 'invention', 'consequences', 'care',
]
assert len(phrases)==90,len(phrases)
assert len({keyword_normalise(x) for x in phrases})==90
bad=[x for x in phrases if keyword_normalise(x) not in text]
assert not bad,bad
d['keywordReview']={'sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'phrases':phrases}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Reviewed',len(phrases),'phrases')
