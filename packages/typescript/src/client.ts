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
 * // Summarize text
 * const summary = await scalix.text.summarize(longArticle);
 * ```
 */

import { configure, getConfig, type ScalixConfig } from './config.js';
import { AudioService } from './services/audio.js';
import { ImagesService } from './services/images.js';
import { ResearchService } from './services/research.js';
import { TextService } from './services/text.js';
import { RAGService } from './services/rag.js';
import { DocGenService } from './services/docgen.js';

export class ScalixClient {
  readonly audio: AudioService;
  readonly images: ImagesService;
  readonly research: ResearchService;
  readonly text: TextService;
  readonly rag: RAGService;
  readonly docgen: DocGenService;

  constructor(options?: { apiKey?: string } & Partial<ScalixConfig>) {
    if (options) {
      configure(options);
    }
    const config = getConfig();
    this.audio = new AudioService(config);
    this.images = new ImagesService(config);
    this.research = new ResearchService(config);
    this.text = new TextService(config);
    this.rag = new RAGService(config);
    this.docgen = new DocGenService(config);
  }
}
