from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import json
import re

work = Path(__file__).resolve().parent
source = Path('.book-work/income-pdf-candidates/c85486b333bac4f9/clean-draft.html')
soup = BeautifulSoup(source.read_text(), 'html.parser')
sections = [
    ('introduction', 'Introduction', 8, 8),
    ('mirror-writing', 'Chapter One — The Mystery Behind Leonardo’s Mirror Writing', 9, 11),
    ('master-of-versatility', 'Chapter Two — Master of Versatility', 12, 22),
    ('codes', 'Chapter Three — Leonardo’s Codes at the Intersection of Art and Science', 23, 26),
    ('mysteries', 'Chapter Four — Mysteries and Conspiracies Around Genius', 27, 32),
    ('legacy', 'Chapter Five — Leonardo’s Legacy and Relevance in the Modern World', 33, 35),
    ('conclusion', 'Conclusion', 38, 39),
    ('bibliography', 'Bibliography', 46, 47),
]
headings = {'INTRODUCTION', 'CHAPTER ONE', 'CHAPTER TWO', 'CHAPTER THREE', 'CHAPTER FOUR', 'CHAPTER FIVE', 'CONCLUSION', 'BIBLIOGRAPHY', 'The Mystery Behind Leonardo’s Mirror Writing', 'Master of Versatility', "Leonardo's Codes at the Intersection of Art and Science", 'Mysteries and Conspiracies Around Genius', "Leonardo's Legacy Relevance in the Modern World"}
parts = []
records = []
for slug, heading, first, last in sections:
    paragraphs = []
    for page in range(first, last + 1):
        node = soup.find('section', {'data-source-page': str(page)})
        assert node is not None, page
        for element in node.select('p'):
            value = re.sub(r'\s+', ' ', element.get_text(' ', strip=True)).strip()
            if not value or value in headings or value in {str(page), str(page-1)}:
                continue
            if paragraphs and slug != 'bibliography' and not re.search(r'[.!?][”"’\']?$', paragraphs[-1]) and not paragraphs[-1].endswith(':'):
                paragraphs[-1] += ' ' + value
            else:
                paragraphs.append(value)
    if slug != 'bibliography':
        readable = []
        for paragraph in paragraphs:
            if len(paragraph.split()) <= 145:
                readable.append(paragraph)
                continue
            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', paragraph)
            group = []
            for sentence in sentences:
                if group and sum(len(item.split()) for item in group) + len(sentence.split()) > 145:
                    readable.append(' '.join(group))
                    group = []
                group.append(sentence)
            if group: readable.append(' '.join(group))
        paragraphs = readable
    records.append({'id': slug, 'pages': [first,last], 'paragraphs': len(paragraphs), 'words': sum(len(x.split()) for x in paragraphs)})
    body = '\n'.join(f'<p>{escape(x)}</p>' for x in paragraphs)
    parts.append(f'<section id="{slug}"><h2>{escape(heading)}</h2>\n{body}\n</section>')
title = 'The Genius of the Renaissance: Leonardo da Vinci'
output = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>{escape(title)}</title></head><body><article>\n<h1>{escape(title)}</h1>\n<p class="book-byline">AI Agent Noah Bradland · 2024</p>\n' + '\n'.join(parts) + '\n</article></body></html>\n'
(work/'book/en/full_content.html').write_text(output)
(work/'qa').mkdir(exist_ok=True)
(work/'qa/source-selection.json').write_text(json.dumps({'source':str(source),'includedPages':[[8,35],[38,39],[46,47]],'excludedPages':[[1,7],[36,37],[40,45]],'reason':'Retained substantive Leonardo introduction, chapters one through five, conclusion, and bibliography. Omitted old rights/promotion, an unrelated inserted Edison chapter, and former-project annexes.','sections':records},indent=2)+'\n')
print(records)
