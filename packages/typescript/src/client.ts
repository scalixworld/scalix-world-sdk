/**
 * ScalixClient — unified access to all Scalix API services.
 *
 * @example
 * ```typescript
 * import { ScalixClient } from '@scalix-world/sdk';
 *
 * const scalix = new ScalixClient({ apiKey: 'sk-scalix-...' });
 *
 * // Search the web
 * const results = await scalix.research.search('quantum computing');
 *
 * // Generate an image
 * const image = await scalix.images.generate('A sunset over mountains');
 *
 * // Transcribe audio
 * const transcript = await scalix.audio.transcribe(audioFile);
 *
 * // Chat completion
 * const reply = await scalix.chat.complete({
 *   model: 'gpt-4o',
 *   messages: [{ role: 'user', content: 'Hello!' }],
 * });
 *
 * // RAG — upload and query documents
 * const doc = await scalix.rag.upload(pdfBlob, { filename: 'report.pdf' });
 * const hits = await scalix.rag.query('revenue growth');
 *
 * // Generate a document
 * const report = await scalix.docgen.create({ prompt: 'Q1 report', format: 'pdf' });
 *
 * // Text utilities
 * const sentiment = await scalix.text.sentiment('I love this product!');
 * const summary = await scalix.text.summarize(longArticle);
 * const translated = await scalix.text.translate('Hello', 'es');
 *
 * // ScalixDB — manage databases
 * const dbs = await scalix.database.list();
 * const db = await scalix.database.create({ name: 'my-app-db' });
 * const result = await scalix.database.query(db.database.id, 'SELECT * FROM users');
 *
 * // Storage — upload files
 * const { uploadUrl } = await scalix.storage.getUploadUrl('application/pdf');
 * ```
 */

import { configure, getConfig, type ScalixConfig } from './config.js';
import { AudioService } from './services/audio.js';
import { ChatService } from './services/chat.js';
import { DocGenService } from './services/docgen.js';
import { ImagesService } from './services/images.js';
import { RAGService } from './services/rag.js';
import { ResearchService } from './services/research.js';
import { TextService } from './services/text.js';
import { DatabaseService } from './services/database.js';
import { StorageService } from './services/storage.js';

export class ScalixClient {
  readonly audio: AudioService;
  readonly chat: ChatService;
  readonly database: DatabaseService;
  readonly docgen: DocGenService;
  readonly images: ImagesService;
  readonly rag: RAGService;
  readonly research: ResearchService;
  readonly storage: StorageService;
  readonly text: TextService;

  constructor(options?: { apiKey?: string } & Partial<ScalixConfig>) {
    if (options) {
      configure(options);
    }
    const config = getConfig();
    this.audio = new AudioService(config);
    this.chat = new ChatService(config);
    this.database = new DatabaseService(config);
    this.docgen = new DocGenService(config);
    this.images = new ImagesService(config);
    this.rag = new RAGService(config);
    this.research = new ResearchService(config);
    this.storage = new StorageService(config);
    this.text = new TextService(config);
  }
}
