#!/usr/bin/env python3
"""Create a print intermediate from canonical English HTML."""
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
source = WORK / "book/en/full_content.html"
target = WORK / "conversion/print.html"
style = """<style>
@page { size: 6in 9in; margin: 0.68in 0.62in 0.66in; }
html { font-family: Georgia, 'Times New Roman', serif; color: #242321; }
body { margin: 0; font-size: 11pt; line-height: 1.43; }
article { max-width: 100%; }
h1 { font-size: 22pt; line-height: 1.15; margin: 0 0 0.8in; text-align: center; break-after: avoid; }
h2 { font-size: 15pt; line-height: 1.2; margin: 0.4in 0 0.13in; break-after: avoid; }
h3 { font-size: 11.5pt; line-height: 1.25; margin: 0 0 0.18in; break-after: avoid; }
p { margin: 0 0 0.13in; orphans: 3; widows: 3; text-align: left; }
h2#preface { margin-top: 0; }
h2#bibliography { margin-top: 0.25in; }
</style>"""
markup = source.read_text(encoding="utf-8").replace("</head>", style + "</head>", 1)
target.write_text(markup, encoding="utf-8")
print(target)
