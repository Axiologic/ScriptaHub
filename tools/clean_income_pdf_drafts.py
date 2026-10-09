#!/usr/bin/env python3
"""Remove identifiable OutfinityGift boilerplate from staged PDF HTML drafts.

This is an editorial preparation step, not a publisher. It retains the source
draft and records every removed paragraph's page and text in a private report.
Ambiguous mentions in the book's own text are only flagged for review.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".book-work/income-pdf-candidates"
REPORT = ROOT / "tasks/income-pdf-cleaning.json"

LETTER_HEADING = re.compile(
    r"^(?:annexes\s+)?a\s+letter\s+to\s+(?:the\s+)?readers\s+and\s+supporters(?:\s+of(?:\s+outfinitygift)?)?(?:\s+dear\s+readers\s+and\s+supporters,?)?\s*$",
    re.I,
)
LETTER_END = re.compile(r"(?:(?:sincerely|kind regards),?\s*)?(?:the\s+)?outfinitygift\s+team\s*$", re.I)
NEXT_SECTION = re.compile(r"^(?:bibliography|references|works cited)(?:\s|$)", re.I)
TOC_LINE = re.compile(
    r"(?:a\s+letter\s+to\s+(?:the\s+)?readers\s+and\s+supporters\s+of\s+outfinitygift)\s*\.+\s*\d+",
    re.I,
)
BRAND = re.compile(r"outfinity\s*gift|outfinitygift|outfinitygift\.com", re.I)
SENTENCE_END = re.compile(r"(?<!\bMr)(?<!\bDr)(?<!\bMs)(?<!\bSt)(?<!\bMrs)[.!?][”\"’']?(?:\s+|$)")
CREATIVE_REFERENCE = "income/The_Unwritten_Masterpiece___A_Treatise_on_Literary_Futility_and_the_Illusion_of_Profundity/content.pdf"
CROSS_PAGE_PROJECT = {
    "income/AI_and_the_New_Educational_Frontier/content.pdf": (7, 8, ""),
    "income/Navigating_the_Unknown__Bilbo_s_Journey_in_The_Hobbit/content.pdf": (
        5, 6, "This book introduces Bilbo’s story and explores the themes of personal "
    ),
    "income/The_Mirage_of_Stability_in_Financial_Crisis/content.pdf": (5, 6, ""),
}
# The PDF prefaces sometimes attach a useful description to a project plug.
# Keep that description as an editorial sentence while dropping the plug.
SUBSTANTIVE_REWRITES = {
    ("income/The_Grand_Defiance/content.pdf", 5): "This work examines human resistance and scientific innovation, from quantum physics to space technology and military strategy.",
    ("income/AI_and_The_End_of_Scarcity/content.pdf", 5): "The book examines how human expertise and AI analysis can illuminate the future of scarcity.",
    (CREATIVE_REFERENCE, 6): "This book offers an unconventional, humorous critique of literary value and AI-generated criticism.",
    ("income/A_Quick_Guide_to_Notorious_Conspiracy_Theories/content.pdf", 6): "This book combines AI and human analysis to examine influential conspiracy theories.",
    ("income/The_Ultimate_Slave_Owner_s_Handbook___An_Endless_Ode_to_Servitude/content.pdf", 5): "The Ultimate Slave Owner's Handbook is a satirical experiment in ethical absurdity.",
    ("income/A_Report_on_Secret_Societies_and_Real_Conspiracies/content.pdf", 6): "The book examines institutional power and societal manipulation through historical research and AI analysis.",
    ("income/Exploring_The_Great_Transformation_of_Economic_Thought/content.pdf", 5): "This book combines AI and human expertise to introduce the history of economic thought.",
    ("income/SG_1_Universe/content.pdf", 5): "The book explores interstellar cultures, technological integration, and human development across time and space.",
    ("income/Are_We_Alone__Imagining_Life_with_Aliens/content.pdf", 6): "The book offers a broad, imaginative examination of potential extraterrestrial life.",
    ("income/A_New_Era_of_Finance___The_Bitcoin_Standard/content.pdf", 5): "This work analyzes Bitcoin and blockchain technology.",
    ("income/A_Humorous_Take_on_Mary_Shelley_s_Frankenstein/content.pdf", 5): "The book blends literary analysis with comedic storytelling.",
}


def tidy(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def paragraph_record(p: html.HtmlElement) -> dict:
    section = p.getparent()
    return {
        "page": int(section.get("data-source-page")),
        "text": tidy(p.text_content()),
    }


def branded_sentence_spans(text: str) -> list[tuple[int, int]]:
    """Find full sentences containing the retired brand in an extracted paragraph."""
    ends = [match.end() for match in SENTENCE_END.finditer(text)]
    boundaries = [0, *ends, len(text)]
    spans = []
    for match in BRAND.finditer(text):
        start = max(point for point in boundaries if point <= match.start())
        end = min(point for point in boundaries if point > match.end())
        if spans and start <= spans[-1][1]:
            spans[-1] = (spans[-1][0], max(spans[-1][1], end))
        else:
            spans.append((start, end))
    return spans


def remove_cross_page_project(doc: html.HtmlElement, source: str) -> list[dict]:
    """Resolve three project sentences whose PDF page break interrupts them."""
    if source not in CROSS_PAGE_PROJECT:
        return []
    first_page, second_page, replacement = CROSS_PAGE_PROJECT[source]
    first = doc.xpath(f'//section[@data-source-page="{first_page}"]/p[contains(., "OutfinityGift")]')
    next_page = doc.xpath(f'//section[@data-source-page="{second_page}"]/p[1]')
    if len(first) != 1 or len(next_page) != 1:
        raise ValueError(f"Cross-page project passage changed in {source}")
    p, following = first[0], next_page[0]
    original = tidy(p.text_content())
    starts = branded_sentence_spans(original)
    if len(starts) != 1 or starts[0][1] != len(original):
        raise ValueError(f"Unexpected project clause on page {first_page}: {source}")
    lead = original[: starts[0][0]].rstrip()
    continuation = tidy(following.text_content())
    stop = SENTENCE_END.search(continuation)
    if stop is None:
        raise ValueError(f"Project continuation has no sentence end: {source}")
    removed = original[starts[0][0] :] + " " + continuation[: stop.end()].strip()
    p.text = tidy(lead + " " + replacement)
    following.text = tidy(continuation[stop.end() :])
    return [{
        "reason": "cross-page-project-sentence",
        "pages": [first_page, second_page],
        "removedText": removed,
        "replacementText": replacement.strip(),
    }]


def remove_editorial_promo(doc: html.HtmlElement, source: str) -> list[dict]:
    """Remove brand-bearing promotional sentences from prefaces, with evidence."""
    decisions = remove_cross_page_project(doc, source)
    for p in list(doc.xpath("//section/p")):
        record = paragraph_record(p)
        text = record["text"]
        if not BRAND.search(text):
            continue
        if source == CREATIVE_REFERENCE and record["page"] in {10, 11}:
            decisions.append({
                "reason": "creative-reference-retained",
                "page": record["page"],
                "text": text,
            })
            continue
        spans = branded_sentence_spans(text)
        if any(end == len(text) and not re.search(r"[.!?][”\"’']?$", text[start:end].strip()) for start, end in spans):
            raise ValueError(f"Unfinished branded sentence in {source}, page {record['page']}")
        removed = [text[start:end].strip() for start, end in spans]
        replacement = SUBSTANTIVE_REWRITES.get((source, record["page"]))
        if replacement and len(spans) != 1:
            raise ValueError(f"Expected one project sentence for editorial rewrite: {source}")
        output = text
        for start, end in reversed(spans):
            output = output[:start] + (replacement + " " if replacement else "") + output[end:]
        output = tidy(output)
        decisions.append({
            "reason": "project-promo-sentence-rewritten" if replacement else "project-promo-sentence-removed",
            "page": record["page"],
            "removedText": removed,
            "replacementText": replacement or "",
            "retainedText": output,
        })
        if output:
            p.text = output
        else:
            p.getparent().remove(p)
    return decisions


def clean_one(folder: Path) -> dict:
    source_report = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    original = (folder / "source-draft.html").read_text(encoding="utf-8")
    doc = html.fromstring(original)
    paragraphs = doc.xpath("//section/p")
    rights_pages = {
        int(section.get("data-source-page"))
        for section in doc.xpath("//section[@data-source-page]")
        if any(tidy(p.text_content()).startswith((
            "© 2024 Outfinity SRL, Iași, România. All rights reserved.",
            "© 2024 OutfinityGift. All rights reserved.",
        )) for p in section.xpath("./p"))
    }
    removed: list[dict] = []
    changes: list[dict] = []
    flags: list[dict] = []
    in_letter = False
    letters_found = 0
    letters_ended = 0

    for index, p in enumerate(paragraphs):
        if p.getparent() is None:
            continue
        record = paragraph_record(p)
        text = record["text"]
        page = record["page"]

        # The repeated rights notice occupies a separate page. Remove the
        # complete page, including generic restriction paragraphs left after
        # the old brand header, rather than just its first paragraph.
        if page in rights_pages:
            removed.append({**record, "reason": "former-rights-page"})
            p.getparent().remove(p)
            continue

        # A letter can be followed by a bibliography: stop at that heading.
        if in_letter and NEXT_SECTION.match(text):
            flags.append({"page": page, "reason": "letter-ended-without-signature", "text": text[:200]})
            in_letter = False

        if not in_letter and LETTER_HEADING.match(text):
            in_letter = True
            letters_found += 1

        if in_letter:
            removed.append({**record, "reason": "former-project-letter"})
            p.getparent().remove(p)
            if LETTER_END.search(text):
                in_letter = False
                letters_ended += 1
            continue

        # TOCs are often collapsed into one PDF-extracted paragraph. Remove
        # only the obsolete entry, preserving all neighboring chapter entries.
        changed = TOC_LINE.sub("", text)
        if changed != text:
            changes.append({"page": page, "reason": "former-project-toc-entry", "before": text, "after": tidy(changed)})
            p.text = tidy(changed)
            text = tidy(changed)

        if BRAND.search(text):
            flags.append({"page": page, "reason": "remaining-brand-mention", "text": text[:800]})

    editorial_decisions = remove_editorial_promo(doc, source_report["source"])
    flags = [flag for flag in flags if flag["reason"] != "remaining-brand-mention"]
    for p in doc.xpath("//section/p"):
        record = paragraph_record(p)
        if BRAND.search(record["text"]):
            flags.append({"page": record["page"], "reason": "remaining-brand-mention", "text": record["text"][:800]})

    if in_letter:
        flags.append({"page": source_report["pageCount"], "reason": "letter-reached-end-of-file", "text": ""})
    if not letters_found:
        flags.append({"page": None, "reason": "letter-heading-not-found", "text": ""})
    if letters_found != letters_ended:
        flags.append({"page": None, "reason": "letter-signature-not-found", "text": f"{letters_found} headings; {letters_ended} signatures"})

    # Empty sections are harmless but waste space and confuse later inspection.
    for section in doc.xpath("//section"):
        if not section.xpath("./p"):
            section.getparent().remove(section)

    output = html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n"
    (folder / "clean-draft.html").write_text(output, encoding="utf-8")
    detail = {
        "source": source_report["source"],
        "sha256": source_report["sha256"],
        "sourceDraft": source_report["draft"],
        "cleanDraft": (folder / "clean-draft.html").relative_to(ROOT).as_posix(),
        "sourceParagraphs": len(paragraphs),
        "retainedParagraphs": len(doc.xpath("//section/p")),
        "removed": removed,
        "changed": changes,
        "editorialDecisions": editorial_decisions,
        "flags": flags,
    }
    (folder / "cleaning-report.json").write_text(json.dumps(detail, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {key: value for key, value in detail.items() if key not in {"removed", "changed"}} | {
        "removedCount": len(removed),
        "changedCount": len(changes),
        "editorialDecisionCount": len(editorial_decisions),
        "editorialDecisionReasons": dict(Counter(item["reason"] for item in editorial_decisions)),
        "removedReasons": dict(Counter(item["reason"] for item in removed)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, help="process just one candidate folder")
    args = parser.parse_args()
    folders = [args.workdir] if args.workdir else sorted(WORK.glob("*/report.json"))
    folders = [folder if folder.is_dir() else folder.parent for folder in folders]
    reports = [clean_one(folder) for folder in folders]
    if not args.workdir:
        REPORT.write_text(json.dumps({"schemaVersion": 1, "books": reports}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = Counter(flag["reason"] for report in reports for flag in report["flags"])
    print(f"Cleaned {len(reports)} drafts; removed {sum(r['removedCount'] for r in reports)} paragraphs; flags {dict(counts)}")


if __name__ == "__main__":
    main()
