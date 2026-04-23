import { BaseService } from './base.js';

export interface Database {
  id: string;
  name: string;
  type: string;
  status: string;
  region?: string;
  plan?: string;
  storageSize?: number;
  createdAt?: string;
}

export interface CreateDatabaseOptions {
  name: string;
  plan?: string;
  region?: string;
}

export interface Branch {
  id: string;
  name: string;
  parentId?: string;
  createdAt?: string;
}

export interface Backup {
  id: string;
  databaseId: string;
  type: string;
  status: string;
  size: number;
  createdAt: string;
}

export interface DatabaseMetrics {
  connections: number;
  queryRate: number;
  errorRate: number;
  storageUsed: number;
  storageTotal: number;
  cpuUsage?: number;
  memoryUsage?: number;
  responseTime?: number;
  timestamp: string;
}

export interface PoolingStatus {
  enabled: boolean;
  managed: boolean;
  provider: string;
  mode: string;
  totalConnections?: number;
  activeConnections?: number;
  idleConnections?: number;
}

export interface EncryptionStatus {
  encryptionAtRest: boolean;
  encryptionInTransit: boolean;
  tlsVersion: string;
  compliant: boolean;
  managed: boolean;
  provider: string;
}

export interface HAStatus {
  enabled: boolean;
  availabilityZones: string[];
  readReplicas: number;
  failoverEnabled: boolean;
  managed: boolean;
}

export interface QueryResult {
  rows: Record<string, unknown>[];
  rowCount: number;
  fields?: Array<{ name: string; dataType: string }>;
}

export interface TableInfo {
  name: string;
  schema: string;
  rowCount?: number;
}

export interface ColumnInfo {
  name: string;
  dataType: string;
  nullable: boolean;
  defaultValue?: string;
}

export class DatabaseService extends BaseService {
  // ─── Core CRUD ─────────────────────

  async list(): Promise<{ databases: Database[] }> {
    return this.request('GET', '/api/scalixdb/databases');
  }

  async create(options: CreateDatabaseOptions): Promise<{ database: Database }> {
    return this.request('POST', '/api/scalixdb/databases', {
      body: options,
    });
  }

