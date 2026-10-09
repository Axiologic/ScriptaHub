from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/aglimpseintofrankherbertsdune-v1-2256feba217c')
source = Path('.book-work/income-pdf-candidates/2256feba217c7410/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 8, 9),
    ('philosophy', 'Chapter One — The Philosophical Foundations of Dune', 10, 12),
    ('anthropology', 'Chapter Two — Anthropological Aspects in Dune', 13, 15),
    ('religion', 'Chapter Three — Religion and Myth-Making in Shaping Civilizations', 16, 17),
    ('science', 'Chapter Four — Science and Technology in the Dune Universe', 18, 22),
    ('society', 'Chapter Five — Societal Structures and Political Systems', 23, 27),
    ('factions', 'Chapter Six — Key Factions and Organizations', 28, 32),
    ('saga', 'Chapter Seven — Key Events and Developments Across the Saga', 33, 38),
    ('plot', 'Chapter Eight — Key Events and Plot Summaries', 39, 45),
    ('themes', 'Chapter Nine — Themes and Literary Analysis', 46, 51),
    ('legacy', 'Chapter Ten — Legacy and Influence of Dune', 52, 56),
    ('conclusion', 'Conclusion', 57, 57),
    ('bibliography', 'Bibliography', 65, 65),
]
headings = {'Introduction', 'Conclusion', 'Bibliography',
            'Chapter One The Philosophical Foundations of Dune',
            'Chapter Two', 'Anthropological Aspects in Dune',
            'Chapter Three', 'Religion and Myth-Making in Shaping Civilizations',
            'Chapter Four', 'Science and Technology in the Dune Universe',
            'Chapter Five', 'Societal Structures and Political Systems',
            'Chapter Six', 'Key Factions and Organizations',
            'Chapter Seven', 'Key Events and Developments Across the Saga',
            'Chapter Eight', 'Key Events and Plot Summaries',
            'Chapter Nine', 'Themes and Literary Analysis',
            'Chapter Ten', 'Legacy and Influence of Dune'}
parts = []
records = []
for slug, label, first, last in sections:
    paragraphs = []
    for page in range(first, last + 1):
        node = soup.find('section', {'data-source-page': str(page)})
        assert node is not None, page
        for element in node.select('p'):
            value = re.sub(r'\s+', ' ', element.get_text(' ', strip=True)).strip()
            value = value.replace('create goals (clones with restored memories)', 'create gholas (clones with restored memories)')
            if not value or value in headings or value in {str(page), str(page - 1)}:
                continue
            if (paragraphs and first != 65 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if first != 65:
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
title = 'A Glimpse into Frank Herbert’s Dune'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[8, 57], [65, 65]],
    'excludedPages': [[1, 7], [58, 64]],
    'reason': 'Retained the original introduction, ten analytical chapters, conclusion and bibliography; excluded rights, promotional preface and retired author/project annexes. Corrected source typo goals to gholas for the Dune clone term.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
