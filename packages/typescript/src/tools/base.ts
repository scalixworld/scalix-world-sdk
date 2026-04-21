/**
 * Tool base class and built-in tool factories.
 */

import type { ToolDefinition, ToolCallResult } from '../types.js';

/**
 * Base class for all agent tools.
 *
 * Use the static factory methods to create built-in tools:
 * - `Tool.codeExec()` — Execute code in a sandbox
 * - `Tool.sql()` — Query a database
 * - `Tool.webSearch()` — Search the web
 * - `Tool.http()` — Make HTTP requests
 * - `Tool.mcp()` — Import tools from an MCP server
 * - `Tool.fromFunction()` — Wrap a function as a tool
 */
export class Tool {
  readonly name: string;
  readonly description: string;
  readonly parameters: Record<string, unknown>;
  private executeFn?: (...args: unknown[]) => unknown;

  constructor(options: {
    name: string;
    description: string;
    parameters?: Record<string, unknown>;
    execute?: (...args: unknown[]) => unknown;
  }) {
    this.name = options.name;
    this.description = options.description;
    this.parameters = options.parameters ?? {};
    this.executeFn = options.execute;
  }

  get definition(): ToolDefinition {
    return {
      name: this.name,
      description: this.description,
      parameters: this.parameters,
    };
  }

  /** Whether this tool has a custom execute function registered. */
  get hasExecuteFn(): boolean {
    return this.executeFn != null;
  }

  async execute(params: Record<string, unknown>): Promise<ToolCallResult> {
    if (!this.executeFn) {
      throw new Error(`Tool '${this.name}' has no execute function`);
    }

    const result = await this.executeFn(params);
    return {
      toolName: this.name,
      arguments: params,
      result,
    };
  }

  // --- Built-in Tool Factories ---

  static codeExec(options?: {
    runtime?: string;
    gpu?: string;
    timeout?: number;
  }): Tool {
    const runtime = options?.runtime ?? 'python';
    return new Tool({
      name: 'code_exec',
      description: `Execute ${runtime} code in a secure sandbox environment.`,
      parameters: {
        type: 'object',
        properties: {
          code: { type: 'string', description: `The ${runtime} code to execute.` },
        },
        required: ['code'],
      },
    });
  }

  static sql(database?: string): Tool {
    return new Tool({
      name: 'sql',
      description: 'Execute a SQL query against the database.',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'The SQL query to execute.' },
        },
        required: ['query'],
      },
    });
  }

  static webSearch(provider?: string): Tool {
    return new Tool({
      name: 'web_search',
      description: 'Search the web for information.',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'The search query.' },
        },
        required: ['query'],
      },
    });
  }

  static http(baseUrl?: string): Tool {
    return new Tool({
      name: 'http',
      description: 'Make HTTP requests to external APIs.',
      parameters: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'The URL to request.' },
          method: {
            type: 'string',
            enum: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
            description: 'HTTP method.',
          },
          body: { type: 'object', description: 'Request body (for POST/PUT).' },
        },
        required: ['url'],
      },
    });
  }

  /**
   * Import tools from an MCP (Model Context Protocol) server.
   *
   * Connects to the MCP server via SSE, discovers available tools,
   * and wraps each as a Scalix Tool with an execute function that
   * calls the remote MCP tool.
   *
   * Note: This is an async operation. Use `await Tool.mcpAsync()` or
   * call this synchronous version which blocks until discovery completes.
   */
  static mcp(serverUrl: string): Tool[] {
    // Synchronous wrapper — delegates to mcpAsync internally
    // For Node.js, we use a sync approach by spawning a subprocess
    throw new Error(
      'Tool.mcp() is async. Use await Tool.mcpAsync(serverUrl) instead.',
    );
  }

  /**
   * Import tools from an MCP server (async version).
   *
   * @param serverUrl - URL of the MCP server's SSE endpoint.
   * @returns List of tools exposed by the MCP server.
   */
  static async mcpAsync(serverUrl: string): Promise<Tool[]> {
    let Client: new (
      info: { name: string; version: string },
    ) => MCPClientSession;
    let SSEClientTransport: new (url: URL) => MCPTransport;

    try {
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const clientMod = require('@modelcontextprotocol/sdk/client/index.js') as {
        Client: typeof Client;
      };
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const sseMod = require('@modelcontextprotocol/sdk/client/sse.js') as {
        SSEClientTransport: typeof SSEClientTransport;
      };
      Client = clientMod.Client;
      SSEClientTransport = sseMod.SSEClientTransport;
    } catch {
      throw new Error(
        '@modelcontextprotocol/sdk package not installed. ' +
          'Run: npm install @modelcontextprotocol/sdk',
      );
    }

    const transport = new SSEClientTransport(new URL(serverUrl));
    const client = new Client({ name: 'scalix-sdk', version: '1.0.0' });
    await client.connect(transport);

    const response = await client.listTools();
    const tools: Tool[] = [];

    for (const mcpTool of response.tools) {
      const toolName = mcpTool.name;
      const inputSchema = (mcpTool.inputSchema ?? {}) as Record<string, unknown>;

      tools.push(
        new Tool({
          name: mcpTool.name,
          description: mcpTool.description ?? `MCP tool: ${mcpTool.name}`,
          parameters: inputSchema,
          execute: async (args: Record<string, unknown>) => {
            // Create a fresh connection for each call
            const t = new SSEClientTransport(new URL(serverUrl));
            const c = new Client({ name: 'scalix-sdk', version: '1.0.0' });
            await c.connect(t);
            try {
              const result = await c.callTool(toolName, args);
              const content = result.content as Array<{ type: string; text?: string }>;
              if (content) {
                const texts = content
                  .filter((p) => p.type === 'text' && p.text)
                  .map((p) => p.text!);
                return texts.join('\n') || JSON.stringify(result);
              }
              return JSON.stringify(result);
            } finally {
              await c.close();
            }
          },
        }),
      );
    }

    await client.close();
    return tools;
  }

  static fromFunction(
    name: string,
    description: string,
    fn: (...args: unknown[]) => unknown,
    parameters?: Record<string, unknown>,
  ): Tool {
    return new Tool({ name, description, parameters, execute: fn });
  }
}

/** Internal type for MCP client session. */
interface MCPClientSession {
  connect(transport: MCPTransport): Promise<void>;
  listTools(): Promise<{ tools: MCPRemoteTool[] }>;
  callTool(name: string, args: Record<string, unknown>): Promise<{ content: unknown }>;
  close(): Promise<void>;
}

/** Internal type for MCP transport. */
interface MCPTransport {
  start(): void;
}

/** Internal type for MCP remote tool descriptor. */
interface MCPRemoteTool {
  name: string;
  description?: string;
  inputSchema?: Record<string, unknown>;
}
