import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('translation_chunks', Path(__file__).resolve().parents[1] / 'tools/html_translation_chunks.py')
chunks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chunks)


class LocalizedAssets(unittest.TestCase):
    def test_reviewed_variant_survives_assembly_and_detects_changed_artwork(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, target = root / 'ro', root / 'en'
            source.mkdir(); target.mkdir()
            (source / 'diagram.png').write_bytes(b'original art')
            (target / 'diagram.svg').write_text('<svg>English diagram</svg>')
            manifest = {
                'source': str(source / 'full.html'),
                'destination': str(target / 'full.html'),
                'localizedAssets': [{
                    'source': 'diagram.png', 'localized': 'diagram.svg',
                    'sourceSha256': hashlib.sha256((source / 'diagram.png').read_bytes()).hexdigest(),
                    'localizedSha256': hashlib.sha256((target / 'diagram.svg').read_bytes()).hexdigest(),
                }],
            }
            markup = '<p>The translated prose stays intact.</p><img src="../ro/diagram.png">'
            self.assertEqual(chunks.localize_assets(markup, manifest), '<p>The translated prose stays intact.</p><img src="diagram.svg">')
            (source / 'diagram.png').write_bytes(b'new unreviewed art')
            with self.assertRaisesRegex(ValueError, 'Changed or missing reviewed diagram'):
                chunks.localize_assets(markup, manifest)


if __name__ == '__main__':
    unittest.main()
