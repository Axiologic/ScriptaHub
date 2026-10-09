from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/aneweraoffinancethebitcoinstandard-v1-e70048434442')
source = Path('.book-work/income-pdf-candidates/e70048434442e8fb/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('metamorphosis', 'Chapter I — The Metamorphosis of Money', 12, 17),
    ('strange-money-history', 'Chapter II — Strange Money History', 18, 23),
    ('precious-metals', 'Chapter III — The Significance of Precious Metals', 24, 29),
    ('fiat-currency', 'Chapter IV — The Impact of Fiat Currency', 30, 35),
    ('conclusion', 'Conclusion — The Metamorphosis of Money', 36, 39),
    ('bibliography', 'Bibliography', 48, 48),
]
headings = {'Chapter I The Metamorphosis of Money', 'Chapter II Strange Money History',
            'Chapter III The Significance of Precious Metals', 'Chapter IV The Impact of Fiat Currency',
            'CONCLUSION The Metamorphosis of Money', 'Bibliography'}
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
            if (paragraphs and first != 48 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if first != 48:
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
title = 'A New Era of Finance: The Bitcoin Standard'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[12, 39], [48, 48]],
    'excludedPages': [[1, 11], [40, 47]],
    'reason': 'Retained four substantive chapters, conclusion and bibliography; excluded rights, promotional preface/introduction and retired author/project annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
