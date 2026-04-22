import { BaseService } from './base.js';

export interface TranscriptionResult {
  text: string;
  language?: string;
  duration?: number;
}

export interface SpeechOptions {
  voice?: string;
  format?: string;
  speed?: number;
}

export class AudioService extends BaseService {
  async transcribe(file: Blob, options?: { language?: string }): Promise<TranscriptionResult> {
    const formData = new FormData();
    formData.append('file', file);
    if (options?.language) formData.append('language', options.language);
    return this.requestMultipart<TranscriptionResult>('/v1/audio/transcribe', formData);
  }

  async speak(text: string, options?: SpeechOptions): Promise<Response> {
    return this.requestRaw('POST', '/v1/audio/speak/kokoro', {
      body: { text, ...options },
    });
  }

  async voices(): Promise<{ voices: Array<{ id: string; name: string }> }> {
    return this.request('GET', '/v1/audio/kokoro/voices');
  }

  async languages(): Promise<{ languages: string[] }> {
    return this.request('GET', '/v1/audio/kokoro/languages');
  }
}
