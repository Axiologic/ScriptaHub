"""Select the complete Jack London novel from the delivered PDF draft."""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent


def display_label(label):
    kind, numeral = label.split()
    return f'{kind.title()} {numeral}'


draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/6df6a30c4c22e557/clean-draft.html').read_text(), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>White Fang</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h = out.new_tag('h1', id='book-title')
h.string = 'White Fang'
article.append(h)
byline = out.new_tag('p', attrs={'class': 'book-byline'})
byline.string = 'Jack London'
article.append(byline)

sections = []
paragraphs = []
joins = []
part = None
for page in range(21, 264):
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source is not None, page
    parts = [re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip() for p in source.find_all('p', recursive=False)]
    parts = [p for p in parts if p and p != str(page)]
    if page == 263:
        assert parts[-1] == 'THE END'
        parts.pop()
    if parts and parts[0].startswith('PART '):
        label = parts.pop(0)
        assert re.fullmatch(r'PART (?:I|II|III|IV|V)', label), (page, label)
        part = label
        heading = out.new_tag('h2', id=f'part-{label.split()[1].lower()}')
        heading.string = display_label(label)
        article.append(heading)
        sections.append({'page': page, 'kind': 'part', 'title': label})
    if parts and parts[0].startswith('CHAPTER '):
        label = parts.pop(0)
        title = parts.pop(0)
        assert re.fullmatch(r'CHAPTER [IVX]+', label), (page, label)
        assert title.isupper(), (page, title)
        heading = out.new_tag('h3', id=f'{part.lower().replace(" ", "-")}-{label.lower().replace(" ", "-")}')
        heading.string = f'{display_label(label)} — {title.title().replace("’S", "’s")}'
        article.append(heading)
        sections.append({'page': page, 'kind': 'chapter', 'part': part, 'label': label, 'title': title})
    for value in parts:
        if paragraphs and paragraphs[-1][1] == page - 1 and (not re.search(r'[.!?…][”’\)]?$', paragraphs[-1][0]) or re.match(r'^[a-z]', value)):
            left, before = paragraphs.pop()
            paragraphs.append((left + ' ' + value, page))
            joins.append({'fromPage': before, 'toPage': page, 'leftEnd': left[-65:], 'rightStart': value[:65]})
        else:
            paragraphs.append((value, page))

# Headings must remain in source order. Reconstruct content in page order with
# limited-length semantic paragraphs, then insert each heading before its page.
article.clear()
article.append(h)
article.append(byline)
by_page = {}
for text, endpage in paragraphs:
    by_page.setdefault(endpage, []).append(text)
headings = {}
for section in sections:
    headings.setdefault(section['page'], []).append(section)
for page in range(21, 264):
    for section in headings.get(page, []):
        if section['kind'] == 'part':
            tag = out.new_tag('h2', id=f'part-{section["title"].split()[1].lower()}')
            tag.string = display_label(section['title'])
        else:
            tag = out.new_tag('h3', id=f'{section["part"].lower().replace(" ", "-")}-{section["label"].lower().replace(" ", "-")}')
            tag.string = f'{display_label(section["label"])} — {section["title"].title().replace("’S", "’s")}'
        article.append(tag)
    for value in by_page.get(page, []):
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“‘])', value)
        groups = []
        group = []
        count = 0
        for sentence in sentences:
            words = len(sentence.split())
            if group and count + words > 145:
                groups.append(' '.join(group))
                group = []
                count = 0
            group.append(sentence)
            count += words
        if group:
            groups.append(' '.join(group))
        for text in groups:
            node = out.new_tag('p')
            node.string = text
            article.append(node)

body = article.get_text(' ', strip=True)
assert len(body.split()) > 65000, len(body.split())
assert len(article.find_all('h2')) == 5
assert len(article.find_all('h3')) == 25
assert not any(word in body.lower() for word in ('outfinity', 'taler vox', 'ai perspective', 'annexes'))
target = root/'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out)+'\n')
qa = root/'qa'
qa.mkdir(exist_ok=True)
(qa/'source-selection.json').write_text(json.dumps({
    'source': 'income/White_Fang/content.pdf',
    'retainedPdfPages': list(range(21,264)),
    'excludedPdfPages': list(range(1,21))+list(range(264,268)),
    'selection': 'Only the five parts and 25 chapters of Jack London’s original novel, through THE END. Excludes retired rights, TOC and preface, all AI Perspective/commentary, duplicate title leaf, and AI-author/OutfinityGift annexes.',
    'chapters': sections,
    'pageBoundaryJoins': joins,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2)+'\n')
print(len(body.split()), 'words;', len(sections), 'part/chapter headings;', len(joins), 'page joins')
