from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/exploringfreedomandserfdomonthepathtoliberty-v1-cb0e7d5d0457')
source = Path('.book-work/income-pdf-candidates/cb0e7d5d045767e5/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 7, 11),
    ('economic-freedom', 'Chapter I — Foundations of Economic Freedom', 12, 16),
    ('central-planning', 'Chapter II — The Dilemmas of Central Planning', 17, 22),
    ('decline-of-freedom', 'Chapter III — The Decline of Freedom', 23, 27),
    ('reclaiming-liberty', 'Chapter IV — Reclaiming Liberty: The Path Forward', 28, 32),
    ('conclusion', 'Conclusion — Freedom or Serfdom? The Paths of Liberty', 33, 37),
    ('bibliography', 'Bibliography', 46, 47),
]
headings = {
    'Introduction', 'Chapter I Foundations of Economic Freedom',
    'Chapter II The Dilemmas of Central Planning', 'Chapter III The Decline of Freedom',
    'Chapter IV Reclaiming Liberty: The Path Forward',
    'Conclusion Freedom or Serfdom? The Paths of Liberty', 'Bibliography',
}
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
            if (paragraphs and first != 46 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if first != 46:
        readable = []
        for paragraph in paragraphs:
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
title = 'Exploring Freedom and Serfdom on the Path to Liberty'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[7, 37], [46, 47]],
    'excludedPages': [[1, 6], [38, 45]],
    'reason': 'Retained the original introduction, four substantive chapters, conclusion and bibliography; excluded rights, promotional preface and retired author/project annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
