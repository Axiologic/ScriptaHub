from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import shutil,re,json
w=Path(__file__).parent;p=w/'The_Society_That_Selects_Us.docx'; backup=w/'qa/pre-spill-repair.docx'
if not backup.exists():shutil.copy2(p,backup)
with ZipFile(backup) as z:f={n:z.read(n) for n in z.namelist()}
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';ns={'w':W};r=E.fromstring(f['word/document.xml']);chapter=None; changed=[]
for x in r.find('w:body',ns):
 t=''.join(x.xpath('.//w:t/text()',namespaces=ns));m=re.fullmatch(r'CHAPTER (\d+)',t)
 if m:chapter=int(m.group(1))
 elif t in ['PART II','PART III','PART IV','EPILOGUE','APPENDIX','GLOSSARY','BIBLIOGRAPHY']:chapter=None
 if chapter not in {2,3,4,5,6,7,8,20}:continue
 for pr in x.xpath('.//w:pPr',namespaces=ns):
  sp=pr.find('w:spacing',ns)
  if sp is None:continue
  style=pr.find('w:pStyle',ns);sty=style.get('{'+W+'}val') if style is not None else ''
  if sty=='Normal' and not m:
   sp.set('{'+W+'}after','0' if chapter in {4,20} else '30');sp.set('{'+W+'}line','270' if chapter in {4,20} else '276')
  elif sty=='Heading2':
   sp.set('{'+W+'}before','100' if chapter in {4,20} else '140');sp.set('{'+W+'}after','60' if chapter in {4,20} else '80')
  elif sty=='Heading1' and chapter in {4,20}:
   sp.set('{'+W+'}before','80');sp.set('{'+W+'}after','120')
  elif m and chapter in {4,20}:
   sp.set('{'+W+'}before','0');sp.set('{'+W+'}after','40')
 changed.append({'chapter':chapter,'text':t[:70]})
f['word/document.xml']=E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(p,'w',ZIP_DEFLATED) as z:
 for n,v in f.items():z.writestr(n,v)
(w/'qa/spill-repair.json').write_text(json.dumps({'changes':'Only chapters 2–8 and 20: body after-spacing 4pt→1.5pt, leading 1.20→1.15, subheading space bounded locally; fonts, page geometry and text unchanged.','paragraphs':changed},indent=2))
