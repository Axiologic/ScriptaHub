#!/usr/bin/env node
/** Report broken local targets and HTML fragments without contacting the network. */
import { lstatSync, readFileSync, readdirSync, readlinkSync, realpathSync, statSync } from 'node:fs';
import { basename, dirname, extname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import { SAXParser } from 'parse5-sax-parser';

const DEFAULT_SITE = fileURLToPath(new URL('../docs', import.meta.url));
const LINK_ATTRIBUTES = new Set(['href', 'src', 'poster']);
const SPACE = /[\t\n\f\r ]/;

function srcsetUrls(value) {
  const urls = [];
  let position = 0;
  while (position < value.length) {
    while (position < value.length && (SPACE.test(value[position]) || value[position] === ',')) position++;
    const start = position;
    while (position < value.length && !SPACE.test(value[position])) position++;
    let url = value.slice(start, position);
    if (!url) break;
    if (url.endsWith(',')) {
      url = url.replace(/,+$/, '');
    } else {
      // A comma inside a URL (notably a data URL) is not a candidate separator.
      // Descriptors end at a comma outside parentheses, as in HTML srcset parsing.
      let parentheses = 0;
      while (position < value.length) {
        const character = value[position++];
        if (character === '(') parentheses++;
        else if (character === ')' && parentheses) parentheses--;
        else if (character === ',' && !parentheses) break;
      }
    }
    if (url) urls.push(url);
  }
  return urls;
}

export function parseHtmlInventory(source) {
  const inventory = { anchors: new Set(), links: [], tags: [] };
  const parser = new SAXParser({ sourceCodeLocationInfo: true });
  parser.on('startTag', ({ tagName, attrs, sourceCodeLocation }) => {
    const line = sourceCodeLocation?.startLine || 1;
    const attributes = Object.fromEntries(attrs.map(({ name, value, prefix }) => [prefix ? `${prefix}:${name}` : name, value]));
    inventory.tags.push({ tagName, attrs: attributes, line });
    for (const [attribute, value] of Object.entries(attributes)) {
      if (!value) continue;
      if (attribute === 'id' || attribute === 'name') inventory.anchors.add(value);
      else if (LINK_ATTRIBUTES.has(attribute)) inventory.links.push({ value, line, attribute });
      else if (attribute === 'srcset') {
        for (const url of srcsetUrls(value)) inventory.links.push({ value: url, line, attribute });
      }
    }
  });
  parser.end(String(source));
  return inventory;
}

function within(path, root) {
  const child = relative(root, path);
  return child !== '..' && !child.startsWith(`..${sep}`) && !isAbsolute(child);
}

function displayPath(path, root) {
  return relative(root, path).split(sep).join('/');
}

function isMissing(error) {
  return error?.code === 'ENOENT' || error?.code === 'ENOTDIR';
}

function canonicalTarget(path, followed = 0) {
  if (followed > 40) throw Object.assign(new Error('Symbolic link loop'), { code: 'ELOOP' });
  try { return realpathSync(path); } catch (error) {
    if (!isMissing(error)) throw error;
    // Follow existing ancestors even when the final file is missing. A dangling
    // symlink must not disguise an out-of-root destination as an ordinary miss.
    try {
      if (lstatSync(path).isSymbolicLink()) {
        return canonicalTarget(resolve(dirname(path), readlinkSync(path)), followed + 1);
      }
    } catch (linkError) { if (!isMissing(linkError)) throw linkError; }
    const parent = dirname(path);
    return parent === path ? path : join(canonicalTarget(parent, followed), basename(path));
  }
}

function decoded(value) {
  // Match URL percent decoding while retaining malformed percent signs and
  // replacing malformed UTF-8; a bad link should be reported, not abort a scan.
  return value.replace(/(?:%[\da-f]{2})+/gi, (bytes) => Buffer.from(bytes.replaceAll('%', ''), 'hex').toString('utf8'));
}

function localReference(value) {
  const reference = value.trim();
  if (!reference || /^[\\/]{2}/.test(reference) || /^[a-z][a-z\d+.-]*:/i.test(reference)) return null;
  const hash = reference.indexOf('#');
  const beforeHash = hash < 0 ? reference : reference.slice(0, hash);
  const query = beforeHash.indexOf('?');
  return {
    reference,
    path: decoded(query < 0 ? beforeHash : beforeHash.slice(0, query)).replaceAll('\\', '/'),
    fragment: decoded(hash < 0 ? '' : reference.slice(hash + 1)),
  };
}

function htmlSources(root, problems) {
  const files = [];
  function visit(folder) {
    for (const entry of readdirSync(folder, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name, 'en'))) {
      const path = join(folder, entry.name);
      if (entry.isDirectory()) visit(path);
      else if (entry.isFile() && extname(entry.name).toLowerCase() === '.html') files.push(path);
      else if (entry.isSymbolicLink() && extname(entry.name).toLowerCase() === '.html') {
        try {
          const target = canonicalTarget(path);
          if (!within(target, root)) problems.push(`${displayPath(path, root)}:1: HTML source escapes docs/: ${displayPath(path, root)}`);
          else if (statSync(target).isFile()) files.push(path);
        } catch (error) {
          if (!isMissing(error) && error.code !== 'ELOOP') throw error;
          problems.push(`${displayPath(path, root)}:1: missing local HTML source`);
        }
      }
    }
  }
  visit(root);
  return files.sort();
}

