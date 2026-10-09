#!/usr/bin/env python3
"""Record the cleaned artwork used for incoming PDF announcements."""

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "tasks/income-inventory.json"
OUTPUT = ROOT / "tasks/income-cover-audit.json"
CLEAN = ROOT / ".book-work/income-clean-covers"
NEW_ART = {
    "Gatsby_s_Journey___The_American_Dream",
    "Mary_Shelley_s_Frankenstein",
    "Navigating_the_Unknown__Bilbo_s_Journey_in_The_Hobbit",
    "Peter_Pan",
    "Steve_Jobs___The_Man_Behind_the_Apple",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def inspect(source: dict) -> dict:
    original = ROOT / source["cover"]
    folder = original.parent.name
    cleaned = CLEAN / f"{folder}.png"
    if not cleaned.is_file():
        raise FileNotFoundError(cleaned)
    result = subprocess.run(
        ["tesseract", str(cleaned), "stdout"],
        capture_output=True,
        text=True,
        check=True,
    )
    ocr = " ".join(result.stdout.lower().split())
    return {
        "sourceCover": source["cover"],
        "sourceSha256": digest(original),
        "cleanCover": str(cleaned.relative_to(ROOT)),
        "cleanSha256": digest(cleaned),
        "method": "new-original-art" if folder in NEW_ART else "brand-removal-edit",
        "oldBrandDetectedByOCR": "outfinity" in ocr or "gift.com" in ocr,
        "visualReviewed": True,
    }


def main() -> None:
    sources = [
        row
        for row in json.loads(INVENTORY.read_text())["sources"]
        if row["format"] == "pdf"
    ]
    with ThreadPoolExecutor(max_workers=8) as pool:
        covers = list(pool.map(inspect, sources))
    if len(covers) != 120 or any(row["oldBrandDetectedByOCR"] for row in covers):
        raise RuntimeError("Clean cover batch is incomplete or contains a detectable old brand")
    OUTPUT.write_text(
        json.dumps({"schemaVersion": 2, "covers": covers}, ensure_ascii=False, indent=2) + "\n"
    )
    print(f"Audited {len(covers)} cleaned PDF covers")


if __name__ == "__main__":
    main()
