#!/usr/bin/env python3
"""Select concrete reader discovery phrases from the finished short reader."""
import hashlib
import json
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("build_books", "tools/build_books.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
work = Path(__file__).resolve().parents[1]
manifest_path = work / "book/manifest.json"
reader = work / "book/en/short_content.html"
source = build.keyword_normalise(build.keyword_source_text(reader))
phrases = [
    "cryptography", "digital money", "banking collapse", "financial crisis",
    "crisis of trust", "deliberate orchestration", "loss of trust", "distributed systems",
    "digital currency", "proof-of-work", "Hashcash", "earlier technical developments",
    "monetary design", "white paper", "housing market", "banks",
    "banking practices", "financial regulation", "housing bubble", "public confidence",
    "centralized finance", "monetary policy", "economic climate", "public launch",
    "launch and acceptance", "risky banking practices", "weak financial regulation",
    "banks and governments", "banking failure", "alternative monetary design",
    "causal link", "historical context", "attacks of September 2001",
    "wars in the Middle East", "United States spending", "loose monetary policy",
    "financial strain", "conventional money", "decentralized alternative",
    "historical setting", "hidden purpose", "sequence of events",
    "orchestration theory", "orchestrated collapse", "new economic order",
    "cryptocurrencies", "traditional monetary systems", "secure system",
    "central banks", "launch environment", "documentary evidence",
    "evidentiary gap", "worldwide crisis", "alternative model",
    "national currencies", "restrictive financial rules", "storing value",
    "transferring money", "conventional banks", "financial alternative",
    "intentional design", "emerging technology", "documented crisis",
    "cryptographic systems", "information and communication", "secure systems",
    "single center", "technical possibility", "technical developments",
    "global events", "established finding", "speculative account", "speculation",
    "concrete evidence", "historical setting", "banking and housing collapse",
    "world economy", "traditional monetary systems", "transparent and secure system",
    "manipulation by governments", "financial rules", "decentralized currency",
    "adoption of cryptocurrency", "recognition and adoption", "public confidence in banks",
    "alternative monetary design", "international events", "financial setting",
    "major banking failure", "centralized banking", "financial regulation",
    "financial systems", "speculative proposal", "forms of digital currency",
    "growth of a housing bubble", "loss of confidence", "financial institutions",
    "unstable national currencies", "restrictive financial rules",
    "technical history", "technical ideas", "cryptography and digital money",
    "proof of work", "decentralization", "economic events",
    "financial collapse", "banking collapse", "monetary systems",
    "centralized institutions", "historical inquiry", "established finding",
]

chosen = []
seen = set()
for phrase in phrases:
    key = build.keyword_normalise(phrase).strip()
    if key in seen or build.keyword_normalise(phrase) not in source or key == build.keyword_normalise("Was the 2008 Crash Planned for Bitcoin?"):
        continue
    chosen.append(phrase)
    seen.add(key)
    if len(chosen) == 90:
        break
if len(chosen) != 90:
    missing = [p for p in phrases if build.keyword_normalise(p).strip() not in source]
    raise SystemExit(f"only {len(chosen)} valid phrases; missing from reader: {missing}")
m = json.loads(manifest_path.read_text(encoding="utf-8"))
m["keywordReview"] = {
    "sourceHash": hashlib.sha256(reader.read_bytes()).hexdigest(),
    "phrases": chosen,
    "reviewedOn": "2026-10-08",
    "method": "source-grounded editorial selection",
}
manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\n".join(f"{i:02d}. {term}" for i, term in enumerate(chosen, 1)))
