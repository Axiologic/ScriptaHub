import assert from "node:assert/strict";
import {mkdtemp, mkdir, writeFile, symlink, rm, copyFile, cp} from "node:fs/promises";
import {tmpdir} from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {spawnSync} from "node:child_process";
import test from "node:test";
import {audit, parseHtmlInventory, decodeHtmlEntities} from "../tools/audit_internal_links.mjs";

const ROOT = fileURLToPath(new URL("..", import.meta.url));

async function fixture(t) {
    const folder = await mkdtemp(path.join(tmpdir(), "scriptahub-links-"));
    t.after(() => rm(folder, {recursive: true, force: true}));
    const site = path.join(folder, "docs");
    await mkdir(site);
    async function put(filename, source) {
        const destination = path.join(site, filename);
        await mkdir(path.dirname(destination), {recursive: true});
        await writeFile(destination, source, "utf8");
        return destination;
    }
    return {folder, site, put};
}

test("inventory decodes attributes and ignores scripts, comments and text elements", () => {
    const inventory = parseHtmlInventory(
        '<!doctype html>\n<A ID="a&amp;b" NAME="legacy" HREF="next.html?x=1&amp;y=2#title">Read</A>\n'
        + '<!-- <img src="missing-comment.png"> -->\n'
        + '<script>const fake = \'<a href="missing-script.html">\';</script>\n'
        + '<style>.x::after{content:\'<img src="missing-style.png">\'}</style>\n'
        + '<textarea><a href="missing-textarea.html"></textarea>\n'
        + '<img src="picture.webp" poster="cover.webp">',
    );
    assert.deepEqual(inventory.anchors, new Set(["a&b", "legacy"]));
    assert.deepEqual(inventory.links, [
        {value: "next.html?x=1&y=2#title", line: 2, attribute: "href"},
        {value: "picture.webp", line: 7, attribute: "src"},
        {value: "cover.webp", line: 7, attribute: "poster"},
    ]);
    assert.deepEqual(inventory.tags[0], {
        tagName: "a", attrs: {id: "a&b", name: "legacy", href: "next.html?x=1&y=2#title"}, line: 2,
    });
    assert.equal(inventory.tags.filter((tag) => tag.tagName === "a").length, 1);
});

test("duplicate attributes and nonvoid self-closing text elements keep HTML behavior", () => {
    const inventory = parseHtmlInventory('<script/><a href="fake.html"></script><a id="first" id="second" href="real.html" href="ignored.html">');
    assert.deepEqual(inventory.anchors, new Set(["first"]));
    assert.deepEqual(inventory.links, [{value: "real.html", line: 1, attribute: "href"}]);
});

test("percent escapes, entities, queries, fragments and directory indexes resolve", async (t) => {
    const {site, put} = await fixture(t);
    await put("index.html", '<h1 id="local">Home</h1><a href="?lang=ro#local">Here</a><a href="chapters/a%20%26%20b.html?lang=ro&amp;x=2#caf%C3%A9">Chapter</a><a href="chapters/#start">Contents</a><a href="document.pdf#page=2">PDF</a>');
    await put("chapters/index.html", '<h1 id="start">Contents</h1><a href="/index.html#local">Home</a>');
    await put("chapters/a & b.html", '<h2 id="caf&#233;">Title</h2><a name="legacy"></a><a href="#legacy">Jump</a>');
    await put("document.pdf", "PDF fixture");
    assert.deepEqual(await audit(site), []);
});

test("missing targets and anchors have stable order and start-tag lines", async (t) => {
    const {site, put} = await fixture(t);
    await put("index.html", '<a href="z.html">Missing</a>\n<img\n src="missing.png">\n<a href="other.html#absent">Anchor</a>\n<a href="empty/">Directory</a>');
    await put("other.html", '<p id="present">Existing</p>');
    await mkdir(path.join(site, "empty"));
    assert.deepEqual(await audit(site), [
        "index.html:1: missing local target: z.html",
        "index.html:2: missing local target: missing.png",
        "index.html:4: missing anchor #absent in other.html",
        "index.html:5: missing local target: empty/",
    ]);
});

