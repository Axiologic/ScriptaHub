from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as E
w=Path(__file__).parent;p=w/'The_Society_That_Selects_Us.docx';W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';ns={'w':W}
with ZipFile(p) as z:f={n:z.read(n) for n in z.namelist()}
r=E.fromstring(f['word/document.xml']);b=r.find('w:body',ns)
for x in b.findall('w:p',ns):
 s=x.find('w:pPr/w:pStyle',ns);sp=x.find('w:pPr/w:spacing',ns)
 if s is not None and s.get('{'+W+'}val')=='Normal' and sp is not None:sp.set('{'+W+'}line','288');sp.set('{'+W+'}after','80')
 if s is not None and s.get('{'+W+'}val')=='ScriptaTOC1':
  pr=x.find('w:pPr',ns);sp=E.SubElement(pr,'{'+W+'}spacing',{f'{{{W}}}after':'60',f'{{{W}}}line':'240',f'{{{W}}}lineRule':'auto'})
for tb in b.findall('w:tbl',ns):
 one=len(tb.findall('.//w:tc',ns))==1
 for tr in tb.findall('w:tr',ns):
  pr=tr.find('w:trPr',ns)
  if pr is None:pr=E.SubElement(tr,'{'+W+'}trPr')
  E.SubElement(pr,'{'+W+'}cantSplit')
 if one:
  for sp in tb.findall('.//w:pPr/w:spacing',ns):sp.set('{'+W+'}after','60');sp.set('{'+W+'}line','250')
f['word/document.xml']=E.tostring(r,encoding='utf-8',xml_declaration=True)
# This manuscript has no code; its unused code style uses the installed text face.
f['word/styles.xml']=f['word/styles.xml'].replace(b'Noto Sans Mono',b'Noto Serif')
with ZipFile(p,'w',ZIP_DEFLATED) as z:
 for n,v in f.items():z.writestr(n,v)
