from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import build_books as books

class KeywordSourceTests(unittest.TestCase):
    def test_old_metadata_cannot_introduce_terms_into_a_new_release(self):
        candidates = books.extract_keyword_candidates('A book', 'Quantum archaeology and medieval astronomy.', 'Browser automation uses hardware security keys. Private execution environments support deterministic tools.', 10)
        self.assertTrue(candidates)
        self.assertFalse(any('archaeology' in term or 'astronomy' in term for term in candidates))

    def test_headings_remain_separate_sentences_when_weighted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'short.html'
            path.write_text('<article><h2>Browser automation</h2><h2>Security evaluation</h2><p>Local preprocessing supports private deployment.</p></article>')
            text = books.keyword_source_text(path)
            self.assertNotIn('automation Security', text)
            self.assertIn('automation. Security', text)

if __name__ == '__main__':
    unittest.main()
