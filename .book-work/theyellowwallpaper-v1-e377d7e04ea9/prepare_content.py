from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/theyellowwallpaper-v1-e377d7e04ea9')
source = Path('.book-work/income-pdf-candidates/e377d7e04ea9eb5f/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('modern-perspective', 'Modern Perspective: Charlotte Perkins Gilman', 7, 8),
    ('historical-context', 'Historical and Cultural Context', 9, 12),
    ('main-characters', 'Main Characters', 13, 16),
    ('narrative-threads', 'Plot Summary by Narrative Threads', 17, 20),
    ('original-story', 'The Yellow Wallpaper — Original Story', 21, 42),
]
headings = {
    'Preface', 'Modern Perspective', 'Historical and Cultural Context',
    'Main Characters', 'Plot Summary by Narrative Threads', 'Original book',
    'The Yellow Wallpaper', 'By Charlotte Perkins Gilman',
}
subheadings = {
    'About Charlotte Perkins Gilman', 'The Narrator (Unnamed Woman)', 'John',
    'Jennie', 'The Protagonist’s Mental Health and Isolation',
    'The Husband’s Control and Dismissal of Her Experiences',
    'The Narrator’s Breakdown and Liberation', 'Conclusion',
}
parts = []
records = []
for slug, label, first, last in sections:
    paragraphs = []
    for page in range(first, last + 1):
        page_node = soup.find('section', {'data-source-page': str(page)})
        assert page_node is not None, page
        texts = [p.get_text(' ', strip=True) for p in page_node.select('p')]
        for text in texts:
            if text in headings or text in {str(page), str(page - 1)}:
                continue
            if text.startswith('About Charlotte Perkins Gilman '):
                text = text[len('About Charlotte Perkins Gilman '):]
            if text in subheadings:
                paragraphs.append(('h3', text))
                continue
            if (paragraphs and paragraphs[-1][0] == 'p'
                    and not re.search(r'[.!?][”"’\']?$', paragraphs[-1][1])
                    and not paragraphs[-1][1].endswith(':')):
                paragraphs[-1] = ('p', paragraphs[-1][1] + ' ' + text)
            else:
                paragraphs.append(('p', text))
    body = '\n'.join(f'<{tag}>{escape(text)}</{tag}>' for tag, text in paragraphs)
    parts.append(f'<section id="{slug}"><h2>{escape(label)}</h2>\n{body}\n</section>')
    records.append({'id': slug, 'pages': [first, last], 'paragraphs': len([1 for tag, _ in paragraphs if tag == 'p']), 'words': sum(len(text.split()) for tag, text in paragraphs if tag == 'p')})
title = 'The Yellow Wallpaper'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{title}</title></head><body><article>\n<h1>{title}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [7, 42],
    'excludedPages': [[1, 6], [43, 46]],
    'reason': 'The contextual analysis and complete Gilman story are preserved; legacy rights notices, table of contents, promotional preface and project/author annexes are excluded.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
