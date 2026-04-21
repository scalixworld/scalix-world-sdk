/**
 * Scalix SDK — Example 03: Multi-Agent Team (TypeScript)
 *
 * Create a team of agents that collaborate on a task.
 *
 * Prerequisites:
 *   npm install scalix
 *   export ANTHROPIC_API_KEY=your-key
 */

import { Agent, Team, Tool } from 'scalix';

const researcher = new Agent({
  model: 'auto',
  instructions: 'You are a research specialist. Find and summarize key information.',
  tools: [Tool.webSearch()],
});

const analyst = new Agent({
  model: 'auto',
  instructions: 'You are a data analyst. Analyze data and extract insights using code.',
  tools: [Tool.codeExec()],
});

const writer = new Agent({
  model: 'auto',
  instructions: 'You are a technical writer. Create clear, structured reports.',
});

const team = new Team({
  agents: { researcher, analyst, writer },
  workflow: 'researcher → analyst → writer',
});

const result = await team.run(
  'Research the current state of AI agent frameworks, ' +
    'analyze their GitHub star growth, and write a brief report.',
);

console.log(result.output);
console.log('\nWorkflow log:', result.workflowLog);
