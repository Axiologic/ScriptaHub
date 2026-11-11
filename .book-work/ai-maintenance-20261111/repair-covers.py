"""Prepend approved artwork without reflowing existing mathematical PDF pages."""
from pathlib import Path
from io import BytesIO
from hashlib import sha256
from datetime import date
import json,sys,shutil
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader,PdfWriter
sys.path.insert(0,'tools')
from book_tasks import archive_reader_links
from build_books import snapshot_edition_covers,LANGUAGES
WORK=Path('.book-work/ai-maintenance-20261111');WORK.mkdir(exist_ok=True)
TITLES=['An Intuitive Introduction to Machine Learning','Machines of Understanding Through Circuits','Meta-Rational Pragmatics']
collection=json.loads(Path('docs/collection.json').read_text());ledger=json.loads(Path('tasks/release-progress.json').read_text());install='--install' in sys.argv
reports=[]
notes={
 'en':'Integrated the approved cover into the PDF downloads while preserving every original content page and mathematical layout.',
 'ro':'Coperta aprobată a fost integrată în PDF-urile descărcabile, cu păstrarea tuturor paginilor originale și a aranjării formulelor.',
 'fr':'Couverture approuvée intégrée aux PDF, avec conservation de toutes les pages originales et de la mise en page mathématique.',
 'de':'Freigegebenes Cover in die PDFs integriert; alle ursprünglichen Inhaltsseiten und mathematischen Darstellungen bleiben erhalten.',
 'es':'Portada aprobada integrada en los PDF, conservando todas las páginas originales y la composición matemática.',
 'pt':'Capa aprovada integrada nos PDF, preservando todas as páginas originais e a disposição das fórmulas.',
 'it':'Copertina approvata integrata nei PDF, conservando tutte le pagine originali e la disposizione delle formule.',
 'pl':'Dodano zatwierdzoną okładkę do PDF, zachowując wszystkie oryginalne strony i układ wzorów.'}
