import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0,'tools')
from build_books import keyword_normalise, keyword_source_text, SHELF_CATEGORIES
root=Path('.book-work/themetamorphosesofdonquixotethroughtimeandspace-v1-93ced8a152d1/book')
source=root/'en/short_content.html';path=root/'manifest.json';m=json.loads(path.read_text())
phrases=[
 'imagined versions','ruined landscapes','modern city','virtual reality','space',
 'speculative retellings','Cervantes','unreasonable hope','different futures',
 'fantasy','heroism','wasteland','ruined cities','scarce resources',
 'old books','knights','survival','armor from scrap','battered bicycle',
 'Rocinante','food','repair tires','abandoned wind turbine','dragon',
 'comic and painful','honor','innocent people','imagining a future',
 'crowded city','retired librarian','comic books','superhero films','improvised mask',
 'cape','shield','toy sword','urban vigilante','corrupt politicians',
 'business interests','construction work','heroic frame','former police officer',
 'taxi','wish for justice','world gone mad','year 2099','war',
 'environmental collapse','imagined monsters','caution','human need to hope',
 'side of the story','squire','former mechanic','finds supplies','negotiates with strangers',
 'loyalty','friendship','virtual knight','immersive game','headset',
 'controllers','haptic suit','virtual danger','actual city','security guard',
 'virtual heroism','public space','chivalric books','digital experience',
 'imagination','cosmic knight','space adventure','former astronaut','worn starship',
 'spacesuit','galaxy','noble missions','practical judgment','machinery',
 'mythic forms','dangerous','exploration','belief','material demands',
 'absurd','persistence','ideals','the road','the danger',
]
text=keyword_normalise(keyword_source_text(source))
shelf={keyword_normalise(label).strip() for localized in SHELF_CATEGORIES.values() for label in localized['en'].split('|')}
missing=[p for p in phrases if keyword_normalise(p) not in text]
collisions=[p for p in phrases if keyword_normalise(p).strip() in shelf]
print('count',len(phrases),'distinct',len(set(phrases)),'missing',missing,'shelf',collisions)
if len(phrases)!=90 or len(set(phrases))!=90 or missing or collisions:raise SystemExit(1)
m['keywordReview']={'sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'phrases':phrases}
path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
