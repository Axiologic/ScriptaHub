"""Cover fitting must retain edge artwork after removing export margins."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location('cover_builder', Path(__file__).resolve().parents[1] / 'tools/build_books.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


@unittest.skipUnless(shutil.which('convert'), 'ImageMagick required')
class CoverDerivativesTest(unittest.TestCase):
    def test_wide_export_preserves_both_edges_of_portrait_art(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, cover, thumb = (root / name for name in ('cover.png', 'cover.webp', 'thumbnail.webp'))
            # Empty export area surrounds a typographic cover with content at
            # both edges. A centre crop would lose both coloured title marks.
            image = Image.new('RGB', (900, 700), 'white')
            draw = ImageDraw.Draw(image)
            draw.rectangle((260, 140, 639, 559), fill='#eeeeee')
            draw.rectangle((260, 230, 275, 380), fill='#ff0000')
            draw.rectangle((624, 230, 639, 380), fill='#0000ff')
            image.save(source)
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            builder.create_display_cover(source, cover)
            builder.create_thumbnail(cover, thumb)
            self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())
            for path, size in ((cover, (640, 960)), (thumb, (320, 480))):
                with Image.open(path) as result:
                    self.assertEqual(result.size, size)
                    pixels = list(result.convert('RGB').getdata())
                    self.assertGreater(sum(r > 180 and g < 70 and b < 70 for r, g, b in pixels), 100)
                    self.assertGreater(sum(b > 180 and r < 70 and g < 70 for r, g, b in pixels), 100)


if __name__ == '__main__':
    unittest.main()
