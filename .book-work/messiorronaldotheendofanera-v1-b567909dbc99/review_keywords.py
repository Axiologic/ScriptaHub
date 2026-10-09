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
phrases = '''football era|goals|honours|greatest|training|teams|adaptation|exceptional players|early talent|Rosario|Argentina|growth hormone deficiency|professional career|Barcelona|La Masia academy|treatment|Madeira|Portugal|Sporting Lisbon|Manchester United|physical training|relentless improvement|intuitive creator|self-made athlete|ways of playing|wing|creative role|dribbling|passing|positioning|vision|tempo|playmaking|team style|young winger|pace|footwork|finishing|headers|powerful shots|different positions|England|Spain|Italy|individual performance|attacking football|defend|train|compete|La Liga|Real Madrid|Ballon d'Or awards|league records|sustained expectation|modern football|assists|decisive moment|global figures|sponsorship|media|philanthropy|young footballers|humility|team play|fitness|personal branding|discipline|charitable work|aspiring players|practice|persistence|pressure|creativity|close control|athleticism|versatility|trophies|statistics|international achievements|clubs and leagues|teammates|simple ranking|winner|contrasting players|extraordinary period|shared legacy|debate|chance|space|comparison'''.split('|')
norm = module.keyword_normalise(module.keyword_source_text(source))
missing = [phrase for phrase in phrases if module.keyword_normalise(phrase) not in norm]
print('count', len(phrases), 'distinct', len(set(phrases)), 'missing', missing)
if len(phrases) != 90 or len(set(phrases)) != 90 or missing:
    raise SystemExit(1)
manifest = json.loads(manifest_path.read_text())
manifest['keywordReview'] = {
    'sourceHash': hashlib.sha256(source.read_bytes()).hexdigest(),
    'phrases': phrases,
    'status': 'reviewed-source-grounded',
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
