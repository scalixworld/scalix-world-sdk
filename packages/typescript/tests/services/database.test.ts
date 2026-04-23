import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { DatabaseService } from '../../src/services/database.js';

vi.mock('../../src/config.js', () => ({
  getConfig: () => ({ apiKey: 'test-key', baseUrl: 'https://api.scalix.world' }),
}));

function mockFetchJson(data: unknown, ok = true, status = 200) {
  global.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    json: () => Promise.resolve(data),
  });
}

const DB_ID = 'db-abc-123';
const BASE = 'https://api.scalix.world';

describe('DatabaseService', () => {
  let service: DatabaseService;

  beforeEach(() => {
    service = new DatabaseService();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ── Core CRUD ───────────────────────────────────────────────

  describe('CRUD operations', () => {
    it('list() calls GET /api/scalixdb/databases', async () => {
      const mockDbs = {
        databases: [
          { id: DB_ID, name: 'mydb', type: 'postgresql', status: 'active' },
        ],
      };
      mockFetchJson(mockDbs);

      const result = await service.list();

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.databases).toHaveLength(1);
      expect(result.databases[0].name).toBe('mydb');
    });

    it('create() sends POST /api/scalixdb/databases with options', async () => {
      const mockDb = {
        database: { id: DB_ID, name: 'newdb', type: 'postgresql', status: 'provisioning' },
      };
      mockFetchJson(mockDb);

      const result = await service.create({
        name: 'newdb',
        plan: 'pro',
        region: 'us-east-1',
      });

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases`,
        expect.objectContaining({ method: 'POST' }),
      );

      const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
      expect(body.name).toBe('newdb');
      expect(body.plan).toBe('pro');
      expect(body.region).toBe('us-east-1');

      expect(result.database.id).toBe(DB_ID);
      expect(result.database.status).toBe('provisioning');
    });

    it('get() calls GET /api/scalixdb/databases/:id', async () => {
      mockFetchJson({
        database: { id: DB_ID, name: 'mydb', type: 'postgresql', status: 'active' },
      });

      const result = await service.get(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.database.id).toBe(DB_ID);
    });

    it('update() sends PATCH /api/scalixdb/databases/:id', async () => {
      mockFetchJson({
        database: { id: DB_ID, name: 'renamed', type: 'postgresql', status: 'active' },
      });

      const result = await service.update(DB_ID, { name: 'renamed' });

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}`,
        expect.objectContaining({ method: 'PATCH' }),
      );

      const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
      expect(body.name).toBe('renamed');
      expect(result.database.name).toBe('renamed');
    });

    it('delete() calls DELETE /api/scalixdb/databases/:id', async () => {
      mockFetchJson({ success: true });

      const result = await service.delete(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}`,
        expect.objectContaining({ method: 'DELETE' }),
      );
      expect(result.success).toBe(true);
    });
  });

  // ── Query Execution ─────────────────────────────────────────

  describe('query()', () => {
    it('sends POST /api/scalixdb/databases/:id/query with SQL', async () => {
      const mockResult = {
        rows: [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }],
        rowCount: 2,
        fields: [
          { name: 'id', dataType: 'integer' },
          { name: 'name', dataType: 'text' },
        ],
      };
      mockFetchJson(mockResult);

      const result = await service.query(DB_ID, 'SELECT * FROM users');

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/query`,
        expect.objectContaining({ method: 'POST' }),
      );

      const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
      expect(body.sql).toBe('SELECT * FROM users');

      expect(result.rows).toHaveLength(2);
      expect(result.rowCount).toBe(2);
      expect(result.fields).toHaveLength(2);
    });
  });

  // ── Table Browsing ──────────────────────────────────────────

  describe('listTables()', () => {
    it('calls GET without schema param', async () => {
      mockFetchJson({
        tables: [{ name: 'users', schema: 'public', rowCount: 100 }],
      });

      const result = await service.listTables(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/tables`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.tables).toHaveLength(1);
      expect(result.tables[0].name).toBe('users');
    });

    it('calls GET with schema query param', async () => {
      mockFetchJson({ tables: [] });

      await service.listTables(DB_ID, 'custom_schema');

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/tables?schema=custom_schema`,
        expect.objectContaining({ method: 'GET' }),
      );
    });

    it('encodes special characters in schema param', async () => {
      mockFetchJson({ tables: [] });

      await service.listTables(DB_ID, 'my schema');

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/tables?schema=my%20schema`,
        expect.objectContaining({ method: 'GET' }),
      );
    });
  });

  // ── Backups ─────────────────────────────────────────────────

  describe('backups', () => {
    it('listBackups() calls GET /api/scalixdb/databases/:id/backups', async () => {
      mockFetchJson({
        backups: [
          { id: 'bk-1', databaseId: DB_ID, type: 'manual', status: 'completed', size: 1024, createdAt: '2026-01-01' },
        ],
      });

      const result = await service.listBackups(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/backups`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.backups).toHaveLength(1);
      expect(result.backups[0].status).toBe('completed');
    });

    it('createBackup() sends POST with optional name', async () => {
      mockFetchJson({
        backup: { id: 'bk-2', databaseId: DB_ID, type: 'manual', status: 'pending', size: 0, createdAt: '2026-04-20' },
      });

      const result = await service.createBackup(DB_ID, 'pre-deploy');

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/backups`,
        expect.objectContaining({ method: 'POST' }),
      );

      const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
      expect(body.name).toBe('pre-deploy');
      expect(result.backup.id).toBe('bk-2');
    });

    it('createBackup() works without name', async () => {
      mockFetchJson({
        backup: { id: 'bk-3', databaseId: DB_ID, type: 'auto', status: 'pending', size: 0, createdAt: '2026-04-20' },
      });

      await service.createBackup(DB_ID);

      const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
      expect(body.name).toBeUndefined();
    });
  });

  // ── Metrics ─────────────────────────────────────────────────

  describe('getMetrics()', () => {
    it('calls GET /api/scalixdb/databases/:id/metrics', async () => {
      const mockMetrics = {
        metrics: {
          connections: 15,
          queryRate: 120,
          errorRate: 0.5,
          storageUsed: 1073741824,
          storageTotal: 10737418240,
          cpuUsage: 35.2,
          memoryUsage: 62.1,
          responseTime: 12.5,
          timestamp: '2026-04-20T12:00:00Z',
        },
      };
      mockFetchJson(mockMetrics);

      const result = await service.getMetrics(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/metrics`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.metrics.connections).toBe(15);
      expect(result.metrics.cpuUsage).toBe(35.2);
      expect(result.metrics.timestamp).toBe('2026-04-20T12:00:00Z');
    });
  });

  // ── Connection ──────────────────────────────────────────────

  describe('getConnection()', () => {
    it('calls GET /api/scalixdb/databases/:id/connection', async () => {
      mockFetchJson({
        connectionString: 'postgresql://user:pass@host:5432/mydb?sslmode=require',
      });

      const result = await service.getConnection(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/connection`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.connectionString).toContain('postgresql://');
    });
  });

  // ── High Availability ──────────────────────────────────────

  describe('enableHA()', () => {
    it('calls POST /api/scalixdb/databases/:id/ha/enable', async () => {
      const mockHA = {
        status: {
          enabled: true,
          availabilityZones: ['us-east-1a', 'us-east-1b'],
          readReplicas: 2,
          failoverEnabled: true,
          managed: true,
        },
      };
      mockFetchJson(mockHA);

      const result = await service.enableHA(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/ha/enable`,
        expect.objectContaining({ method: 'POST' }),
      );
      expect(result.status.enabled).toBe(true);
      expect(result.status.readReplicas).toBe(2);
    });
  });

  // ── Connection Pooling ──────────────────────────────────────

  describe('getPoolingStatus()', () => {
    it('calls GET /api/scalixdb/databases/:id/pooling/status', async () => {
      const mockPooling = {
        pooling: {
          enabled: true,
          managed: true,
          provider: 'pgbouncer',
          mode: 'transaction',
          totalConnections: 100,
          activeConnections: 25,
          idleConnections: 75,
        },
      };
      mockFetchJson(mockPooling);

      const result = await service.getPoolingStatus(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/pooling/status`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.pooling.enabled).toBe(true);
      expect(result.pooling.provider).toBe('pgbouncer');
      expect(result.pooling.activeConnections).toBe(25);
    });
  });

  // ── Branches ────────────────────────────────────────────────

  describe('branches', () => {
    it('listBranches() calls GET', async () => {
      mockFetchJson({ branches: [{ id: 'br-1', name: 'dev', createdAt: '2026-01-01' }] });

      const result = await service.listBranches(DB_ID);

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/branches`,
        expect.objectContaining({ method: 'GET' }),
      );
      expect(result.branches).toHaveLength(1);
    });

    it('createBranch() sends POST with name and parentId', async () => {
      mockFetchJson({ branch: { id: 'br-2', name: 'feature', parentId: 'br-1' } });

      await service.createBranch(DB_ID, { name: 'feature', parentId: 'br-1' });

      const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
      expect(body.name).toBe('feature');
      expect(body.parentId).toBe('br-1');
    });

    it('deleteBranch() calls DELETE with branch id', async () => {
      mockFetchJson({ success: true });

      await service.deleteBranch(DB_ID, 'br-2');

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/branches/br-2`,
        expect.objectContaining({ method: 'DELETE' }),
      );
    });
  });

  // ── Explain ─────────────────────────────────────────────────

  describe('explain()', () => {
    it('sends POST /api/scalixdb/databases/:id/explain with SQL', async () => {
      mockFetchJson({ plan: 'Seq Scan on users  (cost=0.00..10.00 rows=100 width=50)' });

      const result = await service.explain(DB_ID, 'SELECT * FROM users');

      expect(global.fetch).toHaveBeenCalledWith(
        `${BASE}/api/scalixdb/databases/${DB_ID}/explain`,
        expect.objectContaining({ method: 'POST' }),
      );

      const body = JSON.parse(vi.mocked(global.fetch).mock.calls[0][1]!.body as string);
      expect(body.sql).toBe('SELECT * FROM users');
      expect(result.plan).toContain('Seq Scan');
    });
  });

  // ── Error handling ──────────────────────────────────────────

  describe('error handling', () => {
    it('throws on authentication failure', async () => {
      mockFetchJson(
        { error: { message: 'Unauthorized', code: 'auth_error' } },
        false,
        401,
      );

      await expect(service.list()).rejects.toThrow('Unauthorized');
    });

    it('throws on not found', async () => {
      mockFetchJson(
        { error: { message: 'Database not found', code: 'not_found' } },
        false,
        404,
      );

      await expect(service.get('nonexistent')).rejects.toThrow('Database not found');
    });

    it('throws on query error', async () => {
      mockFetchJson(
        { error: { message: 'Syntax error in SQL', code: 'query_error' } },
        false,
        400,
      );

      await expect(service.query(DB_ID, 'SELCT * FORM')).rejects.toThrow('Syntax error in SQL');
    });

    it('throws AuthenticationError when API key is missing', async () => {
      vi.resetModules();
      const { DatabaseService: FreshDatabaseService } = await import('../../src/services/database.js');
      const noKeyService = new FreshDatabaseService({
        baseUrl: 'https://api.scalix.world',
        environment: 'development',
        logLevel: 'info',
        defaultModel: 'auto',
        sandboxMode: 'auto',
        databaseMode: 'auto',
      });

      await expect(noKeyService.list()).rejects.toThrow('API key required');
    });
  });
});
