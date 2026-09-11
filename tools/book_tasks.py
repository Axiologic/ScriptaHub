#!/usr/bin/env python3
"""Inspect source deliveries and install fully prepared, versioned book releases.

No command translates books. Work is staged outside the public catalogue;
installation requires finished English and Romanian full and short readers.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import unicodedata
import uuid
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "fr", "de", "es", "pt", "it", "ro", "pl")
AUTOMATIC_LANGUAGES = ("en", "ro")
EXTENSIONS = {".pdf", ".doc", ".docx"}
DEFAULT_CONTRIBUTORS = [{"authorId": "axiologic-research", "role": "author", "statementId": "scripta-initial"}]


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower())


def source_name(path: Path) -> tuple[str, int]:
    match = re.fullmatch(r"(.+?)[_\s-]+v([1-9]\d*)", path.stem, re.I)
    return (match[1], int(match[2])) if match else (path.stem, 1)


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def archive_reader_links(target: Path, archive: Path) -> None:
    """Keep each snapshot's reader assets and shared stylesheet links usable."""
    for page in archive.glob("**/*.html"):
        original = target / page.relative_to(archive)
        def rebase(match):
            prefix, quote, value = match.groups()
            parsed = urlsplit(value)
            if not parsed.path or parsed.scheme or parsed.netloc or value.startswith("/"):
                return match[0]
            source_target = (original.parent / unquote(parsed.path)).resolve()
            if source_target.is_relative_to(target.resolve()):
                candidate = archive / source_target.relative_to(target.resolve())
                if candidate.is_file(): source_target = candidate
            relative = os.path.relpath(source_target, page.parent)
            if parsed.query: relative += "?" + parsed.query
            if parsed.fragment: relative += "#" + parsed.fragment
            return prefix + quote + relative + quote
        text = page.read_text(encoding="utf-8")
        page.write_text(re.sub(r'(\b(?:src|href)\s*=\s*)(["\x27])(.*?)\2', rebase, text), encoding="utf-8")


def scan(root: Path = ROOT) -> list[dict]:
    books = [(path.parent, read(path)) for path in sorted((root / "docs/books").glob("**/manifest.json"))]
    records = []
    for source in sorted((root / "tasks").glob("**/*")):
        if not source.is_file() or source.suffix.lower() not in EXTENSIONS or source.name.startswith("~$"):
            continue
        # Only deliveries, never sources already copied into a staging/archive tree.
        if any(part.startswith(".") for part in source.relative_to(root / "tasks").parts):
            continue
        title, version = source_name(source)
        key = normalise(title)
        matches = []
        for directory, book in books:
            aliases = [book["title"]["en"], book.get("sourceId", ""), " ".join(book.get("route", [])), *book.get("sourceAliases", [])]
            if key in {normalise(alias) for alias in aliases if alias}:
                matches.append((directory, book))
        record = {"source": str(source.relative_to(root)), "sha256": sha256(source), "filenameTitle": title.replace("_", " "), "sourceVersion": version, "automaticLanguages": list(AUTOMATIC_LANGUAGES)}
        if len(matches) > 1:
            record.update(status="ambiguous", matches=[book["id"] for _, book in matches])
        elif matches:
            directory, book = matches[0]
            history = read(directory / "editions.json") if (directory / "editions.json").exists() else {"editions": []}
            editions = history["editions"]
            matching = next((item for item in editions if item.get("source", {}).get("sha256") == record["sha256"]), None)
            seen = matching is not None
            current_version = max((int(item.get("source", {}).get("version", item["number"])) for item in editions if item.get("status") != "preparing"), default=0)
            explicit_version = bool(re.search(r"[_\s-]+v[1-9]\d*$", source.stem, re.I))
            if not explicit_version and not seen:
                version = current_version + 1
                record["sourceVersion"] = version
            status = ("preparing" if matching.get("status") == "preparing" else "already-imported") if seen else "new-release" if version > current_version else "version-conflict"
            record.update(status=status, bookId=book["id"], directory=str(directory.relative_to(root / "docs")), currentVersion=current_version)
        else:
            record["status"] = "new-book"
        records.append(record)
    # Distinct files with the same title/version require a deliberate resolution.
    groups: dict[tuple[str, int], list[dict]] = {}
    for item in records:
        groups.setdefault((item.get("bookId", normalise(item["filenameTitle"])), item["sourceVersion"]), []).append(item)
    for items in groups.values():
        if len({item["sha256"] for item in items}) > 1:
            for item in items:
                item["status"] = "ambiguous-source"
    return sorted(records, key=lambda item: (normalise(item["filenameTitle"]), item["sourceVersion"], item["source"]))


