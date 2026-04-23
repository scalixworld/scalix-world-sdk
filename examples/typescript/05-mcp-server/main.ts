/**
 * Scalix SDK — Example 05: MCP Server (TypeScript)
 *
 * Expose your Scalix agent as an MCP server.
 *
 * Prerequisites:
 *   npm install scalix @modelcontextprotocol/sdk
 *   export SCALIX_API_KEY=your-key
 *
 * Usage:
 *   npx tsx main.ts
 *   Add to Claude Code settings:
 *     "mcpServers": {
 *       "scalix-agent": {
 *         "command": "npx",
 *         "args": ["tsx", "main.ts"]
 *       }
 *     }
 */

import { Agent, Tool, MCPServer } from 'scalix';

const agent = new Agent({
  model: 'scalix-world-ai',
  instructions: 'You are a helpful coding assistant.',
  tools: [Tool.codeExec(), Tool.webSearch()],
});

const server = new MCPServer({
  agent,
  tools: [Tool.codeExec(), Tool.webSearch()],
  name: 'coding-assistant',
});

server.start(); // stdio transport
