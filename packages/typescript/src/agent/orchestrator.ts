/**
 * Multi-agent orchestration — Team and Pipeline patterns.
 */

import type { Agent } from './agent.js';
import type { AgentResult, TeamResult } from '../types.js';

/**
 * Orchestrate multiple agents working together on a task.
 *
 * Supports three workflow modes:
 * - "sequential" — agents run in insertion order, each receiving
 *   the previous agent's output
 * - "parallel" — all agents run simultaneously on the same prompt,
 *   outputs are combined
 * - "A → B → C" — explicit ordering with arrow syntax
 *
 * @example
 * ```typescript
 * import { Agent, Team, Tool } from 'scalix';
 *
 * const team = new Team({
 *   agents: {
 *     researcher: new Agent({ tools: [Tool.webSearch()] }),
 *     analyst: new Agent({ tools: [Tool.codeExec()] }),
 *     writer: new Agent(),
 *   },
 *   workflow: 'researcher → analyst → writer',
 * });
 *
 * const result = await team.run('Create a market report');
 * ```
 */
export class Team {
  readonly agents: Record<string, Agent>;
  readonly workflow: string;
  private readonly order: string[];

  constructor(options: { agents: Record<string, Agent>; workflow?: string }) {
    this.agents = options.agents;
    this.workflow = options.workflow ?? 'sequential';
    this.order = this.parseWorkflow(this.workflow);
  }

  private parseWorkflow(workflow: string): string[] {
    if (workflow === 'sequential' || workflow === 'parallel') {
      return Object.keys(this.agents);
    }

    // Parse arrow syntax: "researcher → analyst → writer"
    const names = workflow
      .replace(/→/g, '->')
      .split('->')
      .map((s) => s.trim());

    for (const name of names) {
      if (!(name in this.agents)) {
        throw new Error(
          `Agent '${name}' in workflow not found. Available: ${Object.keys(this.agents).join(', ')}`,
        );
      }
    }

    return names;
  }

  async run(prompt: string): Promise<TeamResult> {
    if (this.workflow === 'parallel') {
      return this.runParallel(prompt);
    }
    return this.runSequential(prompt);
  }

  private async runSequential(prompt: string): Promise<TeamResult> {
    const agentResults: Record<string, AgentResult> = {};
    const workflowLog: string[] = [];
    let currentInput = prompt;

    for (const name of this.order) {
      const agent = this.agents[name];
      workflowLog.push(`Running agent: ${name}`);

      const result = await agent.run(currentInput);
      agentResults[name] = result;
      workflowLog.push(`Agent '${name}' completed: ${result.output.length} chars`);

      // Pass this agent's output as input to the next
      currentInput =
        `Previous agent (${name}) produced the following output:\n\n` +
        `${result.output}\n\n` +
        `Original task: ${prompt}\n\n` +
        `Continue from where the previous agent left off.`;
    }

    const finalOutput =
      this.order.length > 0 ? agentResults[this.order[this.order.length - 1]].output : '';

    return { output: finalOutput, agentResults, workflowLog };
  }

  private async runParallel(prompt: string): Promise<TeamResult> {
    const workflowLog: string[] = ['Running all agents in parallel'];

    const entries = await Promise.allSettled(
      this.order.map(async (name) => {
        const result = await this.agents[name].run(prompt);
        return { name, result };
      }),
    );

    const agentResults: Record<string, AgentResult> = {};

    for (const entry of entries) {
      if (entry.status === 'fulfilled') {
        const { name, result } = entry.value;
        agentResults[name] = result;
        workflowLog.push(`Agent '${name}' completed: ${result.output.length} chars`);
      } else {
        workflowLog.push(`Agent failed: ${entry.reason}`);
      }
    }

    // Combine all outputs
    const combinedParts: string[] = [];
    for (const name of this.order) {
      if (name in agentResults) {
        combinedParts.push(`=== ${name} ===\n${agentResults[name].output}`);
      }
    }

    return {
      output: combinedParts.join('\n\n'),
      agentResults,
      workflowLog,
    };
  }
}

/**
 * A linear chain of agents where each agent's output feeds the next.
 *
 * @example
 * ```typescript
 * import { Agent, Pipeline } from 'scalix';
 *
 * const pipeline = new Pipeline([
 *   new Agent({ instructions: 'Extract key facts from the input' }),
 *   new Agent({ instructions: 'Summarize the facts into bullet points' }),
 *   new Agent({ instructions: 'Format as a professional report' }),
 * ]);
 *
 * const result = await pipeline.run('Raw data: ...');
 * ```
 */
export class Pipeline {
  readonly steps: Agent[];

  constructor(steps: Agent[]) {
    this.steps = steps;
  }

  async run(prompt: string): Promise<TeamResult> {
    const agentResults: Record<string, AgentResult> = {};
    const workflowLog: string[] = [];
    let currentInput = prompt;

    for (let i = 0; i < this.steps.length; i++) {
      const stepName = `step_${i}`;
      workflowLog.push(`Running step ${i + 1}/${this.steps.length}`);

      const result = await this.steps[i].run(currentInput);
      agentResults[stepName] = result;
      workflowLog.push(`Step ${i + 1} completed: ${result.output.length} chars`);

      currentInput = result.output;
    }

    const finalOutput =
      this.steps.length > 0 ? agentResults[`step_${this.steps.length - 1}`].output : '';

    return { output: finalOutput, agentResults, workflowLog };
  }
}
