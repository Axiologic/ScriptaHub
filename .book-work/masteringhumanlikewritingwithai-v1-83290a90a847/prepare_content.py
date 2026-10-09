import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

root = Path(__file__).parent
draft = BeautifulSoup(Path('.book-work/income-pdf-candidates/83290a90a847b9c2/clean-draft.html').read_text(), 'html.parser')
title_text = 'Mastering Human-Like Writing with AI'
out = BeautifulSoup(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>{title_text}</title></head><body><article data-reader-content></article></body></html>',
    'html.parser',
)
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = title_text
article.append(h1)
heads = {
    10: 'Introduction to Large Language Models (LLMs)',
    27: 'Understanding Perplexity, Burstiness, and Other Metrics',
    35: 'Humanizing Text Generation',
    42: 'Fine-Tuning LLMs for Personalized Content',
    50: 'Ethical Considerations in Human-Like Content Generation',
    56: 'Imagining a Tool for AI-Driven Science Fiction',
    64: 'Writing AI-Driven Movie Scripts and Dialogue',
    73: 'Experimental Literature and AI: Exploring AI Thought Patterns',
    81: 'Interactive Storytelling and AI: Engaging Human Readers',
    95: 'Future Directions and Innovations in Text-to-Text LLMs',
}
sections = []
for page in range(10, 102):
    source = draft.select_one(f'section[data-source-page="{page}"]')
    assert source, page
    paragraphs = source.find_all('p', recursive=False)
    if page in heads:
        assert paragraphs[0].get_text(' ', strip=True).startswith('Chapter')
        assert heads[page] in paragraphs[1].get_text(' ', strip=True)
        h = out.new_tag('h2', id=f'chapter-{len(sections)+1}')
        h.string = f'Chapter {len(sections)+1} — {heads[page]}'
        article.append(h)
        sections.append({'id': h['id'], 'title': h.get_text(), 'pdfPage': page})
        paragraphs = paragraphs[2:]
    for source_p in paragraphs:
        value = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not value or re.fullmatch(r'\d+', value):
            continue
        p = out.new_tag('p')
        p.string = value
        article.append(p)

joins = []
for p in list(article.find_all('p', recursive=False)):
    previous = p.find_previous_sibling()
    if not previous or previous.name != 'p':
        continue
    left, right = previous.get_text(' ', strip=True), p.get_text(' ', strip=True)
    if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
        joins.append({'leftEnd': left[-80:], 'rightStart': right[:80]})
        previous.string = left + ' ' + right
        p.decompose()

# Four source page breaks leave a sentence fragment beside a capitalized acronym.
# Move each entire unfinished sentence to the next paragraph, preserving paragraph count.
reflows = []
for p in list(article.find_all('p', recursive=False)):
    q = p.find_next_sibling()
    if not q or q.name != 'p':
        continue
    left, right = p.get_text(' ', strip=True), q.get_text(' ', strip=True)
    if not any((left.endswith(a) and right.startswith(b)) for a, b in (
        (' An', 'LLM, by contrast'),
        (' increasingly use', 'LLMs as tools'),
        (' General Data Protection Regulation', '(GDPR), which'),
        (' voice, and structure,', 'AI-generated texts can'),
    )):
        continue
    match = re.search(r'(?<=[.!?])\s+(?=[A-Z][^.!?]*$)', left)
    assert match, (left[-100:], right[:100])
    p.string = left[:match.start()].strip()
    q.string = left[match.end():].strip() + ' ' + right
    reflows.append({'moved': left[match.end():].strip(), 'nextStart': right[:80]})
assert len(reflows) == 4, reflows

# Keep each HTML segment suitable for faithful direct translation.
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
        if group and words + count > 165:
            groups.append(' '.join(group))
            group, words = [], 0
        group.append(sentence)
        words += count
    if group:
        groups.append(' '.join(group))
    if len(groups) > 1:
        for text in groups:
            node = out.new_tag('p')
            node.string = text
            p.insert_before(node)
        p.decompose()

body = article.get_text(' ', strip=True)
assert len(body.split()) > 15000
assert not any(x in body.lower() for x in ('outfinitygift', 'outfinity srl', 'about ai author'))
target = root / 'book/en/full_content.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(str(out) + '\n')
qa = root / 'qa'
qa.mkdir(exist_ok=True)
(qa / 'source-selection.json').write_text(json.dumps({
    'source': 'income/Mastering_Human_Like_Writing_with_AI/content.pdf',
    'retainedPdfPages': list(range(10, 102)),
    'excludedPdfPages': list(range(1, 10)) + list(range(102, 109)),
    'reason': 'Keep ten substantive chapters; exclude title/rights, promotional preface and old-project annexes.',
    'sections': sections,
    'pageBoundaryJoins': joins,
    'capitalizedPageBreakReflows': reflows,
    'readerWords': len(body.split()),
}, ensure_ascii=False, indent=2) + '\n')
print('Prepared original reader:', len(body.split()), 'words;', len(joins), 'page-boundary joins')
