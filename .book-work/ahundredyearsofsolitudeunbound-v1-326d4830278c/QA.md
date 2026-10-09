# A Hundred Years of Solitude Unbound — release QA

- Source `income/A_Hundred_Years_of_Solitude_Unbound/content.pdf`; SHA-256 `326d4830278c6b49a4cef7db47aaa9b4f6d005c75a06f9cb7add3ee25ad2fd8b`. The source remains in `income/` for final cleanup.
- The English full reader was prepared from original essay pages 7–34 and bibliography page 42. Promotional preface, retired appendix and closing invitation were excluded. The short reader follows its introduction, four chapters and conclusion.
- Romanian full translation passes the 72-segment chunk check (chunks 0001–0009); Romanian short translation passes the 20-segment check. All four canonical HTML readers are staged, with no old project branding or promotional copy found.
- The English PDF was produced from the canonical English full HTML, 18 portrait pages. First and last pages were visually inspected; text is legible and bibliography complete. Normalized PDF text matches HTML at a 0.9995 sequence ratio.
- The corrected source cover has no obsolete `15 minutes` badge and was staged using `book_tasks.py cover`, including all eight language derivatives.
- Eight language metadata records each have six source-specific description sentences, at most 14 words per sentence. Ninety editorial discovery phrases occur in the English short reader; the staged manifest has 100 distinct terms in every interface language. Bad proper-name and thematic translations were corrected in the shared incremental cache.
- `python3 tools/book_tasks.py check` reports `Release is ready`. Global `rebuild-keywords`' final catalogue check currently reports a concurrent unpublished manifest and animation template changes that need a shared refresh; the staged book gate itself passes.
