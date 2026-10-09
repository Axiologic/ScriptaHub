from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/stevejobsthemanbehindtheapple-v1-6d73b9faa82a')
source = Path('.book-work/income-pdf-candidates/6d73b9faa82a23a1/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('emerging-technologies', 'Chapter One — Steve Jobs and Today’s Emerging Technologies', 9, 11),
    ('youth', 'Chapter Two — Roots of a Visionary: The Youth of Steve Jobs', 12, 15),
    ('birth-of-apple', 'Chapter Three — The Birth of Apple', 16, 19),
    ('design', 'Chapter Four — Innovation and Design Philosophy', 20, 22),
    ('leadership', 'Chapter Five — Leadership Style and Business Acumen', 23, 25),
    ('comeback', 'Chapter Six — Adversity and Comeback', 26, 29),
    ('industries', 'Chapter Seven — Reinventing Industries', 30, 33),
    ('behind-the-myth', 'Chapter Eight — The Man Behind the Myth', 34, 36),
    ('legacy', 'Chapter Nine — Legacy and Cultural Impact', 37, 39),
    ('conclusion', 'Conclusion', 40, 40),
    ('bibliography', 'Bibliography', 47, 48),
]
headings = {'CONCLUSION', 'BIBLIOGRAPHY',
            'CHAPTER ONE', 'CHAPTER TWO', 'CHAPTER THREE', 'CHAPTER FOUR',
            'CHAPTER FIVE', 'CHAPTER SIX', 'CHAPTER SEVEN', 'CHAPTER EIGHT',
            'CHAPTER NINE', 'Steve Jobs and Today’s Emerging Technologies',
            'Roots of a Visionary: The Youth of Steve Jobs', 'The Birth of Apple',
            'Innovation and Design Philosophy', 'Leadership Style and Business Acumen',
            'Adversity and Comeback', 'Reinventing Industries', 'The Man Behind the Myth',
            'Legacy and Cultural Impact'}
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
            if (paragraphs and first != 47 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if first != 47:
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
title = 'Steve Jobs: The Man Behind the Apple'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[9, 40], [47, 48]],
    'excludedPages': [[1, 8], [41, 46]],
    'reason': 'Retained nine substantive chapters, conclusion and bibliography; excluded rights, promotional preface/introduction and retired author/project annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
