/**
 * Scalix — unified client for the Scalix platform.
 *
 * Chat completions delegate to the OpenAI SDK (Scalix's API is OpenAI-compatible).
 * Platform services (research, RAG, database, etc.) use a native HTTP client.
 *
 * @example
 * ```typescript
 * import { Scalix } from '@scalix-world/sdk';
 *
 * const scalix = new Scalix('sk_scalix_...');
 *
 * // Chat — full OpenAI-compatible (tools, vision, streaming)
 * const response = await scalix.completions.create({
 *   model: 'scalix-world-ai',
 *   messages: [{ role: 'user', content: 'Hello!' }],
 * });
 *
 * // Platform services
 * const results = await scalix.research.search('AI trends');
 * ```
 */

import OpenAI from 'openai';
import type { ScalixConfig } from './config.js';
import { AccountService } from './services/account.js';
import { AudioService } from './services/audio.js';
import { DocGenService } from './services/docgen.js';
import { ImagesService } from './services/images.js';
import { ModelsService } from './services/models.js';
import { RAGService } from './services/rag.js';
import { ResearchService } from './services/research.js';
import { StorageService } from './services/storage.js';
import { TextService } from './services/text.js';

export interface ScalixOptions {
  baseURL?: string;
  maxRetries?: number;
  timeout?: number;
}

export class Scalix {
  /** OpenAI-compatible chat completions — full tool calling, vision, streaming */
  readonly completions: OpenAI['chat']['completions'];

  /** Pre-configured OpenAI client for advanced usage (embeddings, raw access, etc.) */
  readonly openai: OpenAI;

  readonly account: AccountService;
  readonly audio: AudioService;
  readonly docgen: DocGenService;
  readonly images: ImagesService;
  readonly models: ModelsService;
  readonly rag: RAGService;
  readonly research: ResearchService;
  readonly storage: StorageService;
  readonly text: TextService;

  constructor(apiKey: string, options?: ScalixOptions) {
    const base = options?.baseURL ?? 'https://api.scalix.world';
    const baseURL = base.endsWith('/v1') ? base : `${base}/v1`;
    const baseUrl = baseURL.replace(/\/v1$/, '');

    const config: ScalixConfig = { apiKey, baseUrl, maxRetries: options?.maxRetries, timeout: options?.timeout };

    this.openai = new OpenAI({
      baseURL,
      apiKey,
      defaultHeaders: { 'User-Agent': 'Scalix-SDK/2.0' },
    });
    this.completions = this.openai.chat.completions;

    this.account = new AccountService(config);
    this.audio = new AudioService(config);
    this.docgen = new DocGenService(config);
    this.images = new ImagesService(config);
    this.models = new ModelsService(config);
    this.rag = new RAGService(config);
    this.research = new ResearchService(config);
    this.storage = new StorageService(config);
    this.text = new TextService(config);
  }
}

/** @deprecated Use `Scalix` instead */
export const ScalixClient = Scalix;
