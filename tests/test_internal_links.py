from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from audit_internal_links import Link, audit, parse_html_inventory  # noqa: E402


class InternalLinksTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="scriptahub-links-")
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name).resolve()
        self.site = self.folder / "docs"
        self.site.mkdir()

    def put(self, path, source):
        destination = self.site / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source, encoding="utf-8")
        return destination

    def test_inventory_decodes_attributes_and_ignores_scripts_comments_and_text_elements(self):
        inventory = parse_html_inventory(
            '<!doctype html>\n<A ID="a&amp;b" NAME="legacy" HREF="next.html?x=1&amp;y=2#title">Read</A>\n'
            '<!-- <img src="missing-comment.png"> -->\n'
            '<script>const fake = \'<a href="missing-script.html">\';</script>\n'
            '<style>.x::after{content:\'<img src="missing-style.png">\'}</style>\n'
            '<textarea><a href="missing-textarea.html"></textarea>\n'
            '<img src="picture.webp" poster="cover.webp">'
        )
        self.assertEqual(inventory.anchors, {"a&b", "legacy"})
        self.assertEqual(inventory.links, [
            Link("next.html?x=1&y=2#title", 2, "href"),
            Link("picture.webp", 7, "src"),
            Link("cover.webp", 7, "poster"),
        ])
        self.assertEqual(inventory.tags[0], {
            "tagName": "a", "attrs": {"id": "a&b", "name": "legacy", "href": "next.html?x=1&y=2#title"}, "line": 2,
        })
        self.assertEqual(sum(tag["tagName"] == "a" for tag in inventory.tags), 1)

    def test_html_duplicate_attributes_and_nonvoid_selfclosing_text_elements(self):
        inventory = parse_html_inventory('<script/><a href="fake.html"></script><a id="first" id="second" href="real.html" href="ignored.html">')
        self.assertEqual(inventory.anchors, {"first"})
        self.assertEqual(inventory.links, [Link("real.html", 1, "href")])

    def test_resolves_percent_entities_queries_fragments_and_directory_indexes(self):
        self.put("index.html", '<h1 id="local">Home</h1><a href="?lang=ro#local">Here</a><a href="chapters/a%20%26%20b.html?lang=ro&amp;x=2#caf%C3%A9">Chapter</a><a href="chapters/#start">Contents</a><a href="document.pdf#page=2">PDF</a>')
        self.put("chapters/index.html", '<h1 id="start">Contents</h1><a href="/index.html#local">Home</a>')
        self.put("chapters/a & b.html", '<h2 id="caf&#233;">Title</h2><a name="legacy"></a><a href="#legacy">Jump</a>')
        self.put("document.pdf", "PDF fixture")
        self.assertEqual(audit(self.site), [])

    def test_missing_targets_and_anchors_have_stable_order_and_start_tag_lines(self):
        self.put("index.html", '<a href="z.html">Missing</a>\n<img\n src="missing.png">\n<a href="other.html#absent">Anchor</a>\n<a href="empty/">Directory</a>')
        self.put("other.html", '<p id="present">Existing</p>')
        (self.site / "empty").mkdir()
        self.assertEqual(audit(self.site), [
            "index.html:1: missing local target: z.html",
            "index.html:2: missing local target: missing.png",
            "index.html:4: missing anchor #absent in other.html",
            "index.html:5: missing local target: empty/",
        ])

    def test_srcset_keeps_data_urls_and_audits_local_alternatives(self):
        self.put("index.html", '<img srcset=", , data:image/svg+xml,%3Csvg%3E%3C/svg%3E 1x, small.png 2x, missing.png 3x,">')
        self.put("small.png", "image")
        inventory = parse_html_inventory('<img srcset="first.png 1x,second.png 2x, third.png, fourth.png 4x">')
        self.assertEqual([link.value for link in inventory.links], ["first.png", "second.png", "third.png", "fourth.png"])
        self.assertEqual(audit(self.site), ["index.html:1: missing local target: missing.png"])

    def test_external_schemes_and_network_relative_links_are_ignored(self):
        external = ["https://example.invalid/nope", "HTTP://example.invalid/nope", "//example.invalid/nope", "mailto:reader@example.test", "tel:+123", "javascript:void(0)", "data:text/plain,hello", "ftp://example.invalid/book.pdf", "file:///nope", "custom:thing", "https://[invalid"]
        self.put("index.html", "\n".join(f'<a href="{href}">Link</a>' for href in external))
        self.assertEqual(audit(self.site), [])

    def test_traversal_and_symlink_targets_cannot_escape_site_root(self):
        self.put("index.html", '<a href="../outside.html">Outside</a>\n<a href="%2e%2e/outside.html">Encoded</a>\n<a href="assets/secret.pdf">Symlink directory</a>\n<a href="out.pdf">Symlink file</a>\n<a href="dangling.pdf">Dangling symlink</a>\n<a href="chapter/">Index symlink</a>')
        (self.folder / "outside.html").write_text('<a href="not-scanned.html">Outside source</a>', encoding="utf-8")
        (self.folder / "secret.pdf").write_text("outside", encoding="utf-8")
        (self.site / "assets").symlink_to(self.folder, target_is_directory=True)
        (self.site / "out.pdf").symlink_to(self.folder / "secret.pdf")
        (self.site / "dangling.pdf").symlink_to(self.folder / "missing.pdf")
        (self.site / "chapter").mkdir()
        (self.site / "chapter/index.html").symlink_to(self.folder / "outside.html")
        problems = audit(self.site)
        self.assertEqual(len(problems), 7)
        self.assertTrue(all("escapes docs/" in problem for problem in problems))
        self.assertTrue(any("href escapes docs/: chapter/" in problem for problem in problems))
        self.assertFalse(any("not-scanned" in problem for problem in problems))

    def test_inroot_symlinks_and_directory_cycles(self):
        self.put("index.html", '<a href="copy.html#target">Alias</a><a href="assets/page.html#target">Directory alias</a>')
        self.put("real/page.html", '<h1 id="target">Target</h1>')
        (self.site / "copy.html").symlink_to(self.site / "real/page.html")
        (self.site / "assets").symlink_to(self.site / "real", target_is_directory=True)
        (self.site / "real/cycle").symlink_to(self.site, target_is_directory=True)
        self.assertEqual(audit(self.site), [])

    def test_dot_segments_are_collapsed_before_following_directory_symlinks(self):
        self.put("index.html", '<a href="alias/../sibling.html#target">Sibling</a>\n<a href="/alias/%2e%2e/sibling.html#absent">Missing anchor</a>')
        self.put("sibling.html", '<h1 id="target">Root sibling</h1>')
        self.put("real/sibling.html", '<h1 id="absent">Wrong sibling</h1>')
        (self.site / "real/nested").mkdir()
        (self.site / "alias").symlink_to(self.site / "real/nested", target_is_directory=True)
        self.assertEqual(audit(self.site), [
            "index.html:2: missing anchor #absent in sibling.html",
        ])

    def test_malformed_percent_and_decoded_nulls_do_not_stop_the_audit(self):
        self.put("index.html", '<a href="bad%ZZ.html">Literal percent</a>\n<a href="%FF.html">Bad UTF8</a>\n<a href="bad%00.html">Null</a>')
        self.put("bad%ZZ.html", "<p>Literal filename</p>")
        self.assertEqual(audit(self.site), [
            "index.html:2: missing local target: %FF.html",
            "index.html:3: invalid local target: bad%00.html",
        ])

    def test_symlink_file_loop_is_reported_without_aborting_other_links(self):
        self.put("index.html", '<a href="loop.html">Loop</a><a href="missing.pdf">Another failure</a>')
        (self.site / "loop.html").symlink_to("loop.html")
        self.assertEqual(audit(self.site), [
            "loop.html:1: missing local HTML source",
            "index.html:1: missing local target: loop.html",
            "index.html:1: missing local target: missing.pdf",
        ])

    def test_cli_exit_codes_help_and_missing_root(self):
        self.put("index.html", '<a href="missing.html">Missing</a>')

        def run(*args):
            return subprocess.run([sys.executable, "-B", str(ROOT / "tools/audit_internal_links.py"), *map(str, args)], cwd=self.folder, capture_output=True, text=True, timeout=20, check=False)

        report = run("--root", self.site)
        self.assertEqual(report.returncode, 0)
        self.assertIn("missing local target: missing.html", report.stdout)
        self.assertIn("1 local-link problem(s) found", report.stderr)
        self.assertEqual(run("--root", self.site, "--check").returncode, 1)
        missing = run("--root", self.folder / "absent", "--check")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("Missing site root", missing.stderr)
        self.assertEqual(run("--unknown").returncode, 2)
        self.assertEqual(run("--help").returncode, 0)
        self.put("missing.html", "<p>Added</p>")
        valid = run("--root", self.site, "--check")
        self.assertEqual(valid.returncode, 0)
        self.assertIn("No broken local HTML links or fragment anchors", valid.stdout)


if __name__ == "__main__":
    unittest.main()