export function audit(site = DEFAULT_SITE) {
  const root = realpathSync(resolve(site));
  const problems = [];
  const inventory = new Map();
  const anchors = new Map();
  for (const source of htmlSources(root, problems)) {
    const data = parseHtmlInventory(readFileSync(source, 'utf8'));
    inventory.set(source, data.links);
    anchors.set(realpathSync(source), data.anchors);
  }
  for (const [source, links] of inventory) {
    for (const link of links) {
      const parts = localReference(link.value);
      if (!parts) continue;
      const prefix = `${displayPath(source, root)}:${link.line}:`;
      if (parts.path.includes('\0')) {
        problems.push(`${prefix} invalid local target: ${parts.reference}`);
        continue;
      }
      const lexicalTarget = !parts.path ? source : parts.path.startsWith('/')
        ? resolve(root, parts.path.slice(1)) : resolve(dirname(source), parts.path);
      let target;
      try {
        target = canonicalTarget(lexicalTarget);
        if (!within(target, root)) {
          problems.push(`${prefix} ${link.attribute} escapes docs/: ${parts.reference}`);
          continue;
        }
        if (statSync(target).isDirectory()) target = canonicalTarget(join(target, 'index.html'));
        if (!within(target, root)) {
          problems.push(`${prefix} ${link.attribute} escapes docs/: ${parts.reference}`);
          continue;
        }
        if (!statSync(target).isFile()) throw Object.assign(new Error('Not a file'), { code: 'ENOENT' });
      } catch (error) {
        if (!isMissing(error) && error.code !== 'ELOOP') throw error;
        problems.push(`${prefix} missing local target: ${parts.reference}`);
        continue;
      }
      if (parts.fragment) {
        let targetAnchors = anchors.get(target);
        if (!targetAnchors && extname(target).toLowerCase() === '.html') {
          targetAnchors = parseHtmlInventory(readFileSync(target, 'utf8')).anchors;
          anchors.set(target, targetAnchors);
        }
        if (targetAnchors && !targetAnchors.has(parts.fragment)) {
          problems.push(`${prefix} missing anchor #${parts.fragment} in ${displayPath(target, root)}`);
        }
      }
    }
  }
  return problems;
}

export function main(argv = process.argv.slice(2)) {
  let values;
  try {
    ({ values } = parseArgs({ args: argv, options: { root: { type: 'string', default: DEFAULT_SITE }, check: { type: 'boolean' }, help: { type: 'boolean', short: 'h' } } }));
  } catch (error) { console.error(error.message); return 2; }
  if (values.help) {
    console.log('Usage: node tools/audit_internal_links.mjs [--root PATH] [--check]\nReport broken local HTML links and fragments without network requests.');
    return 0;
  }
  try {
    if (!statSync(values.root).isDirectory()) throw new Error('Not a directory');
  } catch {
    console.error(`Missing site root: ${values.root}`);
    return 2;
  }
  try {
    const problems = audit(values.root);
    if (problems.length) {
      console.log(problems.join('\n'));
      console.error(`\n${problems.length} local-link problem(s) found.`);
      return values.check ? 1 : 0;
    }
    console.log(`No broken local HTML links or fragment anchors in ${values.root}.`);
    return 0;
  } catch (error) {
    console.error(`Unable to audit site: ${error.message}`);
    return 2;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) process.exitCode = main();
