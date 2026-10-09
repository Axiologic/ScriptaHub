# Alienation and Innocence: The Catcher in the Rye — release QA

- Source: `income/Alienation_and_Innocence___The_Catcher_in_the_Rye/content.pdf`, SHA-256 `97f35cc78cfaa19855eaab947d7fbd7d826391f6a7b03b06f9f73b5a74c15f5e`.
- Retained original essay: source PDF pages 7–29 (introduction, chapters 1–4, conclusion) and 37–38 (bibliography). Excluded promotional preface, old project annex, rights pages, and duplicate title/closing material.
- English full reader: seven sections, 4,852 words. Token multiset comparison against selected source PDF pages: 99.5% source recall and 99.6% reader precision. Page-break fragments were joined; authorial wording was retained.
- Romanian full reader: 67 translated chunk segments assembled; seven matching sections and 4,532 words.
- English and Romanian short readers: six sections, 909 and 928 words; all chapter links target the corresponding language’s full reader.
- New English PDF: 11 A4 pages, exported from the English canonical HTML. First and final pages visually reviewed; normalized text matches HTML at 99.92% token-sequence similarity.
- Original PDF cover was selected from this delivery and cleaned of the retired brand in the staged images. Source cover hash is recorded in `release.json`.
- Reviewed metadata: localized title, subtitle, six-sentence short description and two-paragraph About Book copy in eight interface languages.
- Reviewed keywords: 90 source-grounded terms plus ten shelf terms, 100 distinct per language. Machine mistranslations of character names and key concepts corrected in the translation cache.
- `python3 tools/book_tasks.py check .book-work/alienationandinnocencethecatcherintherye-v1-97f35cc78cfa` reports `Release is ready`.
- Source PDF remains in `income/` until the coordinated cleanup stage.
