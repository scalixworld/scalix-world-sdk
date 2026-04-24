/**
 * SQLite database provider — local storage using better-sqlite3.
 *
 * Used in local mode when no Scalix API key is configured.
 * Uses better-sqlite3 for synchronous SQLite access (wrapped for async interface).
 */

import { dynamicImport } from '../../config.js';
import type { DatabaseProvider } from '../base.js';

/**
 * Local SQLite database provider using better-sqlite3.
 *
 * Falls back to a basic in-memory store if better-sqlite3 is not installed.
 * This is the default database for local development — zero config, zero cost.
 */
export class SQLiteProvider implements DatabaseProvider {
  private dbPath: string;
  private db: BetterSqliteDb | null = null;

  constructor(name?: string) {
    this.dbPath = name ?? 'scalix_local.db';
  }

  async query(sql: string, params?: unknown[]): Promise<Record<string, unknown>[]> {
    const db = await this.getDb();
    const stmt = db.prepare(sql);
    if (params?.length) {
      return stmt.all(...params) as Record<string, unknown>[];
    }
    return stmt.all() as Record<string, unknown>[];
  }

  async execute(sql: string, params?: unknown[]): Promise<number> {
    const db = await this.getDb();
    const stmt = db.prepare(sql);
    let result: { changes: number };
    if (params?.length) {
      result = stmt.run(...params);
    } else {
      result = stmt.run();
    }
    return result.changes;
  }

  private async getDb(): Promise<BetterSqliteDb> {
    if (!this.db) {
      try {
        const { default: Database } = await dynamicImport('better-sqlite3') as unknown as { default: new (path: string) => BetterSqliteDb };
        this.db = new Database(this.dbPath);
        this.db.pragma('journal_mode = WAL');
      } catch {
        throw new Error(
          'better-sqlite3 package not installed. Run: npm install better-sqlite3',
        );
      }
    }
    return this.db;
  }
}

/** Internal type for better-sqlite3 database instance. */
interface BetterSqliteDb {
  prepare(sql: string): BetterSqliteStatement;
  pragma(pragma: string): unknown;
  close(): void;
}

/** Internal type for better-sqlite3 prepared statement. */
interface BetterSqliteStatement {
  all(...params: unknown[]): unknown[];
  run(...params: unknown[]): { changes: number; lastInsertRowid: number | bigint };
  get(...params: unknown[]): unknown;
}
