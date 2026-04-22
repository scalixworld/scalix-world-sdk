/**
 * Scalix SDK configuration management.
 *
 * Configuration priority (lowest to highest):
 * 1. Defaults (local mode)
 * 2. Config file (~/.scalix/config.json or scalix.config.json)
 * 3. Environment variables
 * 4. Programmatic via configure()
 */

export interface ScalixConfig {
  apiKey?: string;
  projectId?: string;
  environment: 'development' | 'staging' | 'production';
  baseUrl: string;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
  defaultModel: string;
  sandboxMode: 'auto' | 'docker' | 'subprocess' | 'cloud';
  databaseMode: 'auto' | 'sqlite' | 'cloud';
  openaiApiKey?: string;
  anthropicApiKey?: string;
  googleApiKey?: string;
  ollamaHost?: string;
}

const DEFAULT_CONFIG: ScalixConfig = {
  environment: 'development',
  baseUrl: 'https://api.scalix.world',
  logLevel: 'info',
  defaultModel: 'auto',
  sandboxMode: 'auto',
  databaseMode: 'auto',
};

let _config: ScalixConfig | null = null;

/**
 * Configure the Scalix SDK.
 *
 * @example
 * ```typescript
 * import { configure } from 'scalix';
 * configure({ apiKey: 'sk-scalix-...' });
 * ```
 */
export function configure(options: Partial<ScalixConfig>): ScalixConfig {
  _config = loadConfig(options);
  return _config;
}

/**
 * Get the current SDK configuration.
 */
export function getConfig(): ScalixConfig {
  if (!_config) {
    _config = loadConfig({});
  }
  return _config;
}

/**
 * Check if the SDK is in cloud mode (Scalix API key configured).
 */
export function isCloudMode(): boolean {
  return getConfig().apiKey != null;
}

/**
 * Dynamic import that bypasses TypeScript module resolution.
 * Used for optional peer dependencies that may not be installed.
 */
// eslint-disable-next-line @typescript-eslint/no-implied-eval
export const dynamicImport = new Function('specifier', 'return import(specifier)') as (specifier: string) => Promise<unknown>;

function loadConfig(overrides: Partial<ScalixConfig>): ScalixConfig {
  const env = typeof process !== 'undefined' ? process.env : {};

  return {
    ...DEFAULT_CONFIG,
    // Environment variables
    ...(env.SCALIX_API_KEY && { apiKey: env.SCALIX_API_KEY }),
    ...(env.SCALIX_PROJECT_ID && { projectId: env.SCALIX_PROJECT_ID }),
    ...(env.OPENAI_API_KEY && { openaiApiKey: env.OPENAI_API_KEY }),
    ...(env.ANTHROPIC_API_KEY && { anthropicApiKey: env.ANTHROPIC_API_KEY }),
    ...(env.GOOGLE_API_KEY && { googleApiKey: env.GOOGLE_API_KEY }),
    ...(env.OLLAMA_HOST && { ollamaHost: env.OLLAMA_HOST }),
    // Programmatic overrides (highest priority)
    ...overrides,
  };
}
