import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

root = Path('.book-work/areportonsecretsocietiesandrealconspiracies-v1-946e2ffece4f')
source = Path('.book-work/income-pdf-candidates/946e2ffece4f7849/clean-draft.html')
target = root / 'book/en/full_content.html'
draft = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
out = BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A Report on Secret Societies and Real Conspiracies</title></head><body><article data-reader-content></article></body></html>', 'html.parser')
article = out.article
h1 = out.new_tag('h1', id='book-title')
h1.string = 'A Report on Secret Societies and Real Conspiracies'
article.append(h1)

keep_pages = list(range(8, 34)) + list(range(40, 49))
sections = []
chapter = 0
await_chapter_title = False
in_bibliography = False
for page in keep_pages:
    source_section = draft.select_one(f'section[data-source-page="{page}"]')
    assert source_section, page
    for source_p in source_section.find_all('p', recursive=False):
        text = re.sub(r'\s+', ' ', source_p.get_text(' ', strip=True))
        if not text or re.fullmatch(r'\d+', text):
            continue
        if page == 9:
            continue  # prospective draft-release promise, not book content
        if page == 8:
            text = re.sub(r'This report is still in draft form, and we are working diligently to ensure that every detail is accurately documented, with references to reliable sources and evidence\.\s*', '', text)
            text = re.sub(r'As we continue to refine the content, it is essential to recognize that not everything branded as a "conspiracy theory" is entirely false\. Some actions and hidden agendas have been verified, and we believe it is our responsibility to expose them where necessary\.\s*$', '', text)
        if page == 33 and text.startswith('We recognize that many aspects of this report are still evolving.'):
            continue  # promotional promise to update an old project edition
        if text in {'INTRODUCTION', 'CONCLUSION', 'BIBLIOGRAPHY'}:
            section_id = text.lower()
            tag = out.new_tag('h2', id=section_id)
            tag.string = text.title()
            article.append(tag)
            sections.append({'id': section_id, 'title': tag.string, 'page': page})
            in_bibliography = text == 'BIBLIOGRAPHY'
            continue
        if re.fullmatch(r'CHAPTER (ONE|TWO|THREE|FOUR)', text):
            chapter += 1
            await_chapter_title = True
            continue
        if await_chapter_title:
            tag = out.new_tag('h2', id=f'chapter-{chapter}')
            tag.string = f'Chapter {chapter} — {text}'
            article.append(tag)
            sections.append({'id': tag['id'], 'title': tag.string, 'page': page})
            await_chapter_title = False
            continue
        if in_bibliography and text.endswith(':') and len(text.split()) < 8:
            tag = out.new_tag('h3')
            tag.string = text
            article.append(tag)
            continue
        if in_bibliography and (text.startswith('Link to ') or text == 'FAS Report on Biological Testing'):
            continue  # dead link labels in source PDF have no link annotations
        if not in_bibliography and 2 <= len(text.split()) <= 18 and not text.endswith(('.', '!', ';')):
            tag = out.new_tag('h3')
            tag.string = text
            article.append(tag)
            continue
        tag = out.new_tag('p')
        tag.string = text
        article.append(tag)

for paragraph in list(article.find_all('p', recursive=False)):
    previous = paragraph.find_previous_sibling()
    if previous and previous.name == 'p':
        left = previous.get_text(' ', strip=True)
        right = paragraph.get_text(' ', strip=True)
        if left and right and not re.search(r'[.!?:;”"\)]$', left) and re.match(r'^[a-z]', right):
            previous.string = left + ' ' + right
            paragraph.decompose()

assert chapter == 4 and len(sections) == 7, sections
assert not any(word in article.get_text(' ', strip=True).lower() for word in ('outfinitygift', 'outfinity srl', 'end of draft'))
target.write_text(str(out) + '\n', encoding='utf-8')
(root / 'qa').mkdir(exist_ok=True)
(root / 'qa/source-selection.json').write_text(json.dumps({
    'source': 'income/A_Report_on_Secret_Societies_and_Real_Conspiracies/content.pdf',
    'retainedPdfPages': keep_pages,
    'excludedPdfPages': list(range(1, 8)) + list(range(34, 40)),
    'furtherRemoval': 'PDF page 9 prospective draft-release promise; page 8 draft-status and ongoing-revision sentences; page 33 old-project update promise; bibliography link labels without targets',
    'sections': sections,
    'readerWords': len(article.get_text(' ', strip=True).split()),
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared original reader,', len(article.get_text(' ', strip=True).split()), 'words')