test("srcset keeps data URLs and audits local alternatives", async (t) => {
    const {site, put} = await fixture(t);
    await put("index.html", '<img srcset=", , data:image/svg+xml,%3Csvg%3E%3C/svg%3E 1x, small.png 2x, missing.png 3x,">');
    await put("small.png", "image");
    const inventory = parseHtmlInventory('<img srcset="first.png 1x,second.png 2x, third.png, fourth.png 4x">');
    assert.deepEqual(inventory.links.map((link) => link.value), ["first.png", "second.png", "third.png", "fourth.png"]);
    assert.deepEqual(await audit(site), ["index.html:1: missing local target: missing.png"]);
});

test("external schemes and network-relative references are ignored", async (t) => {
    const {site, put} = await fixture(t);
    const external = ["https://example.invalid/nope", "HTTP://example.invalid/nope", "//example.invalid/nope", "mailto:reader@example.test", "tel:+123", "javascript:void(0)", "data:text/plain,hello", "ftp://example.invalid/book.pdf", "file:///nope", "custom:thing", "https://[invalid", "\\\\example.invalid/nope", "/\\example.invalid/nope"];
    await put("index.html", external.map((href) => `<a href="${href}">Link</a>`).join("\n"));
    assert.deepEqual(await audit(site), []);
});

test("traversal and symlink targets cannot escape the site root", async (t) => {
    const {folder, site, put} = await fixture(t);
    await put("index.html", '<a href="../outside.html">Outside</a>\n<a href="%2e%2e/outside.html">Encoded</a>\n<a href="assets/secret.pdf">Symlink directory</a>\n<a href="out.pdf">Symlink file</a>\n<a href="dangling.pdf">Dangling symlink</a>\n<a href="chapter/">Index symlink</a>');
    await writeFile(path.join(folder, "outside.html"), '<a href="not-scanned.html">Outside source</a>');
    await writeFile(path.join(folder, "secret.pdf"), "outside");
    await symlink(folder, path.join(site, "assets"), "dir");
    await symlink(path.join(folder, "secret.pdf"), path.join(site, "out.pdf"));
    await symlink(path.join(folder, "missing.pdf"), path.join(site, "dangling.pdf"));
    await mkdir(path.join(site, "chapter"));
    await symlink(path.join(folder, "outside.html"), path.join(site, "chapter/index.html"));
    const problems = await audit(site);
    assert.equal(problems.length, 7);
    assert.ok(problems.every((problem) => problem.includes("escapes docs/")));
    assert.ok(problems.some((problem) => problem.includes("href escapes docs/: chapter/")));
    assert.ok(problems.every((problem) => !problem.includes("not-scanned")));
});

test("in-root symlinks and directory cycles are supported", async (t) => {
    const {site, put} = await fixture(t);
    await put("index.html", '<a href="copy.html#target">Alias</a><a href="assets/page.html#target">Directory alias</a>');
    await put("real/page.html", '<h1 id="target">Target</h1>');
    await symlink(path.join(site, "real/page.html"), path.join(site, "copy.html"));
    await symlink(path.join(site, "real"), path.join(site, "assets"), "dir");
    await symlink(site, path.join(site, "real/cycle"), "dir");
    assert.deepEqual(await audit(site), []);
});

test("dot segments collapse before directory symlinks are followed", async (t) => {
    const {site, put} = await fixture(t);
    await put("index.html", '<a href="alias/../sibling.html#target">Sibling</a>\n<a href="/alias/%2e%2e/sibling.html#absent">Missing anchor</a>');
    await put("sibling.html", '<h1 id="target">Root sibling</h1>');
    await put("real/sibling.html", '<h1 id="absent">Wrong sibling</h1>');
    await mkdir(path.join(site, "real/nested"));
    await symlink(path.join(site, "real/nested"), path.join(site, "alias"), "dir");
    assert.deepEqual(await audit(site), ["index.html:2: missing anchor #absent in sibling.html"]);
});

