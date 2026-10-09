#!/usr/bin/env python3
"""Select 90 reader-grounded discovery terms, excluding the book title."""
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("build_books", "tools/build_books.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
work = Path(__file__).resolve().parents[1]
reader = work / "book/en/short_content.html"
manifest_path = work / "book/manifest.json"
source = build.keyword_normalise(build.keyword_source_text(reader))
phrases = [
    "French Revolution", "London and Paris", "Reign of Terror", "Bastille",
    "aristocratic power", "family bonds", "political upheaval", "private loyalties",
    "personal redemption", "historical violence", "social change", "compassion",
    "divided past", "Lucie and Darnay", "relationship with Lucie",
    "demand for retribution", "memories of aristocratic violence",
    "inequality and anger", "endurance in prison", "account of justice",
    "cruelty of aristocratic power", "strain of political upheaval",
    "image of renewal", "family in immediate danger", "memory and fear",
    "sense of wasted potential", "act of loyalty", "guided interpretation",
    "justified protest", "difficult return", "unsettled period", "private urgency",
    "damaged person", "moral pressure", "fear and vengeance", "Manette family",
    "spies and opportunists", "trial", "imprisonment",
    "family and community", "oppression and hope", "personal hope",
    "family ties", "return to France", "family's escape", "new victims",
    "means of endurance",
    "rebirth after imprisonment", "sacrifice", "revolutionary fear", "political danger",
    "relative stability", "inequality", "public history", "individual households",
    "banker Jarvis Lorry", "Dr. Manette", "Lucie Manette", "Charles Darnay",
    "Sydney Carton", "Madame Defarge", "eighteen years", "return to life",
    "recalled to life", "renewal", "prisoner", "family",
    "aristocratic cruelty", "oppression", "hope", "social order",
    "trauma", "shoemaking", "memory", "fear", "patient care",
    "recovery", "political past", "French aristocracy", "aristocratic violence",
    "intersecting loyalties", "historical change", "storming of the Bastille",
    "revenge", "retribution", "family name", "spies", "opportunists",
    "trust", "imprisonment and trial",
    "immediate danger", "chosen sacrifice", "guillotine", "loyalty",
    "wasted potential", "family escape", "private courage", "public injustice",
    "grief", "survival", "historical events", "historical fiction",
    "justice", "progress", "love", "humanity", "violence",
    "personal hope", "political danger", "family ties", "return to France",
    "French Revolution", "revolutionary violence", "documentary evidence",
    "private courage", "oppression and hope", "political past",
    "historical forces", "family and community", "political history",
    "Revolution's violence", "public injustice", "historical violence",
    "individual choice", "family's escape", "novel", "interpretation",
    "story", "Dickens", "ending", "complete chapter sequence",
    "tense departure", "social conditions", "public forces",
    "political upheaval", "private loyalties", "human values",
    "Bastille prisoner", "prisoner return", "Dr. Manette's return",
    "London", "Paris", "France", "England", "political conflict",
    "new victims", "aristocratic family", "political revolution",
    "sacrifice and compassion", "revolutionary anger", "historical setting",
]
shelf = {build.keyword_normalise(label).strip() for x in build.SHELF_CATEGORIES.values() for label in x["en"].split("|")}
chosen = []
seen = set()
for phrase in phrases:
    key = build.keyword_normalise(phrase).strip()
    if key in seen or key in shelf or build.keyword_normalise(phrase) not in source or key == build.keyword_normalise("Shadows and Lights: A Tale of Two Cities").strip():
        continue
    chosen.append(phrase)
    seen.add(key)
    if len(chosen) == 90:
        break
if len(chosen) != 90:
    raise SystemExit(f"Only {len(chosen)} valid phrases from English short reader")
m = json.loads(manifest_path.read_text(encoding="utf-8"))
m["keywordReview"] = {"sourceHash": hashlib.sha256(reader.read_bytes()).hexdigest(), "phrases": chosen, "reviewedOn": "2026-10-08", "method": "reader-grounded editorial selection"}
manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\n".join(f"{i:02d}. {phrase}" for i, phrase in enumerate(chosen, 1)))