def prepare(source: Path, source_language: str, english_title: str | None = None, root: Path = ROOT) -> Path:
    source = source.resolve()
    entry = next((item for item in scan(root) if root / item["source"] == source), None)
    if not entry or entry["status"] not in {"new-book", "new-release", "preparing"}:
        raise ValueError(f"Source is not ready for staging: {entry}")
    work = root / ".book-work" / f"{normalise(entry['filenameTitle'])}-v{entry['sourceVersion']}-{entry['sha256'][:12]}"
    if (work / "release.json").is_file():
        return work
    title = english_title or entry["filenameTitle"]
    if entry["status"] == "new-book":
        identifier = "bk-" + uuid.uuid4().hex[:16]
        words = re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower())
        if not words:
            raise ValueError("An English title is required")
        entry.update(bookId=identifier, directory="/".join(["books", *words, identifier]))
    else:
        manifest = read(root / "docs" / entry["directory"] / "manifest.json")
        title = manifest["title"]["en"]
        write(work / "book" / "manifest.json", manifest)
    entry.update(englishTitle=title, sourceLanguage=source_language, requestedLanguages=[], status="preparing", publishedAt=date.today().isoformat(), changes={"en": "", "ro": ""})
    work.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, work / source.name)
    (work / "book" / source_language).mkdir(parents=True, exist_ok=True)
    write(work / "release.json", entry)
    return work


def announce(work: Path, root: Path = ROOT) -> Path:
    """Make a source delivery discoverable immediately, without claiming it is released."""
    from build_books import BOOK_ACTIONS, PREPARATION_LABELS
    release = read(work / "release.json")
    target = root / "docs" / release["directory"]
    if not target.resolve().is_relative_to((root / "docs/books").resolve()):
        raise ValueError("Invalid book directory")
    if (target / "manifest.json").is_file():
        manifest = read(target / "manifest.json")
        history = read(target / "editions.json")
        if manifest["id"] != release["bookId"]:
            raise ValueError("Book identity differs from staged release")
    else:
        manifest = read(work / "book/manifest.json")
        if manifest["id"] != release["bookId"]:
            raise ValueError("Book identity differs from staged release")
        manifest.update(publicationStatus="preparing", currentEdition=None)
        manifest["availableLanguages"] = []
        for code in LANGUAGES:
            folder = target / code
            folder.mkdir(parents=True, exist_ok=True)
            for name in ("cover.png", "cover.webp", "thumbnail.webp"):
                shutil.copy2(work / "book" / code / name, folder / name)
            manifest["editions"][code] = {key: value for key, value in manifest["editions"][code].items() if key not in {"pdf", "fullContent", "shortContent"}}
        history = {"schemaVersion": 1, "bookId": release["bookId"], "currentEdition": None, "editions": []}
    pending = next((entry for entry in history["editions"] if entry.get("source", {}).get("sha256") == release["sha256"]), None)
    if pending and pending.get("status") != "preparing":
        return target
    if pending is None:
        number = max((entry["number"] for entry in history["editions"]), default=0) + 1
        pending = {"id": f"edition-{number}", "number": number, "status": "preparing", "startedAt": date.today().isoformat(), "label": {code: re.sub(r"1$", str(number), BOOK_ACTIONS[code]["editionLabel"]) for code in LANGUAGES}, "changes": {code: PREPARATION_LABELS[code][0] for code in LANGUAGES}, "source": {"filename": Path(release["source"]).name, "version": release["sourceVersion"], "sha256": release["sha256"]}, "pdf": {}, "contributors": release.get("contributors") or DEFAULT_CONTRIBUTORS}
        history["editions"].append(pending)
    manifest["pendingEdition"] = pending["id"]
    from build_books import snapshot_edition_covers
    snapshot_edition_covers(target, pending, work / "book", refresh_pending=True)
    manifest["sourceAliases"] = sorted(set(manifest.get("sourceAliases", []) + [source_name(Path(release["source"]))[0]]))
    write(target / "manifest.json", manifest)
    write(target / "editions.json", history)
    release["editionId"] = pending["id"]
    write(work / "release.json", release)
    return target