for title in TITLES:
 book=next(b for b in collection['books'] if b['title']['en']==title);root=Path('docs')/book['directory'];manifest=json.loads((root/'manifest.json').read_text());history=json.loads((root/'editions.json').read_text());current=next(e for e in history['editions'] if e['id']==history['currentEdition']);folder=WORK/'pdf-covers'/book['id'];folder.mkdir(parents=True,exist_ok=True)
 record=folder/'review.json'
 if install:
  report=json.loads(record.read_text());assert report['previousEdition']==history['currentEdition'],'Edition changed; inspect rather than overwrite'
  archive=root/'edition-files'/current['id'];assert not any((archive/l).exists() for l in LANGUAGES)
  for language,evidence in report['pdfs'].items():
   assert evidence['visualReview']=='passed' and evidence.get('renderedBodyComparison'), 'Rendered review required'
   assert evidence['oldSha256']==sha256((root/current['pdf'][language]).read_bytes()).hexdigest()
   assert evidence['newSha256']==sha256(Path(evidence['candidate']).read_bytes()).hexdigest()
  for language in LANGUAGES:shutil.copytree(root/language,archive/language,ignore=shutil.ignore_patterns('book.html'))
  shutil.copy2(root/'manifest.json',archive/'book-manifest.json');shutil.copy2(root/'editions.json',archive/'edition-history.json');archive_reader_links(root,archive)
  old_paths=dict(current['pdf'])
  for language,pdf in old_paths.items():
   dest=archive/f'{language}.pdf';assert not dest.exists();shutil.copy2(root/pdf,dest);current['pdf'][language]=dest.relative_to(root).as_posix()
  current['readers']={l:{kind:f'edition-files/{current["id"]}/{l}/{name}' for kind,name in [('fullContent','full_content.html'),('shortContent','short_content.html')] if (archive/l/name).exists()} for l in LANGUAGES};current['readers']={l:v for l,v in current['readers'].items() if v}
  number=max(e['number'] for e in history['editions'])+1;new={'id':f'edition-{number}','number':number,'label':{l:label.replace(str(current['number']),str(number)) for l,label in current['label'].items()},'publishedAt':date.today().isoformat(),'changes':notes,'source':current['source'],'contributors':current.get('contributors',[]),'pdf':old_paths,'readers':{l:{kind:path for kind,path in e.items() if kind in ['fullContent','shortContent']} for l,e in manifest['editions'].items() if e.get('fullContent') or e.get('shortContent')},'maintenanceOf':current['id'],'maintenanceKind':'pdf-cover-integration'}
  for language,evidence in report['pdfs'].items():shutil.copy2(evidence['candidate'],root/old_paths[language])
  snapshot_edition_covers(root,new);history['editions'].append(new);history['currentEdition']=new['id'];manifest['currentEdition']=new['id'];(root/'editions.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n');(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  entry=next(e for e in ledger['releases'] if e['bookId']==book['id']);release_file=Path(entry['workdir'])/'release.json';release=json.loads(release_file.read_text());release['editionId']=new['id'];release['pdfCoverMaintenance']={'status':'complete','previousEdition':current['id'],'report':str(record)};release.setdefault('validation',{})['pdfCoverReviewed']=True;release_file.write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n')
  for language,evidence in report['pdfs'].items():shutil.copy2(evidence['candidate'],Path(entry['workdir'])/'book'/language/'book.pdf')
  if title==TITLES[0]:
   for file in ['work/production.json','source/extraction.json']:
    p=Path('presentations/an-intuitive-introduction-to-machine-learning')/file;d=json.loads(p.read_text());d['edition']=new['id'];p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  report['installedEdition']=new['id'];record.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');reports.append(report);print('Installed cover revision:',title,new['id'],flush=True);continue
 report={'title':title,'bookId':book['id'],'previousEdition':current['id'],'pdfs':{},'method':'Clone the existing PDF and prepend one approved image cover; never reflow, translate or rerender original content pages.'}
 for language,pdf in current['pdf'].items():
  original=root/pdf;reader=PdfReader(original);cover=root/manifest['editions'][language]['sourceCover'];im=Image.open(cover);w,h=float(reader.pages[0].mediabox.width),float(reader.pages[0].mediabox.height)
  if abs(im.width/im.height-w/h)>.001:cover=root/manifest['editions'][language]['cover'];im=Image.open(cover)
  buff=BytesIO();page=canvas.Canvas(buff,pagesize=(w,h));page.drawImage(ImageReader(im),0,0,width=w,height=h,mask='auto');page.showPage();page.save();buff.seek(0)
  writer=PdfWriter();writer.clone_document_from_reader(reader);writer.insert_page(PdfReader(buff).pages[0],0);output=folder/f'{language}.pdf'
  with output.open('wb') as f:writer.write(f)
  revised=PdfReader(output);assert len(revised.pages)==len(reader.pages)+1
  for i,oldpage in enumerate(reader.pages):assert oldpage.get_contents().get_data()==revised.pages[i+1].get_contents().get_data(),(title,language,i)
  bookmark_checks=0
  def flatten(items):
   for item in items:
    if isinstance(item,list):yield from flatten(item)
    else:yield item
  # Pair outlines by traversal order, avoiding ambiguity from repeated subsection titles.
  oldoutline=list(flatten(reader.outline));newoutline=list(flatten(revised.outline));assert len(oldoutline)==len(newoutline)
  for a,b in zip(oldoutline,newoutline):
   assert a.title==b.title
   n=reader.get_destination_page_number(a)
   if n is not None and n>=0:assert revised.get_destination_page_number(b)==n+1;bookmark_checks+=1
  report['pdfs'][language]={'original':str(original),'candidate':str(output),'oldSha256':sha256(original.read_bytes()).hexdigest(),'newSha256':sha256(output.read_bytes()).hexdigest(),'cover':str(cover),'coverSha256':sha256(cover.read_bytes()).hexdigest(),'oldPages':len(reader.pages),'newPages':len(revised.pages),'allOriginalContentStreamsIdentical':True,'outlineDestinationsChecked':bookmark_checks,'visualReview':'pending'}
 record.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');reports.append(report);print('Prepared covers without changing content pages:',title,flush=True)
(WORK/'pdf-cover-maintenance.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
