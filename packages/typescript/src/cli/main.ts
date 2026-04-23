#!/usr/bin/env node

/**
 * Scalix CLI — unified command-line tool for AI agent development.
 *
 * Commands:
 *   scalix dev       — Start local development server
 *   scalix deploy    — Deploy agent to Scalix Cloud
 *   scalix logs      — Stream logs from deployed agent
 *   scalix init      — Initialize a new Scalix project
 *   scalix run       — Run an agent locally
 *
 * Usage:
 *   npx scalix --help
 */

import { parseArgs } from 'util';

const HELP = `
Scalix — Build, run, and deploy AI agents.

Usage:
  scalix <command> [options]

Commands:
  init [name]           Initialize a new Scalix agent project
  run <prompt>          Run an agent locally
  dev [entry]           Start local development server
  deploy [entry]        Deploy agent to Scalix Cloud
  logs [deployment]     Stream logs from deployed agent

Options:
  --help, -h            Show this help message
  --version, -v         Show version

Examples:
  scalix init my-agent
  scalix run "What's the weather?" -e agent.ts
  scalix dev agent.ts --port 4000
  scalix deploy agent.ts --name my-agent
  scalix logs --follow
`.trim();

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    console.log(HELP);
    return;
  }

  if (command === '--version' || command === '-v') {
    console.log('scalix 0.1.0');
    return;
  }

  switch (command) {
    case 'init':
      await cmdInit(args.slice(1));
      break;
    case 'run':
      await cmdRun(args.slice(1));
      break;
    case 'dev':
      await cmdDev(args.slice(1));
      break;
    case 'deploy':
      await cmdDeploy(args.slice(1));
      break;
    case 'logs':
      await cmdLogs(args.slice(1));
      break;
    default:
      console.error(`Unknown command: ${command}`);
      console.log('Run "scalix --help" for usage.');
      process.exit(1);
  }
}

async function cmdInit(args: string[]): Promise<void> {
  const fs = await import('fs');
  const path = await import('path');

  const name = args[0] ?? 'my-agent';
  const projectDir = path.join(process.cwd(), name);

  if (fs.existsSync(projectDir)) {
    console.error(`Error: Directory '${name}' already exists.`);
    process.exit(1);
  }

  fs.mkdirSync(projectDir, { recursive: true });

  // Create starter agent.ts
  const agentCode = `import { Agent, Tool } from 'scalix';

const agent = new Agent({
  model: 'auto',
  instructions: 'You are a helpful AI assistant.',
  tools: [
    Tool.codeExec(),
    Tool.webSearch(),
  ],
});

const result = await agent.run('Hello! What can you help me with?');
console.log(result.output);
`;

  fs.writeFileSync(path.join(projectDir, 'agent.ts'), agentCode);

  // Create package.json
  const pkg = {
    name,
    version: '0.1.0',
    type: 'module',
    dependencies: {
      scalix: '^0.1.0',
    },
  };
  fs.writeFileSync(path.join(projectDir, 'package.json'), JSON.stringify(pkg, null, 2) + '\n');

  // Create .env.example
  const envExample = [
    '# Scalix Cloud (optional)',
    '# SCALIX_API_KEY=sk-scalix-...',
    '',
    '# BYOK Local Mode (optional, use your own provider keys)',
    '# ANTHROPIC_API_KEY=sk-ant-...',
    '# OPENAI_API_KEY=sk-...',
    '# GOOGLE_API_KEY=...',
    '',
  ].join('\n');
  fs.writeFileSync(path.join(projectDir, '.env.example'), envExample);

  console.log(`Created Scalix project: ${name}/`);
  console.log(`  agent.ts       — Your agent definition`);
  console.log(`  package.json   — Node.js dependencies`);
  console.log(`  .env.example   — Environment variables`);
  console.log();
  console.log('Get started:');
  console.log(`  cd ${name}`);
  console.log(`  npm install`);
  console.log(`  npx scalix run 'Hello!' -e agent.ts`);
}

async function cmdRun(args: string[]): Promise<void> {
  const { values, positionals } = parseArgs({
    args,
    options: {
      entry: { type: 'string', short: 'e', default: 'agent.ts' },
    },
    allowPositionals: true,
  });

  const prompt = positionals[0];
  if (!prompt) {
    console.error('Error: No prompt provided.');
    console.log('Usage: scalix run "Your prompt here" -e agent.ts');
    process.exit(1);
  }

  const entry = values.entry ?? 'agent.ts';
  const agent = await loadAgent(entry);

  const result = await agent.run(prompt);
  console.log(result.output);
}

