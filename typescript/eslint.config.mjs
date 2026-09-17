import tseslint from 'typescript-eslint';

export default [
  { ignores: ['src/generated/**'] },
  ...tseslint.configs.recommended,
];
