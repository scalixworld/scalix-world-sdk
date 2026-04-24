/**
 * ScalixClient — unified access to all Scalix API services.
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
 */

import { configure, getConfig, type ScalixConfig } from './config.js';
import { AccountService } from './services/account.js';
import { AudioService } from './services/audio.js';
import { ChatService } from './services/chat.js';
import { DatabaseService } from './services/database.js';
import { DocGenService } from './services/docgen.js';
import { ImagesService } from './services/images.js';
import { RAGService } from './services/rag.js';
import { ResearchService } from './services/research.js';
import { StorageService } from './services/storage.js';
import { TextService } from './services/text.js';

export class ScalixClient {
  readonly account: AccountService;
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
    this.account = new AccountService(config);
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
