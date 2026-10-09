from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/adriveintotheworldofthehungergames-v1-347369517139')
source = Path('.book-work/income-pdf-candidates/347369517139e4a7/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 8, 10),
    ('pop-culture', 'Chapter One — How The Hunger Games Shaped Pop Culture', 11, 12),
    ('survival', 'Chapter Two — The Dynamics of Survival: Power, Oppression and Sacrifice', 13, 17),
    ('panem', 'Chapter Three — The Rise of Panem: History and Society', 18, 24),
    ('human-condition', 'Chapter Four — The Human Condition in Panem', 25, 30),
    ('technology', 'Chapter Five — Science and Technology in Panem', 31, 37),
    ('plot', 'Chapter Six — Key Events and Plot Summaries', 38, 39),
    ('conclusion', 'Conclusion', 40, 40),
    ('bibliography', 'Bibliography', 48, 48),
]
headings = {'Introduction', 'Conclusion', 'Bibliography',
            'Chapter One How The Hunger Games Shaped Pop Culture?',
            'Chapter Two The Dynamics of Survival: Power, Oppression and Sacrifice',
            'Chapter Three The Rise of Panem: History and Society',
            'Chapter Four The Human Condition in Panem',
            'Chapter Five Science and Technology in Panem',
            'Chapter Six Key Events and Plot Summaries'}
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
title = 'A Drive into the World of The Hunger Games'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[8, 40], [48, 48]],
    'excludedPages': [[1, 7], [41, 47]],
    'reason': 'Retained the original introduction, six chapters, conclusion and bibliography; excluded rights, promotional preface and retired author/project annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
