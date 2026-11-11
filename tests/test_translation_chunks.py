from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import html_translation_chunks as chunks

TEMP_ROOT = Path(__file__).resolve().parents[1] / ".tmp"
TEMP_ROOT.mkdir(exist_ok=True)


class ChunkTests(unittest.TestCase):
    def test_refresh_accepts_reviewed_source_and_retains_budget_and_memory(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as directory:
            root = Path(directory)
            original = root / "original.html"
            original.write_text('<html lang="en"><body><p>Known source phrase.</p><p>Second prior phrase.</p></body></html>')
            work = root / "job"
            chunks.prepare(original, root / "ro/full_content.html", "ro", work, maximum_words=4)
            for file in sorted((work / "chunks").glob("*.json")):
                data = json.loads(file.read_text())
                for segment in data['segments']:
                    segment['translation'] = {'Known source phrase.': 'Formulare sursă cunoscută.', 'Second prior phrase.': 'A doua formulare anterioară.'}[segment['source']]
                file.write_text(json.dumps(data))
            old = json.loads((work / "manifest.json").read_text())
            replacement = root / "reviewed.html"
            replacement.write_text(original.read_text().replace('Second prior phrase.', 'Second repaired phrase.'))
            chunks.refresh(work, replacement)
            current = json.loads((work / "manifest.json").read_text())
            self.assertEqual(current['source'], str(replacement.resolve()))
            self.assertEqual(current['maximumWords'], 4)
            self.assertEqual(current['chunkCount'], 2)
            segments = [s for file in sorted((work / "chunks").glob("*.json")) for s in json.loads(file.read_text())['segments']]
            self.assertEqual(segments[0]['translation'], 'Formulare sursă cunoscută.')
            self.assertEqual(segments[1]['translation'], '')
            previous = work / "previous" / old['sourceHash'][:12]
            self.assertEqual(json.loads((previous / 'manifest.json').read_text())['source'], str(original.resolve()))
            self.assertTrue(all(s['translation'] for file in (previous / 'chunks').glob('*.json') for s in json.loads(file.read_text())['segments']))

    def test_short_reader_links_to_translated_full_reader(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as folder:
            root = Path(folder)
            source = root / 'en/short_content.html'
            source.parent.mkdir()
            source.write_text('<html lang="en"><body><a href="full_content.html#chapter-1">Read chapter</a></body></html>')
            destination = root / 'ro/short_content.html'
            work = root / 'work'
            chunks.prepare(source, destination, 'ro', work)
            path = next((work / 'chunks').glob('*.json'))
            data = json.loads(path.read_text())
            data['segments'][0]['translation'] = 'Citește capitolul'
            path.write_text(json.dumps(data))
            chunks.assemble(work)
            self.assertIn('href="full_content.html#chapter-1"', destination.read_text())
            self.assertNotIn('../en/full_content.html', destination.read_text())

    def test_round_trip_preserves_structure_assets_and_literal_code(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as folder:
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
