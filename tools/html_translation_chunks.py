#!/usr/bin/env python3
"""Stable local HTML chunks for direct agent translation; no translation service.

Prepare -> fill each JSON segment's translation -> check -> assemble.
Existing work and destinations are never overwritten without --force.
"""
from __future__ import annotations

import argparse
import hashlib
from html import escape, unescape
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

LANGUAGES = ("en", "ro", "fr", "de", "es", "pt", "it", "pl")
TOKEN = re.compile(r"(<!--.*?-->|<[^>]+>)", re.S)
TAG = re.compile(r"<\s*(/?)\s*([\w:-]+)")
MARKER = "<!-- SCRIPTA_TRANSLATION:{id} -->"


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def slots(source: str) -> tuple[str, list[dict]]:
    output, segments, stack = [], [], []
    for token in TOKEN.split(source):
        if token.startswith("<"):
            output.append(token)
            tag = TAG.match(token)
            if tag:
                closing, name = tag.groups(); name = name.lower()
                if closing and name in stack:
                    del stack[len(stack) - 1 - stack[::-1].index(name):]
                elif not closing and not token.endswith("/>") and name not in {"meta", "link", "img", "br", "hr", "input", "source", "wbr"}:
                    stack.append(name)
            continue
        if any(tag in {"script", "style", "code", "pre", "math", "svg"} for tag in stack) or not any(c.isalpha() for c in unescape(token)):
            output.append(token); continue
        prefix, text, suffix = re.match(r"^(\s*)(.*?)(\s*)$", token, re.S).groups()
        segment = {"id": f"t{len(segments) + 1:06d}", "source": unescape(text), "translation": ""}
        segments.append(segment)
        output.append(prefix + MARKER.format(**segment) + suffix)
    return "".join(output), segments


def prepare(source: Path, destination: Path, language: str, work: Path, maximum_words: int = 700, force: bool = False) -> None:
    if maximum_words < 1:
        raise ValueError("maximum-words must be positive")
    if (work / "manifest.json").exists() and not force:
        raise ValueError("Translation work already exists; resume it instead of replacing translations")
    raw = source.read_text(encoding="utf-8")
    raw = re.sub(r'<aside\b[^>]*data-pdf-conversion-warning=["\x27][^"\x27]+["\x27][^>]*>.*?</aside>', '', raw, flags=re.I | re.S)
    raw = re.sub(r'(<html\b[^>]*\blang=)["\x27][^"\x27]+["\x27]', rf'\1"{language}"', raw, count=1, flags=re.I)
    def rebase(match):
        prefix, quote, url = match.groups()
        parsed = urlsplit(unescape(url))
        if not parsed.path or parsed.scheme or parsed.netloc or url.startswith('/'):
            return match[0]
        target = (source.parent / parsed.path).resolve()
        if target == source.resolve():
            target = destination.resolve()
        relative = os.path.relpath(target, destination.parent.resolve())
        if parsed.query: relative += '?' + parsed.query
        if parsed.fragment: relative += '#' + parsed.fragment
        return prefix + quote + escape(relative, quote=True) + quote
    raw = re.sub(r'(\b(?:src|href)\s*=\s*)(["\x27])(.*?)\2', rebase, raw, flags=re.I)
    template, segments = slots(raw)
    chunks, chunk, words = [], [], 0
    for segment in segments:
        count = len(segment["source"].split())
        if chunk and words + count > maximum_words:
            chunks.append(chunk); chunk, words = [], 0
        chunk.append(segment); words += count
    if chunk: chunks.append(chunk)
    (work / "chunks").mkdir(parents=True, exist_ok=True)
    for old in (work / "chunks").glob("*.json"):
        old.unlink()
    (work / "template.html").write_text(template, encoding="utf-8")
    manifest = {"source": str(source.resolve()), "sourceHash": digest(source.read_text(encoding="utf-8")), "destination": str(destination.resolve()), "language": language, "slotCount": len(segments), "chunkCount": len(chunks), "templateHash": digest(template), "sources": {s["id"]: digest(s["source"]) for s in segments}}
    (work / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding="utf-8")
    for index, segments in enumerate(chunks, 1):
        (work / "chunks" / f"{index:04d}.json").write_text(json.dumps({"language": language, "chunk": index, "segments": segments}, ensure_ascii=False, indent=2) + '\n', encoding="utf-8")
    print(f"Prepared {manifest['slotCount']} segments in {len(chunks)} chunks: {work}")


def validate(work: Path) -> tuple[dict, str, dict[str, str]]:
    manifest = json.loads((work / "manifest.json").read_text())
    template = (work / "template.html").read_text(encoding="utf-8")
    if digest(template) != manifest["templateHash"] or digest(Path(manifest["source"]).read_text(encoding="utf-8")) != manifest["sourceHash"]:
        raise ValueError("Source or template changed since preparation")
    translations, errors = {}, []
    for path in sorted((work / "chunks").glob("*.json")):
        payload = json.loads(path.read_text())
        if payload["language"] != manifest["language"]: errors.append(f"Wrong language: {path}")
        for segment in payload["segments"]:
            identifier = segment["id"]
            if identifier in translations or manifest["sources"].get(identifier) != digest(segment["source"]):
                errors.append(f"Duplicate or changed source: {identifier}")
            translation = segment.get("translation", "").strip()
            if not translation: errors.append(f"Untranslated: {path.name}:{identifier}")
            translations[identifier] = translation
    if set(translations) != set(manifest["sources"]): errors.append("Segment set differs from source")
    if errors: raise ValueError('\n'.join(errors))
    return manifest, template, translations


def assemble(work: Path, force: bool = False) -> None:
    manifest, template, translations = validate(work)
    destination = Path(manifest["destination"])
    if destination.exists() and not force: raise ValueError("Destination exists; use --force only for an intended repair")
    for identifier, translation in translations.items():
        template = template.replace(MARKER.format(id=identifier), escape(translation, quote=False))
    if "SCRIPTA_TRANSLATION:" in template: raise ValueError("Unresolved translation marker")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template, encoding="utf-8")
    print(f"Assembled {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("source", type=Path)
    prepare_parser.add_argument("--destination", required=True, type=Path)
    prepare_parser.add_argument("--language", required=True, type=str.lower, choices=LANGUAGES)
    prepare_parser.add_argument("--workdir", required=True, type=Path)
    prepare_parser.add_argument("--maximum-words", type=int, default=700)
    prepare_parser.add_argument("--force", action="store_true")
    for command in ("check", "assemble"):
        p = sub.add_parser(command); p.add_argument("workdir", type=Path)
        if command == "assemble": p.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "prepare": prepare(args.source, args.destination, args.language, args.workdir, args.maximum_words, args.force)
        elif args.command == "assemble": assemble(args.workdir, args.force)
        else:
            manifest, _, _ = validate(args.workdir); print(f"All {manifest['slotCount']} segments are translated")
    except (ValueError, OSError, KeyError) as error:
        print(error, file=sys.stderr); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