async function cmdDev(args: string[]): Promise<void> {
  const { values, positionals } = parseArgs({
    args,
    options: {
      port: { type: 'string', short: 'p', default: '4000' },
      host: { type: 'string', default: '0.0.0.0' },
    },
    allowPositionals: true,
  });

  const entry = positionals[0] ?? 'agent.ts';
  const port = parseInt(values.port ?? '4000', 10);
  const host = values.host ?? '0.0.0.0';

  const agent = await loadAgent(entry);

  const http = await import('http');
  const { A2AServer } = await import('../protocols/a2aServer.js');

  const a2a = new A2AServer({ agent });
  const baseUrl = `http://${host}:${port}`;

  const server = http.createServer(async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    if (req.method === 'GET' && req.url === '/.well-known/agent.json') {
      const card = a2a.getAgentCard(baseUrl);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(card));
      return;
    }

    if (req.method === 'GET' && req.url === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'ok', mode: 'development' }));
      return;
    }

    if (req.method === 'POST' && (req.url === '/' || req.url === '/a2a')) {
      let body = '';
      for await (const chunk of req) body += chunk;
      try {
        const request = JSON.parse(body);
        const response = await a2a.handleJsonRpc(request);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(response));
      } catch {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          jsonrpc: '2.0', id: null,
          error: { code: -32700, message: 'Parse error' },
        }));
      }
      return;
    }

    res.writeHead(404);
    res.end('Not found');
  });

  server.listen(port, host, () => {
    console.log(`Scalix dev server running at ${baseUrl}`);
    console.log(`  A2A:    ${baseUrl}/.well-known/agent.json`);
    console.log(`  Health: ${baseUrl}/health`);
    console.log();
    console.log('Press Ctrl+C to stop.');
  });
}

async function cmdDeploy(args: string[]): Promise<void> {
  const { values, positionals } = parseArgs({
    args,
    options: {
      name: { type: 'string', short: 'n' },
      env: { type: 'string', short: 'e', default: 'production' },
      region: { type: 'string', short: 'r', default: 'us-east-1' },
    },
    allowPositionals: true,
  });

  const entry = positionals[0] ?? 'agent.ts';
  const { getConfig, isCloudMode } = await import('../config.js');

  if (!isCloudMode()) {
    console.error('Error: No API key configured.');
    console.error('Set SCALIX_API_KEY or call configure({ apiKey: "..." })');
    process.exit(1);
  }

  const fs = await import('fs');
  const path = await import('path');

  const entryPath = path.resolve(entry);
  if (!fs.existsSync(entryPath)) {
    console.error(`Error: ${entry} not found.`);
    process.exit(1);
  }

  const config = getConfig();
  const deployName = values.name ?? path.basename(entry, path.extname(entry));
  const sourceCode = fs.readFileSync(entryPath, 'utf-8');

  console.log(`Deploying '${deployName}' to Scalix Cloud...`);

  const resp = await fetch(`${config.baseUrl}/api/hosting/deploy`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${config.apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: deployName,
      source: sourceCode,
      runtime: 'node22',
      environment: values.env,
      region: values.region,
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    console.error(`Deploy failed: ${resp.status} ${text}`);
    process.exit(1);
  }

  const data = (await resp.json()) as Record<string, string>;
  console.log('Deployed successfully!');
  console.log(`  ID:  ${data.id ?? data.deployment_id ?? ''}`);
  console.log(`  URL: ${data.url ?? data.endpoint ?? ''}`);
}

async function cmdLogs(args: string[]): Promise<void> {
  const { values, positionals } = parseArgs({
    args,
    options: {
      follow: { type: 'boolean', short: 'f', default: false },
      tail: { type: 'string', short: 'n', default: '100' },
    },
    allowPositionals: true,
  });

  const deployment = positionals[0];
  const { getConfig, isCloudMode } = await import('../config.js');

  if (!isCloudMode()) {
    console.error('Error: No API key configured.');
    process.exit(1);
  }

  const config = getConfig();
  const params = new URLSearchParams({ tail: values.tail ?? '100' });
  if (deployment) params.set('deployment_id', deployment);

  const resp = await fetch(
    `${config.baseUrl}/api/hosting/logs?${params}`,
    {
      headers: { Authorization: `Bearer ${config.apiKey}` },
    },
  );

  if (!resp.ok) {
    console.error(`Failed to get logs: ${resp.status}`);
    process.exit(1);
  }

  const data = (await resp.json()) as { logs?: Array<Record<string, string> | string> };
  for (const line of data.logs ?? []) {
    if (typeof line === 'object' && line !== null) {
      console.log(`${line.timestamp ?? ''}  ${line.message ?? ''}`);
    } else {
      console.log(String(line));
    }
  }
}

async function loadAgent(entry: string): Promise<import('../agent/agent.js').Agent> {
  const path = await import('path');
  const entryPath = path.resolve(entry);

  try {
    const module = await import(entryPath);

    // Look for an Agent instance export
    const { Agent } = await import('../agent/agent.js');
    for (const key of Object.keys(module)) {
      if (module[key] instanceof Agent) {
        return module[key] as import('../agent/agent.js').Agent;
      }
    }

    // Check default export
    if (module.default instanceof Agent) {
      return module.default as import('../agent/agent.js').Agent;
    }

    console.error('Error: No Agent instance found in the module.');
    console.error('Define an agent: export const agent = new Agent({ model: "auto" });');
    process.exit(1);
  } catch (err) {
    console.error(`Error loading ${entry}: ${err instanceof Error ? err.message : err}`);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
