from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/sg1universe-v1-bfc743ba8543')
source = Path('.book-work/income-pdf-candidates/bfc743ba85436494/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 8, 11),
    ('anthropology', 'Chapter One — Anthropological Aspects', 12, 16),
    ('science', 'Chapter Two — A Bridge Between Ancient and Modern Science', 17, 21),
    ('governance', 'Chapter Three — Galactic Governance in the Stargate Universe', 22, 33),
    ('adventures', 'Chapter Four — Epic Adventures of SG-1', 34, 38),
    ('conclusion', 'Conclusion', 39, 40),
    ('bibliography', 'Bibliography', 47, 47),
]
headings = {'Introduction', 'Chapter One', 'Anthropological Aspects', 'Chapter Two',
            'A Bridge Between Ancient and Modern Science', 'Chapter Three',
            'Galactic Governance in the Stargate Universe', 'Chapter Four',
            'Epic adventures SG-1', 'Conclusion', 'Bibliography'}
parts = []
records = []
for slug, label, first, last in sections:
    paragraphs = []
    for page in range(first, last + 1):
        node = soup.find('section', {'data-source-page': str(page)})
        assert node is not None, page
        for element in node.select('p'):
            value = re.sub(r'\s+', ' ', element.get_text(' ', strip=True)).strip()
            if not value or value in headings or value in {str(page), str(page - 1)}:
                continue
            if (paragraphs and first != 47 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if first != 47:
        readable = []
        for paragraph in paragraphs:
            if len(paragraph.split()) <= 140:
                readable.append(paragraph)
                continue
            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', paragraph)
            group = []
            for sentence in sentences:
                if group and sum(len(item.split()) for item in group) + len(sentence.split()) > 140:
                    readable.append(' '.join(group))
                    group = []
                group.append(sentence)
            if group:
                readable.append(' '.join(group))
        paragraphs = readable
    records.append({'id': slug, 'pages': [first, last], 'paragraphs': len(paragraphs), 'words': sum(len(p.split()) for p in paragraphs)})
    body = '\n'.join(f'<p>{escape(p)}</p>' for p in paragraphs)
    parts.append(f'<section id="{slug}"><h2>{escape(label)}</h2>\n{body}\n</section>')
title = 'SG 1 Universe'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[8, 40], [47, 47]],
    'excludedPages': [[1, 7], [41, 46]],
    'reason': 'Retained original introduction, four substantive chapters, conclusion and bibliography; excluded promotional preface, rights and retired OutfinityGift annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
