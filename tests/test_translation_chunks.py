from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import html_translation_chunks as chunks


class ChunkTests(unittest.TestCase):
    def test_round_trip_preserves_structure_assets_and_literal_code(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'en/full_content.html'
            source.parent.mkdir()
            source.write_text('<html lang="en"><head><title>Book</title></head><body><p lang="en-GB">Hello &amp; welcome.</p><img src="images/a.png"><pre>do_not_translate()</pre></body></html>')
            destination = root / 'ro/full_content.html'
            work = root / 'work'
            chunks.prepare(source, destination, 'ro', work)
            with self.assertRaisesRegex(ValueError, 'Untranslated'):
                chunks.assemble(work)
            path = next((work / 'chunks').glob('*.json'))
            data = json.loads(path.read_text())
            for segment, translation in zip(data['segments'], ['Carte', 'Salut & bun venit.'], strict=True):
                segment['translation'] = translation
            path.write_text(json.dumps(data))
            chunks.assemble(work)
            translated = destination.read_text()
            self.assertIn('<html lang="ro">', translated)
            self.assertIn('<p lang="ro">', translated)
            self.assertNotIn('lang="en-GB"', translated)
            self.assertIn('Salut &amp; bun venit.', translated)
            self.assertIn('../en/images/a.png', translated)
            self.assertIn('<pre>do_not_translate()</pre>', translated)
            with self.assertRaisesRegex(ValueError, 'Destination exists'):
                chunks.assemble(work)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                chunks.prepare(source, destination, 'ro', work)
            source.write_text(source.read_text().replace('Hello', 'Goodbye'))
            with self.assertRaisesRegex(ValueError, 'Source or template changed'):
                chunks.validate(work)


if __name__ == '__main__':
    unittest.main()
