import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/9faf7aec303c823d/clean-draft.html').read_text(encoding='utf-8'), 'html.parser')
title_text = 'Conspiracies in Ancient Civilizations: Secret Organizations and Their Impact on History'
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>{title_text}</title>'
    '</head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
title = out.new_tag('h1', id='book-title')
title.string = title_text
article.append(title)
heads = {
    9: ('Chapter One — Shadows of Ancient Greece', 2),
    17: ('Chapter Two — Shadows of the Eternal City', 2),
    25: ('Chapter Three — Conspiracies and Secret Societies in Ancient India', 2),
    33: ('Chapter Four — Whispers in the Middle Kingdom', 2),
    41: ('Chapter Five — Conspiracies and Secret Societies in Pre-Columbian America', 2),
    49: ('Chapter Six — Sects and Religions in the Hellenistic Middle East', 2),
    55: ('Chapter Seven — Jewish Sects and Early Christian Organizations', 2),
    61: ('Conclusion — Patterns and Parallels in Ancient Conspiracies', 2),
    73: ('Further Reading', 1),
}
kept = list(range(9, 67)) + [73, 74]
sections = []
for page in kept:
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page in heads:
        label, skip = heads[page]
        h = out.new_tag('h2', id='further-reading' if page == 73 else f'chapter-{len(sections)+1}')
        h.string = label
        article.append(h)
        sections.append({'id': h['id'], 'title': label, 'page': page})
        paragraphs = paragraphs[skip:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        value = re.sub(r' Others see its i$', '', value)
        value = re.sub(r' At the same time, it reminds us of the very real dangers that trave\.$', '', value)
        if not value or re.fullmatch(r'\d+', value):
            continue
        p = out.new_tag('p')
        p.string = value
        article.append(p)

for p in list(article.find_all('p', recursive=False)):
    prev = p.find_previous_sibling()
    if prev and prev.name == 'p':
        left, right = prev.get_text(' ', strip=True), p.get_text(' ', strip=True)
        page_join = (left.endswith('to the') and right.startswith('Delphic Oracle,')) or (left.endswith('Kaula and') and right.startswith('Aghori.'))
        if left and right and (page_join or (not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right))):
            prev.string = left + ' ' + right
            p.decompose()

for p in list(article.find_all('p', recursive=False)):
    value = p.get_text(' ', strip=True)
    if len(value.split()) <= 230:
        continue
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“])', value)
    if len(sentences) < 3:
        continue
    groups, group, words = [], [], 0
    for sentence in sentences:
        count = len(sentence.split())
        if group and words + count > 170:
            groups.append(' '.join(group))
            group, words = [], 0
        group.append(sentence)
        words += count
    if group:
        groups.append(' '.join(group))
    if len(groups) > 1:
        for group_text in groups:
            node = out.new_tag('p')
            node.string = group_text
            p.insert_before(node)
        p.decompose()

body = article.get_text(' ', strip=True)
assert len(body.split()) > 7000
assert not any(term in body.lower() for term in ('outfinitygift', 'outfinity srl', 'about ai author'))
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/Conspiracies_in_Ancient_Civilizations_Secret_Organizations_and_Their_Impact_on_History/content.pdf',
    'retainedPdfPages': kept,
    'excludedPdfPages': list(range(1, 9)) + list(range(67, 73)),
    'reason': 'Keep the original seven chapters, conclusion and further reading; remove old rights, promotional preface, contents and former-project annex.',
    'sourceDefects': ['PDF page 12 ends with the unfinished fragment "Others see its i"; omit only that fragment.', 'PDF page 28 ends with the incomplete sentence "At the same time, it reminds us of the very real dangers that trave."; omit only that sentence.', 'Rejoin the phrases split across source pages 15–16 and 30–31.'],
    'sections': sections,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader:', len(body.split()), 'words')
