from pathlib import Path
from bs4 import BeautifulSoup

w = Path(__file__).resolve().parent
p = w / 'book/ro/short_content.html'
full = BeautifulSoup((w / 'book/ro/full_content.html').read_text(), 'html.parser')
ids = {tag.get('id') for tag in full.select('[id]')}
text = p.read_text()
source = '../en/full_content.html#'
target = 'full_content.html#'
if source in text:
    assert text.count(source) == 9
    text = text.replace(source, target)
    p.write_text(text)
short = BeautifulSoup(text, 'html.parser')
links = [a.get('href', '') for a in short.select('a')]
assert len(links) == 9
assert all(href.startswith(target) and href.split('#', 1)[1] in ids for href in links)
