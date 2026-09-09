"""Regression coverage for the Python catalogue renderer and validator."""
import copy
from contextlib import contextmanager
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote, urljoin, urlsplit, unquote


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CLI = ROOT / "tools" / "build_books.py"
SPEC = importlib.util.spec_from_file_location("catalogue_build", CLI)
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)
COLLECTION = json.loads((DOCS / "collection.json").read_text(encoding="utf-8"))
LANGUAGES = tuple(build.LANGUAGES)


def localise(value):
    return {code: value(code) if callable(value) else value for code in LANGUAGES}


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@contextmanager
def docs_root(docs):
    with patch.multiple(build, DOCS=docs, BOOKS=docs / "books", COLLECTION=docs / "collection.json",
                        COLLECTION_SCRIPT=docs / "collection.js"):
        yield


class Elements(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.scripts = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))
        elif tag == "script":
            self.scripts.append(dict(attrs))


class PublishedPagesTests(unittest.TestCase):
    def test_every_published_page_matches_generator_and_only_account_actions_are_gated(self):
        keyword_stats = {code: {entry["id"]: {"count": entry["count"]} for entry in entries}
                         for code, entries in COLLECTION["keywords"].items()}
        total = 0
        for listing in COLLECTION["books"]:
            root = DOCS / listing["directory"]
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            book = {**manifest, "directory": listing["directory"],
                    "descriptions": manifest["shortDescription"], "keywordStats": keyword_stats}
            for language in LANGUAGES:
                page = root / language / "book.html"
                edition = manifest["editions"][language]
                generated = build.book_page(book, language, page, "fullContent" in edition or "shortContent" in edition)
                self.assertTrue(generated.encode("utf-8") == page.read_bytes(), f"Generated page differs: {page}")
                elements = Elements(generated)
                gated = [link for link in elements.links if "data-auth-action" in link]
                self.assertEqual(len(gated), 1 + int("pdf" in edition), str(page))
                for link in elements.links:
                    target = urlsplit(urljoin(page.as_uri(), link["href"])).path
                    expected = ("download" if target.endswith(".pdf") else
                                "feedback" if target.endswith("/feedback/index.html") else None)
                    self.assertEqual(link.get("data-auth-action"), expected, f"{page}: {target}")
                auth = [script for script in elements.scripts if "/auth.js" in script.get("src", "")]
                self.assertEqual(len(auth), 1, str(page))
                self.assertIn("defer", auth[0], str(page))
                auth_path = Path(unquote(urlsplit(urljoin(page.as_uri(), auth[0]["src"])).path))
                self.assertEqual(auth_path, DOCS / "assets" / "auth.js")
                total += 1
        self.assertEqual(total, COLLECTION["bookCount"] * 8)

    def test_shared_pages_load_authentication_before_deferred_consumers(self):
        for relative, consumer in (("feedback/index.html", "workflow.js"),
                                   ("editions/index.html", "workflow.js"), ("reader/index.html", "reader.js")):
            scripts = Elements((DOCS / relative).read_text(encoding="utf-8")).scripts
            auth_index = next(index for index, script in enumerate(scripts) if "/auth.js" in script.get("src", ""))
            consumer_index = next(index for index, script in enumerate(scripts) if consumer in script.get("src", ""))
            self.assertLess(auth_index, consumer_index, relative)
            self.assertIn("defer", scripts[auth_index], relative)
            self.assertIn("defer", scripts[consumer_index], relative)

    def test_canonical_readers_with_pdf_buttons_load_shared_runtime(self):
        checked = 0
        for page in (DOCS / "books").rglob("*_content.html"):
            if page.name not in ("full_content.html", "short_content.html"):
                continue
            elements = Elements(page.read_text(encoding="utf-8"))
            pdfs = [urlsplit(urljoin("https://scriptahub.com/", link.get("href") or "")) for link in elements.links]
            if any(url.scheme == "https" and url.netloc == "scriptahub.com" and url.path.lower().endswith(".pdf") for url in pdfs):
                self.assertTrue(any(re.search(r"/(standalone|auth)\.js$", urlsplit(script.get("src") or "").path)
                                    for script in elements.scripts), str(page))
                checked += 1
        self.assertGreater(checked, 0, "Canonical reader PDF coverage must not disappear")


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="scripta-generator-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.docs = self.directory / "docs"
        listing = copy.deepcopy(next(book for book in COLLECTION["books"] if book["editions"]["en"].get("pdf")))
        self.root = self.docs / listing["directory"]
        self.root.mkdir(parents=True)
        self.manifest = json.loads((DOCS / listing["directory"] / "manifest.json").read_text(encoding="utf-8"))
        self.collection = {**COLLECTION, "books": [listing], "bookCount": 1}
        for language in LANGUAGES:
            (self.root / language).mkdir()
        save_json(self.docs / "collection.json", self.collection)
        self.save_manifest()
        context = docs_root(self.docs)
        context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)

    def save_manifest(self):
        save_json(self.root / "manifest.json", self.manifest)

    def assert_no_generated_outputs(self):
        self.assertFalse((self.root / "en" / "book.html").exists())
        self.assertFalse((self.root / "editions.json").exists())

    def test_refresh_prepares_all_pages_then_is_idempotent_and_preserves_canonical_assets(self):
        canonical = {self.root / "en" / name: f"untouched {name}".encode()
                     for name in ("book.pdf", "full_content.html", "short_content.html", "cover.webp")}
        for path, content in canonical.items():
            path.write_bytes(content)
        plan = build.plan_refresh()
        self.assertEqual(plan["pages"], 8)
        self.assertEqual(len(plan["files"]), 9)
        self.assert_no_generated_outputs()
        self.assertEqual(build.refresh_pages(), {"books": 1, "pages": 8, "changedFiles": 9})
        mtimes = {output["path"]: output["path"].stat().st_mtime_ns for output in plan["files"]}
        self.assertEqual(build.refresh_pages(), {"books": 1, "pages": 8, "changedFiles": 0})
        self.assertEqual(mtimes, {path: path.stat().st_mtime_ns for path in mtimes})
        for path, content in canonical.items():
            self.assertEqual(path.read_bytes(), content)
        history = json.loads((self.root / "editions.json").read_text())
        self.assertEqual(history["bookId"], self.manifest["id"])
        self.assertEqual(history["editions"][0]["pdf"]["en"], self.manifest["editions"]["en"]["pdf"])
        self.assertEqual(set(history["editions"][0]["changes"]), set(LANGUAGES))

    def test_stale_and_missing_pages_are_regenerated_after_manifest_edits(self):
        build.refresh_pages()
        self.manifest["title"]["pl"] = "An updated localized title"
        self.save_manifest()
        (self.root / "fr" / "book.html").unlink()
        result = build.refresh_pages()
        self.assertEqual(result["changedFiles"], 2)
        self.assertIn("An updated localized title", (self.root / "pl" / "book.html").read_text())
        self.assertTrue((self.root / "fr" / "book.html").is_file())

    def test_history_preserves_archives_current_pdf_choices_and_unknown_metadata(self):
        build.ensure_editions_file(self.root, self.manifest)
        path = self.root / "editions.json"
        history = json.loads(path.read_text())
        history["extra"] = {"note": "retain"}
        history["editions"][0]["pdf"]["en"] = "edition-files/first/en.pdf"
        initial = copy.deepcopy(history["editions"][0])
        history["editions"].append({"id": "edition-2", "number": 2, "publishedAt": "2026-09-08",
                                    "changes": {"en": "A second edition"},
                                    "pdf": {"en": "edition-files/current/en.pdf"}, "custom": True})
        history["currentEdition"] = "edition-2"
        before = (json.dumps(history, ensure_ascii=False, indent=4) + "\r\n").encode("utf-8")
        path.write_bytes(before)
        self.assertFalse(build.ensure_editions_file(self.root, self.manifest)["changed"])
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(json.loads(path.read_text())["editions"][0], initial)
        del history["editions"][1]["pdf"]["en"]
        save_json(path, history)
        self.assertTrue(build.ensure_editions_file(self.root, self.manifest)["changed"])
        extended = json.loads(path.read_text())
        self.assertEqual(extended["editions"][0], initial)
        self.assertTrue(extended["editions"][1]["custom"])
        self.assertEqual(extended["extra"], {"note": "retain"})
        self.assertEqual(extended["editions"][1]["pdf"]["en"], self.manifest["editions"]["en"]["pdf"])

    def test_invalid_utf8_generated_page_is_replaced(self):
        build.refresh_pages()
        page = self.root / "en" / "book.html"
        expected = page.read_bytes()
        page.write_bytes(b"\xff\xfe invalid generated output")
        self.assertEqual(build.refresh_pages()["changedFiles"], 1)
        self.assertEqual(page.read_bytes(), expected)

    def test_malformed_history_is_rejected_without_repair_or_partial_page_writes(self):
        output = build.prepare_editions_file(self.root, self.manifest)
        valid = json.loads(output["content"])
        variants = ["{", "{}", "null"]
        for mutate in (lambda h: h.update(currentEdition="missing"),
                       lambda h: h.update(bookId="wrong"),
                       lambda h: h["editions"].append(copy.deepcopy(h["editions"][0])),
                       lambda h: h["editions"][0].update(number=True),
                       lambda h: h["editions"][0].update(publishedAt="2026-02-30"),
                       lambda h: h["editions"][0].update(pdf=[]),
                       lambda h: h["editions"][0].update(pdf={"en": "../outside.pdf"})):
            history = copy.deepcopy(valid)
            mutate(history)
            variants.append(json.dumps(history))
        for invalid in variants:
            with self.subTest(invalid=invalid[:80]):
                path = self.root / "editions.json"
                path.write_text(invalid)
                with self.assertRaises(ValueError):
                    build.refresh_pages()
                self.assertEqual(path.read_text(), invalid)
                self.assertFalse((self.root / "en" / "book.html").exists())

    def test_invalid_final_language_prevents_all_writes(self):
        del self.manifest["title"]["pl"]
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, "missing title.pl"):
            build.refresh_pages()
        self.assert_no_generated_outputs()

    def test_invalid_later_book_prevents_writes_to_earlier_books(self):
        second = copy.deepcopy(self.manifest)
        second["id"] = "bk-second-fixture"
        second_root = self.docs / "books" / "second" / second["id"]
        second_root.mkdir(parents=True)
        for language in LANGUAGES:
            (second_root / language).mkdir()
        del second["title"]["pl"]
        save_json(second_root / "manifest.json", second)
        self.collection["books"].append({"id": second["id"], "directory": second_root.relative_to(self.docs).as_posix()})
        save_json(self.docs / "collection.json", self.collection)
        with self.assertRaisesRegex(ValueError, "missing title.pl"):
            build.refresh_pages()
        self.assert_no_generated_outputs()
        self.assertFalse((second_root / "editions.json").exists())

    def test_output_symlinks_including_dangling_links_are_rejected(self):
        outside = self.directory / "outside.html"
        outside.write_text("untouched")
        for relative, target in (("en/book.html", outside), ("editions.json", outside),
                                 ("en/book.html", self.directory / "absent.html")):
            with self.subTest(relative=relative, target=target.name):
                output = self.root / relative
                output.symlink_to(target)
                try:
                    with self.assertRaisesRegex(ValueError, "Refusing non-file output|Unsafe relative asset path"):
                        build.refresh_pages()
                    self.assertEqual(outside.read_text(), "untouched")
                    self.assertFalse((self.root / "fr" / "book.html").exists())
                finally:
                    output.unlink()
        self.assert_no_generated_outputs()

    def test_parent_directory_symlink_cannot_redirect_outputs(self):
        outside = self.directory / "outside-language"
        outside.mkdir()
        (self.root / "pl").rmdir()
        (self.root / "pl").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Unsafe relative asset path|outside book directory"):
            build.refresh_pages()
        self.assertEqual(list(outside.iterdir()), [])
        self.assert_no_generated_outputs()

    def test_forbidden_keyword_routes_fail_and_remain_untouched(self):
        legacy = self.docs / "keywords"
        legacy.mkdir()
        (legacy / "retain.html").write_text("retain")
        with self.assertRaisesRegex(ValueError, "Legacy docs/keywords"):
            build.refresh_pages()
        self.assertEqual((legacy / "retain.html").read_text(), "retain")
        self.assert_no_generated_outputs()

    def test_cli_dry_run_and_argument_failures_do_not_write(self):
        result = subprocess.run([sys.executable, "-B", str(CLI), "refresh", "--docs", str(self.docs), "--dry-run"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("8 pages, 9 changed files", result.stdout)
        self.assert_no_generated_outputs()
        for arguments in (("refresh", "--unknown"), ("check", "--dry-run"), ("build", "--docs", str(self.docs))):
            result = subprocess.run([sys.executable, "-B", str(CLI), *arguments], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stderr)


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="scripta-catalogue-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.docs = self.directory / "docs"
        directory = "books/a/fixture/bk-0123456789abcdef"
        self.root = self.docs / directory
        self.root.mkdir(parents=True)
        ids = [f"subject:{index}" for index in range(100)]
        self.manifest = {"id": "bk-0123456789abcdef", "route": ["a", "fixture"], "keywordIds": ids,
                         "title": localise("A Fixture"), "subtitle": localise(""),
                         "shortDescription": localise("Description"),
                         "keywords": localise(lambda _: [f"Subject {index}" for index in range(100)]),
                         "coverUrl": localise(lambda code: f"{code}/cover.webp")}
        self.collection = {"bookCount": 1, "books": [{"id": self.manifest["id"], "directory": directory,
                            "keywordIds": copy.deepcopy(ids), "editions": localise(lambda code: {
                                "book": f"{directory}/{code}/book.html", "cover": f"{directory}/{code}/cover.webp"})}],
                           "keywords": localise(lambda _: [{"id": identifier, "label": f"Subject {index}", "count": 1}
                                                          for index, identifier in enumerate(ids)])}
        for language in LANGUAGES:
            (self.root / language).mkdir()
            (self.root / language / "cover.webp").write_text("fixture")
            words = [{"href": f"index.html?lang={language}&keyword={quote(identifier, safe='')}"} for identifier in ids]
            (self.root / language / "book.html").write_text(f"<script>const words={json.dumps(words)};</script>")
        self.history = {"bookId": self.manifest["id"], "currentEdition": "edition-1", "editions": [
            {"id": "edition-1", "publishedAt": "2026-09-08", "changes": localise("Initial"), "pdf": {}}]}
        self.save()
        context = docs_root(self.docs)
        context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)

    def save(self):
        save_json(self.docs / "collection.json", self.collection)
        save_json(self.root / "manifest.json", self.manifest)
        save_json(self.root / "editions.json", self.history)

    def problems(self):
        return "\n".join(build.check())

    def test_unicode_routes_and_keyword_equivalence(self):
        self.assertEqual(build.slugify("Can’t See the World — Café"), "cant-see-the-world-cafe")
        self.assertEqual(build.slugify("Maße"), "mae")
        self.assertEqual(build.keyword_normalise("Maße"), build.keyword_normalise("MASSE"))
        self.assertEqual(build.keyword_normalise("ẞ").strip(), "ss")
        self.assertEqual(build.keyword_normalise("Café"), build.keyword_normalise("Cafe\u0301"))
        self.assertEqual(build.keyword_normalise("ﬁeld").strip(), "field")

    def test_valid_catalogue_in_all_eight_languages(self):
        self.assertEqual(build.check(), [])

    def test_counts_metadata_normalized_duplicates_and_keyword_links_fail(self):
        self.collection["bookCount"] = 2
        self.collection["keywords"]["fr"][0]["count"] = 3
        self.manifest["keywords"]["de"][:2] = ["Maße", "Masse"]
        del self.manifest["subtitle"]["ro"]
        self.save()
        page = self.root / "it" / "book.html"
        page.write_text(page.read_text().replace("keyword=subject%3A0", "keyword=orphan"))
        problems = self.problems()
        for expected in ("bookCount", "fr: keyword count mismatch", "de: expected 100 distinct keywords",
                         "ro: missing subtitle", "it: book-page keyword links"):
            self.assertIn(expected, problems)

    def test_history_current_and_pdf_boundary_errors_fail(self):
        self.history["currentEdition"] = "nonexistent"
        self.history["editions"][0]["pdf"]["en"] = "../../../../outside.pdf"
        self.save()
        problems = self.problems()
        self.assertIn("current edition is missing", problems)
        self.assertIn("unsafe historical PDF", problems)
        for invalid in ("{", "null", "{}", '{"editions": null}'):
            (self.root / "editions.json").write_text(invalid)
            self.assertIn("invalid editions.json", self.problems())

    def test_historical_and_aggregate_assets_cannot_escape_through_symlinks(self):
        outside = self.directory / "outside.pdf"
        outside.write_text("public fixture")
        (self.root / "en" / "book.pdf").symlink_to(outside)
        self.history["editions"][0]["pdf"]["en"] = "en/book.pdf"
        self.collection["books"][0]["editions"]["en"]["pdf"] = (self.root / "en" / "book.pdf").relative_to(self.docs).as_posix()
        self.save()
        self.assertIn("unsafe historical PDF: en/book.pdf", self.problems())
        self.assertIn("unsafe edition asset", self.problems())

    def test_unlisted_manifests_and_forbidden_routes_fail(self):
        orphan = self.docs / "books" / "unlisted"
        orphan.mkdir()
        (orphan / "manifest.json").write_text("{}")
        (self.docs / "keywords").mkdir()
        self.assertIn("manifest missing from collection", self.problems())
        self.assertIn("legacy per-keyword pages", self.problems())

    def test_duplicate_ids_manifest_mismatch_aggregate_divergence_and_missing_language_fail(self):
        self.collection["books"].append(copy.deepcopy(self.collection["books"][0]))
        self.manifest["id"] = "bk-other"
        self.collection["books"][0]["keywordIds"].reverse()
        del self.collection["keywords"]["pl"]
        self.save()
        problems = self.problems()
        for expected in ("duplicate book ID", "manifest ID mismatch", "collection keyword IDs differ", "pl: missing collection keywords"):
            self.assertIn(expected, problems)

    def test_invalid_json_shapes_and_entries_report_problems(self):
        for invalid in ("{", "null", "[]", "{}", '{"books": null}'):
            (self.docs / "collection.json").write_text(invalid)
            self.assertTrue(build.check())
        self.save()
        for invalid in ("{", "null", "[]"):
            (self.root / "manifest.json").write_text(invalid)
            self.assertIn("invalid manifest.json", self.problems())
        self.collection["books"].append(None)
        self.collection["keywords"]["en"].append(None)
        self.save()
        self.assertIn("malformed collection keyword", self.problems())
        self.assertIn("missing or unsafe manifest", self.problems())

    def test_manifest_path_cannot_escape_catalogue(self):
        outside = self.directory / "outside"
        outside.mkdir()
        save_json(outside / "manifest.json", self.manifest)
        symlink = self.docs / "books" / "redirected"
        symlink.symlink_to(outside, target_is_directory=True)
        self.collection["books"][0]["directory"] = "books/redirected"
        self.save()
        self.assertIn("missing or unsafe manifest", self.problems())

    def test_cli_status_for_valid_invalid_and_unknown_arguments(self):
        def run(*arguments):
            return subprocess.run([sys.executable, "-B", str(CLI), *arguments], capture_output=True, text=True)
        valid = run("check", "--docs", str(self.docs))
        self.assertEqual(valid.returncode, 0, valid.stderr)
        (self.docs / "collection.json").write_text("null")
        invalid = run("check", "--docs", str(self.docs))
        self.assertEqual(invalid.returncode, 1, invalid.stderr)
        self.assertIn("books must be an array", invalid.stderr)
        self.assertEqual(run("check", "--oops").returncode, 2)


if __name__ == "__main__":
    unittest.main()
