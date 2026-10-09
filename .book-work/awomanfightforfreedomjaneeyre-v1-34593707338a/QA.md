# A Woman’s Fight for Freedom: Jane Eyre — release QA

- Source: `income/A_Woman_Fight_for_Freedom_Jane_Eyre/content.pdf`, SHA-256 `34593707338a3aaa040ae659c90b4e95a239e26279f14d170bbf088438237a28`.
- Retained original essay: source PDF pages 7–29 (introduction, chapters 1–4, conclusion) and 37–38 (bibliography). Removed rights page, promotional preface, former-project annex, and post-conclusion promotional recommendation list.
- English full reader: seven sections and 4,567 words. Token multiset comparison against selected source pages: 99.47% source recall and 99.55% reader precision. Page-break fragments were joined.
- Romanian full reader: 66 translated chunk segments assembled, with matching section anchors and 3,971 words.
- English and Romanian short readers: six sections, 869 and 887 words, with links to the respective full reader.
- New English PDF: 11 A4 pages exported from canonical English HTML. First and last pages visually reviewed; normalized token-sequence similarity to HTML is 99.91%.
- Cover: the old `15 minutes` badge was removed by a conservative image edit. Full English title, woman, house, field and border remain; all eight staged cover derivatives were regenerated, and new cover hash recorded in `release.json`.
- Authored metadata: localized title, subtitle, six-sentence short description and two-paragraph About Book presentation in eight interface languages.
- Keywords: 90 source-grounded terms plus ten shelf terms, all distinct in each of eight languages. Incorrect machine renderings of named people, places and themes were corrected in the local cache.
- `python3 tools/book_tasks.py check .book-work/awomanfightforfreedomjaneeyre-v1-34593707338a` reports `Release is ready`.
- Original source PDF remains in `income/` for coordinated cleanup.
