from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as E
from html.parser import HTMLParser
import re
w=Path(__file__).parent;p=w/'The_Society_That_Selects_Us.docx';W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';ns={'w':W}
with ZipFile(p) as z:files={n:z.read(n) for n in z.namelist()}
r=E.fromstring(files['word/document.xml']);b=r.find('w:body',ns);seq=list(b);count=0
for i,para in enumerate(seq):
 if para.tag!='{'+W+'}p':continue
 t=''.join(x.text or '' for x in para.findall('.//w:t',ns))
 if re.fullmatch(r'(CHAPTER \d+|PART [IVX]+|PREFACE|EPILOGUE|APPENDIX)',t):
  prop=para.find('w:pPr',ns)
  if prop is None:prop=E.SubElement(para,'{'+W+'}pPr')
  E.SubElement(prop,'{'+W+'}pageBreakBefore');E.SubElement(prop,'{'+W+'}keepNext');count+=1
  if i+1<len(seq):
   nex=seq[i+1].find('w:pPr',ns)
   if nex is not None:
    for e in list(nex):
     if e.tag=='{'+W+'}pageBreakBefore':nex.remove(e)
class Tables(HTMLParser):
 def __init__(self):super().__init__();self.tables=[];self.table=None;self.para=None
 def handle_starttag(self,t,a):
  if t=='table':self.table=[]
  elif t=='p' and self.table is not None:self.para=''
 def handle_data(self,s):
  if self.para is not None:self.para+=s
 def handle_endtag(self,t):
  if t=='p' and self.para is not None:self.table.append(self.para);self.para=None
  elif t=='table':self.tables.append(self.table);self.table=None
v=Tables();v.feed((w/'book/en/full_content.html').read_text())
for table,source in zip(b.findall('w:tbl',ns),v.tables):
 cells=table.findall('.//w:tc',ns)
 if len(cells)!=1:continue
 td=cells[0]
 for old in td.findall('w:p',ns):td.remove(old)
 for i,t in enumerate(source):
  pp=E.SubElement(td,'{'+W+'}p');pr=E.SubElement(pp,'{'+W+'}pPr');E.SubElement(pr,'{'+W+'}spacing',{f'{{{W}}}after':'100',f'{{{W}}}line':'270',f'{{{W}}}lineRule':'auto'})
  run=E.SubElement(pp,'{'+W+'}r');rp=E.SubElement(run,'{'+W+'}rPr');E.SubElement(rp,'{'+W+'}rFonts',{f'{{{W}}}ascii':'Noto Serif',f'{{{W}}}hAnsi':'Noto Serif'});E.SubElement(rp,'{'+W+'}sz',{f'{{{W}}}val':'18'})
  if i==0:E.SubElement(rp,'{'+W+'}b')
  E.SubElement(run,'{'+W+'}t').text=t
files['word/document.xml']=E.tostring(r,encoding='utf-8',xml_declaration=True)
with ZipFile(p,'w',ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
print('moved',count,'labels and repaired seven callout cells')
