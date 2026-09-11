from pathlib import Path
from lxml import html,etree
from weasyprint import HTML
import json,hashlib,re
w=Path(__file__).resolve().parent;src=w/'book/en/full_content.html';doc=html.fromstring(src.read_bytes());pub=w/'publication/en';pub.mkdir(parents=True,exist_ok=True)
for el in doc.xpath('//style|//script|//link[@rel="stylesheet"]'):el.getparent().remove(el)
first,lo,hi,title_size=(6, 8, 28, 31)
main=doc.find('.//main');toc_ids=[]
for el in main:
 ident=el.get('id','');number=int(ident[5:]) if ident.startswith('src-p') else -1
 if lo<=number<=hi and el.tag=='p':
  links=el.xpath('./a[starts-with(@href,"#")]')
  if links:
   toc_ids.append(ident);el.set('class',(el.get('class','')+' print-toc').strip())
   for link in links:
    if re.fullmatch(r'\s*\d+\s*',link.text_content()):el.remove(link)
   links=el.xpath('./a')
   if links and re.fullmatch(r'\s*\d+\s*',links[-1].tail or ''):links[-1].tail=''
 for title in el.xpath('.//strong') if False else []:pass
css='''@page{size:152.4mm 228.6mm;margin:17mm 17mm 18mm;@bottom-center{content:counter(page);font-family:"Noto Serif";font-size:8pt;color:#666}}@page:first{@bottom-center{content:none}}html{color:#202420;background:white}body{margin:0;font-family:"Noto Serif",serif;font-size:10pt;line-height:1.38}main{margin:0;padding:0}h1,h2,h3{font-family:"Red Hat Display",sans-serif;line-height:1.2;break-after:avoid;color:#29483b}h1{font-size:22pt;break-before:page;margin:10pt 0 20pt}h2{font-size:14pt;margin:18pt 0 9pt}h3{font-size:11pt;margin:12pt 0 6pt}p{margin:0 0 8pt;orphans:3;widows:3;text-align:justify;hyphens:auto}a{color:inherit;text-decoration:none;overflow-wrap:anywhere}.print-toc{font-size:8.5pt;text-align:left;margin-bottom:6pt;break-inside:avoid}.print-toc>a:first-child::after{content:leader('.') target-counter(attr(href),page)}.source-toc:not(.print-toc){font-size:8.5pt;text-align:left;margin:9pt 0 5pt;break-after:avoid}.bibliography{font-size:8.2pt;text-align:left;break-inside:avoid;overflow-wrap:anywhere}img{max-width:100%;height:auto}table{width:100%;border-collapse:collapse;font-size:8pt;margin:10pt 0}td,th{padding:4pt;border:0.4pt solid #bbb;overflow-wrap:anywhere}tr{break-inside:avoid}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:7.5pt}code{font-family:"DejaVu Sans Mono",monospace;font-size:7.5pt}math{font-family:"STIX Two Math","DejaVu Serif",serif;font-size:10pt}#src-p1{margin-top:23mm;font:8pt "Red Hat Display";letter-spacing:.7pt;text-align:center}#src-p2{break-before:auto;line-height:1.15;margin:14mm 0 10mm;text-align:center;color:#29483b}#src-p3{font-size:16pt;line-height:1.4;text-align:center}#src-p4{font-size:10pt;text-align:center;margin-top:10mm}#src-p5{font-size:10pt;text-align:center;margin-top:10mm}#src-p2,#src-p3,#src-p4,#src-p5{hyphens:none}'''
css+=f'#src-p2{{font:700 {title_size}pt "Red Hat Display";line-height:1.15}}'
if first==7 and w.name.startswith(('artade','noutatea')):css+='#src-p6{font-size:8pt;text-align:center;margin-top:8mm}'
if w.name.startswith('noutatea'):css+='#src-p7{break-before:page;font:700 22pt "Red Hat Display";color:#29483b;margin:10pt 0 20pt}#src-p8{font-size:11pt;text-align:left;margin-bottom:14pt}'

# Bind source part/chapter labels to the heading they introduce.
for heading in list(main.xpath('./h1')):
 labels=[];previous=heading.getprevious()
 while previous is not None and previous.tag=='p':
  num=int(previous.get('id','src-p0')[5:]);text=previous.text_content().strip()
  if num<=hi or not (re.match(r'^(PART [IVX]+|CHAPTER [0-9]+|APPENDIX [A-Z]|APPENDICES|[IVX]+\s*·)',text) or text in ['EPILOGUE','PROLOGUE','SOURCES AND FURTHER READING']):break
  labels.insert(0,previous);previous=previous.getprevious()
 if labels:
  wrapper=etree.Element('div',{'class':'chapter-opening'});main.insert(main.index(labels[0]),wrapper)
  for el in labels+[heading]:wrapper.append(el)
css += '.chapter-opening{break-before:page;break-inside:avoid}.chapter-opening h1{break-before:auto;margin-top:9pt}.chapter-opening p{font:9pt "Red Hat Display";color:#29483b;text-align:left;margin:0 0 5pt}'
if w.name.startswith('artade'):css+='.print-toc{font-size:8pt;line-height:1.2;margin-bottom:4pt}.source-toc:not(.print-toc){font-size:8pt;margin:7pt 0 4pt}'
if w.name.startswith('incaoin'):css+=','.join('#src-p'+str(i) for i in range(7,12))+'{font-size:9.5pt;line-height:1.32}'

etree.SubElement(doc.find('head'),'style').text=css
f=pub/'publication.html';f.write_bytes(etree.tostring(doc,method='html',encoding='utf-8',doctype='<!doctype html>'))
out=w/'book/en/book.pdf';HTML(filename=str(f),base_url=str(src.parent)).write_pdf(str(out),pdf_tags=True)
(w/'pdf-build.json').write_text(json.dumps({'sourceHtmlSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'publicationHtmlSha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pdfSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'engine':'WeasyPrint','sourceText':'Complete canonical English reader, print CSS only; source TOC page numbers regenerated','pageSize':'6 x 9 inches','tocParagraphIds':toc_ids},indent=2)+'\n');print(out)
