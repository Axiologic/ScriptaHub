from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json, re

root = Path('.book-work/toswipeornottoswipehamletsdilemma-v1-3525e277956a')
source = Path('.book-work/income-pdf-candidates/3525e277956a66ac/clean-draft.html')
soup = BeautifulSoup(source.read_text(), 'html.parser')
sections = [
    ('relevance', 'Chapter One — To Be or Not to Be... Relevant?', 10, 14),
    ('madness-or-marketing', 'Chapter Two — Madness or Marketing?', 15, 19),
    ('hamletonomics', 'Chapter Three — Hamletonomics: The Revenge Economy', 20, 24),
    ('hamlet-2', 'Chapter Four — Hamlet 2.0: The Upgrade Tragedy Needed', 25, 29),
    ('conclusion', 'Conclusion', 30, 33),
]
headings = {'Chapter One', 'To Be or Not to Be... Relevant?', 'Chapter Two', 'Madness or Marketing?', 'Chapter Three', 'Hamletonomics: The Revenge Economy', 'Chapter Four', 'Hamlet 2.0: The Upgrade Tragedy Needed', 'Conclusion'}
records = []
html_sections = []
for sid, label, start, end in sections:
    paras = []
    for page in range(start, end + 1):
        node = soup.find('section', attrs={'data-source-page': str(page)})
        assert node, page
        texts = [p.get_text(' ', strip=True) for p in node.find_all('p')]
        texts = [t for t in texts if t not in headings | {str(page)}]
        for i, t in enumerate(texts):
            if i == 0 and paras and not re.search(r'[.!?][”\'\"]?$', paras[-1]):
                paras[-1] += ' ' + t
            else:
                paras.append(t)
    records.append({'id': sid, 'pages': [start, end], 'paragraphs': len(paras), 'words': sum(len(p.split()) for p in paras)})
    html_sections.append('<section id="%s"><h2>%s</h2>\n%s\n</section>' % (sid, escape(label), '\n'.join('<p>%s</p>' % escape(p) for p in paras)))
title = 'To Swipe or Not to Swipe: Hamlet’s Dilemma'
html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>%s</title></head><body><article>\n<h1>%s</h1>\n' % (escape(title), escape(title)) + '\n'.join(html_sections) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(html)
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({'source': str(source), 'includedPages': [10, 33], 'excludedPages': [[1, 9], [34, 41]], 'reason': 'Four substantive chapters and conclusion retained; rights pages, promotional preface, author/project annex and bibliography excluded.', 'sections': records}, indent=2) + '\n')
print(records)
