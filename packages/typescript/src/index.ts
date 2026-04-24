/**
 * Scalix SDK — TypeScript client for the Scalix API.
 *
 * @example
 * ```typescript
 * import { ScalixClient } from '@scalix-world/sdk';
 *
 * const scalix = new ScalixClient({ apiKey: 'sk_scalix_...' });
 * const reply = await scalix.chat.complete({
 *   model: 'scalix-world-ai',
 *   messages: [{ role: 'user', content: 'Hello!' }],
 * });
 * ```
 *
 * @packageDocumentation
 */

export { ScalixClient } from './client.js';
export { configure, getConfig } from './config.js';
export type { ScalixConfig } from './config.js';
export {
  ScalixError,
  AuthenticationError,
} from './errors.js';
export {
  AccountService,
  AudioService,
  ChatService,
  DatabaseService,
  DocGenService,
  ImagesService,
  RAGService,
  ResearchService,
  StorageService,
  TextService,
} from './services/index.js';
export type {
  ChatMessage,
  ChatCompletionOptions,
  ChatCompletionResult,
  ScalixDatabase,
  CreateDatabaseOptions,
  Branch,
  Backup,
  DatabaseMetrics,
  PoolingStatus,
  EncryptionStatus,
  HAStatus,
  QueryResult,
  TableInfo,
  ColumnInfo,
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
  UploadUrlResult,
  TranscriptionResult,
  SpeechOptions,
  SearchResult,
  ResearchResult,
} from './services/index.js';
