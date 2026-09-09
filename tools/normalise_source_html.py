#!/usr/bin/env python3
"""Turn a LibreOffice HTML source export into a reflowable canonical reader.

Retains text, figures, links, headings, tables and inline emphasis. Removes Word
page geometry and font wrappers, which must not constrain web-reader wrapping.
Requires lxml; conversion from DOC/DOCX to HTML is performed by LibreOffice.
"""
from __future__ import annotations

import argparse
from collections import Counter
from html import escape
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile
from xml.etree import ElementTree

from lxml import html

STYLE = """html{color-scheme:light dark}body{margin:0;font:1.1rem/1.7 Georgia,serif}article{max-width:76ch;margin:auto;padding:2rem 1.2rem}p{text-align:justify;margin:0 0 1em}h1,h2,h3,h4{font-family:system-ui,sans-serif;line-height:1.25;text-align:left;margin:1.6em 0 .7em}img,svg{display:block;max-width:100%;height:auto;margin:1.2em auto}table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.9em;overflow-wrap:anywhere}td,th{padding:.55em;border:1px solid #888;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere}a{color:inherit;text-decoration:underline}li{margin:.35em 0}blockquote{margin:1em;padding-left:1em;border-left:3px solid #888}@media print{body{font-size:11pt}article{max-width:none;padding:0}h1,h2,h3{break-after:avoid}img,table{break-inside:avoid}}"""


def docx_html(source: Path, destination: Path, language: str, title: str) -> dict:
    """Fallback for prose DOCX exports rejected by LibreOffice. Fail on unsupported objects."""
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    a = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
    r = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
    with ZipFile(source) as archive:
        document = ElementTree.fromstring(archive.read('word/document.xml'))
        for node in document.iter():
            if node.tag.split('}')[-1] in {'oMath', 'oMathPara', 'object', 'footnoteReference', 'endnoteReference', 'altChunk', 'numPr'}:
                raise ValueError('This document requires a converter that supports equations, objects, notes and numbering')
        relationships = {node.get('Id'): node.get('Target') for node in ElementTree.fromstring(archive.read('word/_rels/document.xml.rels'))}
        figures = []
        def paragraph(node):
            content = []
            for run in node.iter(w + 'r'):
                text = ''.join(escape(child.text or '') if child.tag == w + 't' else '<br>' if child.tag == w + 'br' else ' ' if child.tag == w + 'tab' else '' for child in run)
                props = run.find(w + 'rPr')
                if props is not None:
                    if props.find(w + 'b') is not None: text = '<strong>' + text + '</strong>'
                    if props.find(w + 'i') is not None: text = '<em>' + text + '</em>'
                content.append(text)
                for image in run.iter(a + 'blip'):
                    member = relationships.get(image.get(r + 'embed'))
                    if not member or not member.startswith('media/'):
                        raise ValueError('Unresolved embedded figure')
                    asset = destination.parent / 'assets' / Path(member).name
                    asset.parent.mkdir(parents=True, exist_ok=True)
                    asset.write_bytes(archive.read('word/' + member))
                    content.append(f'<img src="assets/{escape(asset.name)}" alt="" loading="lazy">')
                    figures.append(asset.name)
            content = ''.join(content)
            if not content.strip(): return ''
            style = node.find(w + 'pPr/' + w + 'pStyle')
            name = style.get(w + 'val', '').lower() if style is not None else ''
            tag = 'h1' if name in {'parttitle', 'title', 'heading1'} else 'h2' if name in {'chaptertitle', 'heading2'} else 'h3' if name == 'heading3' else 'p'
            return f'<{tag}>{content}</{tag}>'
        def blocks(parent):
            output = []
            for child in parent:
                if child.tag == w + 'p': output.append(paragraph(child))
                elif child.tag == w + 'tbl':
                    rows = ['<tr>' + ''.join('<td>' + blocks(cell) + '</td>' for cell in row.findall(w + 'tc')) + '</tr>' for row in child.findall(w + 'tr')]
                    output.append('<table>' + ''.join(rows) + '</table>')
                elif child.tag not in {w + 'sectPr', w + 'tcPr'}:
                    raise ValueError(f'Unsupported document block: {child.tag}')
            return '\n'.join(output)
        content = blocks(document.find(w + 'body'))
        plain_source = Counter(re.findall(r'\w+', ' '.join(node.text or '' for node in document.iter(w + 't'))))
        plain_html = Counter(re.findall(r'\w+', ' '.join(html.fragment_fromstring(content, create_parent=True).itertext())))
        if plain_source != plain_html:
            raise ValueError('DOCX extraction changed text')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f'<!doctype html>\n<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{STYLE}</style></head><body><article data-reader-content>\n{content}\n</article></body></html>\n', encoding='utf-8')
    return {'words': sum(plain_source.values()), 'figures': len(figures), 'paragraphs': len(document.findall('.//' + w + 'p'))}


