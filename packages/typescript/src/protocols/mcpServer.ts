/**
 * MCP (Model Context Protocol) server — expose Scalix agents and tools.
 *
 * Allows any MCP-compatible client (Claude Code, Cursor, Windsurf, etc.)
 * to use Scalix agents and tools via the standard MCP protocol.
 *
 * @example
 * ```typescript
 * import { Agent, Tool } from 'scalix';
 * import { MCPServer } from 'scalix/protocols';
 *
 * const agent = new Agent({ model: 'claude-sonnet-4', tools: [Tool.codeExec()] });
 * const server = new MCPServer({ agent });
 * server.start(); // stdio transport (default)
 * ```
 */

import type { Agent } from '../agent/agent.js';
import type { Tool } from '../tools/base.js';

interface MCPServerOptions {
  agent?: Agent;
  tools?: Tool[];
  name?: string;
}

interface FastMCPInstance {
  tool(
    nameOrOptions: string | { name: string; description: string },
    fn: (...args: unknown[]) => unknown,
  ): void;
  run(options?: { transport?: string }): void;
  sse_app?(): unknown;
}

/**
 * Expose Scalix agents and tools as an MCP server.
 *
 * This allows any MCP-compatible client to discover and invoke
 * Scalix tools, or run the agent directly via a "run_agent" tool.
 */
export class MCPServer {
  private agent: Agent | undefined;
  private tools: Tool[];
  private name: string;
  private mcp: FastMCPInstance | null = null;

  constructor(options: MCPServerOptions) {
    this.agent = options.agent;
    this.tools = options.tools ?? [];
    this.name = options.name ?? 'scalix';
  }

  private buildServer(): FastMCPInstance {
    if (this.mcp) return this.mcp;

    try {
      // The @modelcontextprotocol/sdk provides Server class
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const sdk = require('@modelcontextprotocol/sdk/server/index.js') as {
        Server: new (
          info: { name: string; version: string },
          options: { capabilities: Record<string, unknown> },
        ) => MCPSDKServer;
      };
      return this.buildWithSDK(sdk.Server);
    } catch {
      throw new Error(
        '@modelcontextprotocol/sdk package not installed. ' +
          'Run: npm install @modelcontextprotocol/sdk',
      );
    }
  }

  private buildWithSDK(
    ServerClass: new (
      info: { name: string; version: string },
      options: { capabilities: Record<string, unknown> },
    ) => MCPSDKServer,
  ): FastMCPInstance {
    const server = new ServerClass(
      { name: this.name, version: '1.0.0' },
      { capabilities: { tools: {} } },
    );

    // Collect all tool definitions
    const toolDefs: MCPToolDef[] = [];

    for (const tool of this.tools) {
      toolDefs.push({
        name: tool.name,
        description: tool.description,
        inputSchema: tool.parameters ?? { type: 'object', properties: {} },
      });
    }

    if (this.agent) {
      const desc =
        'Run the Scalix agent' +
        (this.agent.instructions ? `: ${this.agent.instructions.slice(0, 100)}` : '') +
        '. Send a prompt and get the agent\'s response.';
      toolDefs.push({
        name: 'run_agent',
        description: desc,
        inputSchema: {
          type: 'object',
          properties: {
            prompt: { type: 'string', description: 'The prompt to send to the agent' },
          },
          required: ['prompt'],
        },
      });
    }

    // Register tools/list handler
    server.setRequestHandler('tools/list', async () => ({
      tools: toolDefs,
    }));

    // Register tools/call handler
    const agentRef = this.agent;
    const toolsRef = this.tools;
    server.setRequestHandler(
      'tools/call',
      async (request: unknown) => {
        const { params } = request as { params: { name: string; arguments?: Record<string, unknown> } };
        const { name, arguments: args } = params;

        if (name === 'run_agent' && agentRef) {
          const prompt = (args?.prompt as string) ?? '';
          const result = await agentRef.run(prompt);
          return {
            content: [{ type: 'text', text: result.output }],
          };
        }

        // Find matching tool
        const tool = toolsRef.find((t) => t.name === name);
        if (!tool) {
          return {
            content: [{ type: 'text', text: `Unknown tool: ${name}` }],
            isError: true,
          };
        }

        if (tool.hasExecuteFn) {
          const result = await tool.execute(args ?? {});
          return {
            content: [{ type: 'text', text: JSON.stringify(result.result) }],
          };
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({ tool: name, arguments: args }),
            },
          ],
        };
      },
    );

    // Wrap as FastMCPInstance interface for our start() method
    const wrapper: FastMCPInstance = {
      tool: () => {
        /* Already registered above */
      },
      run: (options?: { transport?: string }) => {
        const transport = options?.transport ?? 'stdio';
        if (transport === 'stdio') {
          this.startStdio(server);
        } else {
          throw new Error(`Transport '${transport}' not yet supported in TypeScript SDK`);
        }
      },
    };

    this.mcp = wrapper;
    return wrapper;
  }

  private startStdio(server: MCPSDKServer): void {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const { StdioServerTransport } = require(
      '@modelcontextprotocol/sdk/server/stdio.js',
    ) as {
      StdioServerTransport: new () => { start(): void };
    };

    const transport = new StdioServerTransport();
    server.connect(transport).catch((err: Error) => {
      console.error('MCP server error:', err);
      process.exit(1);
    });
  }

  /**
   * Start the MCP server.
   *
   * @param transport - Transport mechanism. "stdio" for local CLI tools.
   */
  start(transport: string = 'stdio'): void {
    const mcp = this.buildServer();
    mcp.run({ transport });
  }
}

/** Internal type for @modelcontextprotocol/sdk Server instance. */
interface MCPSDKServer {
  setRequestHandler(method: string, handler: (request: unknown) => Promise<unknown>): void;
  connect(transport: unknown): Promise<void>;
}

/** Internal type for MCP tool definitions. */
interface MCPToolDef {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
}
