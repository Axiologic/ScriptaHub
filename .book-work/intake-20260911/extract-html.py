from pathlib import Path
from zipfile import ZipFile
from lxml import etree,html
from html import escape as E
from collections import Counter
import json,re,hashlib,posixpath
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';M='http://schemas.openxmlformats.org/officeDocument/2006/math';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';qn=lambda n:'{'+W+'}'+n
css='''html{color-scheme:light dark}body{margin:0;font:1.08rem/1.7 Georgia,serif}main{max-width:76ch;margin:auto;padding:2.5rem 1.4rem}h1,h2,h3,h4{font-family:system-ui,sans-serif;line-height:1.25;text-wrap:balance;break-after:avoid}h1{font-size:2rem;margin:2.5rem 0 1rem}h2{font-size:1.55rem;margin:2rem 0 1rem}h3{font-size:1.2rem}p{margin:0 0 1em}a{color:inherit;overflow-wrap:anywhere}img{max-width:100%;height:auto;display:block;margin:1rem auto}table{border-collapse:collapse;width:100%;margin:1.5rem 0;font-size:.88em}td,th{text-align:left;vertical-align:top;padding:.6rem;border-bottom:1px solid #999;overflow-wrap:anywhere}table p{margin:0 0 .5em}.table-scroll{overflow-x:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:.85em}.subtitle{font-style:italic;font-size:1.25rem}.callout{padding:.8rem;border-left:3px solid #9aa}.bibliography{font-size:.9em;overflow-wrap:anywhere}.source-toc{font-size:.9em}math{font-size:1.05em;max-width:100%;overflow-x:auto}math[display=block]{display:block;margin:1rem 0} @media(max-width:650px){main{padding:1.2rem}h1{font-size:1.7rem}h2{font-size:1.35rem}}'''
def local(n):return etree.QName(n).localname
for book in json.loads(Path('.book-work/intake-20260911/books.json').read_text()):
 work=Path(book['workdir']);out=work/'book'/book['language']/'full_content.html'
 if out.exists():print('Resuming existing',book['title']);continue
 src=work/book['filename'];assets=out.parent/'assets';assets.mkdir(parents=True,exist_ok=True)
 with ZipFile(src) as z:
  doc=etree.fromstring(z.read('word/document.xml'));body=doc.find(qn('body'));rels={x.get('Id'):x.get('Target') for x in etree.fromstring(z.read('word/_rels/document.xml.rels'))};styles=etree.fromstring(z.read('word/styles.xml'));sty={x.get(qn('styleId')):x for x in styles};bookmarks=set();stats=Counter();ordinal=[0]
  for name in ['footnoteReference','endnoteReference','object','ins','del','vMerge','gridSpan']:
   assert not doc.xpath('//*[local-name()="'+name+'"]'),(book['title'],name)
  def math(n):
   name=local(n)
   if name.endswith('Pr'):return ''
   child=lambda s:next((x for x in n if local(x)==s),None)
   convert=lambda s:math(child(s)) if child(s) is not None else '<mrow></mrow>'
   inner=lambda:''.join(math(x) for x in n if not local(x).endswith('Pr'))
   if name in ['oMath','oMathPara']:return '<math xmlns="http://www.w3.org/1998/Math/MathML" translate="no">'+inner()+'</math>' if name=='oMath' else inner()
   if name in ['e','sub','sup','num','den']:return '<mrow>'+inner()+'</mrow>'
   if name=='r':
    t=''.join(n.xpath('./m:t/text()',namespaces={'m':M}));return '<mtext>'+E(t)+'</mtext>'
   if name in ['sSub','sSup','sSubSup']:
    tag={'sSub':'msub','sSup':'msup','sSubSup':'msubsup'}[name];return '<'+tag+'>'+convert('e')+(convert('sub') if name!='sSup' else '')+(convert('sup') if name!='sSub' else '')+'</'+tag+'>'
   if name=='f':return '<mfrac>'+convert('num')+convert('den')+'</mfrac>'
   if name=='acc':
    chars=n.xpath('./m:accPr/m:chr/@m:val',namespaces={'m':M});return '<mover accent="true">'+convert('e')+'<mo>'+E(chars[0] if chars else '̂')+'</mo></mover>'
   if name=='nary':
    chars=n.xpath('./m:naryPr/m:chr/@m:val',namespaces={'m':M});op='<mo>'+E(chars[0] if chars else '∫')+'</mo>';sub=n.xpath('./m:naryPr/m:subHide/@m:val',namespaces={'m':M});sup=n.xpath('./m:naryPr/m:supHide/@m:val',namespaces={'m':M});usesub=sub!=['1'];usesup=sup!=['1'];tag='munderover' if usesub and usesup else 'munder' if usesub else 'mover' if usesup else None;return '<mrow>'+('<'+tag+'>'+op+(convert('sub') if usesub else '')+(convert('sup') if usesup else '')+'</'+tag+'>' if tag else op)+convert('e')+'</mrow>'
   raise ValueError('Unsupported math '+name)
  def inline(n):
   name=local(n);uri=etree.QName(n).namespace
   if uri==M:return math(n)
   if name in ['pPr','rPr','bookmarkEnd','proofErr','lastRenderedPageBreak','fldChar','instrText','sectPr','tab']:return ' ' if name=='tab' else ''
   if name=='t':return E(n.text or '')
   if name in ['br','cr']:return '<br>'
   if name=='bookmarkStart':
    key=n.get(qn('name'));bookmarks.add(key);return '<span id="'+E(key,quote=True)+'"></span>'
   if name=='hyperlink':
    key=n.get(qn('anchor'));target='#'+key if key else rels.get(n.get('{'+R+'}id'),'');return '<a href="'+E(target,quote=True)+'">'+''.join(inline(c) for c in n)+'</a>'
   if name=='drawing':
    images=[]
    for blip in n.xpath('.//*[local-name()="blip"]'):
     rel=rels[blip.get('{'+R+'}embed')];name=Path(rel).name;data=z.read(posixpath.normpath('word/'+rel));(assets/name).write_bytes(data);images.append('<img src="assets/'+E(name)+'" alt="">');stats['images']+=1
    return ''.join(images)
   if name=='r':
    t=''.join(inline(c) for c in n if local(c)!='rPr');rp=n.find(qn('rPr'))
    if rp is not None:
     for prop,tag in [('b','strong'),('i','em')]:
      a=rp.find(qn(prop))
      if a is not None and a.get(qn('val')) not in ['0','false','off']:t='<'+tag+'>'+t+'</'+tag+'>'
     a=rp.find(qn('vertAlign'))
     if a is not None and a.get(qn('val')) in ['superscript','subscript']:
      tag='sup' if a.get(qn('val'))=='superscript' else 'sub';t='<'+tag+'>'+t+'</'+tag+'>'
    return t
   if name in ['sdt','sdtContent','smartTag','fldSimple','p']:return ''.join(inline(c) for c in n if local(c) not in ['sdtPr','sdtEndPr'])
   raise ValueError('Unsupported inline '+name)
  def paragraph(p):
   ordinal[0]+=1;style=p.find(qn('pPr')+'/'+qn('pStyle'));sid=style.get(qn('val'),'') if style is not None else '';definition=sty.get(sid);level=p.find(qn('pPr')+'/'+qn('outlineLvl'))
   if level is None and definition is not None:level=definition.find(qn('pPr')+'/'+qn('outlineLvl'))
   level=int(level.get(qn('val'))) if level is not None else None
   match=re.search(r'(?:heading|titlu)\s*([1-6])',sid,re.I)
   tag='h'+str(min(6,level+1)) if level is not None and level<6 else 'h'+match[1] if match else 'h1' if sid.lower() in ['title','booktitle','covertitle'] else 'pre' if 'code' in sid.lower() else 'p'
   content=inline(p);plain=''.join(p.xpath('.//w:t/text()',namespaces={'w':W}));stats['paragraphs']+=1
   if not content.strip():return ''
   cls='source-toc' if 'toc' in sid.lower() else 'subtitle' if 'subtitle' in sid.lower() else 'bibliography' if 'bibliograph' in sid.lower() else 'callout' if 'callout' in sid.lower() else ''
   return '<'+tag+' id="src-p'+str(ordinal[0])+'"'+(' class="'+cls+'"' if cls else '')+'>'+content+'</'+tag+'>'
  def blocks(n):
   a=[]
   for c in n:
    name=local(c)
    if name=='p':a.append(paragraph(c))
    elif name=='tbl':
     stats['tables']+=1;rows=[]
     for tr in c.findall(qn('tr')):rows.append('<tr>'+''.join('<td>'+blocks(tc)+'</td>' for tc in tr.findall(qn('tc')))+'</tr>')
     a.append('<div class="table-scroll"><table>'+''.join(rows)+'</table></div>')
    elif name in ['sectPr','tcPr','tblPr','tblGrid','bookmarkStart','bookmarkEnd']:pass
    elif name in ['sdt','sdtContent']:a.append(blocks(c))
    elif name in ['sdtPr','sdtEndPr']:pass
    else:raise ValueError('Unsupported block '+name)
   return '\n'.join(a)
  text=blocks(body);fragment=html.fragment_fromstring(text,create_parent=True)
  # Compare character sequence, ignoring layout whitespace; mathematical operators generated from OMML are additional explicit semantics.
  srcwords=''.join(body.xpath('.//w:t/text()',namespaces={'w':W}));prose=html.fragment_fromstring(text,create_parent=True)
  for n in prose.xpath('//math'):n.drop_tree()
  actual=''.join(prose.itertext());norm=lambda s:re.sub(r'\s+','',s)
  assert norm(srcwords)==norm(actual),(book['title'],'text mismatch')
  ids=fragment.xpath('//@id');assert len(ids)==len(set(ids));links=[s[1:] for s in fragment.xpath('//a/@href') if s.startswith('#')];missing=set(links)-set(ids);assert not missing,(book['title'],missing)
  out.parent.mkdir(parents=True,exist_ok=True);out.write_text('<!doctype html><html lang="'+book['language']+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(book['title'])+'</title><style>'+css+'</style></head><body><main data-reader-content>\n'+text+'\n</main></body></html>\n')
  report={'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'canonicalHtmlSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'sourceTextSequencePreserved':True,'internalAnchorsChecked':True,'counts':dict(stats),'mathEquations':len(body.xpath('.//m:oMath',namespaces={'m':M})),'method':'Direct Word XML conversion, ordered prose, inline emphasis, bookmarks, hyperlinks, source images and native MathML; no OCR.'};(work/'source-extraction-review.json').write_text(json.dumps(report,indent=2)+'\n');print(book['title'],report['counts'],flush=True)
