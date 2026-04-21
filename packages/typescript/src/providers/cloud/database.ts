/**
 * ScalixDB provider — managed Postgres via Scalix Cloud API.
 *
 * Provides managed PostgreSQL with branching, HA, PITR, and auto-scaling.
 * Uses native fetch to call the ScalixDB API endpoints.
 */

import { getConfig, isCloudMode, type ScalixConfig } from '../../config.js';
import { AuthenticationError } from '../../errors.js';
import type { DatabaseProvider } from '../base.js';

/** Database error for ScalixDB operations. */
class DatabaseError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'DatabaseError';
  }
}

/**
 * Query ScalixDB managed Postgres instances.
 *
 * Calls the ScalixDB Cloud API at /api/scalixdb/databases/:id/query.
 * Requires a Scalix API key (cloud mode).
 *
 * Advantages over SQLiteProvider:
 * - Managed PostgreSQL (not SQLite)
 * - Branching (create dev copies of production data)
 * - High availability with automatic failover
 * - Point-in-time recovery
 * - Auto-scaling
 * - Backups and monitoring
 */
export class ScalixDatabaseProvider implements DatabaseProvider {
  private config: ScalixConfig;
  private databaseName: string;
  private databaseId: string | null = null;

  constructor(databaseName: string, config?: ScalixConfig) {
    this.databaseName = databaseName;
    this.config = config ?? getConfig();
    if (!isCloudMode()) {
      throw new AuthenticationError(
        "ScalixDB requires an API key. Call configure({ apiKey: 'sk-scalix-...' }) first.",
      );
    }
  }

  async query(sql: string, params?: unknown[]): Promise<Record<string, unknown>[]> {
    const dbId = await this.resolveDatabaseId();

    const body: Record<string, unknown> = { query: sql };
    if (params?.length) {
      body.params = params;
    }

    const resp = await this.request(`/api/scalixdb/databases/${dbId}/query`, body);

    if (!resp.ok) {
      await this.handleErrorResponse(resp, 'Query');
    }

    const data = (await resp.json()) as Record<string, unknown>;
    return this.normalizeRows(data);
  }

  async execute(sql: string, params?: unknown[]): Promise<number> {
    const dbId = await this.resolveDatabaseId();

    const body: Record<string, unknown> = { query: sql };
    if (params?.length) {
      body.params = params;
    }

    const resp = await this.request(`/api/scalixdb/databases/${dbId}/query`, body);

    if (!resp.ok) {
      await this.handleErrorResponse(resp, 'Execute');
    }

    const data = (await resp.json()) as Record<string, unknown>;
    return (data.rows_affected ?? data.rowCount ?? 0) as number;
  }

  private async resolveDatabaseId(): Promise<string> {
    if (this.databaseId) return this.databaseId;

    const url = `${this.config.baseUrl}/api/scalixdb/databases`;
    const resp = await fetch(url, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
    });

    if (resp.status === 401) {
      throw new AuthenticationError('Invalid API key for ScalixDB');
    }
    if (!resp.ok) {
      const text = await resp.text();
      throw new DatabaseError(`Failed to list databases: ${resp.status} ${text}`);
    }

    const data = (await resp.json()) as Record<string, unknown>;
    const databases = (data.databases ?? data.data ?? []) as Record<string, unknown>[];

    for (const db of databases) {
      const name = (db.name ?? db.database_name ?? '') as string;
      if (name === this.databaseName) {
        this.databaseId = (db.id ?? db.database_id ?? '') as string;
        return this.databaseId;
      }
    }

    throw new DatabaseError(
      `Database '${this.databaseName}' not found. ` +
        'Create it in the Scalix dashboard or via the API.',
    );
  }

  private async request(path: string, body: Record<string, unknown>): Promise<Response> {
    const url = `${this.config.baseUrl}${path}`;
    return fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
  }

  private async handleErrorResponse(resp: Response, operation: string): Promise<never> {
    if (resp.status === 401) {
      throw new AuthenticationError('Invalid API key for ScalixDB');
    }
    if (resp.status === 403) {
      throw new DatabaseError(`Access denied to database '${this.databaseName}'`);
    }
    if (resp.status === 404) {
      throw new DatabaseError(`Database '${this.databaseName}' not found`);
    }

    let errorMsg = await resp.text();
    try {
      const errorData = JSON.parse(errorMsg) as Record<string, unknown>;
      const error = errorData.error as Record<string, unknown> | undefined;
      if (error?.message) {
        errorMsg = error.message as string;
      }
    } catch {
      // Use raw text
    }
    throw new DatabaseError(`${operation} failed: ${errorMsg}`);
  }

  /**
   * Normalize API response rows to array of dicts.
   *
   * The API returns rows in various formats:
   * - Array rows with separate columns → zip into dicts
   * - Already dict rows → return as-is
   */
  private normalizeRows(data: Record<string, unknown>): Record<string, unknown>[] {
    const rows = (data.rows ?? data.results ?? data.data ?? []) as unknown[];
    const columns = (data.columns ?? data.fields ?? []) as unknown[];

    if (!rows.length) return [];

    if (columns.length && Array.isArray(rows[0])) {
      // Rows are arrays, columns are separate — zip them
      const colNames = columns.map((c) =>
        typeof c === 'object' && c !== null ? ((c as Record<string, string>).name ?? String(c)) : String(c),
      );
      return (rows as unknown[][]).map((row) => {
        const obj: Record<string, unknown> = {};
        for (let i = 0; i < colNames.length; i++) {
          obj[colNames[i]] = row[i];
        }
        return obj;
      });
    }

    if (typeof rows[0] === 'object' && rows[0] !== null && !Array.isArray(rows[0])) {
      // Already dict format
      return rows as Record<string, unknown>[];
    }

    return rows as Record<string, unknown>[];
  }
}
