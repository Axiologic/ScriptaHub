from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/echoesfrombeyondtheveil-v1-49afb53aab7f')
source = Path('.book-work/income-pdf-candidates/49afb53aab7fa57e/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('utopia', 'Chapter One — Utopia', 8, 12),
    ('fractured-mirror', 'Chapter Two — The Fractured Mirror', 13, 20),
    ('whispers', 'Chapter Three — Whispers', 21, 29),
    ('beyond', 'Chapter Four — Beyond', 30, 38),
]
headings = {'Chapter One', 'Utopia', 'Chapter Two', 'The Fractured Mirror',
            'Chapter Three', 'Whispers', 'Chapter Four', 'Beyond'}
parts = []
records = []
for slug, label, first, last in sections:
    paragraphs = []
    for page in range(first, last + 1):
        page_node = soup.find('section', {'data-source-page': str(page)})
        assert page_node is not None, page
        for p in page_node.select('p'):
            text = p.get_text(' ', strip=True)
            if text in headings or text in {str(page), str(page - 1)}:
                continue
            if (paragraphs and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + text
            else:
                paragraphs.append(text)
    records.append({'id': slug, 'pages': [first, last], 'paragraphs': len(paragraphs), 'words': sum(len(p.split()) for p in paragraphs)})
    body = '\n'.join(f'<p>{escape(p)}</p>' for p in paragraphs)
    parts.append(f'<section id="{slug}"><h2>{escape(label)}</h2>\n{body}\n</section>')
title = 'Echoes from Beyond the Veil'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [8, 38],
    'excludedPages': [[1, 7], [39, 47]],
    'reason': 'Four complete original fiction chapters retained; promotional preface, retired legal/project chapter and author/project annexes excluded.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
