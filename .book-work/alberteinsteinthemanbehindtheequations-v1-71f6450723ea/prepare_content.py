from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/alberteinsteinthemanbehindtheequations-v1-71f6450723ea')
source = Path('.book-work/income-pdf-candidates/71f6450723ea896c/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('without-einstein', 'Chapter One — Humanity without Albert Einstein', 10, 11),
    ('early-life', 'Chapter Two — Early Life and Education', 12, 15),
    ('breakthroughs', 'Chapter Three — Scientific Breakthroughs', 16, 20),
    ('achievements', 'Chapter Four — Achievements and Contributions', 21, 23),
    ('society', 'Chapter Five — Impact on Society', 24, 28),
    ('philosophies', 'Chapter Six — The Philosophies and Ideologies', 29, 33),
    ('personal-life', 'Chapter Seven — Personal Life and Motivations', 34, 37),
    ('legacy', 'Chapter Eight — Legacy and Modern Influence', 38, 39),
    ('conclusion', 'Conclusion', 40, 41),
    ('bibliography', 'Bibliography', 48, 48),
]
headings = {'CONCLUSION', 'BIBLIOGRAPHY',
            'CHAPTER ONE', 'CHAPTER TWO', 'CHAPTER THREE', 'CHAPTER FOUR',
            'CHAPTER FIVE', 'CHAPTER SIX', 'CHAPTER SEVEN', 'CHAPTER EIGHT',
            'Humanity without Albert Einstein', 'Early Life and Education',
            'Scientific Breakthroughs', 'Achievements and Contributions',
            'Impact on Society', 'The Philosophies and Ideologies',
            'Personal Life and Motivations', 'Legacy and Modern Influence'}
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
title = 'Albert Einstein: The Man Behind the Equations'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[10, 41], [48, 48]],
    'excludedPages': [[1, 9], [42, 47]],
    'reason': 'Retained eight substantive chapters, conclusion and bibliography; excluded rights, promotional preface/introduction and retired author/project annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
