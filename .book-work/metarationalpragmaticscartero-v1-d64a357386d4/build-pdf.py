from pathlib import Path
from lxml import html,etree
from weasyprint import HTML
import json,hashlib
w=Path(__file__).resolve().parent;src=w/'book/en/full_content.html';doc=html.fromstring(src.read_bytes());pub=w/'publication/en';pub.mkdir(parents=True,exist_ok=True)
for style in doc.xpath('//style'):style.getparent().remove(style)
css='''@page{size:152.4mm 228.6mm;margin:17mm 17mm 18mm;@bottom-center{content:counter(page);font-family:"Noto Serif";font-size:8pt;color:#666}}@page:first{@bottom-center{content:none}}html{color:#202420;background:white}body{margin:0;font-family:"Noto Serif",serif;font-size:9.5pt;line-height:1.32}main{margin:0;padding:0}h1,h2,h3{font-family:"Red Hat Display",sans-serif;line-height:1.2;break-after:avoid;color:#29483b}h1{font-size:22pt;break-before:page;margin:10pt 0 20pt}h2{font-size:14pt;margin:15pt 0 8pt}p{margin:0 0 7pt;orphans:3;widows:3;text-align:justify;hyphens:auto}a{color:inherit;text-decoration:none;overflow-wrap:anywhere}.source-toc{text-align:left;font-size:9pt;margin:0 0 7pt;break-inside:avoid}.bibliography{font-size:8.2pt;text-align:left;break-inside:avoid;overflow-wrap:anywhere}#src-p1{margin-top:28mm;font:8pt "Red Hat Display";letter-spacing:1pt;text-align:center}#src-p2{font:700 30pt "Red Hat Display";line-height:1.12;margin:15mm 0 10mm;text-align:center;color:#29483b}#src-p3{font-size:17pt;line-height:1.4;text-align:center}#src-p4{font-size:11pt;text-align:center;margin-top:12mm}#src-p5{font-size:10pt;font-style:italic;text-align:center;margin-top:12mm}'''
css += '''img{max-width:100%;height:auto}table{width:100%;border-collapse:collapse;font-size:8pt}td,th{padding:4pt;border:0.4pt solid #bbb;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:8pt}code{font-family:monospace;font-size:8pt}h3{font-size:11pt;margin:12pt 0 6pt}'''
import re
main=doc.find('body').find('main');children=list(main);heads=doc.xpath('//main/h1');toc_records=[]
for el in children:
    ident=el.get('id','');text=el.text_content().strip()
    if ident.startswith('src-p') and 11<=int(ident[5:])<=47 and el.tag=='p':
        m=re.match(r'^(.*?)\s+(\d+)$',text)
        if m:
            label=m[1];needle=re.sub(r'^(?:\d+|[A-D])\.\s*|^Preface\.\s*','',label)
            target=next((h for h in heads if h.text_content().strip()==needle),None)
            if target is None and label.startswith('B.'):target=next(h for h in heads if h.text_content().startswith('Exercises with'))
            assert target is not None,label
            el.clear();el.set('id',ident);el.set('class','source-toc');a=etree.SubElement(el,'a',href='#'+target.get('id'));a.text=label;toc_records.append(dict(label=label,target=target.get('id')))
        else:el.set('class','toc-part')
    elif re.fullmatch(r'CHAPTER \d+|APPENDIX [A-D]|PREFACE',text):el.set('class','chapter-label')
    elif text.startswith('PART ') or text.startswith('Appendices  /'):el.set('class','part-label')
