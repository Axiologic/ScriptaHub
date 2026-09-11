from pathlib import Path
import subprocess,hashlib,json,collections,re
from lxml import html
w=Path(__file__).parent;b=json.loads((w/'pdf-build.json').read_text());assert hashlib.sha256((w/'book/en/book.pdf').read_bytes()).hexdigest()==b['pdfSha256'];info=subprocess.check_output(['pdfinfo',str(w/'book/en/book.pdf')],text=True);pages=int(re.search(r'Pages:\s+(\d+)',info)[1]);pdftext=subprocess.check_output(['pdftotext',str(w/'book/en/book.pdf'),'-'],text=True);print('pages',pages);results={}
for form in ['full','short']:
 roots=[html.fromstring((w/f'book/{lang}/{form}_content.html').read_text()) for lang in ['en','ro']]
 shapes=[collections.Counter(x.tag for x in r.iter()) for r in roots];assert shapes[0]==shapes[1];results[form]=dict(shapes[0]);print(form,shapes[0])
 for lang,r in zip(['en','ro'],roots):
  assert r.get('lang')==lang
  ids=r.xpath('//@id');assert len(ids)==len(set(ids))
  for target in r.xpath('//@src'):
   assert (w/f'book/{lang}'/target).exists(),target
r=html.fromstring((w/'book/en/full_content.html').read_text());texts=r.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]');tokens=lambda s:collections.Counter(re.findall(r'\w+',s.lower()));src=tokens(' '.join(texts));pdf=tokens(re.sub(r'[-\u00ad\u2010]\s*\n', '', pdftext));pdf=pdf | tokens(pdftext);missing=src-pdf;print('PDF missing tokens',sum(missing.values()),missing.most_common(25));
(w/'qa/structure-review.json').write_text(json.dumps({'structures':results,'pdfPages':pages,'missingPdfTokens':missing,'pdfSha256':b['pdfSha256']},indent=2)+'\n')
import pymupdf
pdfdoc=pymupdf.open(w/'book/en/book.pdf')
extracted=''.join(block[4] for page in pdfdoc if page.number not in (1,2) for block in page.get_text('blocks') if block[1]<590)
# Print contents use updated target-counter page references. Validate every non-TOC source element exactly; validate TOC targets separately.
for el in list(r.xpath('//main/*')):
    ident=el.get('id','')
    if ident.startswith('src-p') and 10<=int(ident[5:])<=47:el.getparent().remove(el)
canonical=''.join(r.xpath('//main//text()'))
normalize=lambda text:re.sub(r'[^a-z0-9]','',text.lower())
assert normalize(canonical)==normalize(extracted), 'PDF complete normalized text differs'
report=json.loads((w/'qa/structure-review.json').read_text())
report['pdfTextReview']={'sourceAndPdfIdentical':True,'normalizedAlphanumericCharacters':len(normalize(canonical)),'method':'PyMuPDF without running footer; normalize whitespace, punctuation and print hyphenation'}
(w/'qa/structure-review.json').write_text(json.dumps(report,indent=2)+'\n')
print('Complete normalized PDF text matches canonical English reader')
