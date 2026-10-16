#!/usr/bin/env python3
"""Place a short edition-credit line in an inspected blank area of a PDF cover."""
from __future__ import annotations

import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--text', default='(c) Outfinity SRL, Iasi.')
    parser.add_argument('--x', type=float, required=True, help='Left offset in PDF points')
    parser.add_argument('--y', type=float, required=True, help='Bottom offset in PDF points')
    parser.add_argument('--size', type=float, default=9)
    args = parser.parse_args()
    if args.source.resolve() == args.destination.resolve():
        parser.error('Source and destination must differ so the original PDF remains intact')
    source_bytes = args.source.read_bytes()
    reader = PdfReader(BytesIO(source_bytes))
    first = reader.pages[0]
    width, height = float(first.mediabox.width), float(first.mediabox.height)
    if not (0 < args.x < width - 20 and 0 < args.y < height - 20):
        parser.error('Credit coordinates fall outside the first page')
    overlay_bytes = BytesIO()
    page = canvas.Canvas(overlay_bytes, pagesize=(width, height))
    page.setFont('Helvetica', args.size)
    page.setFillColorRGB(0.38, 0.38, 0.38)
    page.drawString(args.x, args.y, args.text)
    page.save()
    overlay_bytes.seek(0)
    first.merge_page(PdfReader(overlay_bytes).pages[0])
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    if reader.metadata:
        writer.add_metadata({key: str(value) for key, value in reader.metadata.items() if value is not None})
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    with args.destination.open('wb') as output:
        writer.write(output)
    receipt = {'source': str(args.source), 'destination': str(args.destination), 'sourceSha256': sha256(source_bytes).hexdigest(), 'resultSha256': sha256(args.destination.read_bytes()).hexdigest(), 'pageCount': len(reader.pages), 'text': args.text, 'x': args.x, 'y': args.y, 'fontSize': args.size}
    args.destination.with_suffix('.edition-credit.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(args.destination)


if __name__ == '__main__':
    main()
