import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('build_books',Path(__file__).resolve().parents[1]/'tools/build_books.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)

class AnimationMetadataTests(unittest.TestCase):
    def test_missing_animation_is_optional(self):
        self.assertIsNone(build.animation_record({'id':'book'}))

    def test_animation_belongs_to_its_book(self):
        original=build.DOCS
        with tempfile.TemporaryDirectory() as temp:
            build.DOCS=Path(temp)/'docs'
            folder=build.DOCS/'books'/'test'/'book'/'Animation';folder.mkdir(parents=True)
            (folder/'film.shf').write_text('content')
            animation={'language':'en','status':'preview','durationMs':800000,'edition':'edition-1','page':'Animation/index.html','shf':'Animation/film.shf'}
            book={'id':'book','directory':'books/test/book','animation':animation}
            try:
                self.assertEqual(build.animation_record(book)['page'],'books/test/book/Animation/index.html')
                for value in ['../../../../outside.html','../../../animations/film/index.html','../other/Animation/index.html']:
                    animation['page']=value
                    with self.assertRaises(ValueError):build.animation_record(book)
            finally:build.DOCS=original

    def test_entry_is_generated_from_shared_components_for_any_book(self):
        first=build.animation_page({'id':'book-one','title':{'en':'First & Book'},'directory':'books/first/book/book-one'})
        second=build.animation_page({'id':'book-two','title':{'en':'Second'},'directory':'books/second/book-two'})
        for page,identifier in [(first,'book-one'),(second,'book-two')]:
            self.assertIn(f'data-animation-book="{identifier}"',page)
            self.assertIn('assets/animation.js',page)
            self.assertIn('assets/shf/shf-player.js',page)
            self.assertNotIn('<main',page)
            self.assertNotIn('<shf-player',page)
            self.assertNotIn('<script>',page)
            self.assertLess(len(page),1100)
        self.assertIn('First &amp; Book',first)

if __name__=='__main__':unittest.main()
