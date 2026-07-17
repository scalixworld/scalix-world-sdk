#!/usr/bin/env node
// Dual-format build: emit ESM (dist/esm) + CommonJS (dist/cjs) so the SDK works
// for both `import` and `require` consumers. Zero extra build dependencies — two
// tsc passes plus the per-directory `type` markers Node needs to interpret each
// tree correctly (the root package.json is `"type": "module"`).
import { execFileSync } from 'node:child_process';
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const dist = join(root, 'dist');
const tsc = join(root, 'node_modules', 'typescript', 'bin', 'tsc');

rmSync(dist, { recursive: true, force: true });

for (const project of ['tsconfig.esm.json', 'tsconfig.cjs.json']) {
  execFileSync(process.execPath, [tsc, '-p', project], { cwd: root, stdio: 'inherit' });
}

mkdirSync(join(dist, 'esm'), { recursive: true });
mkdirSync(join(dist, 'cjs'), { recursive: true });
writeFileSync(join(dist, 'esm', 'package.json'), `${JSON.stringify({ type: 'module' }, null, 2)}\n`);
writeFileSync(join(dist, 'cjs', 'package.json'), `${JSON.stringify({ type: 'commonjs' }, null, 2)}\n`);

console.log('build: dual ESM (dist/esm) + CJS (dist/cjs) emitted');