  async get(databaseId: string): Promise<{ database: Database }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}`);
  }

  async update(databaseId: string, updates: Partial<Database>): Promise<{ database: Database }> {
    return this.request('PATCH', `/api/scalixdb/databases/${databaseId}`, {
      body: updates,
    });
  }

  async delete(databaseId: string): Promise<{ success: boolean }> {
    return this.request('DELETE', `/api/scalixdb/databases/${databaseId}`);
  }

  // ─── Branches ─────────────────────

  async listBranches(databaseId: string): Promise<{ branches: Branch[] }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/branches`);
  }

  async createBranch(
    databaseId: string,
    options: { name: string; parentId?: string },
  ): Promise<{ branch: Branch }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/branches`, {
      body: options,
    });
  }

  async deleteBranch(databaseId: string, branchId: string): Promise<{ success: boolean }> {
    return this.request('DELETE', `/api/scalixdb/databases/${databaseId}/branches/${branchId}`);
  }

  async maskBranch(databaseId: string, branchId: string): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/branches/${branchId}/mask`);
  }

  // ─── Backups ─────────────────────

  async listBackups(databaseId: string): Promise<{ backups: Backup[] }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/backups`);
  }

  async createBackup(databaseId: string, name?: string): Promise<{ backup: Backup }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/backups`, {
      body: { name },
    });
  }

  async restoreBackup(databaseId: string, backupId: string): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/backups/${backupId}/restore`);
  }

  async deleteBackup(databaseId: string, backupId: string): Promise<{ success: boolean }> {
    return this.request('DELETE', `/api/scalixdb/databases/${databaseId}/backups/${backupId}`);
  }

  async setBackupSchedule(
    databaseId: string,
    schedule: Record<string, unknown>,
  ): Promise<{ success: boolean }> {
    return this.request('PUT', `/api/scalixdb/databases/${databaseId}/backups/schedule`, {
      body: schedule,
    });
  }

  // ─── PITR (Point-in-Time Recovery) ─────────────────────

  async enablePitr(databaseId: string): Promise<{ success: boolean; message: string }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/pitr/enable`);
  }

  async getRestorePoints(
    databaseId: string,
  ): Promise<{ restorePoints: Array<{ timestamp: string; description: string }> }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/pitr/restore-points`);
  }

  async restorePitr(databaseId: string, targetTime: string): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/pitr/restore`, {
      body: { targetTime },
    });
  }

  // ─── Encryption ─────────────────────

  async getEncryption(databaseId: string): Promise<{ encryption: EncryptionStatus }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/encryption/verify`);
  }

  async updateEncryption(
    databaseId: string,
    settings: Record<string, unknown>,
  ): Promise<{ encryption: EncryptionStatus }> {
    return this.request('PUT', `/api/scalixdb/databases/${databaseId}/encryption`, {
      body: settings,
    });
  }

  async rotateEncryptionKeys(databaseId: string): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/encryption/rotate`);
  }

  // ─── High Availability ─────────────────────

  async getHAStatus(databaseId: string): Promise<{ status: HAStatus }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/ha/status`);
  }

  async enableHA(databaseId: string): Promise<{ status: HAStatus }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/ha/enable`);
  }

  async disableHA(databaseId: string): Promise<{ status: HAStatus }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/ha/disable`);
  }

  // ─── Connection Pooling ─────────────────────

  async getPoolingStatus(databaseId: string): Promise<{ pooling: PoolingStatus }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/pooling/status`);
  }

  async enablePooling(databaseId: string): Promise<{ pooling: PoolingStatus }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/pooling/enable`);
  }

  async disablePooling(databaseId: string): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/pooling/disable`);
  }

  async getPoolingStats(databaseId: string): Promise<{ stats: Record<string, number> }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/pooling/stats`);
  }

  async updatePoolingConfig(
    databaseId: string,
    config: Record<string, unknown>,
  ): Promise<{ success: boolean }> {
    return this.request('PUT', `/api/scalixdb/databases/${databaseId}/pooling/config`, {
      body: config,
    });
  }

  // ─── Query Execution ─────────────────────

  async query(databaseId: string, sql: string): Promise<QueryResult> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/query`, {
      body: { sql },
    });
  }

  async explain(databaseId: string, sql: string): Promise<{ plan: string }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/explain`, {
      body: { sql },
    });
  }

  // ─── Table Browsing ─────────────────────

  async listTables(databaseId: string, schema?: string): Promise<{ tables: TableInfo[] }> {
    const qs = schema ? `?schema=${encodeURIComponent(schema)}` : '';
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/tables${qs}`);
  }

  async listColumns(
    databaseId: string,
    tableName: string,
    schema?: string,
  ): Promise<{ columns: ColumnInfo[] }> {
    const qs = schema ? `?schema=${encodeURIComponent(schema)}` : '';
    return this.request(
      'GET',
      `/api/scalixdb/databases/${databaseId}/tables/${tableName}/columns${qs}`,
    );
  }

  async listRows(
    databaseId: string,
    tableName: string,
    options?: {
      schema?: string;
      limit?: number;
      offset?: number;
      orderBy?: string;
      orderDir?: 'asc' | 'desc';
    },
  ): Promise<{ rows: Record<string, unknown>[]; total: number }> {
    const params = new URLSearchParams();
    if (options?.schema) params.set('schema', options.schema);
    if (options?.limit !== undefined) params.set('limit', String(options.limit));
    if (options?.offset !== undefined) params.set('offset', String(options.offset));
    if (options?.orderBy) params.set('orderBy', options.orderBy);
    if (options?.orderDir) params.set('orderDir', options.orderDir);
    const qs = params.toString() ? `?${params.toString()}` : '';
    return this.request(
      'GET',
      `/api/scalixdb/databases/${databaseId}/tables/${tableName}/rows${qs}`,
    );
  }

  async insertRow(
    databaseId: string,
    tableName: string,
    data: Record<string, unknown>,
  ): Promise<{ success: boolean }> {
    return this.request(
      'POST',
      `/api/scalixdb/databases/${databaseId}/tables/${tableName}/rows`,
      { body: data },
    );
  }

  async updateRow(
    databaseId: string,
    tableName: string,
    data: Record<string, unknown>,
  ): Promise<{ success: boolean }> {
    return this.request(
      'PUT',
      `/api/scalixdb/databases/${databaseId}/tables/${tableName}/rows`,
      { body: data },
    );
  }

  async deleteRow(
    databaseId: string,
    tableName: string,
    conditions: Record<string, unknown>,
  ): Promise<{ success: boolean }> {
    return this.request(
      'DELETE',
      `/api/scalixdb/databases/${databaseId}/tables/${tableName}/rows`,
      { body: conditions },
    );
  }

  // ─── Extensions ─────────────────────

  async listExtensions(
    databaseId: string,
  ): Promise<{ extensions: Array<{ name: string; installed: boolean }> }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/extensions`);
  }

  async enableExtension(databaseId: string, name: string): Promise<{ success: boolean }> {
    return this.request(
      'POST',
      `/api/scalixdb/databases/${databaseId}/extensions/${name}/enable`,
    );
  }

  async disableExtension(databaseId: string, name: string): Promise<{ success: boolean }> {
    return this.request(
      'POST',
      `/api/scalixdb/databases/${databaseId}/extensions/${name}/disable`,
    );
  }

  // ─── Import ─────────────────────

  async importSql(databaseId: string, sql: string): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/import/sql`, {
      body: { sql },
    });
  }

  async importCsv(
    databaseId: string,
    data: { tableName: string; csv: string },
  ): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/import/csv`, {
      body: data,
    });
  }

  // ─── Credentials ─────────────────────

  async rotateCredentials(
    databaseId: string,
  ): Promise<{ connection: Record<string, string> }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/credentials/rotate`);
  }

  // ─── Monitoring ─────────────────────

  async getMetrics(databaseId: string): Promise<{ metrics: DatabaseMetrics }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/metrics`);
  }

  async getLogs(
    databaseId: string,
    options?: { limit?: number },
  ): Promise<{ logs: Array<Record<string, unknown>> }> {
    const qs = options?.limit ? `?limit=${options.limit}` : '';
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/logs${qs}`);
  }

  // ─── Connection ─────────────────────

  async getConnection(databaseId: string): Promise<{ connectionString: string }> {
    return this.request('GET', `/api/scalixdb/databases/${databaseId}/connection`);
  }

  async resetConnection(databaseId: string): Promise<{ success: boolean }> {
    return this.request('POST', `/api/scalixdb/databases/${databaseId}/connection/reset`);
  }
}
