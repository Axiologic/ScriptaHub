#!/usr/bin/env python3
"""Stage source-preserving English readers from reviewed incoming PDF drafts."""
from __future__ import annotations

import argparse
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
import shutil

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / '.book-work/income-pdf-candidates'
SUMMARY_PAGES = {
    'income/Dracula/content.pdf': range(21, 25),
    'income/Grimms__Fairy_Tales/content.pdf': range(13, 19),
    'income/Moby_Dick_Or_The_Whale/content.pdf': range(24, 28),
    'income/Oliver_Twist/content.pdf': range(23, 27),
    'income/The_Adventures_of_Ferdinand_Count_Fathom___Part_I/content.pdf': range(21, 26),
    'income/The_Adventures_of_Ferdinand_Count_Fathom___Part_II/content.pdf': range(22, 27),
    'income/The_Life_and_Adventures_of_Robinson_Crusoe/content.pdf': range(12, 17),
}
FIRST_CONTENT_PAGE = {
    'income/Dracula/content.pdf': 5,
    'income/Grimms__Fairy_Tales/content.pdf': 6,
    'income/Moby_Dick_Or_The_Whale/content.pdf': 12,
    'income/Oliver_Twist/content.pdf': 9,
    'income/The_Adventures_of_Ferdinand_Count_Fathom___Part_I/content.pdf': 7,
    'income/The_Adventures_of_Ferdinand_Count_Fathom___Part_II/content.pdf': 7,
    'income/The_Life_and_Adventures_of_Robinson_Crusoe/content.pdf': 6,
}
SOURCE_CREDITS = {
    'income/Dracula/content.pdf': 'Bram Stoker · delivered edition: AI Agent Taler Vox',
    'income/Grimms__Fairy_Tales/content.pdf': 'Jacob and Wilhelm Grimm · delivered edition: AI Agent Zira Luthor',
    'income/Moby_Dick_Or_The_Whale/content.pdf': 'Herman Melville · delivered edition: AI Agent Taler Vox',
    'income/Oliver_Twist/content.pdf': 'Charles Dickens · delivered edition: AI Agent Taler Vox',
    'income/The_Adventures_of_Ferdinand_Count_Fathom___Part_I/content.pdf': 'Tobias Smollett · delivered edition: AI Agent Taler Vox',
    'income/The_Adventures_of_Ferdinand_Count_Fathom___Part_II/content.pdf': 'Tobias Smollett · delivered edition: AI Agent Taler Vox',
    'income/The_Life_and_Adventures_of_Robinson_Crusoe/content.pdf': 'Daniel Defoe · delivered edition: AI Agent Taler Vox',
}
STYLE = 'body{margin:0;background:#fff;color:#1b2424;font:1.06rem/1.68 Georgia,serif}article{max-width:74ch;margin:auto;padding:2rem 1.2rem}h1,h2,h3{font-family:system-ui,sans-serif;line-height:1.25}h1{font-size:2rem}h2{margin-top:2em}h3{margin-top:1.4em}p{text-align:justify;hyphens:auto;margin:.8em 0}.edition-credit,.source-credit{text-align:left}section{margin:0}a{color:#116766}@media print{article{max-width:none;padding:0}h1,h2,h3{break-after:avoid}}'
OLD_BRAND = re.compile(r'outfinity\s*gift|outfinitygift|outfinity\s+project|all rights reserved', re.I)
END_SENTENCE = re.compile(r'(?<=[.!?])\s+(?=[“"\'‘’A-Z])')


def tidy(value: str) -> str:
    return re.sub(r'\s+', ' ', value).strip()


def render_paragraphs(value: str) -> list[str]:
    sentences = END_SENTENCE.split(value)
    output, current = [], []
    for sentence in sentences:
        if current and sum(len(x.split()) for x in current) >= 115:
            output.append(' '.join(current)); current = []
        current.append(sentence)
    if current:
        output.append(' '.join(current))
    return [f'<p>{escape(item)}</p>' for item in output if item]


