import { defineConfig } from '@hey-api/openapi-ts';

// Generates a fetch-based TypeScript client FROM the committed spec at ../openapi.json.
// Output lands in src/generated/ and IS the package's public API since the cutover:
// src/index.ts re-exports it. Regenerate with: npm run generate:ts
export default defineConfig({
  input: '../openapi.json',
  output: {
    path: 'src/generated',
    postProcess: [],
    // Emit explicit .js extensions on relative imports so the tsc ESM output
    // is loadable by plain Node (extensionless specifiers only work in bundlers).
    importFileExtension: '.js',
  },
  // Fetch-based client — no extra runtime dependency beyond the global fetch.
  plugins: ['@hey-api/client-fetch'],
});
