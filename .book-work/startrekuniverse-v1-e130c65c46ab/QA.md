# Star Trek Universe — release QA

- Source: `income/Star_Trek_Universe/content.pdf`, 45 pages, SHA-256 `e130c65c46abbeae025bec6dc205661f084c2f1453b9454e03ddfd02b9b84401`. Source remains in `income/` for final cleanup.
- The English full reader retains the original essay on source pages 8–38 and both bibliography entries on page 45. It excludes the promotional preface and retired AI-author appendix. Long source paragraphs were split only at sentence boundaries; text order and word count were preserved.
- EN/RO full and ten-minute HTML readers are staged. Romanian full translation passes the 56-segment chunk check, and Romanian short passes the 41-segment check. No retired-brand or promotional matches remain in readers.
- The English PDF was generated from canonical English full HTML and has 16 portrait pages. First and last pages were visually inspected; text and bibliography are legible. Normalized PDF text matches HTML at a 0.9997 sequence ratio.
- The source delivery cover has no old project or reading-time badge and was recorded through `book_tasks.py cover` with all eight derivatives.
- Each interface language has six source-specific short-description sentences, at most 13 words per sentence. Ninety reviewed discovery phrases occur in the English short reader; each language has 100 distinct keywords. Important franchise terms were corrected in the incremental translation cache.
- `python3 tools/book_tasks.py check` reports `Release is ready`.
