from hashlib import sha256
from pathlib import Path
import json

from lxml import etree, html
from weasyprint import HTML

root = Path('.book-work/incompletetribes-v1-e9dde0116308')
source = root / 'book/en/full_content.html'
destination = root / 'book/en/book.pdf'
publication = root / 'publication/en'
publication.mkdir(parents=True, exist_ok=True)

document = html.fromstring(source.read_bytes())
article = document.xpath('//article')[0]
assert article.get('data-prepared-incomplete-tribes') == 'true'
assert 'draft' not in ' '.join(article.itertext()).lower().split()[:20]

style = etree.SubElement(document.find('head'), 'style')
style.text = '''
@page { size: 152.4mm 228.6mm; margin: 18mm 18mm 19mm;
  @bottom-center { content: counter(page); font: 8pt "Noto Serif"; color: #596568; } }
@page:first { @bottom-center { content: none; } }
html { color: #1d282d; background: #fff; }
body { margin: 0; font: 10.4pt/1.49 "Noto Serif", serif; }
article { margin: 0; padding: 0; }
h1, h2, h3 { color: #254b58; font-family: "Red Hat Display", sans-serif;
  line-height: 1.2; break-after: avoid; }
h1 { font-size: 28pt; text-align: center; margin: 32mm 0 8mm; }
.book-subtitle { font: 14pt/1.4 "Red Hat Display", sans-serif;
  color: #42616c; text-align: center; margin: 0 0 18mm; hyphens: none; }
h2 { font-size: 19pt; break-before: page; margin: 0 0 13mm; }
h3 { font-size: 14pt; break-before: page; margin: 0 0 10mm; }
p { margin: 0 0 8pt; text-align: justify; orphans: 3; widows: 3; hyphens: auto; }
h1 + p + p { font-style: italic; }
blockquote { margin: 7mm 12mm; font-style: italic; }
a { color: #254b58; text-decoration: none; overflow-wrap: anywhere; }
img { max-width: 100%; height: auto; }
#notes ~ p { font-size: 8.5pt; text-align: left; overflow-wrap: anywhere; }
'''
html_path = publication / 'publication.html'
html_path.write_bytes(etree.tostring(document, method='html', encoding='utf-8', doctype='<!doctype html>'))
HTML(filename=str(html_path), base_url=str(source.parent)).write_pdf(str(destination), pdf_tags=True)
receipt = {
    'sourceHtmlSha256': sha256(source.read_bytes()).hexdigest(),
    'pdfSha256': sha256(destination.read_bytes()).hexdigest(),
    'engine': 'WeasyPrint',
    'pageSize': '6 x 9 inches',
    'content': 'Complete canonical English reader, with print styling only',
}
(root / 'pdf-build.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(destination)
