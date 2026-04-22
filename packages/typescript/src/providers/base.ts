/**
 * Abstract provider interfaces and Database convenience class.
 */

import { isCloudMode } from '../config.js';
import type { Message, StreamEvent, SandboxResult } from '../types.js';

export interface LLMProvider {
  chat(
    messages: Message[],
    model: string,
    options?: {
      tools?: Record<string, unknown>[];
      temperature?: number;
      stream?: boolean;
    },
  ): Promise<Message>;

  streamChat(
    messages: Message[],
    model: string,
    options?: {
      tools?: Record<string, unknown>[];
      temperature?: number;
    },
  ): AsyncGenerator<StreamEvent>;
}

export interface SandboxProvider {
  execute(
    code: string,
    options?: {
      runtime?: string;
      timeout?: number;
      gpu?: string;
    },
  ): Promise<SandboxResult>;
}

export interface DatabaseProvider {
  query(sql: string, params?: unknown[]): Promise<Record<string, unknown>[]>;
  execute(sql: string, params?: unknown[]): Promise<number>;
}

/**
 * Convenience class for database access.
 *
 * @example
 * ```typescript
 * // Local SQLite
 * const db = new Database();
 *
 * // ScalixDB managed instance
 * const db = new Database('my-scalixdb');
 *
 * const results = await db.query('SELECT * FROM users');
 * ```
 */
export class Database {
  readonly name?: string;
  private provider: DatabaseProvider | null = null;

  constructor(name?: string) {
    this.name = name;
  }

  async query(sql: string, params?: unknown[]): Promise<Record<string, unknown>[]> {
    const provider = await this.getProvider();
    return provider.query(sql, params);
  }

  async execute(sql: string, params?: unknown[]): Promise<number> {
    const provider = await this.getProvider();
    return provider.execute(sql, params);
  }

  private async getProvider(): Promise<DatabaseProvider> {
    if (!this.provider) {
      if (this.name && isCloudMode()) {
        const { ScalixDatabaseProvider } = await import('../providers/cloud/database.js');
        this.provider = new ScalixDatabaseProvider(this.name);
      } else {
        const { SQLiteProvider } = await import('../providers/local/sqliteStore.js');
        this.provider = new SQLiteProvider(this.name);
      }
    }
    return this.provider;
  }
}
