#!/usr/bin/env python3
"""Render a complete canonical reader as a 6 x 9 inch download PDF.

Default (``WORKDIR``): the staged English reader becomes ``book/en/book.pdf``.
A book delivered in Romanian also gets a Romanian PDF rendered from its
canonical Romanian reader (``--language ro``). Translations never become PDFs.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
from html import escape
import json
import re
from pathlib import Path
from lxml import etree,html
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
COPYRIGHT_LABELS={
    'en':{'heading':'Copyright','rights':'All rights reserved.','edition':'Edition {number} · published {date} on ScriptaHub (scriptahub.com).','title':'Original title: {title}.'},
    'ro':{'heading':'Copyright','rights':'Toate drepturile rezervate.','edition':'Ediția {number} · publicată pe {date} pe ScriptaHub (scriptahub.com).','title':'Titlul în engleză: {title}.'},
}


def statement_text(parts) -> str:
    if isinstance(parts,str):return escape(parts)
    return ''.join(escape(part) if isinstance(part,str) else f'<a href="{escape(part["url"])}">{escape(part["label"])}</a>' for part in parts)


def copyright_page(book:Path,language:str,edition_id:str|None=None,publication_date:str|None=None) -> str:
    """Use the selected staged edition's credits, or the current published edition."""
    labels=COPYRIGHT_LABELS[language]
    history=json.loads((book/'editions.json').read_text())
    selected=edition_id or history['currentEdition']
    edition=next((item for item in history['editions'] if item['id']==selected),None)
    if edition is None:raise ValueError(f'No recorded copyright edition {selected!r} in {book}')
    manifest=json.loads((book/'manifest.json').read_text())
    registry=json.loads((ROOT/'docs/contributors.json').read_text())
    credits=edition.get('contributors') or []
    authors=[registry['authors'][item['authorId']]['name'] for item in credits if item['authorId'] in registry['authors']]
    published=publication_date or edition.get('publishedAt','')
    if not published:raise ValueError('The selected copyright edition needs a publication date')
    year=str(published)[:4]
    statements=[statement_text(registry['statements'][item['statementId']]['description'][language]) for item in credits if item['statementId'] in registry.get('statements',{})]
    lines=[f'<p>© {year} {escape(", ".join(dict.fromkeys(authors)) or "ScriptaHub")}. {labels["rights"]}</p>']
    lines+=[f'<p>{text}</p>' for text in dict.fromkeys(statements)]
    lines.append(f'<p>{escape(labels["edition"].format(number=edition["number"],date=published))}</p>')
    if language!='en':lines.append(f'<p>{escape(labels["title"].format(title=manifest["title"]["en"]))}</p>')
    return f'<section class="copyright-page"><h2>{labels["heading"]}</h2>{"".join(lines)}</section>'


def prepare_print_front_matter(doc,title:str='') -> int:
    """Style a recognized title and omit source pagination from linked contents."""
    paragraphs=doc.xpath('//article/p')
    if paragraphs and title and ' '.join(paragraphs[0].text_content().split())==title:
        paragraphs[0].set('class',(paragraphs[0].get('class','')+' book-print-title').strip())
    removed=0
    for heading in doc.xpath('//h1|//h2'):
        if heading.text_content().strip().casefold() not in {'cuprins','contents','table of contents'}:continue
        for node in heading.itersiblings():
            if node.tag in {'h1','h2'}:break
            for link in node.xpath('.//a[starts-with(@href,"#")]'):
                if link.tail and re.fullmatch(r'\s*\d+\s*',link.tail):
                    link.tail=''
                    removed+=1
    return removed