css += ".source-toc a::after{content:leader('.') target-counter(attr(href),page)}.toc-part{font-size:9pt;font-weight:bold;text-align:left;margin:9pt 0 5pt}.chapter-label{break-before:page;break-after:avoid;font:9pt 'Red Hat Display';color:#29483b;margin:0 0 10pt}.chapter-label+h1{break-before:auto}.part-label{break-before:page;break-after:avoid;font:10pt 'Red Hat Display';margin:0 0 16pt;color:#29483b}.part-label+.chapter-label{break-before:auto}#src-p2,#src-p3,#src-p4,#src-p5,#src-p6,#src-p7,#src-p8{hyphens:none;text-align:center}#src-p1{margin-top:15mm}#src-p2{font-size:27pt;margin:12mm 0 8mm}#src-p3{font-size:16pt}#src-p4{font-size:12pt;margin-top:7mm}#src-p5{font-size:13pt;margin-top:10mm;font-style:normal}#src-p6,#src-p7,#src-p8{font-size:8pt;line-height:1.3}#src-p6{margin-top:8mm}#src-p7{margin-top:8mm}#src-p8{margin-top:5mm}th{background:#edf0ed}thead{display:table-header-group}tr{break-inside:avoid}"
(w/'pdf-toc.json').write_text(json.dumps(toc_records,indent=2)+'\n')
css += '#src-p98,#src-p99,#src-p100,#src-p101,#src-p102,#src-p103,#src-p104,#src-p105,#src-p106,#src-p107,#src-p108,#src-p109,#src-p110,#src-p111,#src-p112,#src-p113,#src-p114,#src-p115,#src-p116,#src-p117,#src-p118,#src-p119,#src-p120,#src-p121,#src-p122,#src-p123,#src-p124,#src-p125,#src-p126,#src-p127,#src-p128,#src-p129,#src-p130,#src-p131,#src-p132,#src-p133,#src-p134,#src-p135,#src-p136,#src-p137,#src-p138,#src-p139,#src-p306,#src-p307,#src-p308,#src-p309,#src-p310,#src-p311,#src-p312,#src-p313,#src-p314,#src-p315,#src-p316,#src-p317,#src-p318,#src-p319,#src-p320,#src-p321,#src-p322,#src-p323,#src-p324,#src-p325,#src-p326,#src-p327,#src-p328,#src-p329,#src-p330,#src-p331,#src-p332,#src-p333,#src-p334,#src-p335,#src-p336,#src-p337,#src-p338,#src-p339,#src-p340,#src-p341,#src-p342,#src-p343,#src-p344,#src-p345,#src-p346,#src-p347,#src-p348,#src-p349,#src-p350,#src-p351,#src-p513,#src-p514,#src-p515,#src-p516,#src-p517,#src-p518,#src-p519,#src-p520,#src-p521,#src-p522,#src-p523,#src-p524,#src-p525,#src-p526,#src-p527,#src-p528,#src-p529,#src-p530,#src-p531,#src-p532,#src-p533,#src-p534,#src-p535,#src-p536,#src-p537,#src-p538,#src-p539,#src-p540,#src-p541,#src-p542,#src-p543,#src-p544,#src-p545,#src-p546,#src-p547,#src-p548,#src-p549,#src-p550,#src-p551,#src-p552,#src-p553,#src-p554,#src-p555,#src-p556,#src-p557,#src-p558,#src-p559,#src-p560,#src-p561{font-size:9.2pt;line-height:1.29}h1#src-p98,h1#src-p306,h1#src-p513{font-size:22pt;line-height:1.2}h2{font-size:14pt!important;line-height:1.2!important}'
for table in doc.xpath('//table'):
    if 'Mathematical Object' in table.text_content():table.set('class','vocabulary-table')
css += '.vocabulary-table td{padding:3pt}.vocabulary-table p{font-size:8pt!important;line-height:1.25!important;margin:0}'
etree.SubElement(doc.find('head'),'style').text=css
f=pub/'publication.html';f.write_bytes(etree.tostring(doc,method='html',encoding='utf-8',doctype='<!doctype html>'))
out=w/'book/en/book.pdf';HTML(filename=str(f),base_url=str(src.parent)).write_pdf(str(out),pdf_tags=True)
(w/'pdf-build.json').write_text(json.dumps(dict(sourceHtmlSha256=hashlib.sha256(src.read_bytes()).hexdigest(),pdfSha256=hashlib.sha256(out.read_bytes()).hexdigest(),engine='WeasyPrint',sourceText='All canonical English reader elements preserved; print styling only',pageSize='6 x 9 inches'),indent=2)+'\n')
print(out)
