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
phrases = '''creation|responsibility|humour|central moral problem|living being|horror|abandonment|creature|survive|care|maker|conflict|scientific triumph|rejection|revenge|family and friends|biotechnology|creators|natural forces|alchemical writing|University of Ingolstadt|curiosity|obsession|life and death|family|friends|human body|experiment|scientific ambition|Geneva|language|human customs|belong|loneliness|anger|William|Justine|silence|injustice|companion|isolation|monstrosity|appearance|harmful acts|need for care|second creature|guilt|first creation|consequences|far from home|betrayal|wedding night|fear|possible harm|Elizabeth|victim|grief|Europe|Arctic|pursuit|companionship|peace|final encounter|chain of loss|act of creation|later choice|ambition|empathy|duties|new knowledge|making life|accepting responsibility|exclusion|cruelty|ethical consequences|powerful technologies|people affected|scientific responsibility|create life|learn|protect|teach|fears|promises|destroys|boundary|voice|moral problem|threat|understanding'''.split('|')
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
