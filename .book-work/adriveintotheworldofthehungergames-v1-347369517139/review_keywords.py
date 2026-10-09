import hashlib
import importlib.util
import json
from pathlib import Path

workspace = Path(__file__).parent
manifest_path = workspace / 'book/manifest.json'
source = workspace / 'book/en/short_content.html'
spec = importlib.util.spec_from_file_location('build_books', 'tools/build_books.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
phrases = '''Panem|wealthy Capitol|poorer districts|fear|scarcity|annual televised contest|children|survival|Katniss|protection|private act of protection|public challenge|politics|social structure|technology|popular culture|spectacle|resist|books and films|dystopian fiction|reluctant resistance|Mockingjay|hope|rebellion|inequality|violence as entertainment|control|fan discussion|prequel|original trilogy|power|oppression|sacrifice|weapons|defeated rebellion|competition|solidarity|Prim|arena|compassion|brutality|moral problem|compulsory terror|fellow children|refuse to surrender|environmental disaster|war|collapse|rigid district system|wealth|information|economic roles|work|District 13|annual reaping|punishment|history|regime|geography|labour|hunger|controlled memory|political power|suffering|entertainment|terror|Tributes|alliances|acts of care|obedience|deprivation|dignity|engineered contest|coercion|human life|surveillance|broadcast spectacle|medical interventions|engineered creatures|muttations|uneven access|technical power|Capitol luxury|district hardship|monitor|communications|practical knowledge|resistance|institutions|moral choice'''.split('|')
norm = module.keyword_normalise(module.keyword_source_text(source))
shelf = {module.keyword_normalise(label).strip() for localized in module.SHELF_CATEGORIES.values() for label in localized['en'].split('|')}
missing = [phrase for phrase in phrases if module.keyword_normalise(phrase) not in norm]
invalid = [phrase for phrase in phrases if module.keyword_normalise(phrase).strip() in shelf]
print('count', len(phrases), 'distinct', len(set(phrases)), 'missing', missing, 'shelf', invalid)
if len(phrases) != 90 or len(set(phrases)) != 90 or missing or invalid:
    raise SystemExit(1)
manifest = json.loads(manifest_path.read_text())
manifest['keywordReview'] = {
    'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(),
    'phrases': phrases,
    'status': 'reviewed-source-grounded',
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
