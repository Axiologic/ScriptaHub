from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

root = Path('.book-work/aristotlethephilosopherwhoshapedwesternthought-v1-255163137d22')
source = Path('.book-work/income-pdf-candidates/255163137d22db4c/clean-draft.html')
soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
sections = [
    ('introduction', 'Introduction', 8, 9),
    ('life', 'Chapter One — Aristotle’s Life and Historical Context', 10, 12),
    ('science', 'Chapter Two — Evolution of Scientific Thought', 13, 22),
    ('ethics-politics', 'Chapter Three — Ethical and Political Philosophy', 23, 29),
    ('metaphysics', 'Chapter Four — Metaphysics and Theories of Existence', 30, 34),
    ('logic', 'Chapter Five — Epistemology and Logic', 35, 40),
    ('conclusion', 'Conclusion', 41, 42),
    ('bibliography', 'Bibliography', 49, 50),
]
headings = {'INTRODUCTION', 'CHAPTER ONE', 'CHAPTER TWO', 'CHAPTER THREE',
            'CHAPTER FOUR', 'CHAPTER FIVE', 'CONCLUSION', 'BIBLIOGRAPHY',
            "Aristotle's life and historical context", 'Evolution of Scientific Thought',
            'The lasting impact on biology and physic', 'Ethical and Political Philosophy Reflections',
            "Aristotle's Metaphysics and Theories of Existence",
            'Epistemology and Logic in Aristotle’s Philosophy'}
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
            if (paragraphs and first != 49 and not re.search(r'[.!?][”"’\']?$', paragraphs[-1])
                    and not paragraphs[-1].endswith(':')):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if first != 49:
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
title = 'Aristotle: The Philosopher Who Shaped Western Thought'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(root / 'book/en/full_content.html').write_text(output, encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': str(source), 'includedPages': [[8, 42], [49, 50]],
    'excludedPages': [[1, 7], [43, 48]],
    'reason': 'Retained original introduction, five substantive chapters, conclusion and bibliography; excluded rights, promotional preface and retired OutfinityGift annexes.',
    'sections': records,
}, indent=2) + '\n', encoding='utf-8')
print(records)
