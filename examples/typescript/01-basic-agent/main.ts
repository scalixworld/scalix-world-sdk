/**
 * Scalix SDK — Example 01: Basic Agent (TypeScript)
 *
 * Create a simple AI agent that can answer questions.
 * No Scalix account needed — runs in local mode.
 *
 * Prerequisites:
 *   npm install scalix
 *   export ANTHROPIC_API_KEY=your-key
 */

import { Agent } from 'scalix';

const agent = new Agent({
  model: 'claude-sonnet-4',
  instructions: 'You are a helpful assistant that gives concise, clear answers.',
});

const result = await agent.run('What are the top 3 programming languages in 2026?');
console.log(result.output);
