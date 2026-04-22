/**
 * Core Agent class — the central abstraction of the Scalix SDK.
 */

import { getConfig, isCloudMode, dynamicImport } from '../config.js';
import type { Tool } from '../tools/base.js';
import type {
  AgentOptions,
  AgentResult,
  Message,
  StreamEvent,
  ToolCall,
  ToolCallResult,
  ToolDefinition,
} from '../types.js';
import type { LLMProvider } from '../providers/base.js';

/**
 * An AI agent that can reason, use tools, and maintain state.
 *
 * The agent runs an LLM in a loop: it sends messages to the model,
 * executes any tool calls the model requests, feeds results back,
 * and repeats until the model produces a final text response.
 *
 * @example
 * ```typescript
 * import { Agent, Tool } from 'scalix';
 *
 * const agent = new Agent({
 *   model: 'claude-sonnet-4',
 *   instructions: 'You are a helpful data analyst.',
 *   tools: [Tool.codeExec(), Tool.webSearch()],
 * });
 *
 * const result = await agent.run('Analyze the top trending repos');
 * console.log(result.output);
 * ```
 */
export class Agent {
  readonly model: string;
  readonly instructions: string;
  readonly tools: Tool[];
  readonly memory: boolean;
  readonly maxTurns: number;
  readonly temperature: number;
  readonly timeout: number;

  private history: Message[] = [];
  private llmProvider: LLMProvider | null = null;
  private toolExecutor: ToolExecutor | null = null;

  constructor(options: AgentOptions = {}) {
    this.model = options.model ?? 'auto';
    this.instructions = options.instructions ?? '';
    this.tools = options.tools ?? [];
    this.memory = options.memory ?? false;
    this.maxTurns = options.maxTurns ?? 10;
    this.temperature = options.temperature ?? 0.7;
    this.timeout = options.timeout ?? 300;
  }

  private async getLLMProvider(): Promise<LLMProvider> {
    if (!this.llmProvider) {
      if (isCloudMode()) {
        const { ScalixRouterProvider } = await import('../providers/cloud/router.js');
        this.llmProvider = new ScalixRouterProvider(getConfig()) as LLMProvider;
      } else {
        const { DirectLLM } = await import('../providers/local/directLlm.js');
        this.llmProvider = new DirectLLM(getConfig()) as LLMProvider;
      }
    }
    return this.llmProvider;
  }

  private getToolExecutor(): ToolExecutor {
    if (!this.toolExecutor) {
      this.toolExecutor = new ToolExecutor(this.tools, getConfig());
    }
    return this.toolExecutor;
  }

  /**
   * Execute the agent with the given prompt.
   *
   * The agent will call the LLM, execute any tool calls, and loop
   * until it produces a final text response or hits maxTurns.
   */
  async run(prompt: string): Promise<AgentResult> {
    const llm = await this.getLLMProvider();
    const executor = this.getToolExecutor();

    // Build initial messages
    const messages = this.buildMessages(prompt);
    const allToolResults: ToolCallResult[] = [];

    // Get tool definitions for the LLM
    const toolDefs = this.tools.length > 0
      ? this.tools.map((t) => t.definition as unknown as Record<string, unknown>)
      : undefined;

    let hitMaxTurns = false;

    for (let turn = 0; turn < this.maxTurns; turn++) {
      // Call LLM
      const response = await llm.chat(messages, this.model, {
        tools: toolDefs,
        temperature: this.temperature,
      });

      messages.push(response);

      // If no tool calls, we have the final response
      if (!response.toolCalls?.length) {
        break;
      }

      // Execute each tool call
      for (const toolCall of response.toolCalls) {
        const toolResult = await executor.execute(toolCall);
        allToolResults.push(toolResult);

        // Add tool result as a message for the next LLM call
        let resultContent: string;
        if (toolResult.error) {
          resultContent = `Error: ${toolResult.error}`;
        } else if (typeof toolResult.result === 'string') {
          resultContent = toolResult.result;
        } else {
          resultContent = JSON.stringify(toolResult.result);
        }

        messages.push({
          role: 'tool',
          content: resultContent,
          toolCallId: toolCall.id,
          name: toolCall.name,
        });
      }

      // Check if this was the last turn
      if (turn === this.maxTurns - 1) {
        hitMaxTurns = true;
      }
    }

    // If we hit max turns, get a final response without tools
    if (hitMaxTurns) {
      const finalResponse = await llm.chat(messages, this.model, {
        temperature: this.temperature,
      });
      messages.push(finalResponse);
    }

    // Update memory
    if (this.memory) {
      this.history = [...messages];
    }

    // Extract final output
    const finalOutput = messages.length > 0 ? messages[messages.length - 1].content : '';

    return {
      output: finalOutput,
      messages,
      toolCalls: allToolResults,
    };
  }

