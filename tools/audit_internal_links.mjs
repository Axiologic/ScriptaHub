#!/usr/bin/env node
/** Report broken local links and fragment anchors without contacting the web. */

import {readFile, readdir, lstat, stat, readlink, realpath} from "node:fs/promises";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {assertNodeVersion} from "./lib/runtime.mjs";

assertNodeVersion();

export const DEFAULT_SITE = fileURLToPath(new URL("../docs", import.meta.url));
const LINK_ATTRIBUTES = new Set(["href", "src", "poster"]);
const TEXT_ELEMENTS = new Set(["script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes"]);
const ASCII_SPACE = /[\t\n\f\r ]/;
const EXTERNAL_REFERENCE = /^(?:[\\/]{2}|[a-z][a-z\d+.-]*:)/i;
const MISSING_CODES = new Set(["ENOENT", "ENOTDIR", "ELOOP"]);
const entityPath = new URL("../external/html-entities/entities.json", import.meta.url);
const namedReferences = JSON.parse(await readFile(entityPath, "utf8"));
const WINDOWS_CODEPOINTS = [
    0x20ac, 0x81, 0x201a, 0x192, 0x201e, 0x2026, 0x2020, 0x2021,
    0x2c6, 0x2030, 0x160, 0x2039, 0x152, 0x8d, 0x17d, 0x8f,
    0x90, 0x2018, 0x2019, 0x201c, 0x201d, 0x2022, 0x2013, 0x2014,
    0x2dc, 0x2122, 0x161, 0x203a, 0x153, 0x9d, 0x17e, 0x178,
];

function numericCharacter(value) {
    const hexadecimal = /^#x/i.test(value);
    let codepoint = Number.parseInt(value.slice(hexadecimal ? 2 : 1), hexadecimal ? 16 : 10);
    if (codepoint === 0 || codepoint > 0x10ffff || (codepoint >= 0xd800 && codepoint <= 0xdfff)) {
        return "\ufffd";
    }
    if (codepoint >= 0x80 && codepoint <= 0x9f) {
        codepoint = WINDOWS_CODEPOINTS[codepoint - 0x80];
    } else if ((codepoint >= 1 && codepoint <= 8) || codepoint === 11
        || (codepoint >= 14 && codepoint <= 31) || codepoint === 127
        || (codepoint >= 0xfdd0 && codepoint <= 0xfdef)
        || (codepoint & 0xffff) >= 0xfffe) {
        return "";
    }
    return String.fromCodePoint(codepoint);
}

/** Match the original tool's html.unescape behavior, including legacy names. */
export function decodeHtmlEntities(value) {
    return value.replace(/&(#(?:[xX][0-9a-fA-F]+|[0-9]+);?|[^\t\n\f <&#;]{1,32};?)/g, (reference, name) => {
        if (name.startsWith("#")) {
            return numericCharacter(name);
        }
        for (let length = name.length; length > 0; length--) {
            const entry = namedReferences[`&${name.slice(0, length)}`];
            if (entry) {
                return entry.characters + name.slice(length);
            }
        }
        return reference;
    });
}

export function srcsetUrls(value) {
    const urls = [];
    let position = 0;
    while (position < value.length) {
        while (position < value.length && (ASCII_SPACE.test(value[position]) || value[position] === ",")) {
            position++;
        }
        const start = position;
        while (position < value.length && !ASCII_SPACE.test(value[position])) {
            position++;
        }
        let url = value.slice(start, position);
        if (!url) {
            break;
        }
        if (url.endsWith(",")) {
            url = url.replace(/,+$/, "");
        } else {
            let parentheses = 0;
            while (position < value.length) {
                const character = value[position++];
                if (character === "(") {
                    parentheses++;
                } else if (character === ")" && parentheses) {
                    parentheses--;
                } else if (character === "," && !parentheses) {
                    break;
                }
            }
        }
        if (url) {
            urls.push(url);
        }
    }
    return urls;
}