def normalise(source: Path, destination: Path, language: str, title: str, docx: Path | None = None) -> dict:
    document = html.document_fromstring(source.read_bytes())
    body = document.find('body')
    if body is None:
        raise ValueError('Export has no body')
    for node in body.xpath('.//div[@title="header" or @title="footer"]'):
        node.drop_tree()
    for node in body.xpath('.//script | .//style'):
        node.drop_tree()
    before = ' '.join(body.itertext())
    assets = destination.parent / 'assets'
    image_count = 0
    for node in list(body.iter()):
        # Font and positioning wrappers are layout artifacts; preserve inline semantics.
        for attribute in ('style', 'class', 'align', 'valign', 'width', 'height', 'border', 'cellpadding', 'cellspacing', 'bgcolor', 'color', 'face', 'size'):
            node.attrib.pop(attribute, None)
        if node.tag == 'a' and node.get('name') and not node.get('id'):
            node.set('id', node.get('name'))
        if node.tag == 'img':
            parsed = urlsplit(node.get('src', ''))
            if not parsed.scheme and parsed.path:
                original = (source.parent / unquote(parsed.path)).resolve()
                if not original.is_file():
                    raise ValueError(f'Missing source figure: {original}')
                assets.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, assets / original.name)
                node.set('src', 'assets/' + original.name)
            node.set('loading', 'lazy')
            node.set('alt', node.get('alt') or '')
            image_count += 1
        if node.text and node.tag not in {'pre', 'code'}:
            node.text = re.sub(r'\s+', ' ', node.text)
        if node.tail:
            node.tail = re.sub(r'\s+', ' ', node.tail)
    for node in body.xpath('.//font | .//span[not(@id)]'):
        node.drop_tag()
    for node in body.xpath('.//p'):
        if not ''.join(node.itertext()).strip() and not node.xpath('.//img | .//a[@id] | .//svg') and not node.get('id'):
            node.drop_tree()
    content = '\n'.join(html.tostring(node, encoding='unicode') for node in body)
    result = f'<!doctype html>\n<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{STYLE}</style></head><body><article data-reader-content>\n{content}\n</article></body></html>\n'
    words = lambda text: Counter(re.findall(r"\w+", text.casefold()))
    if words(before) != words(' '.join(body.itertext())):
        raise ValueError('Normalisation changed source text')
    if docx:
        with ZipFile(docx) as archive:
            xml = ElementTree.fromstring(archive.read('word/document.xml'))
        ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        source_words = words(' '.join(node.text or '' for node in xml.iter(ns + 't')))
        absent = source_words - words(before)
        if sum(absent.values()) > max(20, sum(source_words.values()) * .005):
            raise ValueError(f'Source export lost text: {sum(absent.values())} words, sample {absent.most_common(15)}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result, encoding='utf-8')
    return {'words': sum(words(before).values()), 'figures': image_count, 'tables': len(body.xpath('.//table')), 'headings': len(body.xpath('.//h1 | .//h2 | .//h3'))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--language', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--docx', type=Path)
    parser.add_argument('--direct-docx', action='store_true', help='Read simple prose DOCX directly if LibreOffice cannot open it')
    args = parser.parse_args()
    print(docx_html(args.source, args.destination, args.language, args.title) if args.direct_docx else normalise(args.source, args.destination, args.language, args.title, args.docx))


if __name__ == '__main__':
    main()
