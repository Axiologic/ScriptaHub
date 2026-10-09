import hashlib
import importlib.util
import json
from pathlib import Path

w = Path(__file__).parent
source = w / 'book/en/short_content.html'
manifest_path = w / 'book/manifest.json'
spec = importlib.util.spec_from_file_location('build_books', 'tools/build_books.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
phrases = '''Arrakis|desert planet|spice melange|interstellar navigation|galactic civilization|spice|ecology|literary legacy|Paul Atreides|prescience|possible futures|Golden Path|humanity’s survival|free will|leadership|moral cost|Fremen|water|shared resource|stillsuits|bodily moisture|spiritual beliefs|scarcity|desert’s ecology|sandworms|spice cycle|cultural adaptation|practical skills|demanding environment|Bene Gesserit|Missionaria Protectiva|breeding program|Kwisatz Haderach|prophecy|political force|spiritual experience|manipulation of faith|community’s hopes|Butlerian Jihad|thinking machines|human mind|Mentats|analytical abilities|Guild Navigators|spice-induced prescience|biological engineering|Tleilaxu|gholas|extreme environments|technological development|human potential|dependence on tools|economic life|Great Houses|Padishah Emperor|Sardaukar|balance of power|House Atreides|House Harkonnen|political practices|Spacing Guild|transport monopoly|CHOAM|wealth|imperial influence|control of Arrakis|factions|loyalty|scarce resources|resource scarcity|series’ conflicts|Paul’s ascent|jihad|Leto II’s long rule|Scattering|Old Empire|original six novels|continuations|genetic manipulation|ecological change|shifting factions|survival|personal decisions|civilizations|multiple viewpoints|invented terms|chapter epigraphs|environmental thinking|foreseeing danger|control the future'''.split('|')
norm = b.keyword_normalise(b.keyword_source_text(source))
shelf = {b.keyword_normalise(label).strip() for localized in b.SHELF_CATEGORIES.values() for label in localized['en'].split('|')}
missing = [p for p in phrases if b.keyword_normalise(p) not in norm]
invalid = [p for p in phrases if b.keyword_normalise(p).strip() in shelf]
print('count', len(phrases), 'distinct', len(set(phrases)), 'missing', missing, 'shelf', invalid)
if len(phrases) != 90 or len(set(phrases)) != 90 or missing or invalid:
    raise SystemExit(1)
m = json.loads(manifest_path.read_text())
m['keywordReview'] = {'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(), 'phrases': phrases, 'status': 'reviewed-source-grounded'}
manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