def record_progress(root: Path = ROOT) -> Path:
    """Rebuild a durable handover from sources, public entries and actual chunk files."""
    rows = []
    for path in sorted((root / ".book-work").glob("*/release.json")):
        release = read(path)
        work = path.parent
        public = root / "docs" / release["directory"]
        readers = {code: {name: (work / "book" / code / name).is_file() for name in ("full_content.html", "short_content.html")} for code in AUTOMATIC_LANGUAGES}
        translations = []
        for manifest in sorted((work / "translations").glob("**/manifest.json")):
            info = read(manifest)
            chunks = [read(chunk) for chunk in sorted((manifest.parent / "chunks").glob("*.json"))]
            next_chunk = next((f"{chunk['chunk']:04d}.json" for chunk in chunks if any(not s.get("translation", "").strip() for s in chunk["segments"])), None)
            translations.append({"language": info["language"], "workdir": str(manifest.parent.relative_to(root)), "chunksComplete": sum(all(s.get("translation", "").strip() for s in chunk["segments"]) for chunk in chunks), "chunkCount": len(chunks), "segmentsComplete": sum(bool(s.get("translation", "").strip()) for chunk in chunks for s in chunk["segments"]), "segmentCount": info["slotCount"], "nextChunk": next_chunk})
        meta = read(work / "book/manifest.json") if (work / "book/manifest.json").is_file() else {}
        short_source = work / "book/en/short_content.html"
        keyword_ready = len(meta.get("keywordIds", [])) == 100 and short_source.is_file() and meta.get("keywordSourceHash") == sha256(short_source)
        rows.append({"source": release["source"], "sha256": release["sha256"], "bookId": release["bookId"], "title": release["englishTitle"], "sourceVersion": release["sourceVersion"], "editionId": release.get("editionId"), "status": release["status"], "workdir": str(work.relative_to(root)), "bookPage": f"docs/{release['directory']}/en/book.html", "pageVisible": (public / "en/book.html").is_file(), "readers": readers, "translations": translations, "keywordCount": len(meta.get("keywordIds", [])), "keywordsRefreshed": keyword_ready, "englishPdfReady": (work / "book/en/book.pdf").is_file(), "validation": release.get("validation", {}), "coverSource": release.get("coverSource")})
    write(root / "tasks/release-progress.json", {"updatedAt": date.today().isoformat(), "releases": rows})
    lines = ["# Book release work — persistent handover", "", "Regenerate with `python3 tools/book_tasks.py status`. Resume the recorded workspaces; do not create new IDs or restart translated chunks.", "", "Policy: show new books and pending edition entries immediately as **In preparation**; existing book pages stay free of pending-release notices. Complete EN/RO full and short readers, metadata, 100 keywords, covers and PDF QA before promoting a release. Other reader languages require a request. Preserve all older downloads.", ""]
    for row in rows:
        lines += [f"## {row['title']} — source v{row['sourceVersion']}", "", f"- Source: `{row['source']}`", f"- SHA-256: `{row['sha256']}`", f"- Book ID: `{row['bookId']}`; edition: `{row['editionId'] or 'not yet announced'}`", f"- Workspace: `{row['workdir']}`", f"- [{'x' if row['pageVisible'] else ' '}] Visible book page: `{row['bookPage']}`"]
        for code, formats in row["readers"].items():
            for name, ready in formats.items():
                lines.append(f"- [{'x' if ready else ' '}] {code.upper()} {name}")
        for translation in row["translations"]:
            lines.append(f"- Translation `{translation['workdir']}`: **{translation['chunksComplete']}/{translation['chunkCount']} chunks**, {translation['segmentsComplete']}/{translation['segmentCount']} segments complete.")
            if translation["nextChunk"]:
                lines.append(f"  Resume at `{translation['nextChunk']}`; preserve already filled segments.")
        validation = row["validation"]
        lines += [f"- [{'x' if row['keywordsRefreshed'] else ' '}] Refresh 100 keywords per interface language from this release's English short reader (staged count: {row['keywordCount']})", f"- [{'x' if row['englishPdfReady'] else ' '}] English PDF staged"]
        checks = [
            (validation.get("pdfReviewed"), "Inspect representative PDF pages, including figures and tables."),
            (validation.get("readerStructureChecked") and validation.get("translationReviewed"), "Verify reader structure, local images and translation completeness against the source."),
            (validation.get("metadataReviewed"), "Refresh descriptions, About Book and release notes in all interface languages."),
            (bool(row.get("coverSource")), "Inspect and record this delivery's cover; preserve historical covers."),
            (row["status"] == "installed", "Install the staged edition and preserve historical readers and downloads."),
            (validation.get("catalogueChecked") and validation.get("linksChecked"), "Refresh catalogue and pass catalogue and internal-link checks."),
        ]
        lines += [f"- [{'x' if ready else ' '}] {label}" for ready, label in checks]
        if not validation.get("browserLayoutReviewed"):
            lines.append("- Browser layout review pending: no browser is currently exposed to the UI tool; source structure and styles can be checked independently.")
        lines.append("")
    destination = root / "tasks/RELEASE-PROGRESS.md"
    destination.write_text("\n".join(lines), encoding="utf-8")
    return destination


