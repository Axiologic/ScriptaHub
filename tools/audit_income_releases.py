#!/usr/bin/env python3
"""Validate installed incoming releases without touching source deliveries."""

from collections import Counter
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "fr", "de", "es", "pt", "it", "ro", "pl")
RETIRED = re.compile(r"outfinity\s*gift|outfinitygift|all rights reserved", re.I)


def main() -> None:
    inventory = json.loads((ROOT / "tasks/income-inventory.json").read_text())["sources"]
    by_hash = {entry["sha256"]: entry for entry in inventory}
    collection = json.loads((ROOT / "docs/collection.json").read_text())["books"]
    checked = []
    failures = []
    legacy_source_archives = []
    for book in collection:
        directory = ROOT / "docs" / book["directory"]
        history = json.loads((directory / "editions.json").read_text())
        current = next((edition for edition in history["editions"] if edition["id"] == history["currentEdition"]), None)
        if current is None or current.get("source", {}).get("sha256") not in by_hash:
            continue
        delivery = by_hash[current["source"]["sha256"]]
        if delivery["status"] == "already-installed":
            if "path" in current["source"]:
                legacy_source_archives.append({"book": book["title"]["en"], "path": current["source"]["path"]})
            continue
        # An installer can promote history before the aggregate catalogue is
        # refreshed. Audit the new release after that shared refresh finishes.
        if book.get("publicationStatus") != "published" or book.get("currentEdition") != current["id"]:
            continue
        title = book["title"]["en"]
        problems = []
        if "path" in current["source"]:
            problems.append("redundant source archive")
        if not (directory / current.get("pdf", {}).get("en", "MISSING")).is_file():
            problems.append("missing English PDF")
        else:
            pdf = directory / current["pdf"]["en"]
            if delivery["format"] == "pdf":
                text = subprocess.check_output(["pdftotext", str(pdf), "-"], text=True, errors="replace")
                if RETIRED.search(text):
                    problems.append("retired project or rights notice in PDF")
        for language in ("en", "ro"):
            for kind in ("full_content.html", "short_content.html"):
                reader = directory / language / kind
                if not reader.is_file():
                    problems.append(f"missing {language}/{kind}")
                elif delivery["format"] == "pdf" and RETIRED.search(reader.read_text()):
                    problems.append(f"retired project or rights notice in {language}/{kind}")
        for language in LANGUAGES:
            if len(set(book["keywords"].get(language, []))) != 100:
                problems.append(f"keywords {language} != 100 unique")
        if delivery["format"] == "pdf":
            statements = {credit.get("statementId") for credit in current.get("contributors", [])}
            if not {"incoming-axiologic", "incoming-outfinity"}.issubset(statements):
                problems.append("missing Axiologic/Outfinity contribution credits")
        if problems:
            failures.append({"book": title, "problems": problems})
        checked.append({"book": title, "source": delivery["source"], "format": delivery["format"]})
    report = {
        "schemaVersion": 1,
        "checked": checked,
        "counts": dict(Counter(entry["format"] for entry in checked)),
        "legacySourceArchivesForFinalCleanup": legacy_source_archives,
        "failures": failures,
    }
    (ROOT / "tasks/income-release-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Audited {len(checked)} installed incoming releases; failures: {len(failures)}")
    if failures:
        for failure in failures:
            print(f"{failure['book']}: {', '.join(failure['problems'])}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