function tagEnd(source, start) {
    let quote = null;
    let state = "attribute";
    for (let position = start; position < source.length; position++) {
        const character = source[position];
        if (quote) {
            if (character === quote) {
                quote = null;
                state = "attribute";
            }
        } else if (character === ">") {
            return position;
        } else if (state === "value") {
            if (ASCII_SPACE.test(character)) {
                continue;
            }
            if (character === '"' || character === "'") {
                quote = character;
            } else {
                state = "unquoted";
            }
        } else if (state === "unquoted") {
            if (ASCII_SPACE.test(character)) {
                state = "attribute";
            }
        } else if (character === "=") {
            state = "value";
        }
    }
    return -1;
}

function tagAttributes(source) {
    const attributes = new Map();
    let position = 0;
    while (position < source.length) {
        while (position < source.length && (ASCII_SPACE.test(source[position]) || source[position] === "/")) {
            position++;
        }
        const nameStart = position;
        if (source[position] === "=") {
            position++;
        }
        while (position < source.length && !/[\t\n\f\r =>/]/.test(source[position])) {
            position++;
        }
        if (position === nameStart) {
            position++;
            continue;
        }
        const name = source.slice(nameStart, position).toLowerCase();
        while (position < source.length && ASCII_SPACE.test(source[position])) {
            position++;
        }
        let value = null;
        if (source[position] === "=") {
            position++;
            while (position < source.length && ASCII_SPACE.test(source[position])) {
                position++;
            }
            const quote = source[position] === '"' || source[position] === "'" ? source[position++] : null;
            const valueStart = position;
            while (position < source.length && (quote ? source[position] !== quote : !ASCII_SPACE.test(source[position]))) {
                position++;
            }
            value = decodeHtmlEntities(source.slice(valueStart, position));
            if (quote && position < source.length) {
                position++;
            }
        }
        if (!attributes.has(name)) {
            attributes.set(name, value);
        }
    }
    return Object.fromEntries(attributes);
}

/** Collect start tags, anchors and references; this is an inventory, not a DOM. */
export function parseHtmlInventory(source) {
    const inventory = {links: [], anchors: new Set(), tags: []};
    let position = 0;
    let line = 1;
    const advance = (end) => {
        for (let index = position; index < end; index++) {
            if (source[index] === "\n") {
                line++;
            }
        }
        position = end;
    };
    while (position < source.length) {
        const start = source.indexOf("<", position);
        if (start < 0) {
            break;
        }
        advance(start);
        if (source.startsWith("<!--", position)) {
            if (source.startsWith("<!-->", position) || source.startsWith("<!--->", position)) {
                advance(position + (source[position + 4] === ">" ? 5 : 6));
                continue;
            }
            const ending = /--(?:\s*|!)>/g;
            ending.lastIndex = position + 4;
            const match = ending.exec(source);
            if (!match) {
                break;
            }
            advance(ending.lastIndex);
            continue;
        }
        if (/[!?/]/.test(source[position + 1] ?? "")) {
            const end = source.indexOf(">", position + 2);
            if (end < 0) {
                break;
            }
            advance(end + 1);
            continue;
        }
        const name = /^[a-zA-Z][^\t\n\f\r />]*/.exec(source.slice(position + 1));
        if (!name) {
            advance(position + 1);
            continue;
        }
        const end = tagEnd(source, position + 1 + name[0].length);
        if (end < 0) {
            break;
        }
        const tagName = name[0].toLowerCase();
        const attrs = tagAttributes(source.slice(position + 1 + name[0].length, end));
        inventory.tags.push({tagName, attrs, line});
        for (const [attribute, value] of Object.entries(attrs)) {
            if ((attribute === "id" || attribute === "name") && value) {
                inventory.anchors.add(value);
            } else if (LINK_ATTRIBUTES.has(attribute) && value) {
                inventory.links.push({value, line, attribute});
            } else if (attribute === "srcset" && value) {
                inventory.links.push(...srcsetUrls(value).map((url) => ({value: url, line, attribute})));
            }
        }
        advance(end + 1);
        if (TEXT_ELEMENTS.has(tagName)) {
            const closing = new RegExp(`</${tagName}(?=[\\t\\n\\f\\r />])[^>]*>`, "ig");
            closing.lastIndex = position;
            if (!closing.exec(source)) {
                break;
            }
            advance(closing.lastIndex);
        }
    }
    return inventory;
}

