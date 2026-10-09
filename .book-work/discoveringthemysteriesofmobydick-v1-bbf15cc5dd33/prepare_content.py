from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json, re

root = Path('.book-work/discoveringthemysteriesofmobydick-v1-bbf15cc5dd33')
source = Path('.book-work/income-pdf-candidates/bbf15cc5dd33b83e/clean-draft.html')
if not source.exists():
    source = next(Path('.book-work/income-pdf-candidates').glob('bbf15cc5dd33*/clean-draft.html'))
soup = BeautifulSoup(source.read_text(), 'html.parser')
sections = [
    ('introduction', 'Introduction', 7, 10),
    ('sailing-into-the-unknown', 'Chapter One — Sailing into the Unknown', 11, 14),
    ('the-cost-of-obsession', 'Chapter Two — The Cost of Obsession', 15, 18),
    ('defying-the-waves', 'Chapter Three — Defying the Waves', 19, 23),
    ('natures-fury', 'Chapter Four — Nature’s Fury', 24, 28),
    ('conclusion', 'Conclusion', 29, 31),
]
headings = {'INTRODUCTION', 'CHAPTER ONE', 'Sailing into the Unknown', 'CHAPTER TWO', 'The Cost of Obsession', 'CHAPTER THREE', 'Defying the Waves', 'CHAPTER FOUR', "Nature's Fury", 'CONCLUSION'}
records = []
html_sections = []
for sid, label, start, end in sections:
    paras = []
    for page in range(start, end + 1):
        node = soup.find('section', attrs={'data-source-page': str(page)})
        assert node, page
        texts = [p.get_text(' ', strip=True) for p in node.find_all('p')]
        texts = [t for t in texts if t not in headings and t != str(page)]
        for idx, t in enumerate(texts):
            if idx == 0 and paras and not re.search(r'[.!?][”\'\"]?$', paras[-1]):
                paras[-1] += ' ' + t
            else:
                paras.append(t)
    records.append({'id': sid, 'sourcePages': [start, end], 'paragraphs': len(paras), 'words': sum(len(p.split()) for p in paras)})
    html_sections.append('<section id="%s"><h2>%s</h2>\n%s\n</section>' % (sid, escape(label), '\n'.join('<p>%s</p>' % escape(p) for p in paras)))
html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Discovering the Mysteries of Moby Dick</title></head><body><article>\n<h1>Discovering the Mysteries of Moby Dick</h1>\n' + '\n'.join(html_sections) + '\n</article></body></html>\n'
(root/'book/en/full_content.html').write_text(html)
(root/'qa').mkdir(exist_ok=True)
(root/'qa/source-selection.json').write_text(json.dumps({'source': str(source), 'includedPages': [7,31], 'excludedPages': [[1,6],[32,38]], 'reason': 'Four substantive chapters, introduction and conclusion retained; promotional preface, front matter and annex/bibliography excluded.', 'sections': records}, indent=2) + '\n')
print(records)
