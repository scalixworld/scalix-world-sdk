/**
 * A2A (Agent-to-Agent Protocol) server — expose Scalix agents to other agents.
 *
 * Implements Google's A2A protocol, allowing external agents built on any
 * framework (LangChain, CrewAI, OpenAI, etc.) to discover and collaborate
 * with Scalix agents.
 *
 * @example
 * ```typescript
 * import { Agent } from 'scalix';
 * import { A2AServer } from 'scalix/protocols';
 *
 * const agent = new Agent({ model: 'scalix-world-ai' });
 * const a2a = new A2AServer({ agent });
 * a2a.start(5000);
 * ```
 */

import type { Agent } from '../agent/agent.js';
import { randomUUID } from 'crypto';

interface A2AServerOptions {
  agent: Agent;
  name?: string;
  description?: string;
  version?: string;
  skills?: AgentSkill[];
}

interface AgentSkill {
  id: string;
  name: string;
  description: string;
}

interface AgentCard {
  name: string;
  description: string;
  url: string;
  version: string;
  capabilities: {
    streaming: boolean;
    pushNotifications: boolean;
  };
  defaultInputModes: string[];
  defaultOutputModes: string[];
  skills: AgentSkill[];
}

interface JsonRpcRequest {
  jsonrpc: string;
  id: number | string;
  method: string;
  params: Record<string, unknown>;
}

interface A2ATask {
  id: string;
  contextId: string;
  status: { state: string; message?: string };
  artifacts?: Array<{ parts: Array<{ type: string; text: string }> }>;
}

/**
 * Expose a Scalix agent via the A2A protocol.
 *
 * Implements the core A2A specification:
 * - Agent Card at /.well-known/agent.json for discovery
 * - JSON-RPC 2.0 request handling for message/send
 * - Task lifecycle management (working → completed/failed)
 */
export class A2AServer {
  private agent: Agent;
  private name: string;
  private description: string;
  private version: string;
  private skills: AgentSkill[];
  private tasks: Map<string, A2ATask> = new Map();

  constructor(options: A2AServerOptions) {
    this.agent = options.agent;
    this.name = options.name ?? 'scalix-agent';
    this.description =
      options.description ?? this.agent.instructions ?? 'A Scalix AI agent';
    this.version = options.version ?? '1.0.0';
    this.skills = options.skills ?? this.autoSkills();
  }

  private autoSkills(): AgentSkill[] {
    const skills: AgentSkill[] = [];
    if (this.agent.instructions) {
      skills.push({
        id: 'general',
        name: 'General Assistant',
        description: this.agent.instructions.slice(0, 200),
      });
    }
    for (const tool of this.agent.tools ?? []) {
      skills.push({
        id: tool.name,
        name: tool.name,
        description: tool.description,
      });
    }
    return skills.length > 0
      ? skills
      : [{ id: 'default', name: 'Agent', description: this.description }];
  }

  getAgentCard(baseUrl: string = 'http://localhost:5000'): AgentCard {
    return {
      name: this.name,
      description: this.description,
      url: baseUrl,
      version: this.version,
      capabilities: {
        streaming: false,
        pushNotifications: false,
      },
      defaultInputModes: ['text/plain'],
      defaultOutputModes: ['text/plain'],
      skills: this.skills,
    };
  }

  async handleJsonRpc(request: JsonRpcRequest): Promise<Record<string, unknown>> {
    const { method, params, id: rpcId } = request;

    try {
      let result: Record<string, unknown>;

      switch (method) {
        case 'message/send':
          result = await this.handleMessageSend(params);
          break;
        case 'tasks/get':
          result = this.handleTasksGet(params);
          break;
        case 'tasks/cancel':
          result = this.handleTasksCancel(params);
          break;
        default:
          return {
            jsonrpc: '2.0',
            id: rpcId,
            error: { code: -32601, message: `Method not found: ${method}` },
          };
      }

      return { jsonrpc: '2.0', id: rpcId, result };
    } catch (err) {
      return {
        jsonrpc: '2.0',
        id: rpcId,
        error: {
          code: -32000,
          message: err instanceof Error ? err.message : String(err),
        },
      };
    }
  }

  private async handleMessageSend(
    params: Record<string, unknown>,
  ): Promise<Record<string, unknown>> {
    const message = (params.message ?? {}) as Record<string, unknown>;
    const parts = (message.parts ?? []) as Array<Record<string, unknown>>;

    // Extract text content
    const promptParts: string[] = [];
    for (const part of parts) {
      if (part.type === 'text' && typeof part.text === 'string') {
        promptParts.push(part.text);
      }
    }
    const prompt = promptParts.join('\n') || String(message.content ?? '');

    const taskId = randomUUID();
    const contextId = (params.contextId as string) ?? randomUUID();

    this.tasks.set(taskId, {
      id: taskId,
      contextId,
      status: { state: 'working' },
    });

    const agentResult = await this.agent.run(prompt);

    const artifacts = [
      {
        parts: [{ type: 'text', text: agentResult.output }],
      },
    ];

    const task: A2ATask = {
      id: taskId,
      contextId,
      status: { state: 'completed' },
      artifacts,
    };
    this.tasks.set(taskId, task);

    return task as unknown as Record<string, unknown>;
  }

  private handleTasksGet(params: Record<string, unknown>): Record<string, unknown> {
    const taskId = params.id as string;
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`Task not found: ${taskId}`);
    return task as unknown as Record<string, unknown>;
  }

  private handleTasksCancel(params: Record<string, unknown>): Record<string, unknown> {
    const taskId = params.id as string;
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`Task not found: ${taskId}`);
    task.status = { state: 'canceled' };
    return task as unknown as Record<string, unknown>;
  }

  /**
   * Start the A2A server using Node.js built-in HTTP.
   */
  async start(port: number = 5000, host: string = '0.0.0.0'): Promise<void> {
    const http = await import('http');
    const baseUrl = `http://${host}:${port}`;

    const server = http.createServer(async (req, res) => {
      // CORS headers
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

      if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
      }

      // Agent Card endpoint
      if (req.method === 'GET' && req.url === '/.well-known/agent.json') {
        const card = this.getAgentCard(baseUrl);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(card));
        return;
      }

      // JSON-RPC endpoint
      if (req.method === 'POST' && (req.url === '/' || req.url === '')) {
        let body = '';
        for await (const chunk of req) {
          body += chunk;
        }

        try {
          const request = JSON.parse(body) as JsonRpcRequest;
          const response = await this.handleJsonRpc(request);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(response));
        } catch {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(
            JSON.stringify({
              jsonrpc: '2.0',
              id: null,
              error: { code: -32700, message: 'Parse error' },
            }),
          );
        }
        return;
      }

      res.writeHead(404);
      res.end('Not found');
    });

    server.listen(port, host, () => {
      console.log(`A2A server listening at ${baseUrl}`);
      console.log(`Agent Card: ${baseUrl}/.well-known/agent.json`);
    });
  }
}
