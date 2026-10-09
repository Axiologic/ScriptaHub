from hashlib import sha256
from pathlib import Path
import json

from lxml import etree, html
from weasyprint import HTML

root=Path(__file__).parent
source=root/'book/en/full_content.html'
destination=root/'book/en/book.pdf'
publication=root/'publication/en'
publication.mkdir(parents=True,exist_ok=True)
document=html.fromstring(source.read_bytes())
assert document.xpath('//article[@data-reader-content]')
style=etree.SubElement(document.find('head'),'style')
style.text='''
@page { size: 152.4mm 228.6mm; margin: 17mm 17mm 18mm;
  @bottom-center { content: counter(page); font: 8pt "Noto Serif"; color: #63717a; } }
@page:first { @bottom-center { content: none; } }
body { color: #1e2c36; margin: 0; font: 10.2pt/1.48 "Noto Serif", serif; }
article { max-width: none; padding: 0; }
h1,h2,h3 { color: #274d63; font-family: "Red Hat Display", sans-serif;
  line-height: 1.22; break-after: avoid; }
h1 { font-size: 21pt; margin: 22mm 0 13mm; }
h2 { font-size: 15pt; break-before: page; margin: 0 0 10mm; }
h3 { font-size: 11.5pt; margin: 8mm 0 4mm; }
p { margin: 0 0 8pt; orphans: 3; widows: 3; text-align: justify; hyphens: none; }
table { width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 8pt; break-inside: avoid; }
td,th { padding: 3pt; border: 0.5pt solid #8999a5; vertical-align: top; text-align: left; overflow-wrap: normal; }
td p,th p { text-align: left; margin: 0; }
td:nth-child(1),th:nth-child(1) { width: 21%; }
td:nth-child(2),th:nth-child(2) { width: 19%; }
td:nth-child(3),th:nth-child(3) { width: 34%; }
td:nth-child(4),th:nth-child(4) { width: 26%; }
th { background: #e7eef1; }
tr { break-inside: avoid; }
a { color: inherit; text-decoration: none; overflow-wrap: anywhere; }
'''
print_html=publication/'publication.html'
print_html.write_bytes(etree.tostring(document,method='html',encoding='utf-8',doctype='<!doctype html>'))
HTML(filename=str(print_html),base_url=str(source.parent)).write_pdf(str(destination),pdf_tags=True)
(root/'pdf-build.json').write_text(json.dumps({
    'sourceHtmlSha256':sha256(source.read_bytes()).hexdigest(),
    'pdfSha256':sha256(destination.read_bytes()).hexdigest(),
    'engine':'WeasyPrint',
    'pageSize':'6 x 9 inches',
    'content':'Complete canonical English reader, with print styling only',
},indent=2)+'\n')
print(destination)
