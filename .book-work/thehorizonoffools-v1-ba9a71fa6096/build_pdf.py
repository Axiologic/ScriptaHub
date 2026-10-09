from hashlib import sha256
from pathlib import Path
import json

from lxml import etree, html
from weasyprint import HTML

root = Path('.book-work/thehorizonoffools-v1-ba9a71fa6096')
source = root / 'book/en/full_content.html'
destination = root / 'book/en/book.pdf'
publication = root / 'publication/en'
publication.mkdir(parents=True, exist_ok=True)
document = html.fromstring(source.read_bytes())
assert document.xpath('//article[@data-reader-content]')
style = etree.SubElement(document.find('head'), 'style')
style.text = '''
@page { size: 152.4mm 228.6mm; margin: 17mm 17mm 18mm;
  @bottom-center { content: counter(page); font: 8pt "Noto Serif"; color: #63717a; } }
@page:first { @bottom-center { content: none; } }
body { color: #1f2b38; margin: 0; font: 10.3pt/1.46 "Noto Serif", serif; }
h1,h2 { color: #254c68; font-family: "Red Hat Display", sans-serif;
  line-height: 1.2; break-after: avoid; }
h1 { font-size: 23pt; margin: 28mm 0 15mm; }
h2 { font-size: 17pt; break-before: page; margin: 0 0 12mm; }
p { margin: 0 0 8pt; orphans: 3; widows: 3; text-align: justify; hyphens: auto; }
a { color: inherit; text-decoration: none; overflow-wrap: anywhere; }
'''
print_html = publication / 'publication.html'
print_html.write_bytes(etree.tostring(document, method='html', encoding='utf-8', doctype='<!doctype html>'))
HTML(filename=str(print_html), base_url=str(source.parent)).write_pdf(str(destination), pdf_tags=True)
(root / 'pdf-build.json').write_text(json.dumps({
    'sourceHtmlSha256': sha256(source.read_bytes()).hexdigest(),
    'pdfSha256': sha256(destination.read_bytes()).hexdigest(),
    'engine': 'WeasyPrint',
    'pageSize': '6 x 9 inches',
    'content': 'Complete canonical English reader, with print styling only',
}, indent=2) + '\n')
print(destination)
