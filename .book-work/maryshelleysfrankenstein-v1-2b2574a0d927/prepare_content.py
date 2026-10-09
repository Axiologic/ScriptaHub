from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/maryshelleysfrankenstein-v1-2b2574a0d927')
source = Path('.book-work/income-pdf-candidates/2b2574a0d9271412/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 7, 9),
    ('a-mad-scientists-dream', 'Chapter One — A Mad Scientist’s Dream', 10, 14),
    ('the-monsters-birth', 'Chapter Two — The Monster’s Birth', 15, 20),
    ('the-bride-of-frankenstein', 'Chapter Three — The Bride of Frankenstein... Sort Of', 21, 25),
    ('the-wedding-night', 'Chapter Four — The Wedding Night and the Final Reckoning', 26, 31),
    ('final-words', 'Final Words', 32, 35),
    ('bibliography', 'Bibliography', 42, 42),
]
headings = {
    'INTRODUCTION', 'CHAPTER ONE', 'A Mad Scientist’s Dream', 'CHAPTER TWO',
    'The Monster’s Birth – “It’s Alive!', 'CHAPTER THREE',
    'The Bride of Frankenstein... Sort Of', 'CHAPTER FOUR',
    'The Wedding Night and the Final Reckoning', 'FINAL WORDS', 'BIBLIOGRAPHY',
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
            if page == 7 and value.startswith('Welcome, dear reader, to a condensed journey'):
                continue
            if slug == 'introduction' and 'In just four chapters, this summary captures' in value:
                value = value.split(' In just four chapters, this summary captures', 1)[0]
            if (paragraphs and page != 42 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    records.append({'id': slug, 'pages': [first, last], 'paragraphs': len(paragraphs), 'words': sum(len(p.split()) for p in paragraphs)})
    body = '\n'.join(f'<p>{escape(p)}</p>' for p in paragraphs)
    parts.append(f'<section id="{slug}"><h2>{escape(label)}</h2>\n{body}\n</section>')
title = 'Mary Shelley’s Frankenstein'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[7, 35], [42, 42]],
    'excludedPages': [[1, 6], [36, 41]],
    'reason': 'Retained the original introduction, four chapters, final reflections and bibliography; excluded retired rights, promotional preface and author/project annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
