from pathlib import Path
from lxml import html
import json,collections,hashlib,sys
for arg in sys.argv[1:]:
 w=Path(arg);results={}
 for form in ['full','short']:
  trees=[html.fromstring((w/f'book/{lang}/{form}_content.html').read_bytes()) for lang in ['en','ro']]
  shapes=[collections.Counter(el.tag for el in tree.iter()) for tree in trees];assert shapes[0]==shapes[1],(w,form,shapes)
  for lang,tree in zip(['en','ro'],trees):
   assert tree.get('lang')==lang
   ids=tree.xpath('//@id');assert len(ids)==len(set(ids))
   for src in tree.xpath('//@src'):
    if not src.startswith(('http:','https:','data:')):assert (w/f'book/{lang}'/src).exists(),src
   if form=='short':
    full=html.fromstring((w/f'book/{lang}/full_content.html').read_bytes());targets=set(full.xpath('//@id'))
    for href in tree.xpath('//details//a/@href'):
     assert href=='full_content.html' or href.startswith('full_content.html#'),href
     if '#' in href:assert href.split('#',1)[1] in targets,href
  results[form]=dict(shapes[0])
 if (w/'pdf-qa.json').exists():
  qa=json.loads((w/'pdf-qa.json').read_text());assert qa['status'] in {'passed','passed-with-notes'} and (qa.get('allPageContactSheetsVisuallyReviewed') or qa.get('visualReview',{}).get('allContactSheetsReviewed'));pdfhash=qa['pdfSha256'];sourcehash=qa['sourceHtmlSha256']
 else:
  qa=json.loads((w/'pdf-review.json').read_text());assert qa['status'] in {'passed','passed-with-notes'} and qa['visual_review']['all_pages_rendered'] and qa['visual_review']['contact_sheets_reviewed'];pdfhash=qa['pdf_sha256'];sourcehash=qa['canonical_english_html_sha256'];assert not json.loads((w/'qa/pdf/text-check.json').read_text())['unmatched']
 assert hashlib.sha256((w/'book/en/book.pdf').read_bytes()).hexdigest()==pdfhash
 assert hashlib.sha256((w/'book/en/full_content.html').read_bytes()).hexdigest()==sourcehash
 report=json.loads((w/'summary-en/report.json').read_text());assert report.get('status')=='passed',report
 m=json.loads((w/'book/manifest.json').read_text());assert all(len(k)==100 for k in m['keywords'].values())
 (w/'qa/reader-structure-review.json').write_text(json.dumps(dict(shapes=results,enRoTopologyMatches=True,shortSourceMapLinksVerified=True,pdfReceiptHashVerified=True,summaryValidationPassed=True),indent=2)+'\n');print(w.name,'passed')
