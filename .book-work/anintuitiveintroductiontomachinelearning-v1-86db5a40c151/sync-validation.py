from pathlib import Path
from hashlib import sha256
from lxml import html
from collections import Counter
from zipfile import ZipFile
from lxml import etree
import json,sys,unicodedata,re,subprocess
w=Path(__file__).resolve().parent;root=w.parents[1]
sys.path.insert(0,str(root/'tools'));import build_books as b
release=json.loads((w/'release.json').read_text());public=root/'docs'/release['directory']
receipt={}
for lang,name in [('en','An Intuitive Introduction to Machine Learning.docx'),('ro','O introducere intuitiva in Machine Learning.docx')]:
    doc=html.fromstring((w/f'book/{lang}/full_content.html').read_bytes())
    images=[(w/f'book/{lang}'/n.get('src')).read_bytes() for n in doc.xpath('//img')]
    math=len(doc.xpath('//math'))
    for n in doc.xpath('//head|//math'):n.drop_tree()
    prose=''.join(doc.itertext())
    norm=lambda s:Counter(re.sub(r'\W|\d|_','',unicodedata.normalize('NFKC',s).casefold()))
    pdftext=subprocess.check_output(['pdftotext',str(w/f'book/{lang}/book.pdf'),'-']).decode()
    assert not norm(prose)-norm(pdftext)
    with ZipFile(root/'income'/name) as z:
        x=etree.fromstring(z.read('word/document.xml'))
        source=''.join(x.xpath('//*[local-name()="t" and namespace-uri()="http://schemas.openxmlformats.org/wordprocessingml/2006/main"]/text()'))
        media=[z.read(n) for n in z.namelist() if n.startswith('word/media/')]
    assert not norm(source)-norm(prose)
    assert all(i in media for i in images)
    assert math==len(x.xpath('//*[local-name()="oMath"]'))==36
    for f in ['full_content.html','short_content.html']:
        assert re.sub(r'(?<=>)[ \t]+(?=\n)','',(w/f'book/{lang}'/f).read_text())==(public/lang/f).read_text()
    assert (w/f'book/{lang}/book.pdf').read_bytes()==(public/lang/'book.pdf').read_bytes()
    receipt[lang]={'sourceProseLettersPreserved':True,'pdfProseLettersPreserved':True,'imagesByteIdentical':len(images),'sourceEquationsPreserved':math,'publishedFilesMatchStaging':True}
for p in [w/'book/manifest.json',public/'manifest.json']:
    m=json.loads(p.read_text());digest=sha256((p.parent/'en/short_content.html').read_bytes()).hexdigest()
    m['keywordSourceHash']=digest;m['keywordReview']['sourceHash']=digest
    p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(w/'qa/source-fidelity.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
