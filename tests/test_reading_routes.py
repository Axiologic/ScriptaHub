"""Validate generated reading actions against each book's actual format inventory."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit, unquote

DOCS = Path(__file__).resolve().parents[1] / 'docs'

class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

class ReadingRoutesTests(unittest.TestCase):
    def test_every_localized_page_prefers_its_language_then_english(self):
        collection = json.loads((DOCS / 'collection.json').read_text())
        for book in collection['books']:
            for language, edition in book['editions'].items():
                with self.subTest(book=book['id'], language=language):
                    page = DOCS / edition['book']
                    source = page.read_text()
                    elements = Links(source).elements
                    self.assertNotIn('data-book-reading-language', source)
                    self.assertIn('assets/book-view.js?v=', source)
                    self.assertIn('assets/text-show.js?v=', source)
                    self.assertIn('data-text-show', source)
                    for format_name, key in [('read', 'fullContent'), ('short', 'shortContent')]:
                        links = [a for tag, a in elements if 'data-reading-format' in a and a['data-reading-format'] == format_name]
                        target = language if key in edition else 'en'
                        if key not in book['editions'][target]:
                            self.assertEqual(links, [])
                            continue
                        self.assertEqual(len(links), 1)
                        url = urlsplit(links[0]['href'])
                        self.assertTrue(url.path.endswith('reader/index.html'))
                        params = parse_qs(url.query)
                        self.assertEqual(params['language'], [target])
                        self.assertEqual(params['lang'], [language])
                        self.assertEqual(params['format'], [format_name])
                        self.assertEqual((DOCS / 'reader' / params['html'][0]).resolve(), (DOCS / book['editions'][target][key]).resolve())
                    pdfs = [a for _, a in elements if 'data-download-pdf' in a]
                    english_pdf = book['editions']['en'].get('pdf')
                    self.assertEqual(len(pdfs), int(bool(english_pdf)))
                    if pdfs:
                        self.assertEqual((page.parent / unquote(pdfs[0]['href'])).resolve(), (DOCS / english_pdf).resolve())
                    notices = [a for _, a in elements if 'data-translation-notice' in a]
                    missing = next((name for name, key in [('read', 'fullContent'), ('short', 'shortContent')] if key not in edition), None)
                    self.assertEqual(len(notices), int(bool(missing)))
                    if notices:
                        params = parse_qs(urlsplit(notices[0]['href']).query)
                        self.assertEqual(params['target'], [language])
                        self.assertEqual(params['lang'], [language])
                        self.assertEqual(params['format'], [missing])
                        self.assertEqual(params['book'], [book['directory']])

if __name__ == '__main__':
    unittest.main()
