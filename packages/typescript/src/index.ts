/**
 * Scalix World SDK — Build, run, and deploy AI agents.
 *
 * @example
 * ```typescript
 * import { Agent, Tool } from 'scalix';
 *
 * const agent = new Agent({
 *   model: 'claude-sonnet-4',
 *   tools: [Tool.codeExec(), Tool.webSearch()],
 * });
 *
 * const result = await agent.run('Analyze trending GitHub repos');
 * console.log(result.output);
 * ```
 *
 * Connect to Scalix infrastructure:
 * ```typescript
 * import { configure } from 'scalix';
 * configure({ apiKey: 'sk-scalix-...' });
 * ```
 *
 * @packageDocumentation
 */

export { ScalixClient } from './client.js';
export { Agent } from './agent/agent.js';
export { Team, Pipeline } from './agent/orchestrator.js';
export { Tool } from './tools/base.js';
export { Database } from './providers/base.js';
export { configure, getConfig } from './config.js';
export type { ScalixConfig } from './config.js';
export type {
  AgentResult,
  AgentOptions,
  Message,
  ToolCall,
  ToolCallResult,
  StreamEvent,
  Usage,
  TeamResult,
  ToolDefinition,
  SandboxResult,
  ModelInfo,
} from './types.js';
export {
  ScalixError,
  ConfigurationError,
  AuthenticationError,
  ProviderError,
  SandboxError,
  RouterError,
  ToolError,
  DeploymentError,
} from './errors.js';
export { MCPServer } from './protocols/mcpServer.js';
export { A2AServer } from './protocols/a2aServer.js';
export {
  AudioService,
  ChatService,
  DatabaseService,
  DocGenService,
  ImagesService,
  RAGService,
  ResearchService,
  StorageService,
  TextService,
} from './services/index.js';
export type {
  ChatMessage,
  ChatCompletionOptions,
  ChatCompletionResult,
  ScalixDatabase,
  CreateDatabaseOptions,
  Branch,
  Backup,
  DatabaseMetrics,
  PoolingStatus,
  EncryptionStatus,
  HAStatus,
  QueryResult,
  TableInfo,
  ColumnInfo,
  DocFormat,
  DocStyle,
  DocGenOptions,
  DocGenResult,
  DocTemplate,
  DocFormatInfo,
  RAGDocument,
  RAGQueryResult,
  RAGUploadResult,
  SentimentResult,
  SummaryResult,
  TranslationResult,
  UploadUrlResult,
} from './services/index.js';