test("malformed percent escapes and decoded nulls do not stop the audit", async (t) => {
    const {site, put} = await fixture(t);
    await put("index.html", '<a href="bad%ZZ.html">Literal percent</a>\n<a href="%FF.html">Bad UTF8</a>\n<a href="bad%00.html">Null</a>');
    await put("bad%ZZ.html", "<p>Literal filename</p>");
    assert.deepEqual(await audit(site), [
        "index.html:2: missing local target: %FF.html",
        "index.html:3: invalid local target: bad%00.html",
    ]);
});

test("symlink file loops are reported while other references are still audited", async (t) => {
    const {site, put} = await fixture(t);
    await put("index.html", '<a href="loop.html">Loop</a><a href="missing.pdf">Another failure</a>');
    await symlink("loop.html", path.join(site, "loop.html"));
    assert.deepEqual(await audit(site), [
        "loop.html:1: missing local HTML source",
        "index.html:1: missing local target: loop.html",
        "index.html:1: missing local target: missing.pdf",
    ]);
});

test("CLI reports, exit codes, help and missing roots work from another directory", async (t) => {
    const {folder, site, put} = await fixture(t);
    await put("index.html", '<a href="missing.html">Missing</a>');
    const run = (...args) => spawnSync(process.execPath, [path.join(ROOT, "tools/audit_internal_links.mjs"), ...args], {
        cwd: folder, encoding: "utf8", timeout: 20000,
    });
    const report = run("--root", site);
    assert.equal(report.status, 0, report.stderr);
    assert.match(report.stdout, /missing local target: missing.html/);
    assert.match(report.stderr, /1 local-link problem\(s\) found/);
    assert.equal(run("--root", site, "--check").status, 1);
    const missing = run("--root", path.join(folder, "absent"), "--check");
    assert.equal(missing.status, 2);
    assert.match(missing.stderr, /Missing site root/);
    assert.equal(run("--unknown").status, 2);
    assert.equal(run("--root").status, 2);
    assert.equal(run("--help").status, 0);
    await put("missing.html", "<p>Added</p>");
    const valid = run(`--root=${site}`, "--check");
    assert.equal(valid.status, 0, valid.stderr);
    assert.match(valid.stdout, /No broken local HTML links or fragment anchors/);
});

test("named references, multi-codepoint names and numeric recovery preserve original decoding", () => {
    assert.equal(decodeHtmlEntities("&CounterClockwiseContourIntegral;&NotEqualTilde;&fjlig;&Afr;"), "∳≂̸fj𝔄");
    assert.equal(decodeHtmlEntities("a&amp;b &notit; &bogus; &#x1f600; &#128;"), "a&b ¬it; &bogus; 😀 €");
    assert.equal(decodeHtmlEntities("&#0;&#xD800;&#1114112;&#xFDD0;&#1;&#13;"), "���\r");
    const inventory = parseHtmlInventory('<a href="a&sol;b&num;caf&eacute;" id="&NotEqualTilde;" name="caf&#xe9;">');
    assert.deepEqual(inventory.links, [{value: "a/b#café", line: 1, attribute: "href"}]);
    assert.deepEqual(inventory.anchors, new Set(["≂̸", "café"]));
});

test("quoted angle brackets, boolean attributes and prototype names do not confuse the inventory", () => {
    const inventory = parseHtmlInventory('<a title="<img src=missing>" disabled __proto__="safe" href=real.html id=anchor>\n<img src="other>name.png">');
    assert.equal(inventory.tags[0].attrs.disabled, null);
    assert.equal(Object.getPrototypeOf(inventory.tags[0].attrs), Object.prototype);
    assert.equal(inventory.tags[0].attrs.__proto__, "safe");
    assert.deepEqual(inventory.links, [
        {value: "real.html", line: 1, attribute: "href"},
        {value: "other>name.png", line: 2, attribute: "src"},
    ]);
});

