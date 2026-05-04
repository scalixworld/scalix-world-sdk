import { BaseService } from './base.js';

export type DocFormat = 'xlsx' | 'docx' | 'pdf' | 'html' | 'csv';
export type DocStyle = 'professional' | 'casual' | 'creative';

export interface DocGenOptions {
  prompt: string;
  format: DocFormat;
  template_id?: string;
  style?: DocStyle;
  language?: string;
}

export interface DocGenResult {
  status: string;
  doc_id: string;
  format: string;
  download_url: string;
  created_at: string;
  size_bytes?: number;
}

export interface DocTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  format: string;
  tags: string[];
}

export interface DocFormatInfo {
  format: string;
  mime_type: string;
  description: string;
  max_size_bytes: number;
  supported_styles: string[];
}

export class DocGenService extends BaseService {
  async create(options: DocGenOptions): Promise<DocGenResult> {
    return this.request<DocGenResult>('POST', '/v1/docgen/create', {
      body: options,
    });
  }

  async preview(
    options: Pick<DocGenOptions, 'prompt' | 'format' | 'style'>,
  ): Promise<{ html_content: string }> {
    return this.request('POST', '/v1/docgen/preview', { body: options });
  }

  async formats(): Promise<DocFormatInfo[]> {
    return this.request('GET', '/v1/docgen/formats');
  }

  async templates(): Promise<DocTemplate[]> {
    return this.request('GET', '/v1/docgen/templates');
  }

  async history(
    options?: { limit?: number; offset?: number },
  ): Promise<{ documents: DocGenResult[]; total: number }> {
    const params = new URLSearchParams();
    if (options?.limit != null) params.set('limit', String(options.limit));
    if (options?.offset != null) params.set('offset', String(options.offset));
    const qs = params.toString();
    return this.request('GET', `/v1/docgen/history${qs ? `?${qs}` : ''}`);
  }

  async download(docId: string): Promise<Response> {
    return this.requestRaw('GET', `/v1/docgen/download/${docId}`);
  }

  async share(
    docId: string,
    targetEmail: string,
  ): Promise<{ success: boolean; message: string; shared_with_uid: string }> {
    return this.request('POST', '/v1/docgen/share', {
      body: { doc_id: docId, target_email: targetEmail },
    });
  }

  async revise(docId: string, prompt: string): Promise<DocGenResult> {
    return this.request<DocGenResult>('POST', '/v1/docgen/revise', {
      body: { doc_id: docId, prompt },
    });
  }

  async versions(
    docId: string,
  ): Promise<{ versions: Array<{ version_id: string; created_at: string }> }> {
    return this.request('GET', `/v1/docgen/versions/${docId}`);
  }
}
