#!/usr/bin/env python3
"""Add approved cover art without reflowing a PDF's existing content pages."""
import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def prepend_cover(source, cover, output):
    reader = PdfReader(source)
    page = reader.pages[0]
    width, height = float(page.mediabox.width), float(page.mediabox.height)
    with Image.open(cover) as image:
        # Fit all artwork, rather than stretch or crop the title and author.
        scale = min(width / image.width, height / image.height)
        w, h = image.width * scale, image.height * scale
        buffer = BytesIO()
        drawing = canvas.Canvas(buffer, pagesize=(width, height))
        drawing.drawImage(ImageReader(image), (width-w)/2, (height-h)/2,
                          width=w, height=h, mask='auto')
        drawing.showPage()
        drawing.save()
    buffer.seek(0)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.insert_page(PdfReader(buffer).pages[0], 0)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + '.pending')
    try:
        with temporary.open('wb') as stream:
            writer.write(stream)
        revised = PdfReader(temporary)
        if len(revised.pages) != len(reader.pages) + 1:
            raise ValueError('Unexpected content page count')
        for index, original in enumerate(reader.pages):
            if original.get_contents().get_data() != revised.pages[index+1].get_contents().get_data():
                raise ValueError(f'Content changed on page {index+1}')
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('cover', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    prepend_cover(args.source, args.cover, args.output)
