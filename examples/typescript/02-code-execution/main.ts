/**
 * Scalix SDK — Example 02: Code Execution (TypeScript)
 *
 * Create an agent that can write and execute code.
 *
 * Local mode: code runs in Docker on your machine.
 * Cloud mode: code runs in Scalix Sandbox (Firecracker + GPU).
 *
 * Prerequisites:
 *   npm install scalix
 *   export ANTHROPIC_API_KEY=your-key
 *   Docker must be running (for local mode)
 */

import { Agent, Tool } from 'scalix';

const agent = new Agent({
  model: 'claude-sonnet-4',
  instructions: 'You are a data analyst. Write and execute Python code to answer questions.',
  tools: [Tool.codeExec({ runtime: 'python', timeout: 30 })],
});

const result = await agent.run(
  'Generate a list of the first 20 Fibonacci numbers and calculate their average.',
);

console.log(result.output);

for (const tc of result.toolCalls) {
  console.log(`\n--- Tool: ${tc.toolName} ---`);
  console.log(`Result: ${JSON.stringify(tc.result)}`);
}
