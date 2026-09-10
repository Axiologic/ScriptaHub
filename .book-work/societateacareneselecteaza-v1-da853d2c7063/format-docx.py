from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as E
import copy
w=Path(__file__).parent;p=w/'The_Society_That_Selects_Us.docx';ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
for k,v in ns.items():E.register_namespace(k,v)
def el(k,**attrs):return E.Element('{'+ns[k.split(':')[0]]+'}'+k.split(':')[1],{('{'+ns['w']+'}'+a if k.startswith('w:') else a):str(v) for a,v in attrs.items()})
with ZipFile(p) as z:files={n:z.read(n) for n in z.namelist()}
r=E.fromstring(files['word/document.xml']);b=r.find('w:body',ns);first=b[0];inline=first.find('.//wp:inline',ns)
# Source-specific full-bleed illustrated cover: page-anchored art, independent of body margins.
inline.tag='{'+ns['wp']+'}anchor';inline.attrib.update(simplePos='0',relativeHeight='0',behindDoc='1',locked='0',layoutInCell='1',allowOverlap='1')
inline.insert(0,el('wp:simplePos',x=0,y=0))
for pos,axis in [('positionH','horizontal'),('positionV','vertical')]:
 e=el('wp:'+pos,relativeFrom='page');off=el('wp:posOffset');off.text='0';e.append(off);inline.insert(1 if axis=='horizontal' else 2,e)
for ext in inline.findall('.//wp:extent',ns)+inline.findall('.//a:xfrm/a:ext',ns):ext.set('cx','5486400');ext.set('cy','8229600')
inline.insert(4,el('wp:wrapNone'))
pp=first.find('w:pPr',ns);pp.clear();pp.append(el('w:spacing',before=0,after=0,line=20,lineRule='exact'))
sect=copy.deepcopy(b.find('w:sectPr',ns))
for f in list(sect):
 if f.tag.endswith('}footerReference'):sect.remove(f)
sect.find('w:pgMar',ns).attrib.update({f'{{{ns["w"]}}}{k}':'0' for k in ['top','left','right','bottom','header','footer']});pp.append(sect)
# The next title begins the next section itself; no additional blank-page break.
for e in list(b[1].find('w:pPr',ns)):
 if e.tag.endswith('}pageBreakBefore'):b[1].find('w:pPr',ns).remove(e)
for i,para in enumerate(b.findall('w:p',ns)):
 text=''.join(x.text or '' for x in para.findall('.//w:t',ns));prop=para.find('w:pPr',ns)
 if prop is None:prop=el('w:pPr');para.insert(0,prop)
 style=prop.find('w:pStyle',ns)
 if style is not None and style.get('{'+ns['w']+'}val')=='ScriptaBookSubtitle' and i>3:style.set('{'+ns['w']+'}val','Normal')
 if text.startswith(('CHAPTER ','PART ')) and len(text)<20:prop.append(el('w:keepNext'))
 prop.append(el('w:widowControl'))
# Consistent native table geometry and repeating table headers.
for tbl in b.findall('w:tbl',ns):
 rows=tbl.findall('w:tr',ns);cols=len(rows[0].findall('w:tc',ns));width=6840;cw=width//cols;pr=tbl.find('w:tblPr',ns)
 pr.append(el('w:tblW',w=width,type='dxa'));pr.append(el('w:tblLayout',type='fixed'))
 for ri,row in enumerate(rows):
  rp=row.find('w:trPr',ns)
  if rp is None:rp=el('w:trPr');row.insert(0,rp)
  if ri==0:rp.append(el('w:tblHeader'))
  for td in row.findall('w:tc',ns):
   tp=td.find('w:tcPr',ns)
   if tp is None:tp=el('w:tcPr');td.insert(0,tp)
   for old in tp.findall('w:tcW',ns):tp.remove(old)
   tp.append(el('w:tcW',w=cw,type='dxa'))
files['word/document.xml']=E.tostring(r,encoding='utf-8',xml_declaration=True)
with ZipFile(p,'w',ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
print('Book-specific cover anchoring and paragraph/table geometry applied')