def add_cover(doc, cover:Path) -> dict:
    """Place complete artwork on its own unnumbered, marginless first page."""
    if not cover.is_file():raise ValueError(f'Missing PDF cover: {cover}')
    section=etree.Element('section',{'class':'pdf-cover','aria-label':'Cover'})
    etree.SubElement(section,'img',{'src':cover.resolve().as_uri(),'alt':'','loading':'eager'})
    doc.find('body').insert(0,section)
    return {'path':str(cover.resolve()),'sha256':sha256(cover.read_bytes()).hexdigest()}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workdir',type=Path,nargs='?',help='Release workspace; renders book/<language>/full_content.html')
    parser.add_argument('--language',default='en',choices=('en','ro'))
    parser.add_argument('--source',type=Path,help='Reader HTML (overrides the workspace path)')
    parser.add_argument('--destination',type=Path,help='PDF path (overrides the workspace path)')
    parser.add_argument('--copyright-book',type=Path,help='Published book directory whose current edition credits form a copyright page')
    parser.add_argument('--cover',type=Path,help='Full-page cover; defaults to the staged manifest pdfCover or cover.png')
    parser.add_argument('--keep-rights-notice',action='store_true',help="Keep an authored book's own English rights notice")
    args=parser.parse_args()
    if not args.workdir and not (args.source and args.destination):parser.error('Give a workspace or --source and --destination')
    work=args.workdir.resolve() if args.workdir else None
    source=(args.source or work/f'book/{args.language}/full_content.html').resolve()
    destination=(args.destination or work/f'book/{args.language}/book.pdf').resolve()
    if not source.is_file():raise SystemExit(f'Missing {args.language} reader')
    markup=source.read_text()
    # The retired OutfinityGift notice must not reach downloads from income deliveries.
    if 'outfinitygift' in markup.lower() or ('all rights reserved' in markup.lower() and not args.keep_rights_notice):raise SystemExit('Retired rights text remains')
    doc=html.fromstring(markup.encode())
    book_manifest=json.loads((args.copyright_book/'manifest.json').read_text()) if args.copyright_book else {}
    staged_manifest=json.loads((work/'book/manifest.json').read_text()) if work and (work/'book/manifest.json').is_file() else {}
    cover=args.cover
    cover_manifest=staged_manifest or book_manifest
    cover_root=work/'book' if staged_manifest else args.copyright_book
    if cover is None and cover_root:
        cover_path=cover_manifest.get('pdfCover',{}).get(args.language)
        if not cover_path:cover_path=cover_manifest.get('editions',{}).get(args.language,{}).get('sourceCover')
        if cover_path:cover=cover_root/cover_path
        elif (source.parent/'cover.png').is_file():cover=source.parent/'cover.png'
    removed_page_labels=prepare_print_front_matter(doc,book_manifest.get('title',{}).get(args.language,''))
    style=etree.SubElement(doc.find('head'),'style')
    style.text='''
@page { size: 6in 9in; margin: .72in .72in .75in;
  @bottom-center { content: counter(page); font: 8pt "Noto Serif"; color: #667070; } }
@page:first { @bottom-center { content: none; } }
@page book-cover { size: 6in 9in; margin: 0; counter-reset: page 0; @bottom-center { content: none; } }
section.pdf-cover { page: book-cover; break-after: page; width: 6in; height: 9in; margin: 0; padding: 0; line-height: 0; }
section.pdf-cover img { display: block; width: 100%; height: 100%; max-width: none; max-height: none; margin: 0; object-fit: contain; }
body { color: #202a2a; font: 10.2pt/1.45 "Noto Serif", serif; }
article { max-width: none; padding: 0; }
h1,h2,h3 { font-family: "Red Hat Display", sans-serif; color: #244e52; break-after: avoid; }
h1 { font-size: 22pt; margin: 30mm 0 8mm; }
h2 { font-size: 14pt; margin: 10mm 0 4mm; }
h3 { font-size: 11pt; margin: 6mm 0 3mm; }
p { margin: 0 0 7pt; text-align: justify; hyphens: auto; orphans: 3; widows: 3; }
p.edition-credit { text-align: left; }
p.book-print-title { font: bold 28pt/1.1 "Red Hat Display", sans-serif; color: #244e52; margin: 30mm 0 12mm; text-align: left; }
section { margin: 0; }
img { max-width: 100%; max-height: 7.3in; height: auto; object-fit: contain; }
figure { margin: 0 0 7pt; break-inside: avoid; }
section.copyright-page { break-before: page; break-after: page; padding-top: 45mm; }
section.copyright-page p { text-align: left; font-size: 8.6pt; }
'''
    if args.copyright_book:
        release=json.loads((work/'release.json').read_text()) if work and (work/'release.json').is_file() else {}
        if release and (ROOT/'docs'/release['directory']).resolve()!=args.copyright_book.resolve():
            raise ValueError('The copyright book must match the staged release')
        page=html.fragment_fromstring(copyright_page(args.copyright_book.resolve(),args.language,release.get('editionId'),release.get('publishedAt')))
        body=doc.find('body')
        # The copyright page follows the title page: insert it before the first
        # contents, front-matter or chapter heading, else before the second
        # heading (titles are often split across two headings).
        headings=list(body.iter('h1','h2'))
        opening=re.compile(r'^\s*(cuprins|contents|cuvânt\s+înainte|foreword|prolog|prologue|prefa|preface|introducere|introduction|not[ăa]\b|note\b|capitolul|chapter|partea|part\b|[0-9]+\.|[IVX]+\.)',re.I)
        target=next((node for node in headings if opening.match(node.text_content())),None)
        if target is None and len(headings)>=2:target=headings[1]
        if target is not None:target.addprevious(page)
        else:body.insert(0,page)
    cover_receipt=add_cover(doc,cover) if cover else None
    # Print intermediates stay in the workspace, never beside published files.
    output=(work/f'publication/{args.language}') if work else ROOT/'.book-work/reports/pdf-builds'/sha256(str(destination).encode()).hexdigest()[:16]
    output.mkdir(parents=True,exist_ok=True)
    print_html=output/'clean-publication.html'
    print_markup=etree.tostring(doc,method='html',encoding='unicode',doctype='<!doctype html>')
    print_markup=re.sub(r'(</(?:p|h[1-6]|table|tr|td|th|section|article|div|body|html|head)>)[ \t]+(?=\n)',r'\1',print_markup)
    print_html.write_text(print_markup,encoding='utf-8')
    HTML(string=print_html.read_text(encoding='utf-8'),base_url=str(source.parent)).write_pdf(str(destination),pdf_tags=True)
    receipt={'sourceHtml':str(source),'sourceHtmlSha256':sha256(source.read_bytes()).hexdigest(),'pdf':str(destination),'pdfSha256':sha256(destination.read_bytes()).hexdigest(),'engine':'WeasyPrint','pageSize':'6 x 9 inches','language':args.language,'input':f'Complete canonical {args.language} HTML reader','omittedSourceContentsPageLabels':removed_page_labels,'cover':cover_receipt}
    (output/'pdf-build.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(destination)


if __name__=='__main__':
    main()
