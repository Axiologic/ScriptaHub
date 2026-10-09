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
phrases = '''covert action|speculation|institutional misconduct|secret experiments|digital media|secrecy|hidden coordination|recorded event|accusation|reported meeting|corporate and state power|opioid epidemic|aggressive marketing|pharmaceutical firms|prescribing practices|private prisons|financial incentives|rehabilitation|fair punishment|lobbying|influence over policy|political process|public purpose|Edward Snowden’s disclosures|large-scale surveillance|corporate ties to war|Operation Snow White|government information|infiltration|private aims|institutional access|forced sterilization|medical and state authority|biological weapons testing|exposure to hazards|USS Liberty|contested interpretations|MKUltra|Project Sunshine|poisoning of industrial alcohol|Prohibition|official cover-ups|official explanations|Gulf of Tonkin incident|evidence used to justify war|Watergate|illegal political activity|investigation|disclosure|public record|secret research|violence|political deception|transparency|independent scrutiny|accountability|data collection|Cambridge Analytica|personal data|political profiles|target messages|Russian interference|U.S. elections|targeted advertising|Brexit referendum|online quizzes|health tests|intelligence tests|personal information|small disclosures|false or misleading stories|public opinion|platform design|organized campaigns|Fellowship|religious network|political figures|Freemasonry|fraternal network|historical study|Illuminati|historical fact|modern legend|Opus Dei|Skull and Bones|restricted membership|private practices|elite relationships|membership list|coordinated plot'''.split('|')
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