def source_section(section: html.HtmlElement, page: int) -> str:
    parts = [f'<section id="source-page-{page}" data-source-page="{page}">']
    for p in section.xpath('./p'):
        value = tidy(p.text_content())
        if not value or value == str(page):
            continue
        if OLD_BRAND.search(value):
            raise ValueError(f'Retired notice remained on source page {page}: {value[:100]}')
        heading = not re.search(r'\.{3,}\s*\d+', value) and len(value) < 100 and (
            value.isupper() or re.match(r'^(Chapter|Part|Introduction|Preface|Conclusion|Historical and Cultural Context|Plot Summary)\b', value, re.I)
        )
        if heading:
            parts.append(f'<h2>{escape(value)}</h2>')
        else:
            parts.extend(render_paragraphs(value))
    parts.append('</section>')
    return '\n'.join(parts)


def write_reader(path: Path, title: str, source_credit: str, sections: list[str], short: bool) -> None:
    subtitle = ' — ten-minute reading' if short else ''
    intro = '<p><em>A short reading guide drawn from the delivered edition’s own contextual chapters.</em></p>' if short else ''
    markup = f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title + subtitle)}</title><style>{STYLE}</style></head><body><article data-reader-content=""><h1>{escape(title)}</h1><p class="source-credit">{escape(source_credit)}</p><p class="edition-credit">Edition: (c) Outfinity SRL, Iasi.</p>{intro}\n' + '\n'.join(sections) + ('\n<p><a href="full_content.html">Read the complete English edition.</a></p>' if short else '') + '\n</article></body></html>\n'
    path.write_text(markup, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', type=Path)
    parser.add_argument('--force', action='store_true', help='rebuild from the same reviewed cleaning receipt')
    args = parser.parse_args()
    work = args.workspace.resolve()
    release = json.loads((work/'release.json').read_text())
    source = release['source']
    if source not in SUMMARY_PAGES or release['status'] != 'preparing':
        parser.error('Not one of the reviewed incoming PDF workspaces')
    candidate = CANDIDATES / release['sha256'][:16]
    report = json.loads((candidate/'cleaning-report.json').read_text())
    if report['source'] != source or report['sha256'] != release['sha256'] or report['flags']:
        parser.error('Source cleaning is unreviewed or has unresolved flags')
    clean = html.fromstring((candidate/'clean-draft.html').read_bytes())
    pages = {int(s.get('data-source-page')): s for s in clean.xpath('//section[@data-source-page]')}
    title = json.loads((work/'book/manifest.json').read_text())['title']['en']
    full = work/'book/en/full_content.html'
    short = work/'book/en/short_content.html'
    qa = work/'qa/source-preserving-reader'
    qa.mkdir(parents=True, exist_ok=True)
    if full.exists() and not (qa/'previous-full_content.html').exists():
        shutil.copy2(full, qa/'previous-full_content.html')
    if short.exists() and not (qa/'previous-short_content.html').exists():
        shutil.copy2(short, qa/'previous-short_content.html')
    if args.force or not (qa/'prepared.json').exists():
        selected_full = [(page, section) for page, section in sorted(pages.items()) if page >= FIRST_CONTENT_PAGE[source]]
        write_reader(full, title, SOURCE_CREDITS[source], [source_section(section, page) for page, section in selected_full], False)
        if not short.exists() or (args.force and not (qa/'previous-short_content.html').exists()):
            selected = list(SUMMARY_PAGES[source])
            if any(page not in pages for page in selected):
                parser.error('One or more summary pages are absent after cleaning')
            write_reader(short, title, SOURCE_CREDITS[source], [source_section(pages[page], page) for page in selected], True)
        else:
            markup = short.read_text()
            if 'OutfinityGift' in markup or 'outfinitygift' in markup.lower():
                parser.error('Existing short reader still contains the retired project')
            if '(c) Outfinity SRL, Iasi.' not in markup:
                markup = markup.replace('</h1>', '</h1><p class="edition-credit">Edition: (c) Outfinity SRL, Iasi.</p>', 1)
                short.write_text(markup)
        receipt = {'source':source,'sourceSha256':release['sha256'],'cleaningReport':str((candidate/'cleaning-report.json').relative_to(ROOT)),'retainedPages':sorted(pages),'fullReaderSha256':sha256(full.read_bytes()).hexdigest(),'shortReaderSha256':sha256(short.read_bytes()).hexdigest(),'shortPages':list(SUMMARY_PAGES[source]) if not (qa/'previous-short_content.html').exists() else 'existing editorial short reader retained'}
        (qa/'prepared.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(full, short)

if __name__ == '__main__':
    main()
