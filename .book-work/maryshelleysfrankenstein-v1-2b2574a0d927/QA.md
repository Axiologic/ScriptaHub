# Mary Shelley’s Frankenstein — release QA

- Source: `income/Mary_Shelley_s_Frankenstein/content.pdf`, SHA-256 `2b2574a0d927141289cce612487566371705f15521f02f79d83a11952176a9c8`.
- Retained the original retelling on pp. 7–35 and bibliography on p. 42. Excluded pp. 1–6 and 36–41 (rights, promotional preface, retired-project annexes), plus a 15-minute promotion and summary advertisement embedded in the introduction. Source remains in `income/` until final cleanup.
- English full reader: 6,080 words in seven sections. Romanian full reader: 5,561 words, translated as 89/89 stable chunk segments, checked and assembled. English/Romanian ten-minute readers: 576/577 words in six sections, with links to matching full sections.
- New English PDF generated from canonical full HTML: nine A4 pages, 6,149 PDF tokens versus 6,152 HTML tokens (99.95%). First and final pages inspected visually; bibliography present and legible.
- Clean cover from the delivered source is recorded and contains the English title without retired branding or duration badge.
- Reviewed title, subtitle, six-sentence short description, and About Book metadata in all eight interface languages. About Book identifies this as a 2024 retelling, distinct from Shelley’s original novel.
- Ninety source-grounded discovery phrases, reviewed cache corrections, and 100 distinct keywords in each of the eight languages. `book_tasks.py check` reported release ready. The edition was installed at `docs/books/mary/shelleys/frankenstein/bk-8ca6150303fa4cb2/`; `refresh-covers`, `refresh`, catalogue check, and internal-link audit passed. The source remains in `income/`.
