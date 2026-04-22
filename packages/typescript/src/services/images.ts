import { BaseService } from './base.js';

export interface ImageGenerateOptions {
  model?: string;
  size?: string;
  n?: number;
  quality?: string;
}

export interface ImageResult {
  images?: Array<{ url?: string; b64_json?: string }>;
  jobId?: string;
}

export interface ImageJobStatus {
  jobId: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  result?: ImageResult;
}

export class ImagesService extends BaseService {
  async generate(prompt: string, options?: ImageGenerateOptions): Promise<ImageResult> {
    return this.request('POST', '/v1/images/generate', {
      body: { prompt, ...options },
    });
  }

  async generateAsync(prompt: string, options?: ImageGenerateOptions): Promise<{ jobId: string }> {
    return this.request('POST', '/v1/images/generate/queue', {
      body: { prompt, ...options },
    });
  }

  async getJob(jobId: string): Promise<ImageJobStatus> {
    return this.request('GET', `/v1/images/jobs/${encodeURIComponent(jobId)}`);
  }

  async getJobResult(jobId: string): Promise<ImageResult> {
    return this.request('GET', `/v1/images/jobs/${encodeURIComponent(jobId)}/result`);
  }

  async models(): Promise<{ models: Array<{ id: string; name: string }> }> {
    return this.request('GET', '/v1/images/models');
  }
}