test("each raw-text element suppresses fake links even after a self-closing slash", () => {
    for (const tag of ["script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes"]) {
        const inventory = parseHtmlInventory(`<${tag}/><a href="missing.html">\n</${tag.toUpperCase()}><a href="real.html">`);
        assert.deepEqual(inventory.links, [{value: "real.html", line: 2, attribute: "href"}], tag);
    }
    assert.deepEqual(parseHtmlInventory('<script><a href="hidden.html">').links, []);
    assert.deepEqual(parseHtmlInventory('<!-- <a href="hidden.html">').links, []);
});

test("dangling symlink ancestors are confined and in-root aliases retain source-relative links", async (t) => {
    const {folder, site, put} = await fixture(t);
    await put("index.html", '<a href="dangling/leaf.pdf">Outside</a><a href="missing/leaf.pdf">Inside</a>');
    await put("real/page.html", '<a href="sibling.html">Relative</a>');
    await put("real/sibling.html", "<p>Sibling</p>");
    await symlink(path.join(folder, "absent"), path.join(site, "dangling"), "dir");
    await symlink(path.join(site, "absent"), path.join(site, "missing"), "dir");
    await symlink(path.join(site, "real/page.html"), path.join(site, "copy.html"));
    assert.deepEqual(await audit(site), [
        "copy.html:1: missing local target: sibling.html",
        "index.html:1: href escapes docs/: dangling/leaf.pdf",
        "index.html:1: missing local target: missing/leaf.pdf",
    ]);
});

test("symlink destination dot segments follow filesystem ordering before confinement", async (t) => {
    const {folder, site, put} = await fixture(t);
    await put("index.html", '<a href="tricky.pdf">Outside through a nested link</a>');
    await put("safe.pdf", "Inside file with the same name");
    await mkdir(path.join(folder, "outside/nested"), {recursive: true});
    await writeFile(path.join(folder, "outside/safe.pdf"), "Outside file");
    await symlink(path.join(folder, "outside/nested"), path.join(site, "alias"), "dir");
    await symlink("alias/../safe.pdf", path.join(site, "tricky.pdf"));
    assert.deepEqual(await audit(site), ["index.html:1: href escapes docs/: tricky.pdf"]);
});

test("recoverable malformed HTML keeps the same inventory as the original tool", () => {
    const inventory = parseHtmlInventory('<!--><a href=one\'two.html><!-- x --!><a href=one"two.html><a =foo href=third.html>');
    assert.deepEqual(inventory.links.map((link) => link.value), ["one'two.html", 'one"two.html', "third.html"]);
    assert.equal(inventory.tags[2].attrs["=foo"], null);
    assert.deepEqual(parseHtmlInventory('<script><a href=hidden></ script><a href=still-hidden>').links, []);
    for (const closing of ["</script >", "</script foo>", "</script/>", "</script\n>"]) {
        const result = parseHtmlInventory(`<script><a href=hidden>${closing}<a href=visible>`);
        assert.deepEqual(result.links.map((link) => link.value), ["visible"]);
    }
});

test("a copied auditor resolves bundled resources through a symlink from another directory", async (t) => {
    const {folder, site, put} = await fixture(t);
    await put("index.html", '<h1 id="caf&#233;">Title</h1><a href="#caf%C3%A9">Chapter</a>');
    const copied = path.join(folder, "copied");
    await mkdir(path.join(copied, "tools/lib"), {recursive: true});
    await mkdir(path.join(copied, "external"));
    await copyFile(path.join(ROOT, "tools/audit_internal_links.mjs"), path.join(copied, "tools/audit_internal_links.mjs"));
    await copyFile(path.join(ROOT, "tools/lib/runtime.mjs"), path.join(copied, "tools/lib/runtime.mjs"));
    await cp(path.join(ROOT, "external/html-entities"), path.join(copied, "external/html-entities"), {recursive: true});
    const alias = path.join(folder, "aliased");
    await symlink(copied, alias, "dir");
    const result = spawnSync(process.execPath, [path.join(alias, "tools/audit_internal_links.mjs"), "--root", site, "--check"], {
        cwd: tmpdir(), encoding: "utf8", timeout: 20000,
    });
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /No broken local HTML links or fragment anchors/);
});
