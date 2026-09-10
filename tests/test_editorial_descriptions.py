import json
import tempfile
from unittest.mock import patch
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import build_books
from build_books import editorial_description_problems, LANGUAGES

class EditorialDescriptionsTests(unittest.TestCase):
    def setUp(self):
        self.record = {'id': 'bk-test', 'shortDescriptionEditorial': {'version': 1}, 'shortDescription': {language: 'A specific subject is introduced. A second idea sets its scope. The evidence raises another question. A named method makes it concrete. The argument identifies its central tension. Its limits remain open to examination.' for language in LANGUAGES}}

    def test_six_complete_short_sentences_are_accepted(self):
        self.assertEqual(editorial_description_problems(self.record), [])

    def test_numbered_outline_and_incomplete_fragments_are_rejected(self):
        self.record['shortDescription']['ro'] = '1.1 Ce presupune execuția și unde trebuie trasată limita încrederii 1.2 Decalajul formalizării'
        errors = editorial_description_problems(self.record)
        self.assertTrue(any('six complete' in error for error in errors))
        self.assertTrue(any('outline' in error for error in errors))

    def test_missing_locale_and_overlong_sentence_are_rejected(self):
        del self.record['shortDescription']['pl']
        self.record['shortDescription']['en'] = ' '.join(['Word'] * 23) + '. Two. Three. Four. Five. Six.'
        errors = editorial_description_problems(self.record)
        self.assertTrue(any('eight languages' in error for error in errors))
        self.assertTrue(any('22 words' in error for error in errors))

    def test_legacy_enrichment_cannot_replace_reviewed_descriptions_with_reader_fragments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'manifest.json'
            self.record['editions'] = {'en': {'shortContent': 'toc.html'}}
            path.write_text(json.dumps(self.record))
            (root / 'toc.html').write_text('<p>1.1 A very long numbered contents entry which must never become an editorial description. 1.2 Another chapter heading.</p>')
            before = path.read_bytes()
            with patch.object(build_books, 'BOOKS', root), patch.object(build_books, 'rebuild_collection_from_manifests'), patch.object(build_books, 'refresh_pages'):
                self.assertEqual(build_books.enrich_metadata(), 0)
                self.assertEqual(build_books.recover_editorial_descriptions(), (0, []))
            self.assertEqual(path.read_bytes(), before)

if __name__ == '__main__':
    unittest.main()
