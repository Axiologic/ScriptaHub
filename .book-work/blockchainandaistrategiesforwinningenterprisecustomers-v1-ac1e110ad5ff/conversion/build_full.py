#!/usr/bin/env python3
"""Reflow the substantive report, keeping its original wording."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib
import json
import re

work = Path(__file__).resolve().parents[1]
root = Path(__file__).resolve().parents[3]
source = root / '.book-work/income-pdf-candidates/ac1e110ad5ff88b0/clean-draft.html'
pages = {int(s['data-source-page']): [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)) for p in s.select('p')] for s in BeautifulSoup(source.read_text(), 'html.parser').select('section[data-source-page]')}

def body(start, end):
    chunks = []
    for page in range(start, end + 1):
        rows = pages[page]
        skip = {9:1, 11:3, 14:3, 17:3, 20:3, 26:1}.get(page, 0)
        chunks.extend(p for p in rows[skip:] if not p.isdigit())
    return ' '.join(chunks)

sections = [
  ('introduction', 'Introduction', 9, 10, [
    'The report,', 'Despite its briefness,', 'Unfortunately, attempting']),
  ('ch1', 'Chapter One — Sales-Driven Startup Without a Product', 11, 13, [
    'Building direct relationships', 'Starting a startup', 'A successful approach', 'A lean approach']),
  ('ch2', 'Chapter Two — Non-Profit Umbrella for an Enterprise Startup', 14, 16, [
    'A promising model', 'A key element', "It's crucial to start", 'For example, with 100 members', 'Initially, the startup', 'By joining the community']),
  ('ch3', 'Chapter Three — Promotion and Funding Strategies', 17, 19, [
    'Participating in business accelerators', 'Offering training sessions', 'Building an online community', 'In Europe, accessing European Research Grants']),
  ('ch4', 'Chapter Four — Short Summary of Best Practices', 20, 25, [
    'Creating a successful startup', 'Embracing a lean approach', 'Leveraging strategic partnerships', 'Utilizing the "Jobs to Be Done"', 'Fostering an educational community', 'Participation in accelerators', 'Focusing on thought leadership', 'Exploring funding opportunities', 'Forming consortia with larger companies enhances', 'Iterating based on market feedback', 'Implementing a structured approach', 'In addition to these foundational practices', 'Cultivating a culture of innovation', 'Leveraging data analytics', 'Developing a scalable business model', 'Finally, networking relentlessly', 'By integrating these best practices']),
  ('conclusion', 'Conclusion', 26, 27, [
    'To succeed in the AI', 'Creating a non-profit professional community', 'Additionally, participating', 'Finally, forming consortia']),
]
parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Blockchain and AI: Strategies for Winning Enterprise Customers</title></head><body><article>', '<h1>Blockchain and AI: Strategies for Winning Enterprise Customers</h1>', '<p class="byline">Sînică Alboaie · 2024</p>']
receipt = {}
for anchor, heading, start, end, starts in sections:
    text = body(start, end)
    indices = [text.find(marker) for marker in starts]
    assert all(i >= 0 for i in indices), (anchor, list(zip(starts, indices)))
    assert indices == sorted(indices) and indices[0] == 0, (anchor, indices)
    paragraphs = [text[indices[i]:indices[i+1] if i+1 < len(indices) else None].strip() for i in range(len(indices))]
    assert all(paragraphs)
    parts.append(f'<h2 id="{anchor}">{escape(heading)}</h2>')
    parts.extend(f'<p>{escape(p)}</p>' for p in paragraphs)
    receipt[anchor] = {'pages':[start,end], 'paragraphs':len(paragraphs), 'words':len(text.split())}
parts.append('<h2 id="bibliography">Bibliography</h2>')
refs = [p for page in (36,37) for p in pages[page] if p not in ('BIBLIOGRAPHY','36','37')]
assert len(refs) == 7
parts.append('<ol>')
parts.extend(f'<li id="reference-{i}">{escape(ref)}</li>' for i, ref in enumerate(refs,1))
parts.extend(['</ol>', '</article></body></html>'])
out = work / 'book/en/full_content.html'
out.write_text('\n'.join(parts)+'\n', encoding='utf-8')
(work / 'conversion/receipt.json').write_text(json.dumps({'sourceCleanDraft':str(source.relative_to(root)), 'sourceCleanDraftSha256':hashlib.sha256(source.read_bytes()).hexdigest(), 'included':receipt, 'bibliographyReferences':7, 'excluded':'cover/title, legacy rights, promotional preface, former-project/author annexes, promotional letter'}, indent=2)+'\n')
print(out)