  /**
   * Execute the agent and stream events as they occur.
   */
  async *stream(prompt: string): AsyncGenerator<StreamEvent> {
    const llm = await this.getLLMProvider();
    const executor = this.getToolExecutor();
    const messages = this.buildMessages(prompt);

    const toolDefs = this.tools.length > 0
      ? this.tools.map((t) => t.definition as unknown as Record<string, unknown>)
      : undefined;

    for (let turn = 0; turn < this.maxTurns; turn++) {
      // If no tools, stream directly
      if (!this.tools.length) {
        yield* llm.streamChat(messages, this.model, {
          temperature: this.temperature,
        });
        return;
      }

      // With tools, get full response to check for tool calls
      const response = await llm.chat(messages, this.model, {
        tools: toolDefs,
        temperature: this.temperature,
      });

      messages.push(response);

      if (!response.toolCalls?.length) {
        // Stream the final text response
        yield { type: 'text_delta', data: response.content };
        yield { type: 'done' };
        return;
      }

      // Execute tools and stream their results
      for (const toolCall of response.toolCalls) {
        yield {
          type: 'tool_call_start',
          toolName: toolCall.name,
          toolCallId: toolCall.id,
          data: toolCall.arguments as unknown as Record<string, unknown>,
        };

        const toolResult = await executor.execute(toolCall);

        let resultContent: string;
        if (toolResult.error) {
          resultContent = `Error: ${toolResult.error}`;
        } else if (typeof toolResult.result === 'string') {
          resultContent = toolResult.result;
        } else {
          resultContent = JSON.stringify(toolResult.result);
        }

        yield {
          type: 'tool_result',
          toolName: toolCall.name,
          toolCallId: toolCall.id,
          data: resultContent,
        };

        messages.push({
          role: 'tool',
          content: resultContent,
          toolCallId: toolCall.id,
          name: toolCall.name,
        });
      }
    }

    yield { type: 'done' };
  }

  /**
   * Build the message list for an LLM call.
   */
  private buildMessages(prompt: string): Message[] {
    const messages: Message[] = [];

    // System prompt
    if (this.instructions) {
      messages.push({ role: 'system', content: this.instructions });
    }

    // History (if memory enabled)
    if (this.memory && this.history.length > 0) {
      for (const msg of this.history) {
        if (msg.role !== 'system') {
          messages.push(msg);
        }
      }
    }

    // User prompt
    messages.push({ role: 'user', content: prompt });

    return messages;
  }

  /**
   * Get JSON Schema definitions for all registered tools.
   */
  getToolDefinitions(): ToolDefinition[] {
    return this.tools.map((tool) => tool.definition);
  }

  /**
   * Clear the agent's conversation history.
   */
  clearMemory(): void {
    this.history = [];
  }
}

/**
 * Executes tool calls by routing to the appropriate handler.
 *
 * Maps tool names to their execution backends:
 * - code_exec → subprocess / Docker
 * - sql → better-sqlite3
 * - web_search → fetch-based search
 * - http → fetch request
 * - Custom tools → their registered execute functions
 */
class ToolExecutor {
  private tools: Map<string, Tool>;

  constructor(
    tools: Tool[],
    _config: ReturnType<typeof getConfig>,
  ) {
    this.tools = new Map(tools.map((t) => [t.name, t]));
  }

  async execute(toolCall: ToolCall): Promise<ToolCallResult> {
    const start = performance.now();

    const tool = this.tools.get(toolCall.name);
    if (!tool) {
      return {
        toolName: toolCall.name,
        arguments: toolCall.arguments,
        result: null,
        error: `Unknown tool: ${toolCall.name}`,
      };
    }

    try {
      let result: unknown;

      switch (toolCall.name) {
        case 'code_exec':
          result = await this.executeCode(toolCall.arguments);
          break;
        case 'sql':
          result = await this.executeSql(toolCall.arguments);
          break;
        case 'web_search':
          result = await this.executeWebSearch(toolCall.arguments);
          break;
        case 'http':
          result = await this.executeHttp(toolCall.arguments);
          break;
        default:
          // Custom tool with registered function
          result = await tool.execute(toolCall.arguments);
          return result as ToolCallResult;
      }

      const durationMs = performance.now() - start;
      return {
        toolName: toolCall.name,
        arguments: toolCall.arguments,
        result,
        durationMs,
      };
    } catch (err) {
      const durationMs = performance.now() - start;
      return {
        toolName: toolCall.name,
        arguments: toolCall.arguments,
        result: null,
        error: err instanceof Error ? err.message : String(err),
        durationMs,
      };
    }
  }

