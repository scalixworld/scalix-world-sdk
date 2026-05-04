/**
 * Scalix SDK — unified client for the Scalix platform.
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
 *
 * @packageDocumentation
 */

export { Scalix, ScalixClient } from './client.js';
export type { ScalixOptions } from './client.js';
export type { ScalixConfig } from './config.js';
export {
  ScalixError,
  AuthenticationError,
  BadRequestError,
  PermissionDeniedError,
  NotFoundError,
  ConflictError,
  UnprocessableEntityError,
  RateLimitError,
  InternalServerError,
} from './errors.js';
export {
  AccountService,
  AudioService,
  DocGenService,
  ImagesService,
  ModelsService,
  RAGService,
  ResearchService,
  StorageService,
  TextService,
} from './services/index.js';
export type {
  UserInfo,
  UserBudget,
  UserUsage,
  ScalixModel,
  DocFormat,
  DocStyle,
  DocGenOptions,
  DocGenResult,
  DocTemplate,
  DocFormatInfo,
  ImageGenerateOptions,
  ImageResult,
  ImageJobStatus,
  RAGDocument,
  RAGQueryResult,
  RAGUploadResult,
  SentimentResult,
  SummaryResult,
  TranslationResult,
  GrammarResult,
  AutocompleteResult,
  VectorSearchResult,
  UploadUrlResult,
  TranscriptionResult,
  SpeechOptions,
  SearchResult,
  ResearchResult,
} from './services/index.js';
