from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

w = Path(__file__).resolve().parent
source = Path('.book-work/income-pdf-candidates/a7c72a5bac4407f1/clean-draft.html')
soup = BeautifulSoup(source.read_text(), 'html.parser')
sections = [
    ('introduction', 'Introduction', 8, 12),
    ('foundations', 'Chapter I — Foundations of Economic Thought', 13, 17),
    ('market-disruption', 'Chapter II — The Social Disruptions of the Market Economy', 18, 22),
    ('protective-responses', 'Chapter III — The Protective Responses to Market Forces', 23, 28),
    ('path-forward', 'Chapter IV — The Path Forward: Integrating Protection and Economic Freedom', 29, 34),
    ('conclusion', 'Conclusion', 35, 40),
    ('bibliography', 'Bibliography', 49, 49),
]
headings = {heading.replace(' — ', ' ') for _, heading, _, _ in sections} | {'Introduction','Conclusion','Bibliography'}
parts = []
records = []
for slug, heading, first, last in sections:
    paragraphs = []
    for page in range(first, last + 1):
        node = soup.find('section', {'data-source-page': str(page)})
        assert node is not None, page
        for element in node.select('p'):
            value = re.sub(r'\s+', ' ', element.get_text(' ', strip=True)).strip()
            if not value or value in headings or value in {str(page), str(page-1)}:
                continue
            if slug != 'bibliography' and paragraphs and not re.search(r'[.!?][”"’\']?$', paragraphs[-1]) and not paragraphs[-1].endswith(':'):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    readable = []
    for paragraph in paragraphs:
        if len(paragraph.split()) <= 135 or slug == 'bibliography':
            readable.append(paragraph)
            continue
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“*])', paragraph)
        group = []
        for sentence in sentences:
            if group and sum(len(x.split()) for x in group) + len(sentence.split()) > 135:
                readable.append(' '.join(group))
                group = []
            group.append(sentence)
        if group:
            readable.append(' '.join(group))
    records.append({'id': slug, 'pages': [first,last], 'paragraphs': len(readable), 'words': sum(len(x.split()) for x in readable)})
    parts.append('<section id="'+slug+'"><h2>'+escape(heading)+'</h2>\n' + '\n'.join('<p>'+escape(x)+'</p>' for x in readable) + '\n</section>')
title = 'Exploring The Great Transformation of Economic Thought'
html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>'+escape(title)+'</title></head><body><article>\n<h1>'+escape(title)+'</h1>\n<p class="byline">AI Agent Adria Morgan · 2024</p>\n'+'\n'.join(parts)+'\n</article></body></html>\n'
(w/'book/en/full_content.html').write_text(html)
(w/'qa').mkdir(exist_ok=True)
(w/'qa/source-selection.json').write_text(json.dumps({'source': str(source), 'sourceVersion':1, 'sourcePages':49, 'includedPages':[[8,40],[49,49]], 'excludedPages':[[1,7],[41,48]], 'reason':'Retained thematic introduction, four original chapters, conclusion and bibliography; excluded rights, contents, promotional preface, author/project annexes and OutfinityGift advertising.', 'sections':records}, indent=2)+'\n')
print(records)
