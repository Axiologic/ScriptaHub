import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { assertNodeVersion } from './lib/runtime.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));

async function main() {
    assertNodeVersion(undefined, 'build:auth');
    let build;
    const licenses = new Map();
    try {
        const versions = { esbuild: '0.28.2', 'openid-client': '6.8.7', jose: '6.2.12', oauth4webapi: '3.8.8' };
        for (const [name, expected] of Object.entries(versions)) {
            const folder = path.join(root, 'node_modules', name);
            const metadata = JSON.parse(await readFile(path.join(folder, 'package.json'), 'utf8'));
            if (metadata.version !== expected) throw new Error(`Expected ${name} ${expected}, found ${metadata.version}`);
            if (name !== 'esbuild') licenses.set(name, await readFile(path.join(folder, 'LICENSE.md')));
        }
        ({ build } = await import('esbuild'));
        // Probe the platform binary before creating any browser output.
        const { transform } = await import('esbuild');
        await transform('');
    } catch (error) {
        throw new Error(`build:auth requires the pinned npm packages and esbuild platform binary. Run npm ci in ${root}; see dependencies.md. ${error.message}`);
    }
    await build({
        absWorkingDir: root,
        entryPoints: ['src/auth.js', 'src/auth-callback.js'],
        outdir: 'docs/assets',
        bundle: true,
        minify: true,
        format: 'iife',
        platform: 'browser',
        target: ['es2022'],
        legalComments: 'external',
    });
    await mkdir(path.join(root, 'docs/assets/licenses'), { recursive: true });
    for (const [name, license] of licenses) {
        await writeFile(path.join(root, 'docs/assets/licenses', `${name}.txt`), license);
    }
}

try {
    await main();
} catch (error) {
    console.error(error.message);
    process.exitCode = 1;
}
