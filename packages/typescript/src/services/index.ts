export { BaseService } from './base.js';
export { AudioService } from './audio.js';
export type { TranscriptionResult, SpeechOptions } from './audio.js';
export { ChatService } from './chat.js';
export type { ChatMessage, ChatCompletionOptions, ChatCompletionResult } from './chat.js';
export { DocGenService } from './docgen.js';
export type { DocFormat, DocStyle, DocGenOptions, DocGenResult, DocTemplate, DocFormatInfo } from './docgen.js';
export { ImagesService } from './images.js';
export type { ImageResult, ImageGenerateOptions, ImageJobStatus } from './images.js';
export { RAGService } from './rag.js';
export type { RAGDocument, RAGQueryResult, RAGUploadResult } from './rag.js';
export { ResearchService } from './research.js';
export type { SearchResult, ResearchResult } from './research.js';
export { TextService } from './text.js';
export type { SentimentResult, SummaryResult, TranslationResult } from './text.js';
export { DatabaseService } from './database.js';
export type {
  Database as ScalixDatabase, CreateDatabaseOptions, Branch, Backup, DatabaseMetrics,
  PoolingStatus, EncryptionStatus, HAStatus, QueryResult, TableInfo, ColumnInfo,
} from './database.js';
export { StorageService } from './storage.js';
export type { UploadUrlResult } from './storage.js';