export async function parseHtml(filename) {
    return parseHtmlInventory(await readFile(filename, "utf8"));
}

export function isWithin(filename, root) {
    const relative = path.relative(root, filename);
    return relative === "" || (!path.isAbsolute(relative) && relative !== ".." && !relative.startsWith(`..${path.sep}`));
}

export function isLocal(reference) {
    return !EXTERNAL_REFERENCE.test(reference);
}

/** Resolve existing symlink ancestors even when the final destination is missing. */
async function resolveTarget(filename, links = new Set()) {
    // Symlink destinations use filesystem ordering for their own dot segments.
    // Only the browser URL was normalized before entering this resolver.
    const absolute = path.isAbsolute(filename) ? filename : path.resolve(filename);
    const parsed = path.parse(absolute);
    const parts = absolute.slice(parsed.root.length).split(path.sep).filter(Boolean);
    let resolved = parsed.root;
    for (let index = 0; index < parts.length; index++) {
        if (parts[index] === ".") {
            continue;
        }
        if (parts[index] === "..") {
            resolved = path.dirname(resolved);
            continue;
        }
        resolved = path.join(resolved, parts[index]);
        let metadata;
        try {
            metadata = await lstat(resolved);
        } catch (error) {
            if (error.code === "ENOENT" || error.code === "ENOTDIR") {
                return path.join(resolved, ...parts.slice(index + 1));
            }
            throw error;
        }
        if (metadata.isSymbolicLink()) {
            if (links.has(resolved)) {
                throw Object.assign(new Error(`Symlink loop: ${resolved}`), {code: "ELOOP"});
            }
            const nextLinks = new Set(links).add(resolved);
            const link = await readlink(resolved);
            const destination = path.isAbsolute(link) ? link : `${path.dirname(resolved)}${path.sep}${link}`;
            resolved = await resolveTarget(destination, nextLinks);
        }
    }
    return resolved;
}

async function fileMetadata(filename) {
    try {
        return await stat(filename);
    } catch (error) {
        if (MISSING_CODES.has(error.code)) {
            return null;
        }
        throw error;
    }
}

function displayPath(filename, root) {
    return path.relative(root, filename).split(path.sep).join("/");
}

async function htmlSources(site, problems) {
    const files = [];
    async function visit(folder) {
        const entries = await readdir(folder, {withFileTypes: true});
        entries.sort((left, right) => left.name < right.name ? -1 : left.name > right.name ? 1 : 0);
        for (const entry of entries) {
            const filename = path.join(folder, entry.name);
            const html = path.extname(filename).toLowerCase() === ".html";
            if (entry.isSymbolicLink()) {
                if (!html) {
                    continue;
                }
                const display = displayPath(filename, site);
                try {
                    const target = await resolveTarget(filename);
                    if (!isWithin(target, site)) {
                        problems.push(`${display}:1: HTML source escapes docs/: ${display}`);
                    } else if ((await fileMetadata(target))?.isFile()) {
                        files.push(filename);
                    } else {
                        problems.push(`${display}:1: missing local HTML source`);
                    }
                } catch (error) {
                    if (!MISSING_CODES.has(error.code)) {
                        throw error;
                    }
                    problems.push(`${display}:1: missing local HTML source`);
                }
            } else if (entry.isDirectory()) {
                await visit(filename);
            } else if (entry.isFile() && html) {
                files.push(filename);
            }
        }
    }
    await visit(site);
    return files.sort();
}

/** urllib-style percent decoding leaves malformed escapes and replaces bad UTF-8. */
function unquote(value) {
    return value.replace(/(?:%[0-9a-fA-F]{2})+/g, (run) => {
        const bytes = run.match(/[0-9a-fA-F]{2}/g).map((byte) => Number.parseInt(byte, 16));
        return Buffer.from(bytes).toString("utf8");
    });
}