  private async executeCode(
    args: Record<string, unknown>,
  ): Promise<string> {
    const { execFile } = await import('child_process');
    const { promisify } = await import('util');
    const { writeFile, unlink } = await import('fs/promises');
    const { tmpdir } = await import('os');
    const { join } = await import('path');

    const execFileAsync = promisify(execFile);
    const code = (args.code as string) ?? '';
    const runtime = (args.runtime as string) ?? 'python';

    const runtimeCommands: Record<string, { cmd: string; flag: string }> = {
      python: { cmd: 'python3', flag: '-c' },
      node: { cmd: 'node', flag: '-e' },
    };

    const rtConfig = runtimeCommands[runtime];
    if (rtConfig) {
      // Inline execution for python/node
      try {
        const { stdout, stderr } = await execFileAsync(rtConfig.cmd, [rtConfig.flag, code], {
          timeout: 30_000,
        });
        let output = stdout;
        if (stderr) output += `\nSTDERR:\n${stderr}`;
        return output;
      } catch (err: unknown) {
        const e = err as { stdout?: string; stderr?: string; code?: number };
        let output = e.stdout ?? '';
        if (e.stderr) output += `\nSTDERR:\n${e.stderr}`;
        output += `\n[Exit code: ${e.code ?? 1}]`;
        return output;
      }
    }

    // File-based execution for go/rust
    const extMap: Record<string, string> = { go: '.go', rust: '.rs' };
    const ext = extMap[runtime] ?? '.txt';
    const filePath = join(tmpdir(), `scalix_${Date.now()}${ext}`);

    try {
      await writeFile(filePath, code, 'utf-8');
      const cmdMap: Record<string, string[]> = {
        go: ['go', 'run', filePath],
        rust: ['sh', '-c', `rustc ${filePath} -o /tmp/scalix_out && /tmp/scalix_out`],
      };
      const cmd = cmdMap[runtime];
      if (!cmd) throw new Error(`Unsupported runtime: ${runtime}`);

      const { stdout, stderr } = await execFileAsync(cmd[0], cmd.slice(1), {
        timeout: 30_000,
      });
      let output = stdout;
      if (stderr) output += `\nSTDERR:\n${stderr}`;
      return output;
    } finally {
      await unlink(filePath).catch(() => {});
    }
  }

  private async executeSql(args: Record<string, unknown>): Promise<unknown> {
    // Use better-sqlite3 for local mode (sync but fast)
    const query = (args.query as string) ?? '';
    try {
      const mod = await dynamicImport('better-sqlite3') as { default: new (path: string) => { prepare: (sql: string) => { all: () => unknown[]; run: () => { changes: number } }; close: () => void } };
      const db = new mod.default('scalix_local.db');
      const stmt = db.prepare(query);

      if (query.trim().toUpperCase().startsWith('SELECT')) {
        const rows = stmt.all();
        db.close();
        return rows;
      } else {
        const result = stmt.run();
        db.close();
        return { changes: result.changes };
      }
    } catch {
      throw new Error(
        'better-sqlite3 not installed. Run: npm install better-sqlite3',
      );
    }
  }

  private async executeWebSearch(args: Record<string, unknown>): Promise<string> {
    const query = (args.query as string) ?? '';
    const config = getConfig();
    const searchUrl = config.searchBaseUrl
      ?? `${config.baseUrl}/research/search`;
    const headers: Record<string, string> = {
      'User-Agent': 'Scalix-SDK/0.1',
      'Content-Type': 'application/json',
    };
    if (config.apiKey) headers['Authorization'] = `Bearer ${config.apiKey}`;
    const resp = await fetch(searchUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query }),
    });
    const text = await resp.text();
    return text.slice(0, 5000);
  }

  private async executeHttp(args: Record<string, unknown>): Promise<unknown> {
    const url = (args.url as string) ?? '';
    const method = ((args.method as string) ?? 'GET').toUpperCase();
    const body = args.body as Record<string, unknown> | undefined;

    const resp = await fetch(url, {
      method,
      ...(body ? { body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } } : {}),
    });

    const text = await resp.text();
    return { status: resp.status, body: text.slice(0, 5000) };
  }
}
