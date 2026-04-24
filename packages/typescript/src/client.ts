/**
 * ScalixClient — unified access to all Scalix API services.
 *
 * @example
 * ```typescript
 * import { ScalixClient } from '@scalix-world/sdk';
 *
 * const scalix = new ScalixClient({ apiKey: 'sk_scalix_...' });
 *
 * // Search the web
 * const results = await scalix.research.search('quantum computing');
 *
 * // Transcribe audio
 * const transcript = await scalix.audio.transcribe(audioFile);
 *
 * // Chat completion
 * const reply = await scalix.chat.complete({
 *   model: 'scalix-world-ai',
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
 *
 * // Account — manage API keys and usage
 * const keys = await scalix.account.listApiKeys();
 * const usage = await scalix.account.usage();
 * ```
 */

import { configure, getConfig, type ScalixConfig } from './config.js';
import { AccountService } from './services/account.js';
import { AudioService } from './services/audio.js';
import { ChatService } from './services/chat.js';
import { DocGenService } from './services/docgen.js';
import { RAGService } from './services/rag.js';
import { ResearchService } from './services/research.js';
import { TextService } from './services/text.js';
import { DatabaseService } from './services/database.js';
import { StorageService } from './services/storage.js';

export class ScalixClient {
  readonly account: AccountService;
  readonly audio: AudioService;
  readonly chat: ChatService;
  readonly database: DatabaseService;
  readonly docgen: DocGenService;
  readonly rag: RAGService;
  readonly research: ResearchService;
  readonly storage: StorageService;
  readonly text: TextService;

  constructor(options?: { apiKey?: string } & Partial<ScalixConfig>) {
    if (options) {
      configure(options);
    }
    const config = getConfig();
    this.account = new AccountService(config);
    this.audio = new AudioService(config);
    this.chat = new ChatService(config);
    this.database = new DatabaseService(config);
    this.docgen = new DocGenService(config);
    this.rag = new RAGService(config);
    this.research = new ResearchService(config);
    this.storage = new StorageService(config);
    this.text = new TextService(config);
  }
}
