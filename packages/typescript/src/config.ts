export interface ScalixConfig {
  apiKey?: string;
  baseUrl: string;
  defaultModel: string;
}

const DEFAULT_CONFIG: ScalixConfig = {
  baseUrl: 'https://api.scalix.world',
  defaultModel: 'scalix-world-ai',
};

let _config: ScalixConfig | null = null;

export function configure(options: Partial<ScalixConfig>): ScalixConfig {
  const env = typeof process !== 'undefined' ? process.env : {};
  _config = {
    ...DEFAULT_CONFIG,
    ...(env.SCALIX_API_KEY && { apiKey: env.SCALIX_API_KEY }),
    ...(env.SCALIX_BASE_URL && { baseUrl: env.SCALIX_BASE_URL }),
    ...options,
  };
  return _config;
}

export function getConfig(): ScalixConfig {
  if (!_config) {
    _config = configure({});
  }
  return _config;
}
