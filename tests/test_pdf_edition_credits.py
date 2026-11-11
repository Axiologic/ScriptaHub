import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('pdf_renderer', Path(__file__).resolve().parents[1] / 'tools/render_clean_income_pdf.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class EditionCredits(unittest.TestCase):
    def test_print_contents_keeps_links_and_omits_source_page_numbers(self):
        doc = renderer.html.fromstring('<html><body><article><p><b>Example</b></p><h1>Contents</h1><p><a href="#one">Chapter 1</a> 42</p><h1 id="one">Chapter 1</h1><p>The value is 42.</p></article></body></html>')
        self.assertEqual(renderer.prepare_print_front_matter(doc, 'Example'), 1)
        self.assertEqual(doc.xpath('//a')[0].get('href'), '#one')
        self.assertEqual(doc.xpath('//a')[0].tail, '')
        self.assertIn('The value is 42.', doc.text_content())
        self.assertEqual(doc.xpath('//article/p')[0].get('class'), 'book-print-title')

    def test_staged_edition_uses_its_own_number_and_planned_date(self):
        with tempfile.TemporaryDirectory() as folder:
            book = Path(folder)
            (book / 'manifest.json').write_text(json.dumps({'title': {'en': 'Symbolic World Models'}}))
            (book / 'editions.json').write_text(json.dumps({
                'currentEdition': None,
                'editions': [{'id': 'edition-1', 'number': 1, 'status': 'preparing', 'contributors': []}],
            }))
            page = renderer.copyright_page(book, 'ro', 'edition-1', '2026-11-11')
            self.assertIn('Ediția 1', page)
            self.assertIn('2026-11-11', page)
            self.assertIn('Symbolic World Models', page)

    def test_current_edition_is_default_and_missing_selection_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            book = Path(folder)
            (book / 'manifest.json').write_text(json.dumps({'title': {'en': 'Example'}}))
            (book / 'editions.json').write_text(json.dumps({
                'currentEdition': 'edition-2',
                'editions': [{'id': 'edition-2', 'number': 2, 'publishedAt': '2025-03-12', 'contributors': []}],
            }))
            self.assertIn('Edition 2', renderer.copyright_page(book, 'en'))
            self.assertIn('2025-03-12', renderer.copyright_page(book, 'en'))
            with self.assertRaisesRegex(ValueError, 'No recorded copyright edition'):
                renderer.copyright_page(book, 'en', 'edition-3')


if __name__ == '__main__':
    unittest.main()
