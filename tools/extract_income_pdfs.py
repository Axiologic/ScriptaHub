#!/usr/bin/env python3
"""Extract reviewable HTML candidates from incoming PDFs without publishing them."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "tasks/income-inventory.json"
WORK = ROOT / ".book-work/income-pdf-candidates"


def extract(source: Path) -> list[str]:
    raw = subprocess.check_output(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(source), "-"],
        text=True,
        errors="replace",
    )
    pages = raw.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def paragraphs(page: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", page.strip())
    return [re.sub(r"\s*\n\s*", " ", block).strip() for block in blocks if block.strip()]


def main() -> None:
    entries = json.loads(INVENTORY.read_text(encoding="utf-8"))["sources"]
    reports = []
    for entry in entries:
        if entry["format"] != "pdf" or entry["status"] != "new-book":
            continue
        source = ROOT / entry["source"]
        pages = extract(source)
        if len(pages) != entry["pages"]:
            raise ValueError(f"Page count changed: {source}")
        output = WORK / entry["sha256"][:16]
        output.mkdir(parents=True, exist_ok=True)
        sections = []
        brand_pages = []
        low_text_pages = []
        for number, page in enumerate(pages, start=1):
            if "outfinitygift" in page.lower():
                brand_pages.append(number)
            if len(page.split()) < 12:
                low_text_pages.append(number)
            content = "\n".join(f"<p>{escape(block)}</p>" for block in paragraphs(page))
            sections.append(f'<section data-source-page="{number}">\n{content}\n</section>')
        html = "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><title>Source extraction for editorial review</title></head><body>\n" + "\n".join(sections) + "\n</body></html>\n"
        (output / "source-draft.html").write_text(html, encoding="utf-8")
        report = {
            "source": entry["source"],
            "sha256": entry["sha256"],
            "pageCount": len(pages),
            "wordCount": sum(len(page.split()) for page in pages),
            "brandPagesForReview": brand_pages,
            "lowTextPagesForReview": low_text_pages,
            "draft": (output / "source-draft.html").relative_to(ROOT).as_posix(),
            "status": "extracted-for-review",
        }
        (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        reports.append(report)
    (ROOT / "tasks/income-pdf-extraction.json").write_text(json.dumps({"schemaVersion": 1, "books": reports}, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(reports)} PDF drafts; {sum(r['pageCount'] for r in reports)} pages total")


if __name__ == "__main__":
    main()
