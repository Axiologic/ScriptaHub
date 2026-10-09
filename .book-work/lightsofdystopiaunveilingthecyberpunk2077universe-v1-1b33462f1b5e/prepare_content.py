from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/lightsofdystopiaunveilingthecyberpunk2077universe-v1-1b33462f1b5e')
source = Path('.book-work/income-pdf-candidates/1b33462f1b5e3c28/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 7, 9),
    ('soulkiller', 'Digital Eternity: The Promise and Peril of Soulkiller Technology', 10, 14),
    ('night-city', 'The Neon-Lit Dystopia of Night City', 15, 17),
    ('identity', 'Humanity Redefined: Technology and Identity', 18, 25),
    ('power', 'Power Dynamics in a Fragmented Society', 26, 29),
    ('experience', 'The Human Experience in a Cyberpunk World', 30, 38),
    ('conclusion', 'Conclusion', 39, 40),
    ('bibliography', 'Bibliography', 47, 47),
]
headings = {'Introduction', 'Chapter One', 'Chapter Two', 'Chapter Three', 'Chapter Four', 'Chapter Five', 'Conclusion', 'Bibliography'}
headings |= {label for _, label, _, _ in sections}
parts, records = [], []
for slug, label, first, last in sections:
    paragraphs = []
    for page in range(first, last + 1):
        node = soup.find('section', {'data-source-page': str(page)})
        assert node is not None, page
        for element in node.select('p'):
            value = re.sub(r'\s+', ' ', element.get_text(' ', strip=True)).strip()
            if not value or value in headings or value in {str(page), str(page - 1)}:
                continue
            if paragraphs and not re.search(r'[.!?][”"’\']?$', paragraphs[-1]) and not paragraphs[-1].endswith(':'):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    readable = []
    for value in paragraphs:
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', value)
        group = []
        for sentence in sentences:
            if group and sum(len(part.split()) for part in group) + len(sentence.split()) > 150:
                readable.append(' '.join(group))
                group = []
            group.append(sentence)
        if group:
            readable.append(' '.join(group))
    body = '\n'.join(f'<p>{escape(value)}</p>' for value in readable)
    parts.append(f'<section id="{slug}"><h2>{escape(label)}</h2>\n{body}\n</section>')
    records.append({'id': slug, 'pages': [first, last], 'paragraphs': len(readable), 'words': sum(len(p.split()) for p in readable)})
title = 'Lights of Dystopia: Unveiling the Cyberpunk 2077 Universe'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[7, 40], [47, 47]],
    'excludedPages': [[1, 6], [41, 46]],
    'reason': 'Keep substantive introduction, five chapters, conclusion, and bibliography; omit legacy rights, promotional preface, and non-substantive annex.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
