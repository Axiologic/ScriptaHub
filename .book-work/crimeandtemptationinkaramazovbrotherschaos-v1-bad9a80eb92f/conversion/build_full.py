#!/usr/bin/env python3
"""Reflow the source's introduction, chapters, conclusion and bibliography."""
from bs4 import BeautifulSoup
from html import escape
from pathlib import Path
import hashlib, json, re

w = Path(__file__).resolve().parents[1]
root = Path(__file__).resolve().parents[3]
src = root / '.book-work/income-pdf-candidates/bad9a80eb92f36fa/clean-draft.html'
pages = {int(s['data-source-page']): [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)) for p in s.select('p')]
         for s in BeautifulSoup(src.read_text(), 'html.parser').select('section[data-source-page]')}
heads = {
    'INTRODUCTION': ('introduction', 'Introduction'),
    'Sins, Secrets, and Family Ties Unraveled': ('chapter-one', 'Chapter One — Sins, Secrets, and Family Ties Unraveled'),
    'Blood, Betrayal, and a Killer’s Confession': ('chapter-two', 'Chapter Two — Blood, Betrayal, and a Killer’s Confession'),
    'Truth, Faith, and Madness on the Midnight Debates': ('chapter-three', 'Chapter Three — Truth, Faith, and Madness on the Midnight Debates'),
    'Karamazov Survival Guide: Dodging Temptation and Chaos': ('chapter-four', 'Chapter Four — Karamazov Survival Guide: Dodging Temptation and Chaos'),
    'CONCLUSION': ('conclusion', 'Conclusion'),
}
skip = {'CHAPTER ONE', 'CHAPTER TWO', 'CHAPTER THREE', 'CHAPTER FOUR'}
nodes = []
for page in range(7, 35):
    for text in pages[page]:
        if text.isdigit() or text in skip or text.startswith(("If you're looking for a profound exploration", 'While the film delivers a captivating portrayal')):
            continue
        if text in heads:
            anchor, label = heads[text]
            nodes.append(('h2', anchor, label))
            continue
        if (text[0].islower() or text.startswith('Ivan’s cynicism.')) and nodes and nodes[-1][0] == 'p' and page not in (7, 11, 16, 21, 26, 31):
            tag, anchor, prior = nodes[-1]
            nodes[-1] = (tag, anchor, prior + ' ' + text)
        else:
            nodes.append(('p', '', text))
assert sum(n[0] == 'h2' for n in nodes) == 6
parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Crime and Temptation in Karamazov Brothers Chaos</title></head><body><article>',
         '<h1>Crime and Temptation in Karamazov Brothers Chaos</h1>',
         '<p class="byline">AI Agent Chloe Vohan · 2024</p>']
for tag, anchor, text in nodes:
    parts.append(f'<{tag}{f" id={chr(34)}{anchor}{chr(34)}" if anchor else ""}>{escape(text)}</{tag}>')
refs = [x for x in pages[41] if x not in ('BIBLIOGRAPHY', '41')]
assert len(refs) == 2
parts.append('<h2 id="bibliography">Bibliography</h2><ol>')
parts.extend(f'<li id="reference-{i}">{escape(x)}</li>' for i, x in enumerate(refs, 1))
parts.extend(['</ol>', '</article></body></html>'])
out = w / 'book/en/full_content.html'
out.write_text('\n'.join(parts) + '\n', encoding='utf-8')
(w / 'conversion/receipt.json').write_text(json.dumps({
    'sourceCleanDraft': str(src.relative_to(root)),
    'sourceCleanDraftSha256': hashlib.sha256(src.read_bytes()).hexdigest(),
    'includedPages': 'introduction 7–10, chapters 11–30, conclusion 31–34, bibliography 41',
    'excluded': 'former rights page 3, promotional preface 5–6, concluding film/book promotion on page 34, former-project/AI-author annexes 35–40',
    'chapters': 4,
    'bibliographyReferences': 2,
}, indent=2) + '\n')
print(out, len(nodes), 'nodes')
