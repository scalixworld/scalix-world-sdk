import { BaseService } from './base.js';

export interface UploadUrlResult {
  uploadUrl: string;
  fileUrl: string;
}

export class StorageService extends BaseService {
  async getUploadUrl(mimeType: string, size?: number): Promise<UploadUrlResult> {
    return this.request<UploadUrlResult>('POST', '/v1/storage/upload-url', {
      body: { mimeType, size },
    });
  }
}
