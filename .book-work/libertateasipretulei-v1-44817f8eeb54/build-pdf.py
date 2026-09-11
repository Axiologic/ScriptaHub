from pathlib import Path
from lxml import html,etree
from weasyprint import HTML
import json,hashlib
w=Path(__file__).resolve().parent;src=w/'book/en/full_content.html';doc=html.fromstring(src.read_bytes());pub=w/'publication/en';pub.mkdir(parents=True,exist_ok=True)
for style in doc.xpath('//style'):style.getparent().remove(style)
css='@page{size:152.4mm 228.6mm;margin:17mm 17mm 18mm;@bottom-center{content:counter(page);font-family:"Noto Serif";font-size:8pt;color:#666}}@page:first{@bottom-center{content:none}}html{color:#202420;background:white}body{margin:0;font-family:"Noto Serif",serif;font-size:10pt;line-height:1.38}main{margin:0;padding:0}h1,h2,h3{font-family:"Red Hat Display",sans-serif;line-height:1.2;break-after:avoid;color:#29483b}h1{font-size:21pt;break-before:page;margin:10pt 0 20pt}h2{font-size:14pt;margin:18pt 0 9pt}h3{font-size:11pt;margin:12pt 0 6pt}p{margin:0 0 8pt;orphans:3;widows:3;text-align:justify;hyphens:auto}a{color:inherit;text-decoration:none;overflow-wrap:anywhere}.source-toc{text-align:left;font-size:9pt;margin:0 0 7pt;break-inside:avoid}.source-toc a::after{content:leader(\'.\') target-counter(attr(href),page)}.bibliography{font-size:8.2pt;text-align:left;break-inside:avoid;overflow-wrap:anywhere}img{max-width:100%;height:auto}table{width:100%;border-collapse:collapse;font-size:8pt}td,th{padding:4pt;border:.4pt solid #bbb;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:8pt}code{font-family:monospace;font-size:8pt}#src-p1{margin-top:25mm;font:8pt "Red Hat Display";letter-spacing:1pt;text-align:center}#src-p2{font:700 29pt "Red Hat Display";line-height:1.15;margin:14mm 0 9mm;text-align:center;color:#29483b;break-before:auto}#src-p3{font-size:17pt;line-height:1.4;text-align:center;break-before:auto}#src-p4,#src-p5{font-size:11pt;text-align:center;margin-top:10mm}#src-p6{font-size:8pt;text-align:center;margin-top:10mm}#src-p1,#src-p2,#src-p3,#src-p4,#src-p5,#src-p6{hyphens:none}#src-p3{font:700 25pt "Red Hat Display";margin-top:0}#src-p4{font-size:16pt;line-height:1.4}#src-p5{font-size:11pt}'
import re
for para in doc.xpath('//p[contains(concat(" ",normalize-space(@class)," ")," source-toc ")]'):
    links=para.xpath('./a')
    if links and re.fullmatch(r'\s*\d+\s*',links[-1].tail or ''):links[-1].tail=''
for para in doc.xpath('//main/p'):
    txt=para.text_content().strip()
    if para.get('class')!='source-toc' and txt.startswith('PART '):para.set('class','part-label')
    elif re.fullmatch(r'CHAPTER \d+',txt):para.set('class','chapter-label')
css += '.part-label,.chapter-label{break-before:page;break-after:avoid;font:9pt "Red Hat Display";color:#29483b;text-align:left;hyphens:none}.part-label+.chapter-label{break-before:auto}.chapter-label+h1,.part-label+h1{break-before:auto}'
etree.SubElement(doc.find('head'),'style').text=css
f=pub/'publication.html';f.write_bytes(etree.tostring(doc,method='html',encoding='utf-8',doctype='<!doctype html>'))
out=w/'book/en/book.pdf';HTML(filename=str(f),base_url=str(src.parent)).write_pdf(str(out),pdf_tags=True)
(w/'pdf-build.json').write_text(json.dumps(dict(sourceHtmlSha256=hashlib.sha256(src.read_bytes()).hexdigest(),pdfSha256=hashlib.sha256(out.read_bytes()).hexdigest(),engine='WeasyPrint',sourceText='All canonical English reader elements preserved; print styling only',pageSize='6 x 9 inches'),indent=2)+'\n')
print(out)
