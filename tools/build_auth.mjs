import { build } from 'esbuild';
import { readFile, writeFile, mkdir } from 'node:fs/promises';

await build({
  entryPoints: ['src/auth.js', 'src/auth-callback.js'],
  outdir: 'docs/assets', bundle: true, minify: true, format: 'iife',
  platform: 'browser', target: ['es2022'], legalComments: 'external',
});
await mkdir('docs/assets/licenses', { recursive: true });
for (const name of ['openid-client', 'oauth4webapi', 'jose']) {
  await writeFile(`docs/assets/licenses/${name}.txt`, await readFile(`node_modules/${name}/LICENSE.md`));
}
