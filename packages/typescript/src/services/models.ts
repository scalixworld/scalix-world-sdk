import { BaseService } from './base.js';

export interface ScalixModel {
  id: string;
  object: string;
  created: number;
  owned_by: string;
  context_window: number;
  max_output_tokens: number;
  description: string;
  plan_required: string;
}

export class ModelsService extends BaseService {
  async list(): Promise<ScalixModel[]> {
    const resp = await this.request<{ data: ScalixModel[] }>('GET', '/v1/models');
    return resp.data;
  }

  async get(modelId: string): Promise<ScalixModel | undefined> {
    const models = await this.list();
    return models.find(m => m.id === modelId);
  }
}
