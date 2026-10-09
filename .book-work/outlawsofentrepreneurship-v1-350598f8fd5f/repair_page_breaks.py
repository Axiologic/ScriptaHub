"""Merge three PDF page-break paragraph splits and preserve finished RO chunks."""

import json
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
work = root / 'translations/ro/full'
source = root / 'book/en/full_content.html'
destination = root / 'book/ro/full_content.html'

old = {}
for path in sorted((work / 'chunks').glob('*.json')):
    for segment in json.loads(path.read_text(encoding='utf-8'))['segments']:
        old[segment['source']] = segment['translation']
assert old and all(old.values())

groups = [
    ('If there’s one constant in the world of entrepreneurship', 3),
    ('As we come to the end of our exploration into the world of entrepreneurship', 2),
]
merged_translations = {}
for start, count in groups:
    soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
    first = next(p for p in soup.article.find_all('p', recursive=False) if p.get_text(' ', strip=True).startswith(start))
    parts = [first]
    for _ in range(count - 1):
        nxt = parts[-1].find_next_sibling()
        assert nxt and nxt.name == 'p'
        parts.append(nxt)
    source_parts = [p.get_text(' ', strip=True) for p in parts]
    translation = ' '.join(old[s] for s in source_parts)
    merged_source = ' '.join(source_parts)
    merged_translations[merged_source] = translation
    first.string = merged_source
    for item in parts[1:]:
        item.decompose()
    source.write_text(str(soup) + '\n', encoding='utf-8')

command = [
    'python3', 'tools/html_translation_chunks.py', 'prepare', str(source),
    '--language', 'ro', '--destination', str(destination), '--workdir', str(work), '--force',
]
subprocess.run(command, check=True)
missing = []
for path in sorted((work / 'chunks').glob('*.json')):
    data = json.loads(path.read_text(encoding='utf-8'))
    for segment in data['segments']:
        segment['translation'] = old.get(segment['source']) or merged_translations.get(segment['source'], '')
        if not segment['translation']:
            missing.append(segment['id'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
assert not missing, missing
subprocess.run(['python3', 'tools/html_translation_chunks.py', 'check', str(work)], check=True)
subprocess.run(['python3', 'tools/html_translation_chunks.py', 'assemble', str(work), '--force'], check=True)
(root / 'qa/page-break-repair.json').write_text(json.dumps({
    'reason': 'PDF page-break extraction split three sentences across paragraphs.',
    'mergedSourceSegments': [['t000016', 't000017', 't000018'], ['t000020', 't000021']],
    'translationsPreserved': True,
}, indent=2) + '\n', encoding='utf-8')
