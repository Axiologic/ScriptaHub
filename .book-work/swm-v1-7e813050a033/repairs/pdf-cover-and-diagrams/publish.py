"""Publish a validated asset-only correction while retaining edition 1 verbatim."""
from pathlib import Path
from hashlib import sha256
import json,shutil,sys
sys.path.insert(0,'tools')
from book_tasks import archive_reader_links
from build_books import LANGUAGES,snapshot_edition_covers,edition_record
W=Path('.book-work/swm-v1-7e813050a033');R=W/'repairs/pdf-cover-and-diagrams'
release=json.loads((W/'release.json').read_text());root=Path('docs')/release['directory']
hp=root/'editions.json';history=json.loads(hp.read_text());manifest=json.loads((root/'manifest.json').read_text())
assert history['currentEdition']=='edition-1','Already promoted or unexpected current edition; inspect before proceeding'
qa=json.loads((R/'verification.json').read_text());old=next(e for e in history['editions'] if e['id']=='edition-1');new=next(e for e in history['editions'] if e['id']=='edition-2')
for lang in ['en','ro']:
 assert qa[lang]['pdfSha256']==sha256((W/f'book/{lang}/book.pdf').read_bytes()).hexdigest()
 assert not qa[lang]['missingTextBlocks'] and not qa[lang]['outsidePageWords']
archive=root/'edition-files/edition-1';assert not (archive/'en.pdf').exists() and not (archive/'ro.pdf').exists()
for lang in LANGUAGES:assert not (archive/lang).exists()
before={'pdf':{},'readers':{}}
for lang in ['en','ro']:
 before['pdf'][lang]=sha256((root/f'{lang}/book.pdf').read_bytes()).hexdigest()
 before['readers'][lang]={kind:sha256((root/lang/name).read_bytes()).hexdigest() for kind,name in [('fullContent','full_content.html'),('shortContent','short_content.html')]}
for lang in LANGUAGES:
 shutil.copytree(root/lang,archive/lang,ignore=shutil.ignore_patterns('book.html'))
shutil.copy2(root/'manifest.json',archive/'book-manifest.json');shutil.copy2(hp,archive/'edition-history.json')
archive_reader_links(root,archive)
for lang,path in list(old['pdf'].items()):
 target=archive/f'{lang}.pdf';shutil.copy2(root/path,target);assert sha256(target.read_bytes()).hexdigest()==before['pdf'][lang]
 old['pdf'][lang]=target.relative_to(root).as_posix()
old['readers']={lang:{kind:f'edition-files/edition-1/{lang}/{name}' for kind,name in [('fullContent','full_content.html'),('shortContent','short_content.html')]} for lang in ['en','ro']}
# Only the English reader and its reviewed artwork change; both PDF downloads gain covers.
shutil.copy2(W/'book/en/full_content.html',root/'en/full_content.html')
shutil.copytree(W/'book/en/assets',root/'en/assets',dirs_exist_ok=True)
for lang in ['en','ro']:shutil.copy2(W/f'book/{lang}/book.pdf',root/f'{lang}/book.pdf')
new.pop('status');new.pop('startedAt');new['publishedAt']=release['publishedAt'];new['pdf']={lang:f'{lang}/book.pdf' for lang in ['en','ro']};new['readers']={lang:{kind:f'{lang}/{name}' for kind,name in [('fullContent','full_content.html'),('shortContent','short_content.html')]} for lang in ['en','ro']}
snapshot_edition_covers(root,new)
history['currentEdition']='edition-2';manifest['currentEdition']='edition-2';manifest.pop('pendingEdition',None);manifest['pdfCover']=json.loads((W/'book/manifest.json').read_text())['pdfCover'];manifest['editions']={lang:edition_record(root,lang) for lang in LANGUAGES}
hp.write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n');(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(R/'publication-receipt.json').write_text(json.dumps({'previousEdition':'edition-1','newEdition':'edition-2','priorHashes':before,'archivedPdfHashes':{lang:sha256((archive/f'{lang}.pdf').read_bytes()).hexdigest() for lang in ['en','ro']},'newPdfHashes':{lang:sha256((root/f'{lang}/book.pdf').read_bytes()).hexdigest() for lang in ['en','ro']},'oldCoverSnapshotsPreserved':True,'manuscriptChanged':False,'sourceSha256':release['sha256']},ensure_ascii=False,indent=2)+'\n')
release['assetRepair']['status']='installed';release['validation'].update(pdfReviewed=True,translationReviewed=True,pdfReport=str(R/'verification.json'),sourceImageNote='Romanian source diagrams are unchanged; all three English diagrams use reviewed SVG variants preserving source nodes, arrows and meanings. Both PDFs embed full-page covers.');(W/'release.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n')
print('Published maintenance edition 2; original PDFs and complete reader assets preserved under edition-files/edition-1/.')