def stage_cover(work: Path, artwork: Path, root: Path = ROOT) -> None:
    """Select the cover extracted and visually checked from this source delivery."""
    from build_books import create_display_cover, create_thumbnail
    release = read(work / "release.json")
    artwork = artwork.resolve()
    if not artwork.is_file() or artwork.suffix.lower() != ".png":
        raise ValueError("Provide the inspected PNG cover extracted from this delivery")
    for code in LANGUAGES:
        folder = work / "book" / code
        folder.mkdir(parents=True, exist_ok=True)
        if artwork != (folder / "cover.png").resolve():
            shutil.copy2(artwork, folder / "cover.png")
        create_display_cover(folder / "cover.png", folder / "cover.webp")
        create_thumbnail(folder / "cover.webp", folder / "thumbnail.webp")
    release["coverSource"] = {"path": str(artwork.relative_to(root.resolve())), "sha256": sha256(artwork), "deliverySha256": release["sha256"]}
    write(work / "release.json", release)


def validate_stage(work: Path, root: Path = ROOT) -> list[str]:
    from html.parser import HTMLParser
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(); self.text = []
        def handle_data(self, value):
            self.text.append(value)
    release = read(work / "release.json")
    errors = []
    source = root / release["source"]
    if not source.is_file() or sha256(source) != release["sha256"]:
        errors.append("Source delivery changed after staging")
    artwork = release.get("coverSource", {})
    artwork_path = root / artwork.get("path", "")
    if artwork.get("deliverySha256") != release["sha256"] or not artwork_path.is_file() or sha256(artwork_path) != artwork.get("sha256"):
        errors.append("Select and record the inspected cover from this source delivery with the cover command")
    for code in LANGUAGES:
        staged_cover = work / "book" / code / "cover.png"
        if staged_cover.is_file() and sha256(staged_cover) != artwork.get("sha256"):
            errors.append(f"Staged {code} cover differs from this delivery's selected artwork")
    permitted = set(AUTOMATIC_LANGUAGES) | set(release.get("requestedLanguages", []))
    if not permitted.issubset(LANGUAGES):
        errors.append("Unsupported requested language")
    for language in LANGUAGES:
        for name in ("full_content.html", "short_content.html"):
            path = work / "book" / language / name
            if language in permitted and not path.is_file():
                errors.append(f"Missing finished reader: {language}/{name}")
            elif path.is_file():
                if language not in permitted:
                    errors.append(f"Translation not requested: {language}/{name}")
                source_html = path.read_text(encoding="utf-8")
                parsed = Text(); parsed.feed(source_html)
                if len(" ".join(parsed.text).split()) < 100 or "TRANSLATION:" in source_html:
                    errors.append(f"Incomplete reader: {language}/{name}")
                if not re.search(rf'<html\b[^>]*\blang=[\"\x27]{language}(?:-[\w]+)?[\"\x27]', source_html, re.I):
                    errors.append(f"Incorrect HTML language: {language}/{name}")
    manifest_path = work / "book/manifest.json"
    if not manifest_path.is_file():
        errors.append("Missing authored manifest")
    else:
        manifest = read(manifest_path)
        short_source = work / "book/en/short_content.html"
        if not short_source.is_file() or manifest.get("keywordSourceHash") != sha256(short_source):
            errors.append("Discovery keywords must be refreshed from this release's English short reader")
        if manifest.get("id") != release["bookId"]:
            errors.append("Manifest book ID differs from staged release")
        from build_books import about_book_section, title_route
        route = list(title_route(manifest.get("title", {}).get("en", "")))
        if manifest.get("route") != route or release["directory"] != "/".join(["books", *route, release["bookId"]]):
            errors.append("Manifest route differs from the English title or staged directory")
        ids = manifest.get("keywordIds", [])
        if len(ids) != 100 or len(set(ids)) != 100:
            errors.append("Expected 100 distinct keyword identifiers")
        for language in LANGUAGES:
            for field in ("title", "subtitle", "shortDescription", "aboutBook"):
                if not manifest.get(field, {}).get(language):
                    errors.append(f"Missing {language} {field}")
            try:
                about_book_section(manifest, language)
            except ValueError as error:
                errors.append(str(error))
            keywords = manifest.get("keywords", {}).get(language, [])
            if len(keywords) != 100 or len({normalise(word) for word in keywords}) != 100:
                errors.append(f"Expected 100 distinct {language} keywords")
            for name in ("cover.png", "cover.webp", "thumbnail.webp"):
                if not (work / "book" / language / name).is_file():
                    errors.append(f"Missing cover asset: {language}/{name}")
    if not all(release.get("changes", {}).get(code) for code in AUTOMATIC_LANGUAGES):
        errors.append("English and Romanian release notes are required")
    if not (work / "book/en/book.pdf").is_file():
        errors.append("Missing English PDF download")
    return errors


