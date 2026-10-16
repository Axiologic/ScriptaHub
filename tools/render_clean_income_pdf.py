#!/usr/bin/env python3
"""Render the complete cleaned English reader as an English download PDF."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import sys
from lxml import etree,html
from weasyprint import HTML

work=Path(sys.argv[1]).resolve()
source=work/'book/en/full_content.html'
destination=work/'book/en/book.pdf'
if not source.is_file():raise SystemExit('Missing English reader')
markup=source.read_text()
if 'outfinitygift' in markup.lower() or 'all rights reserved' in markup.lower():raise SystemExit('Retired rights text remains')
doc=html.fromstring(markup)
style=etree.SubElement(doc.find('head'),'style')
style.text='''
@page { size: 6in 9in; margin: .72in .72in .75in;
  @bottom-center { content: counter(page); font: 8pt "Noto Serif"; color: #667070; } }
@page:first { @bottom-center { content: none; } }
body { color: #202a2a; font: 10.2pt/1.45 "Noto Serif", serif; }
article { max-width: none; padding: 0; }
h1,h2,h3 { font-family: "Red Hat Display", sans-serif; color: #244e52; break-after: avoid; }
h1 { font-size: 22pt; margin: 30mm 0 8mm; }
h2 { font-size: 14pt; margin: 10mm 0 4mm; }
h3 { font-size: 11pt; margin: 6mm 0 3mm; }
p { margin: 0 0 7pt; text-align: justify; hyphens: auto; orphans: 3; widows: 3; }
p.edition-credit { text-align: left; }
section { margin: 0; }
'''
publication=work/'publication/en'
publication.mkdir(parents=True,exist_ok=True)
print_html=publication/'clean-publication.html'
print_html.write_bytes(etree.tostring(doc,method='html',encoding='utf-8',doctype='<!doctype html>'))
HTML(filename=str(print_html),base_url=str(source.parent)).write_pdf(str(destination),pdf_tags=True)
receipt={'sourceHtml':str(source),'sourceHtmlSha256':sha256(source.read_bytes()).hexdigest(),'pdf':str(destination),'pdfSha256':sha256(destination.read_bytes()).hexdigest(),'engine':'WeasyPrint','pageSize':'6 x 9 inches','input':'Complete source-preserving cleaned English HTML reader'}
(work/'publication/en/pdf-build.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(destination)
