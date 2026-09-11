from pathlib import Path
from lxml import html,etree
from weasyprint import HTML
import json,hashlib,re
w=Path(__file__).resolve().parent;src=w/'book/en/full_content.html';doc=html.fromstring(src.read_bytes());pub=w/'publication/en';pub.mkdir(parents=True,exist_ok=True)
for style in doc.xpath('//style'):style.getparent().remove(style)
css='''@page{size:152.4mm 228.6mm;margin:17mm 17mm 18mm;@bottom-center{content:counter(page);font-family:"Noto Serif";font-size:8pt;color:#666}}@page:first{@bottom-center{content:none}}html{color:#202420;background:white}body{margin:0;font-family:"Noto Serif",serif;font-size:10pt;line-height:1.38}main{margin:0;padding:0}h1,h2,h3{font-family:"Red Hat Display",sans-serif;line-height:1.2;break-after:avoid;color:#29483b}h1{font-size:22pt;break-before:page;margin:10pt 0 20pt}h2{font-size:14pt;margin:18pt 0 9pt}h3{font-size:11pt;margin:12pt 0 6pt}p{margin:0 0 8pt;orphans:3;widows:3;text-align:justify;hyphens:auto}a{color:inherit;text-decoration:none;overflow-wrap:anywhere}img{max-width:100%;height:auto}table{width:100%;border-collapse:collapse;font-size:8pt}td,th{padding:4pt;border:0.4pt solid #bbb;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:8pt}code{font-family:monospace;font-size:8pt}.source-toc{text-align:left;font-size:9pt;margin:0 0 7pt;break-inside:avoid}.source-toc a::after{content:leader('.') target-counter(attr(href),page)}.bibliography{font-size:8.2pt;text-align:left;break-inside:avoid;overflow-wrap:anywhere}.part-label{break-before:page;break-after:avoid;font:9pt "Red Hat Display";letter-spacing:.5pt;color:#29483b}.part-label+h1{break-before:auto}.cover{text-align:center;hyphens:none}.cover-title{break-before:auto;font-size:31pt;line-height:1.15;margin:15mm 0 10mm}.cover-kicker{margin-top:25mm;font:8pt "Red Hat Display";letter-spacing:.8pt}.cover-subtitle{font-size:16pt;line-height:1.4}.cover-note{font-size:10pt;margin-top:10mm}.toc-title{break-before:page;font:700 22pt "Red Hat Display";margin:10pt 0 20pt;color:#29483b}.toc-part{font:8pt "Red Hat Display";margin:12pt 0 7pt;break-after:avoid;text-align:left}'''
rules='dinreguli' in w.name
cover_ids=range(1,9) if rules else [1,3,4,6,7]
for n in cover_ids:
 el=doc.get_element_by_id(f'src-p{n}'); cls='cover '
 cls += 'cover-title' if el.tag=='h1' else 'cover-kicker' if n==1 else 'cover-subtitle' if el.get('class')=='subtitle' else 'cover-note'
 el.set('class',cls)
if rules:
 css+='#src-p5{margin-top:13mm;font:8pt "Red Hat Display"}#src-p6{font-size:16pt;margin-top:4mm}#src-p7{font-size:9pt;margin-top:7mm}#src-p8{font-size:8pt;margin-top:7mm}'
else:css+='#src-p6{font-size:11pt;margin-top:14mm}#src-p7{margin-top:16mm;font-size:9pt}'
toc_start,toc_end=(9,43) if rules else (9,46)
for n in range(toc_start,toc_end+1):
 try:el=doc.get_element_by_id(f'src-p{n}')
 except KeyError:continue
 if not el.text_content().strip():continue
 if 'Contents' in el.text_content() and not el.xpath('./a'):el.set('class','toc-title');continue
 links=el.xpath('./a')
 if links:
  el.set('class','source-toc')
  if re.fullmatch(r'\s*\d+\s*',links[-1].tail or ''):links[-1].tail=''
 else:el.set('class','toc-part')
for el in doc.xpath('//main/p'):
 n=int(el.get('id','src-p0').split('p')[-1])
 if n>toc_end and re.match(r'^(PART [IVX]+\s*/|[IVX]+ · |APPENDICES\s*/|TOOLS ·)',el.text_content().strip()):el.set('class','part-label')
etree.SubElement(doc.find('head'),'style').text=css
f=pub/'publication.html';f.write_bytes(etree.tostring(doc,method='html',encoding='utf-8',doctype='<!doctype html>'))
out=w/'book/en/book.pdf';HTML(filename=str(f),base_url=str(src.parent)).write_pdf(str(out),pdf_tags=True)
(w/'pdf-build.json').write_text(json.dumps(dict(sourceHtmlSha256=hashlib.sha256(src.read_bytes()).hexdigest(),pdfSha256=hashlib.sha256(out.read_bytes()).hexdigest(),engine='WeasyPrint',sourceText='Complete canonical English reader preserved; print styles and regenerated TOC page numbers only',pageSize='6 x 9 inches'),indent=2)+'\n')
print(out)
