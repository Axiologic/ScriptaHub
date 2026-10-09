from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/thenikolateslastorythealternatingcurrentofdestiny-v1-26cc062649aa')
source = Path('.book-work/income-pdf-candidates/26cc062649aab431/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 8, 9),
    ('no-tesla-no-progress', 'Chapter One — No Tesla, No Progress?', 10, 12),
    ('early-life', 'Chapter Two — Early Life and Education', 13, 14),
    ('scientific-breakthroughs', 'Chapter Three — Scientific Breakthroughs', 15, 18),
    ('impact-on-society', 'Chapter Four — Impact on Society', 19, 21),
    ('war-of-currents', 'Chapter Five — Tesla vs. Edison: The War of Currents', 22, 25),
    ('challenges', 'Chapter Six — Challenges and Controversies', 26, 29),
    ('philosophies', 'Chapter Seven — Philosophies and Ideologies', 30, 36),
    ('personal-life', 'Chapter Eight — Personal Life and Early Influences', 37, 38),
    ('conclusion', 'Conclusion', 39, 39),
    ('bibliography', 'Bibliography', 46, 47),
]
headings = {'INTRODUCTION', 'CONCLUSION', 'BIBLIOGRAPHY',
            'CHAPTER ONE', 'CHAPTER TWO', 'CHAPTER THREE', 'CHAPTER FOUR',
            'CHAPTER FIVE', 'CHAPTER SIX', 'CHAPTER SEVEN', 'CHAPTER EIGHT',
            'No Tesla, No Progress?', 'Early Life and Education',
            'Scientific Breakthroughs', 'Impact on Society',
            'Tesla vs. Edison: The War of Currents', 'Challenges and Controversies',
            'Philosophies and Ideologies', 'Personal Life and Early Influences'}
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
            if (paragraphs and first != 46 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if first != 46:
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
title = 'The Nikola Tesla Story: The Alternating Current of Destiny'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[8, 39], [46, 47]],
    'excludedPages': [[1, 7], [40, 45]],
    'reason': 'Retained the original introduction, eight chapters, conclusion and bibliography; excluded rights, promotional preface and retired author/project annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
