"""A cover insertion must retain content, links, and bookmark destinations."""
import sys
import unittest
import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from prepend_pdf_cover import prepend_cover

class CoverInsertionTest(unittest.TestCase):
    def test_preserves_pages_and_outline(self):
        scratch = Path(__file__).resolve().parents[1] / '.tmp'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            root = Path(directory)
            body = BytesIO()
            drawing = canvas.Canvas(body, pagesize=(432,648))
            for text in ['Chapter one: x + y = z', 'Chapter two: unchanged']:
                drawing.drawString(40,500,text)
                drawing.linkURL('https://example.com', (40,480,180,520))
                drawing.showPage()
            drawing.save()
            body.seek(0)
            writer = PdfWriter()
            writer.clone_document_from_reader(PdfReader(body))
            writer.add_outline_item('Second chapter',1)
            source = root/'source.pdf'
            with source.open('wb') as stream: writer.write(stream)
            cover = root/'cover.png'
            Image.new('RGB',(432,648),'#215b60').save(cover)
            output = root/'covered.pdf'
            prepend_cover(source,cover,output)
            old,new = PdfReader(source),PdfReader(output)
            self.assertEqual(len(new.pages),3)
            self.assertEqual(new.get_destination_page_number(new.outline[0]),2)
            self.assertEqual(new.outline[0].title,'Second chapter')
            self.assertEqual(len(new.pages[0].images),1)
            for index,page in enumerate(old.pages):
                self.assertEqual(page.get_contents().get_data(),new.pages[index+1].get_contents().get_data())
                self.assertEqual(page.extract_text(),new.pages[index+1].extract_text())
                self.assertEqual(new.pages[index+1]['/Annots'][0].get_object()['/A']['/URI'],'https://example.com')
            self.assertFalse(output.with_suffix('.pdf.pending').exists())

if __name__ == '__main__': unittest.main()
