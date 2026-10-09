from hashlib import sha256
from pathlib import Path
import json
import base64
from io import BytesIO

from lxml import etree, html
from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML

root = Path('.book-work/acheekyguidetoancientgreekphilosophy-v1-5952af7eae3a')
source = root / 'book/en/full_content.html'
destination = root / 'book/en/book.pdf'
publication = root / 'publication/en'
publication.mkdir(parents=True, exist_ok=True)
document = html.fromstring(source.read_bytes())
assert document.xpath('//article[@data-reader-content]')
# The source contains one Japanese katakana glyph in a shrug emoticon.
# Rasterize only that glyph for print so PDF/A-style font embedding does not
# include a CJK variable font that Poppler rejects. The reader stays canonical.
font = ImageFont.truetype('/usr/share/fonts/google-noto-sans-cjk-vf-fonts/NotoSansCJK-VF.ttc', 128)
glyph = Image.new('RGBA', (160, 160), (255, 255, 255, 0))
ImageDraw.Draw(glyph).text((16, -22), 'ツ', font=font, fill='#1f2b38')
bounds = glyph.getbbox()
glyph = glyph.crop(bounds)
buffer = BytesIO()
glyph.save(buffer, format='PNG')
data_url = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')
replacements = 0
for paragraph in document.xpath('//article//p'):
    if paragraph.text and '¯_(ツ)_/¯' in paragraph.text:
        head, tail = paragraph.text.split('¯_(ツ)_/¯', 1)
        paragraph.text = head
        shrug = etree.SubElement(paragraph, 'span')
        shrug.set('class', 'shrug')
        shrug.text = '¯_('
        picture = etree.SubElement(shrug, 'img')
        picture.set('src', data_url)
        picture.set('alt', 'ツ')
        picture.set('class', 'shrug-glyph')
        picture.tail = ')_/¯'
        shrug.tail = tail
        replacements += 1
assert replacements == 1
style = etree.SubElement(document.find('head'), 'style')
style.text = '''
@page { size: 152.4mm 228.6mm; margin: 17mm 17mm 18mm;
  @bottom-center { content: counter(page); font: 8pt "Liberation Serif"; color: #63717a; } }
@page:first { @bottom-center { content: none; } }
body { color: #1f2b38; margin: 0; font: 10.3pt/1.46 "Liberation Serif", serif; }
h1,h2 { color: #254c68; font-family: "Liberation Sans", sans-serif;
  line-height: 1.2; break-after: avoid; }
h1 { font-size: 23pt; margin: 28mm 0 15mm; }
h2 { font-size: 17pt; break-before: page; margin: 0 0 12mm; }
p { margin: 0 0 8pt; orphans: 3; widows: 3; text-align: justify; hyphens: auto; }
a { color: inherit; text-decoration: none; overflow-wrap: anywhere; }
.shrug { white-space: nowrap; }
.shrug-glyph { display: inline; width: .85em; height: .8em; vertical-align: -.07em; }
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
