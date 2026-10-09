from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import re

workspace = Path(__file__).parent
source = Path('.book-work/income-pdf-candidates/b567909dbc99ffb9/clean-draft.html')
soup = BeautifulSoup(source.read_text(), 'html.parser')
chapters = {
    'Chapter One The Rise of Two Giants': ('chapter-1', 'Chapter One: The Rise of Two Giants'),
    'Chapter Two Defining the Modern Era of Football': ('chapter-2', 'Chapter Two: Defining the Modern Era of Football'),
    'Chapter Three Rivalry and Records': ('chapter-3', 'Chapter Three: Rivalry and Records'),
    'Chapter Four Beyond the Pitch – Influence and Legacy': ('chapter-4', 'Chapter Four: Beyond the Pitch – Influence and Legacy'),
    'Chapter 5 The Debate – Who Is the Greatest?': ('chapter-5', 'Chapter Five: The Debate – Who Is the Greatest?'),
}
subheads = {'Lionel Messi: The Prodigy from Rosario', 'Cristiano Ronaldo: The Self-Made Superstar'}
sections = []

for section in soup.select('section[data-source-page]'):
    page = int(section['data-source-page'])
    if page not in (*range(7, 38), 44):
        continue
    for paragraph in section.select('p'):
        value = re.sub(r'\s+', ' ', paragraph.get_text(' ', strip=True))
        value = value.replace('**', '')
        if not value or value.isdecimal():
            continue
        if page == 44:
            if value == 'Bibliography':
                sections.append(('bibliography', 'Bibliography', []))
            else:
                sections[-1][2].append(('p', value))
            continue
        if page == 7 and value.startswith('Introduction '):
            sections.append(('introduction', 'Introduction', []))
            value = value[len('Introduction '):]
        if value in chapters:
            ident, label = chapters[value]
            sections.append((ident, label, []))
            continue
        if not sections:
            continue
        if value in subheads:
            sections[-1][2].append(('h3', value))
            continue
        blocks = sections[-1][2]
        if blocks and blocks[-1][0] == 'p' and (not re.search(r'[.!?][”"’\)]?$', blocks[-1][1]) or value[:1].islower()):
            blocks[-1] = ('p', blocks[-1][1] + ' ' + value)
        else:
            blocks.append(('p', value))

title = 'Messi or Ronaldo? The End of an Era'
output = ['<!doctype html>', f'<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body>', '<main>', f'<h1>{escape(title)}</h1>', '<p class="byline">AI Agent Aarion Sykes · 2024</p>']
for ident, heading, blocks in sections:
    output.append(f'<section id="{ident}"><h2>{escape(heading)}</h2>')
    for kind, value in blocks:
        if kind != 'p' or len(value.split()) <= 170:
            output.append(f'<{kind}>{escape(value)}</{kind}>')
            continue
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“"‘])', value)
        part = []
        for sentence in sentences:
            if part and len(' '.join(part).split()) + len(sentence.split()) > 150:
                output.append(f'<p>{escape(" ".join(part))}</p>')
                part = []
            part.append(sentence)
        if part:
            output.append(f'<p>{escape(" ".join(part))}</p>')
    output.append('</section>')
output.extend(['</main>', '</body></html>'])
(workspace / 'book/en/full_content.html').write_text('\n'.join(output) + '\n')
print([(ident, len(blocks)) for ident, _, blocks in sections])
