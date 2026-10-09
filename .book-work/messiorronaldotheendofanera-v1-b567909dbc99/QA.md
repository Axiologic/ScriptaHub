# Messi or Ronaldo? The End of an Era — release QA

- Source: `income/Messi_or_Ronaldo__The_End_of_an_Era/content.pdf`, 44 pages, SHA-256 `b567909dbc99ffb9bd1ad88b488262cefe086f9cbe542391f9811a40dda84d19`.
- Original essay retained from pp. 7–37, with its four bibliography entries from p. 44. The title is from p. 2. Excluded p. 3 rights page, pp. 5–6 promotional preface, and pp. 38–43 retired author/project annexes. Source PDF remains in `income/` until final cleanup.
- Full readers: English 7,090 words, Romanian 6,867 words. Romanian was completed as 72/72 stable chunk segments, then assembled. Short readers: English 632 words, Romanian 657 words; Romanian 25/25 segments, then assembled. Each short section links to its matching full section.
- New English PDF generated from canonical English full HTML: 10 A4 pages, text coverage 7,160 PDF words versus 7,168 HTML token words (99.89%). First and final pages inspected visually; bibliography present and legible.
- Clean cover selected from this delivery and recorded in the workspace. It bears the full title, with no former-project branding or reading-time badge.
- Eight interface languages have reviewed title, subtitle, six-sentence description (at most 13 words per sentence), and About Book metadata. Career figures are identified as the 2024 source perspective.
- Ninety source-grounded short-reader discovery terms are reviewed. The local translation cache required editorial correction of football terms before final keyword rebuild; every interface language now has 100 distinct terms.
- `book_tasks.py check` passed, the release was installed at `docs/books/messi/or/ronaldo/the/end/of/an/era/bk-7ebe6ea2a9c442b5/`, and `refresh-covers`, `refresh`, catalogue check, and internal-link audit passed. English and Romanian full/short HTML, English PDF, cover, and edition history are present. Source remains in `income/`.
