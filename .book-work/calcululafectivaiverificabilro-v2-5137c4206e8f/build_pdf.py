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
article=document.xpath('//article[@data-reader-content]')[0]
front=[node for node in article if node.tag=='p'][:4]
assert len(front)==4
for node,role in zip(front,('cover-title','cover-subtitle','cover-deck','cover-edition')):
    node.set('class',role)
style=etree.SubElement(document.find('head'),'style')
style.text='''
@page { size: 152.4mm 228.6mm; margin: 16mm 16mm 18mm;
  @bottom-center { content: counter(page); font: 8pt "Noto Serif"; color: #63717a; } }
@page:first { @bottom-center { content: none; } }
body { color: #1d2a39; margin: 0; font: 9.4pt/1.42 "Noto Serif", serif; }
.cover-title { font: 40pt/1.08 "Noto Serif", serif; color: #1d2a39; margin: 32mm 0 14mm; text-align: left; hyphens: none; overflow-wrap: normal; }
.cover-subtitle { font: italic 13pt/1.4 "Noto Serif", serif; color: #53606b; margin: 0 0 18mm; text-align: left; }
.cover-deck { font: 700 10pt/1.4 "Red Hat Display", sans-serif; color: #53606b; margin: 0 0 25mm; text-align: left; }
.cover-edition { font: italic 9pt/1.5 "Noto Serif", serif; color: #63717a; margin-top: 25mm; break-after: page; text-align: left; }
h1,h2 { color: #254c68; font-family: "Red Hat Display", sans-serif; line-height: 1.2; break-after: avoid; }
h1 { font-size: 19pt; margin: 11mm 0 5mm; }
h2 { font-size: 13pt; margin: 8mm 0 3mm; }
p { margin: 0 0 6pt; orphans: 3; widows: 3; text-align: justify; hyphens: auto; overflow-wrap: anywhere; }
table { border-collapse: collapse; width: 100%; font-size: 7.3pt; margin: 5mm 0; table-layout: fixed; }
th,td { border: 0.4pt solid #79909e; padding: 1.6mm; vertical-align: top; text-align: left; overflow-wrap: anywhere; }
td p,th p { margin: 0; text-align: left; }
thead { display: table-header-group; background: #edf3f6; }
tr { break-inside: avoid; }
'''
print_html=publication/'publication.html'
print_html.write_bytes(etree.tostring(document,method='html',encoding='utf-8',doctype='<!doctype html>'))
HTML(filename=str(print_html),base_url=str(source.parent)).write_pdf(str(destination),pdf_tags=True)
(root/'pdf-build.json').write_text(json.dumps({
 'sourceHtmlSha256':sha256(source.read_bytes()).hexdigest(),
 'pdfSha256':sha256(destination.read_bytes()).hexdigest(),
 'engine':'WeasyPrint',
 'pageSize':'6 x 9 inches',
 'content':'Complete canonical English reader with print styling only'
},indent=2)+'\n')
print(destination)