export async function audit(site) {
    site = await realpath(site);
    const problems = [];
    const inventory = new Map();
    const anchors = new Map();
    for (const source of await htmlSources(site, problems)) {
        const data = await parseHtml(source);
        inventory.set(source, data.links);
        anchors.set(await resolveTarget(source), data.anchors);
    }
    for (const [source, links] of inventory) {
        for (const link of links) {
            const reference = link.value.trim();
            if (!reference || !isLocal(reference)) {
                continue;
            }
            const hash = reference.indexOf("#");
            const beforeHash = hash < 0 ? reference : reference.slice(0, hash);
            const localPath = unquote(beforeHash.split("?", 1)[0]).replaceAll("\\", "/");
            const fragment = hash < 0 ? "" : unquote(reference.slice(hash + 1));
            const prefix = `${displayPath(source, site)}:${link.line}:`;
            if (localPath.includes("\0")) {
                problems.push(`${prefix} invalid local target: ${reference}`);
                continue;
            }
            // Collapse URL dot segments before following filesystem symlinks.
            const lexicalTarget = !localPath ? source
                : localPath.startsWith("/") ? path.resolve(site, localPath.slice(1))
                : path.resolve(path.dirname(source), localPath);
            let target;
            try {
                target = await resolveTarget(lexicalTarget);
                if (!isWithin(target, site)) {
                    problems.push(`${prefix} ${link.attribute} escapes docs/: ${reference}`);
                    continue;
                }
                let metadata = await fileMetadata(target);
                if (metadata?.isDirectory()) {
                    target = await resolveTarget(path.join(target, "index.html"));
                    metadata = await fileMetadata(target);
                }
                if (!isWithin(target, site)) {
                    problems.push(`${prefix} ${link.attribute} escapes docs/: ${reference}`);
                    continue;
                }
                if (!metadata?.isFile()) {
                    problems.push(`${prefix} missing local target: ${reference}`);
                    continue;
                }
            } catch (error) {
                if (!MISSING_CODES.has(error.code)) {
                    throw error;
                }
                problems.push(`${prefix} missing local target: ${reference}`);
                continue;
            }
            if (fragment) {
                let targetAnchors = anchors.get(target);
                if (!targetAnchors && path.extname(target).toLowerCase() === ".html") {
                    targetAnchors = (await parseHtml(target)).anchors;
                    anchors.set(target, targetAnchors);
                }
                if (targetAnchors && !targetAnchors.has(fragment)) {
                    problems.push(`${prefix} missing anchor #${fragment} in ${displayPath(target, site)}`);
                }
            }
        }
    }
    return problems;
}

export async function main(argv = process.argv.slice(2)) {
    let root = DEFAULT_SITE;
    let check = false;
    for (let index = 0; index < argv.length; index++) {
        const argument = argv[index];
        if (argument === "--help" || argument === "-h") {
            console.log("Usage: node tools/audit_internal_links.mjs [--root ROOT] [--check]\n\nReport broken local links and fragment anchors without contacting the web.\n\n  --root ROOT  static-site root to scan (default: docs)\n  --check      return 1 if a broken local link or anchor is found");
            return 0;
        }
        if (argument === "--check") {
            check = true;
        } else if (argument === "--root" && argv[index + 1] && !argv[index + 1].startsWith("--")) {
            root = argv[++index];
        } else if (argument.startsWith("--root=")) {
            root = argument.slice("--root=".length);
        } else {
            console.error(`Invalid argument: ${argument}. Use --help for usage.`);
            return 2;
        }
    }
    try {
        if (!(await fileMetadata(root))?.isDirectory()) {
            console.error(`Missing site root: ${root}`);
            return 2;
        }
        const problems = await audit(root);
        if (problems.length) {
            console.log(problems.join("\n"));
            console.error(`\n${problems.length} local-link problem(s) found.`);
            return check ? 1 : 0;
        }
        console.log(`No broken local HTML links or fragment anchors in ${root}.`);
        return 0;
    } catch (error) {
        console.error(`Unable to audit site: ${error.message}`);
        return 2;
    }
}

if (process.argv[1] && await realpath(process.argv[1]).catch(() => null) === fileURLToPath(import.meta.url)) {
    process.exitCode = await main();
}
