#!/usr/bin/env python3
"""Record incoming source identities without copying source documents into Git."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
INCOME = ROOT / "income"
OUT = ROOT / "tasks/income-inventory.json"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def normalise(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", value)


def pdf_pages(path: Path) -> int:
    info = subprocess.check_output(["pdfinfo", str(path)], text=True, errors="replace")
    match = re.search(r"^Pages:\s*(\d+)", info, re.M)
    if not match:
        raise ValueError(f"PDF page count unavailable: {path}")
    return int(match[1])


def main() -> None:
    installed = {}
    for path in (ROOT / "docs/books").glob("**/editions.json"):
        history = json.loads(path.read_text(encoding="utf-8"))
        for edition in history.get("editions", []):
            source = edition.get("source") or {}
            if source.get("sha256"):
                installed[source["sha256"]] = {
                    "bookId": history["bookId"],
                    "editionId": edition["id"],
                }
    records = []
    for path in sorted(INCOME.iterdir()):
        if path.is_dir():
            source = path / "content.pdf"
            cover = path / "cover.png"
            if not source.is_file() or not cover.is_file():
                raise ValueError(f"Incomplete PDF delivery: {path}")
            title = path.name.replace("_", " ").strip()
            record = {
                "source": source.relative_to(ROOT).as_posix(),
                "titleFromFolder": title,
                "format": "pdf",
                "sha256": digest(source),
                "pages": pdf_pages(source),
                "cover": cover.relative_to(ROOT).as_posix(),
                "coverSha256": digest(cover),
            }
            if path.name in {"Outfinitism___Redefining_the_Infinity", "Meta_Rationality_as_Wisdom"}:
                record["status"] = "historical-precursor-review"
                record["relatedBookId"] = "bk-bf2a0af6d5194217"
            else:
                record["status"] = "new-book"
            if path.name in {"The_Adventures_of_Ferdinand_Count_Fathom___Part_I", "The_Adventures_of_Ferdinand_Count_Fathom___Part_II"}:
                record["workGroup"] = "the-adventures-of-ferdinand-count-fathom"
        elif path.suffix.lower() in {".doc", ".docx"}:
            record = {
                "source": path.relative_to(ROOT).as_posix(),
                "titleFromFilename": path.stem.replace("_", " ").strip(),
                "format": path.suffix.lower().lstrip("."),
                "sha256": digest(path),
            }
            match = installed.get(record["sha256"])
            record["status"] = "already-installed" if match else "new-book-or-release"
            if match:
                record.update(match)
        else:
            raise ValueError(f"Unexpected item in income: {path}")
        records.append(record)
    payload = {
        "schemaVersion": 1,
        "sourceCount": len(records),
        "rightsDeclaration": "The contributor stated on 2026-10-08 that they represent Axiologic and Outfinity, authored the incoming content, and that the incoming PDF contributions are public domain for ScriptaHub.",
        "cleanupPolicy": "Keep source deliveries until converted readers and final PDFs pass validation; then retain hashes and remove redundant DOCX/source copies.",
        "sources": records,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {len(records)} source identities in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
