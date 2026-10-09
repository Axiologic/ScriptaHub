from hashlib import sha256
from html import escape
from pathlib import Path
import json
import re
import subprocess

root = Path('.book-work/theinventionoftheinternetacomprehensiveoverview-v1-6b57770a1fc5')
pdf = root / 'content.pdf'
pages = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-']).decode().split('\f')
assert len(pages) - 1 == 51

sections = {
 8: ('introduction', 'Introduction', 1),
 10: ('chapter-1', 'Chapter 1 — Disconnected: Envisioning Life Without the Internet', 3),
 14: ('chapter-2', 'Chapter 2 — The Pioneers of the Internet', 2),
 22: ('chapter-3', 'Chapter 3 — The Collaborative Nature of Innovation', 3),
 24: ('chapter-4', 'Chapter 4 — The Birth of ARPANET', 2),
 28: ('chapter-5', 'Chapter 5 — Evolution and Expansion', 2),
 32: ('chapter-6', 'Chapter 6 — The Purpose Behind the Internet', 2),
 40: ('chapter-7', 'Chapter 7 — Challenges and Future Directions', 2),
 43: ('conclusion', 'Conclusion', 1),
 50: ('bibliography', 'Bibliography', 1),
}
selected = list(range(8, 27)) + list(range(28, 44)) + [50, 51]
blocks = []
current = []
names = re.compile(r'^(?:J\.C\.R\. Licklider|Paul Baran|Donald Davies|Leonard Kleinrock|Vint Cerf) \(\d{4}-')
bib_starts = ('Abbate,', 'Baran,', 'Berners-Lee,', 'Bolt Beranek', 'Cerf,', 'Clark,',
              'Hafner,', 'Leiner,', 'Licklider,', 'Lukasik,')
for page_number in selected:
    if page_number in sections:
        if current:
            blocks.append(('p', ' '.join(current)))
            current = []
        slug, label, skip = sections[page_number]
        blocks.append(('h2', slug, label))
    else:
        skip = 0
    lines = [line for line in pages[page_number - 1].splitlines() if line.strip()]
    lines = [line for line in lines if not re.fullmatch(r'\d+', line.strip())]
    lines = lines[skip:]
    for line in lines:
        content = re.sub(r'\s+', ' ', line.strip())
        indent = len(line) - len(line.lstrip())
        if names.match(content):
            if current:
                blocks.append(('p', ' '.join(current)))
                current = []
            blocks.append(('h3', content))
            continue
        new_paragraph = (content.startswith(bib_starts) if page_number >= 50 else indent >= 7)
        if new_paragraph and current:
            blocks.append(('p', ' '.join(current)))
            current = []
        current.append(content)
if current:
    blocks.append(('p', ' '.join(current)))

# The delivered PDF repeats the final TCP/IP paragraph of page 26 on page 27.
# Page 29 also starts a sentence mid-word, and three source text-layer words
# are visibly corrupted. Record these minimal editorial repairs in QA.
repairs = {
    'Protocol/Internet Protocol (TCP/IP) by Vint Cerf and Bob Kahn in the mid-1970s.':
      'The development of Transmission Control Protocol/Internet Protocol (TCP/IP) by Vint Cerf and Bob Kahn in the mid-1970s.',
    'timetners': 'partners',
    'timevents': 'events',
    'caInternetes': 'capabilities',
}
for index, block in enumerate(blocks):
    if block[0] != 'p':
        continue
    content = block[1]
    for old, new in repairs.items():
        content = content.replace(old, new)
    blocks[index] = ('p', content)

title = 'The Invention of the Internet: A Comprehensive Overview'
body = [f'<h1 id="book-title">{escape(title)}</h1>', '<p class="book-byline">AI Agent Althea Zappa</p>']
for block in blocks:
    if block[0] == 'h2':
        body.append(f'<h2 id="{block[1]}">{escape(block[2])}</h2>')
    elif block[0] == 'h3':
        body.append(f'<h3>{escape(block[1])}</h3>')
    else:
        body.append(f'<p>{escape(block[1])}</p>')
html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" '
        'content="width=device-width,initial-scale=1"/><title>' + escape(title) + '</title></head><body>'
        '<article data-reader-content>' + '\n'.join(body) + '</article></body></html>\n')
destination = root / 'book/en/full_content.html'
destination.write_text(html)
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/The_Invention_of_the_Internet___A_Comprehensive_Overview/content.pdf',
    'retainedPdfPages': selected,
    'excludedPdfPages': list(range(1,8)) + [27] + list(range(44,50)),
    'editorialRepairs': {'duplicateParagraph': 'PDF p.27 repeats the final TCP/IP paragraph of p.26; retain p.26 only', 'sourceTextLayer': repairs},
    'sections': [{'id':v[0],'title':v[1],'page':k} for k,v in sections.items()],
    'readerWords': len(' '.join(b[1] for b in blocks if b[0]=='p').split()),
    'sourceSha256': sha256(pdf.read_bytes()).hexdigest(),
}, indent=2) + '\n')
print(destination,'paragraphs',sum(b[0]=='p' for b in blocks),'words',len(' '.join(b[1] for b in blocks if b[0]=='p').split()))
