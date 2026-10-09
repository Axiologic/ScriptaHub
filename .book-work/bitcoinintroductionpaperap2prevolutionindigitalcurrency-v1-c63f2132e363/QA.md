# Bitcoin Introduction Paper — release QA

- Source: `income/Bitcoin_Introduction_Paper_A_P2P_Revolution_in_Digital_Currency/content.pdf`, SHA-256 `c63f2132e363c7a9031057ceea6f571e3b0b1c814a1d6fdf041e0e3552fc2654`.
- Retained original essay: source PDF pages 9–23 (introduction, three chapters, conclusion) and 32 (bibliography). Excluded rights page, promotional preface and former-project author/annex material.
- English full reader: six sections, 2,025 words. Selected source PDF lexical token recall is 99.23%; reader precision is 98.90%. Page-break fragments were joined and literal Markdown emphasis markers removed without altering wording.
- Romanian full reader: 24 translated chunk segments, six corresponding sections, 1,853 words.
- English and Romanian short readers: five sections, 640 and 651 words, with chapter links in the corresponding language.
- New English PDF: five A4 pages exported from the canonical English HTML. First and last pages visually reviewed; normalized token sequence similarity to HTML is 99.78%.
- Cover from this delivery has the full English title and no retired-project branding or duration badge; all eight staged cover derivatives are present.
- Reviewed metadata: localized title, subtitle, six-sentence short description and two-paragraph About Book copy in eight interface languages.
- Ninety English short-read discovery phrases were reviewed and translated locally. Machine mistranslations of technical terms were corrected in the cache. The staged manifest has exactly 100 distinct terms in each of eight languages.
- `python3 tools/book_tasks.py check .book-work/bitcoinintroductionpaperap2prevolutionindigitalcurrency-v1-c63f2132e363` reports `Release is ready`.
- Original source PDF remains in `income/` for coordinated cleanup.
