from pathlib import Path
from hashlib import sha256
import sys,json
work=Path(__file__).resolve().parent
sys.path.insert(0,str(work.parents[1]/'tools'))
import build_books as builder
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
manifest=load(work/'book/manifest.json')
terms=(work/'discovery-terms.txt').read_text().splitlines()
assert len(terms)==len(set(terms))==90
manifest['keywordReview']={'sourceHash':sha256((work/'book/en/short_content.html').read_bytes()).hexdigest(),'phrases':terms,'reviewedOn':'2026-10-26'}
manifest['shortDescriptionEditorial']={'version':1,'reviewedOn':'2026-10-26','sentences':6,'basis':'Delivered English and Romanian manuscripts; complete readers and chapter-grounded short editions'}
save(work/'book/manifest.json',manifest)
release=load(work/'release.json')
statement={
'en':'© 2026 Sînică Alboaie. This first iteration was donated to scriptahub.com by Sînică Alboaie. Feedback and public contributions are invited. Educational, non-commercial use is permitted.',
'ro':'© 2026 Sînică Alboaie. Această primă iterație a fost donată scriptahub.com de Sînică Alboaie. Așteptăm feedback și contribuții din partea publicului. Este permisă folosirea educativă, necomercială.',
'fr':'© 2026 Sînică Alboaie. Cette première version a été offerte à scriptahub.com par Sînică Alboaie. Les retours et contributions du public sont bienvenus. L’usage éducatif non commercial est autorisé.',
'de':'© 2026 Sînică Alboaie. Diese erste Fassung wurde scriptahub.com von Sînică Alboaie gespendet. Rückmeldungen und Beiträge der Öffentlichkeit sind willkommen. Nichtkommerzielle Bildungsnutzung ist erlaubt.',
'es':'© 2026 Sînică Alboaie. Esta primera versión fue donada a scriptahub.com por Sînică Alboaie. Se esperan comentarios y contribuciones del público. Se permite el uso educativo no comercial.',
'pt':'© 2026 Sînică Alboaie. Esta primeira versão foi doada a scriptahub.com por Sînică Alboaie. São bem-vindos comentários e contribuições do público. É permitido o uso educativo não comercial.',
'it':'© 2026 Sînică Alboaie. Questa prima versione è stata donata a scriptahub.com da Sînică Alboaie. Sono benvenuti commenti e contributi del pubblico. È consentito l’uso educativo non commerciale.',
'pl':'© 2026 Sînică Alboaie. Ta pierwsza wersja została przekazana scriptahub.com przez Sînică Alboaie. Zapraszamy do uwag i wkładu czytelników. Dozwolone jest niekomercyjne wykorzystanie edukacyjne.'}
release['contributors']=[{'authorId':'sinica-alboaie','role':'author','description':statement}]
release['changes']={
'en':'First iteration donated by Sînică Alboaie: complete original English and Romanian readers, ten-minute editions, illustrated cover and downloadable PDFs. Public feedback and contributions are welcome; educational, non-commercial use is permitted.',
'ro':'Prima iterație donată de Sînică Alboaie: textele originale complete în română și engleză, ediții de zece minute, copertă ilustrată și PDF-uri descărcabile. Așteptăm feedback și contribuții publice; este permisă folosirea educativă, necomercială.'}
release['coverSource']['kind']='authored-cover'
release['coverSource']['method']='Built-in image generation; original illustrated cover with full uppercase title and author; source manuscripts inspected, artwork authored for this delivery'
release['validation']={'readerStructureChecked':True,'translationReviewed':True,'metadataReviewed':True,'pdfReviewed':True,'evidence':'qa/pdf/report.json; summary-en/report.json; summary-ro-final/report.json; original supplied EN/RO texts, not translated readers'}
save(work/'release.json',release)
cache=load(builder.KEYWORD_TRANSLATION_CACHE)
for lang,fixes in load(work/'keyword-corrections.json').items():
    cache['translations'][lang].update(fixes)
save(builder.KEYWORD_TRANSLATION_CACHE,cache)
print('Saved reviewed discovery terms, explicit author credits and release notes')