def install(work: Path, root: Path = ROOT) -> Path:
    """Validate before mutation, archive the entire old release, then install prepared files."""
    errors = validate_stage(work, root)
    if errors:
        raise ValueError("\n".join(errors))
    release = read(work / "release.json")
    target = root / "docs" / release["directory"]
    if not target.resolve().is_relative_to((root / "docs/books").resolve()):
        raise ValueError("Invalid book directory")
    if (target / "editions.json").is_file():
        history = read(target / "editions.json")
    else:
        if target.exists():
            raise ValueError("Existing book lacks edition history")
        history = {"schemaVersion": 1, "bookId": release["bookId"], "currentEdition": None, "editions": []}
    published = [item for item in history["editions"] if item.get("status") != "preparing"]
    if any(item.get("source", {}).get("sha256") == release["sha256"] for item in published):
        raise ValueError("This source is already installed")
    if release["sourceVersion"] <= max((int(item.get("source", {}).get("version", item["number"])) for item in published), default=0):
        raise ValueError("Source version must advance")
    pending = next((item for item in history["editions"] if item.get("status") == "preparing" and item.get("source", {}).get("sha256") == release["sha256"]), None)
    number = pending["number"] if pending else max((item["number"] for item in history["editions"]), default=0) + 1
    current = next((item for item in published if item["id"] == history.get("currentEdition")), None)
    if current:
        archive = target / "edition-files" / current["id"]
        if archive.exists() and any(child.name not in ("source", "covers") for child in archive.iterdir()):
            raise ValueError("Archive already exists; inspect before retrying, never overwrite history")
        archive.mkdir(parents=True, exist_ok=True)
        # Snapshot every language directory, including images and other local dependencies.
        for code in LANGUAGES:
            if (target / code).exists():
                shutil.copytree(target / code, archive / code, ignore=shutil.ignore_patterns("book.html"))
        shutil.copy2(target / "manifest.json", archive / "book-manifest.json")
        shutil.copy2(target / "editions.json", archive / "edition-history.json")
        archive_reader_links(target, archive)
        from build_books import snapshot_edition_covers
        snapshot_edition_covers(target, current)
        for code, path in current.get("pdf", {}).items():
            destination = archive / f"{code}.pdf"
            shutil.copy2(target / path, destination)
            current["pdf"][code] = destination.relative_to(target).as_posix()
        current["readers"] = {code: {kind: f"edition-files/{current['id']}/{code}/{name}" for kind, name in (("fullContent", "full_content.html"), ("shortContent", "short_content.html")) if (archive / code / name).is_file()} for code in LANGUAGES}
        current["readers"] = {code: values for code, values in current["readers"].items() if values}
        # A previous translation cannot masquerade as the current release.
        for code in LANGUAGES:
            for name in ("full_content.html", "short_content.html", "book.pdf"):
                path = target / code / name
                if path.exists():
                    path.unlink()
    shutil.copytree(work / "book", target, dirs_exist_ok=True)
    for code in LANGUAGES:
        for name in ("full_content.html", "short_content.html"):
            page = target / code / name
            if page.is_file():
                markup = page.read_text(encoding="utf-8")
                page.write_text(re.sub(r"(?<=>)[ \t]+(?=\n)", "", markup), encoding="utf-8")
    identifier = f"edition-{number}"
    source_archive = target / "edition-files" / identifier / "source" / Path(release["source"]).name
    source_archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / release["source"], source_archive)
    from build_books import BOOK_ACTIONS
    labels = {code: re.sub(r"1$", str(number), BOOK_ACTIONS[code]["editionLabel"]) for code in LANGUAGES}
    edition = {"id": identifier, "number": number, "label": labels, "publishedAt": release["publishedAt"], "changes": release["changes"], "source": {"filename": Path(release["source"]).name, "version": release["sourceVersion"], "sha256": release["sha256"], "path": source_archive.relative_to(target).as_posix()}, "pdf": {"en": "en/book.pdf"}, "contributors": release.get("contributors") or (pending or {}).get("contributors") or DEFAULT_CONTRIBUTORS}
    from build_books import snapshot_edition_covers
    edition["status"] = "preparing"
    snapshot_edition_covers(target, edition, refresh_pending=True)
    edition.pop("status")
    history["currentEdition"] = identifier
    if pending:
        history["editions"][history["editions"].index(pending)] = edition
    else:
        history["editions"].append(edition)
    write(target / "editions.json", history)
    manifest = read(target / "manifest.json")
    manifest["currentEdition"] = identifier
    manifest["publicationStatus"] = "published"
    manifest["releasePolicy"] = "en-ro-on-request"
    manifest.pop("pendingEdition", None)
    manifest["sourceAliases"] = sorted(set(manifest.get("sourceAliases", []) + [source_name(Path(release["source"]))[0]]))
    from build_books import edition_record
    manifest["editions"] = {code: edition_record(target, code) for code in LANGUAGES}
    from build_books import LANGUAGES as LANGUAGE_NAMES
    manifest["availableLanguages"] = [LANGUAGE_NAMES[code] for code, item in manifest["editions"].items() if "fullContent" in item or "shortContent" in item]
    write(target / "manifest.json", manifest)
    release["status"] = "installed"
    write(work / "release.json", release)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("scan")
    commands.add_parser("status")
    stage = commands.add_parser("prepare")
    stage.add_argument("source", type=Path)
    stage.add_argument("--source-language", required=True, choices=LANGUAGES)
    stage.add_argument("--english-title")
    cover = commands.add_parser("cover")
    cover.add_argument("workdir", type=Path)
    cover.add_argument("artwork", type=Path)
    for command in ("check", "install", "announce"):
        sub = commands.add_parser(command); sub.add_argument("workdir", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "scan":
            print(json.dumps(scan(), ensure_ascii=False, indent=2))
        elif args.command == "status":
            print(record_progress())
        elif args.command == "prepare":
            print(prepare(args.source, args.source_language, args.english_title))
        elif args.command == "cover":
            stage_cover(args.workdir, args.artwork)
            print("Staged this delivery's cover and all language derivatives")
        elif args.command == "check":
            errors = validate_stage(args.workdir)
            print("\n".join(errors) if errors else "Release is ready")
            return int(bool(errors))
        elif args.command == "announce":
            print(announce(args.workdir))
        else:
            print(install(args.workdir))
    except (ValueError, OSError, KeyError) as error:
        print(error, file=sys.stderr); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
