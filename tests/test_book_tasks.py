import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import book_tasks as tasks
import build_books


class TaskTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "tasks").mkdir()
        self.book = self.root / "docs/books/assistos/bk-test"
        self.book.mkdir(parents=True)
        tasks.write(self.book / "manifest.json", {"id": "bk-test", "title": {"en": "AssistOS"}, "route": ["assistos"], "sourceId": "AssistOS"})
        tasks.write(self.book / "editions.json", {"bookId": "bk-test", "currentEdition": "edition-1", "editions": [{"id": "edition-1", "number": 1, "pdf": {"en": "en/book.pdf"}}]})

    def delivery(self, name, content=b"source"):
        path = self.root / "tasks" / name
        path.write_bytes(content)
        return path

    def test_pending_cover_snapshot_breaks_existing_hard_link(self):
        source = self.book / "en/cover.webp"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(b"new cover")
        snapshot = self.book / "edition-files/edition-2/covers/en.webp"
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.hardlink_to(source)
        edition = {"id": "edition-2", "status": "preparing", "covers": {"en": "edition-files/edition-2/covers/en.webp"}}

        build_books.snapshot_edition_covers(self.book, edition, refresh_pending=True)
        self.assertEqual(snapshot.read_bytes(), b"new cover")
        self.assertFalse(snapshot.samefile(source))
        source.write_bytes(b"revised cover")
        self.assertEqual(snapshot.read_bytes(), b"new cover")

        build_books.snapshot_edition_covers(self.book, edition, refresh_pending=True)
        self.assertEqual(snapshot.read_bytes(), b"revised cover")
        self.assertFalse(snapshot.samefile(source))

    def test_filename_matching_versions_and_new_titles(self):
        self.delivery("AssistOs_v3.DOCX")
        self.delivery("AssistOs_v2.pdf")
        self.delivery("THOSE_WHO_NO_LONGER_RUN.docx")
        rows = tasks.scan(self.root)
        self.assertEqual([(r["status"], r["sourceVersion"]) for r in rows], [("new-release", 2), ("new-release", 3), ("new-book", 1)])
        self.assertEqual(rows[0]["bookId"], "bk-test")

    def test_unsuffixed_existing_title_advances_and_explicit_old_version_conflicts(self):
        self.delivery("AssistOS.docx")
        self.assertEqual(tasks.scan(self.root)[0]["sourceVersion"], 2)
        self.delivery("AssistOS_v1.doc")
        self.assertIn("version-conflict", [r["status"] for r in tasks.scan(self.root)])

    def test_duplicate_title_version_requires_resolution(self):
        self.delivery("AssistOS_v2.pdf", b"one")
        self.delivery("AssistOS_v2.docx", b"two")
        self.assertEqual({r["status"] for r in tasks.scan(self.root)}, {"ambiguous-source"})

    def test_incomplete_translation_cannot_modify_a_published_book(self):
        source = self.delivery("AssistOs_v2.docx")
        work = tasks.prepare(source, "en", root=self.root)
        before = (self.book / "editions.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "Missing finished reader"):
            tasks.install(work, self.root)
        self.assertEqual((self.book / "editions.json").read_bytes(), before)
        self.assertFalse((self.book / "edition-files").exists())

    def test_retained_keywords_must_match_previous_manifest(self):
        source = self.delivery("AssistOs_v2.docx")
        work = tasks.prepare(source, "en", root=self.root)
        release = tasks.read(work / "release.json")
        release["retainPreviousKeywords"] = True
        tasks.write(work / "release.json", release)
        previous = tasks.read(self.book / "manifest.json")
        previous.update(keywordIds=["original"], keywords={"en": ["original"]}, keywordSourceHash="old-hash")
        tasks.write(self.book / "manifest.json", previous)
        tasks.write(work / "book/manifest.json", previous)
        short = work / "book/en/short_content.html"
        short.parent.mkdir(parents=True, exist_ok=True)
        short.write_text('<html lang="en">' + ('word ' * 110) + '</html>')
        error = "Discovery keywords must be refreshed from this release's English short reader"
        self.assertNotIn(error, tasks.validate_stage(work, self.root))
        previous["keywords"]["en"] = ["changed"]
        tasks.write(work / "book/manifest.json", previous)
        self.assertIn(error, tasks.validate_stage(work, self.root))

    def test_announcement_is_visible_without_replacing_the_current_release(self):
        (self.book / "en").mkdir()
        (self.book / "en/book.pdf").write_bytes(b"published PDF")
        work = tasks.prepare(self.delivery("AssistOS_v2.docx"), "en", root=self.root)
        tasks.announce(work, self.root)
        tasks.announce(work, self.root)
        history = tasks.read(self.book / "editions.json")
        self.assertEqual(history["currentEdition"], "edition-1")
        self.assertEqual(len(history["editions"]), 2)
        pending = history["editions"][1]
        self.assertEqual(pending["id"], "edition-2")
        self.assertEqual(pending["status"], "preparing")
        self.assertNotIn("publishedAt", pending)
        self.assertEqual((self.book / "en/book.pdf").read_bytes(), b"published PDF")
        self.assertEqual(tasks.scan(self.root)[0]["status"], "preparing")
        (work / "book/en/book.pdf").write_bytes(b"new PDF")
        with patch.object(tasks, "validate_stage", return_value=[]):
            tasks.install(work, self.root)
        history = tasks.read(self.book / "editions.json")
        self.assertEqual(len(history["editions"]), 2)
        self.assertEqual(history["currentEdition"], "edition-2")
        self.assertNotIn("status", history["editions"][1])
        self.assertEqual((self.book / history["editions"][0]["pdf"]["en"]).read_bytes(), b"published PDF")

    def test_install_archives_downloads_and_translations_and_is_idempotent(self):
        for code in ("en", "fr"):
            folder = self.book / code
            folder.mkdir()
            (folder / "full_content.html").write_text('<html><head><link href="../../../../reader/standalone.css"></head><body><img src="picture.png">Old</body></html>')
            (folder / "picture.png").write_bytes(b"picture")
            (folder / "cover.webp").write_bytes(b"old cover")
        (self.book / "en/book.pdf").write_bytes(b"old pdf")
        source = self.delivery("AssistOS_v2.docx")
        work = tasks.prepare(source, "en", root=self.root)
        for code in ("en", "ro"):
            (work / "book" / code).mkdir(parents=True, exist_ok=True)
            (work / "book" / code / "full_content.html").write_text("new reader")
            (work / "book" / code / "cover.webp").write_bytes(b"new cover")
        (work / "book/en/book.pdf").write_bytes(b"new pdf")
        # Structural validation is tested separately; isolate installation mechanics.
        with patch.object(tasks, "validate_stage", return_value=[]):
            tasks.install(work, self.root)
        history = tasks.read(self.book / "editions.json")
        old = history["editions"][0]
        self.assertEqual((self.book / old["pdf"]["en"]).read_bytes(), b"old pdf")
        self.assertEqual((self.book / "en/book.pdf").read_bytes(), b"new pdf")
        self.assertEqual((self.book / old["covers"]["en"]).read_bytes(), b"old cover")
        self.assertEqual((self.book / history["editions"][1]["covers"]["en"]).read_bytes(), b"new cover")
        source_record = history["editions"][1]["source"]
        self.assertEqual(source_record["filename"], source.name)
        self.assertEqual(source_record["sha256"], tasks.sha256(source))
        self.assertNotIn("path", source_record)
        self.assertFalse((self.book / "edition-files/edition-2/source").exists())
        self.assertEqual((self.book / "en/cover.webp").read_bytes(), b"new cover")
        self.assertIn("fr", old["readers"])
        self.assertFalse((self.book / "fr/full_content.html").exists())
        snapshot = self.book / old["readers"]["fr"]["fullContent"]
        self.assertIn('src="picture.png"', snapshot.read_text())
        self.assertIn('../../../../../../reader/standalone.css', snapshot.read_text())
        self.assertEqual(tasks.scan(self.root)[0]["status"], "already-imported")
        with patch.object(tasks, "validate_stage", return_value=[]):
            with self.assertRaisesRegex(ValueError, "already installed"):
                tasks.install(work, self.root)
        self.assertEqual(len(list(self.book.glob("**/manifest.json"))), 1)
        # A release's source directory must not prevent its later archival.
        third = self.delivery("AssistOS_v3.docx", b"third source")
        next_work = tasks.prepare(third, "en", root=self.root)
        (next_work / "book/en/book.pdf").write_bytes(b"third pdf")
        (next_work / "book/en/cover.webp").write_bytes(b"third cover")
        with patch.object(tasks, "validate_stage", return_value=[]):
            tasks.install(next_work, self.root)
        history = tasks.read(self.book / "editions.json")
        self.assertEqual(len(history["editions"]), 3)
        self.assertEqual((self.book / history["editions"][1]["pdf"]["en"]).read_bytes(), b"new pdf")
        self.assertEqual((self.book / history["editions"][0]["covers"]["en"]).read_bytes(), b"old cover")
        self.assertEqual((self.book / history["editions"][1]["covers"]["en"]).read_bytes(), b"new cover")
        self.assertEqual((self.book / history["editions"][2]["covers"]["en"]).read_bytes(), b"third cover")
        self.assertNotIn("path", history["editions"][2]["source"])

    def test_pdf_source_remains_archived_for_a_new_edition(self):
        source = self.delivery("AssistOS_v2.pdf", b"delivered PDF")
        (self.book / "en").mkdir()
        (self.book / "en/book.pdf").write_bytes(b"prior PDF")
        work = tasks.prepare(source, "en", root=self.root)
        (work / "book/en/book.pdf").write_bytes(b"reader PDF")
        with patch.object(tasks, "validate_stage", return_value=[]):
            tasks.install(work, self.root)
        history = tasks.read(self.book / "editions.json")
        source_record = history["editions"][1]["source"]
        self.assertEqual(source_record["sha256"], tasks.sha256(source))
        self.assertEqual((self.book / source_record["path"]).read_bytes(), b"delivered PDF")

    def test_incoming_pdf_retains_only_source_hash(self):
        incoming = self.root / "income/AssistOS"
        incoming.mkdir(parents=True)
        source = incoming / "content.pdf"
        source.write_bytes(b"old source PDF")
        (self.book / "en").mkdir()
        (self.book / "en/book.pdf").write_bytes(b"prior PDF")
        work = tasks.prepare(source, "en", root=self.root)
        (work / "book/en/book.pdf").write_bytes(b"clean reader PDF")
        with patch.object(tasks, "validate_stage", return_value=[]):
            tasks.install(work, self.root)
        history = tasks.read(self.book / "editions.json")
        current = history["editions"][1]
        self.assertEqual(current["source"]["sha256"], tasks.sha256(source))
        self.assertNotIn("path", current["source"])
        self.assertFalse((self.book / "edition-files/edition-2/source").exists())
        self.assertEqual((self.book / history["editions"][0]["pdf"]["en"]).read_bytes(), b"prior PDF")

    def test_first_release_promotes_announced_draft_without_duplicate_edition(self):
        work = tasks.prepare(self.delivery("New_Book.docx"), "en", root=self.root)
        release = tasks.read(work / "release.json")
        target = self.root / "docs" / release["directory"]
        # Minimal metadata isolates the promotion mechanics from editorial checks.
        tasks.write(work / "book/manifest.json", {
            "id": release["bookId"], "title": {"en": "New Book"},
            "route": ["new", "book"], "sourceId": "New_Book",
            "editions": {code: {"book": f"{code}/book.html"} for code in tasks.LANGUAGES},
        })
        for code in tasks.LANGUAGES:
            (work / "book" / code).mkdir(exist_ok=True)
            for name in ("cover.png", "cover.webp", "thumbnail.webp"):
                (work / "book" / code / name).write_bytes(b"draft cover")
        tasks.announce(work, self.root)
        self.assertIsNone(tasks.read(target / "editions.json")["currentEdition"])
        # Draft artwork can be improved before the first release. It must
        # update the visible cover and its pending-history snapshot.
        (work / "book/en/cover.webp").write_bytes(b"revised draft cover")
        tasks.announce(work, self.root)
        self.assertEqual((target / "en/cover.webp").read_bytes(), b"revised draft cover")
        pending = tasks.read(target / "editions.json")["editions"][0]
        self.assertEqual((target / pending["covers"]["en"]).read_bytes(), b"revised draft cover")
        (work / "book/en/book.pdf").write_bytes(b"first PDF")
        (work / "book/en/cover.webp").write_bytes(b"final cover")
        with patch.object(tasks, "validate_stage", return_value=[]):
            tasks.install(work, self.root)
        history = tasks.read(target / "editions.json")
        self.assertEqual(history["currentEdition"], "edition-1")
        self.assertEqual(len(history["editions"]), 1)
        first = history["editions"][0]
        self.assertNotIn("status", first)
        self.assertEqual((target / first["pdf"]["en"]).read_bytes(), b"first PDF")
        self.assertEqual((target / first["covers"]["en"]).read_bytes(), b"final cover")
        self.assertEqual(tasks.read(target / "manifest.json")["publicationStatus"], "published")


if __name__ == "__main__":
    unittest.main()
