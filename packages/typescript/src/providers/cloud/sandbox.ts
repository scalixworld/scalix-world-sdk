/**
 * Scalix Sandbox provider — wraps the existing @scalix-world/sandbox SDK.
 *
 * Provides Firecracker microVM isolation and GPU compute.
 * This is a thin wrapper that delegates to the existing @scalix-world/sandbox package.
 */

import { getConfig, isCloudMode, dynamicImport, type ScalixConfig } from '../../config.js';
import { AuthenticationError, ProviderError, SandboxError } from '../../errors.js';
import type { SandboxProvider } from '../base.js';
import type { SandboxResult } from '../../types.js';

/** Map SDK runtime names to @scalix-world/sandbox runtime identifiers. */
const RUNTIME_MAP: Record<string, string> = {
  python: 'python3.12',
  'python3.12': 'python3.12',
  'python3.13': 'python3.13',
  node: 'node22',
  node22: 'node22',
  node24: 'node24',
  go: 'go1.22',
  'go1.22': 'go1.22',
  rust: 'rust-latest',
  'rust-latest': 'rust-latest',
};

/** Map runtime names to inline execution commands. null = file-based execution. */
const RUNTIME_EXEC_CMD: Record<string, [string, string] | null> = {
  python: ['python3', '-c'],
  'python3.12': ['python3', '-c'],
  'python3.13': ['python3', '-c'],
  node: ['node', '-e'],
  node22: ['node', '-e'],
  node24: ['node', '-e'],
  go: null,
  'go1.22': null,
  rust: null,
  'rust-latest': null,
};

/** File extensions for file-based runtimes. */
const EXT_MAP: Record<string, string> = {
  go: '.go',
  'go1.22': '.go',
  rust: '.rs',
  'rust-latest': '.rs',
};

/**
 * Execute code in Scalix Sandbox — Firecracker microVMs with GPU support.
 *
 * Wraps the existing `@scalix-world/sandbox` TypeScript SDK.
 * Requires a Scalix API key (cloud mode).
 *
 * Advantages over Docker sandbox:
 * - Firecracker microVM isolation (production-grade security)
 * - GPU access (T4, A100, H100)
 * - Persistent snapshots
 * - Resource monitoring and metrics
 * - Auto-scaling
 */
export class ScalixSandboxProvider implements SandboxProvider {
  private config: ScalixConfig;
  private configured = false;

  constructor(config?: ScalixConfig) {
    this.config = config ?? getConfig();
    if (!isCloudMode()) {
      throw new AuthenticationError(
        "Scalix Sandbox requires an API key. Call configure({ apiKey: 'sk_scalix_...' }) first.",
      );
    }
  }

  private async ensureConfigured(): Promise<void> {
    if (this.configured) return;

    try {
      const { configure } = await dynamicImport('@scalix-world/sandbox') as unknown as {
        configure: (opts: { apiKey: string; baseUrl?: string }) => void;
      };
      configure({
        apiKey: this.config.apiKey!,
        baseUrl: this.config.baseUrl,
      });
      this.configured = true;
    } catch {
      throw new ProviderError(
        '@scalix-world/sandbox package not installed. Run: npm install @scalix-world/sandbox',
      );
    }
  }

  async execute(
    code: string,
    options?: {
      runtime?: string;
      timeout?: number;
      gpu?: string;
    },
  ): Promise<SandboxResult> {
    await this.ensureConfigured();

    const runtime = options?.runtime ?? 'python';
    const timeout = options?.timeout ?? 30;
    const gpu = options?.gpu;

    // Validate runtime
    const sandboxRuntime = RUNTIME_MAP[runtime];
    if (!sandboxRuntime) {
      throw new SandboxError(
        `Unsupported runtime '${runtime}'. Supported: ${Object.keys(RUNTIME_MAP).join(', ')}`,
      );
    }

    const { Sandbox } = await dynamicImport('@scalix-world/sandbox') as unknown as {
      Sandbox: {
        create: (config: Record<string, unknown>) => Promise<SandboxInstance>;
      };
    };

    // Build creation config
    const createConfig: Record<string, unknown> = {
      runtime: sandboxRuntime,
      timeout: timeout * 1000,
    };

    if (gpu) {
      createConfig.gpu = { type: gpu, count: 1 };
    }

    const sandbox = await Sandbox.create(createConfig);

    try {
      const execCmd = RUNTIME_EXEC_CMD[runtime];
      let result: CommandResult;

      if (execCmd) {
        // Inline execution (python -c, node -e)
        const [cmd, flag] = execCmd;
        result = await sandbox.runCommand(cmd, [flag, code]);
      } else {
        // File-based execution (go, rust)
        const ext = EXT_MAP[runtime] ?? '.txt';
        const filePath = `/tmp/code${ext}`;

        await sandbox.writeFile(filePath, code);

        if (runtime === 'go' || runtime === 'go1.22') {
          result = await sandbox.runCommand('go', ['run', filePath]);
        } else if (runtime === 'rust' || runtime === 'rust-latest') {
          result = await sandbox.runCommand('sh', [
            '-c',
            `rustc ${filePath} -o /tmp/out && /tmp/out`,
          ]);
        } else {
          result = await sandbox.runCommand('cat', [filePath]);
        }
      }

      // Normalize output — the SDK may expose stdout/stderr as methods or properties
      const stdout =
        typeof result.stdout === 'function' ? result.stdout() : String(result.stdout ?? '');
      const stderr =
        typeof result.stderr === 'function' ? result.stderr() : String(result.stderr ?? '');
      const exitCode = result.exitCode ?? result.exit_code ?? 0;
      const durationMs = result.durationMs ?? result.duration_ms;

      return {
        stdout,
        stderr,
        exitCode,
        files: [],
        durationMs,
      };
    } finally {
      try {
        await sandbox.stop();
      } catch {
        // Best-effort cleanup
      }
    }
  }
}

/** Internal type for the @scalix-world/sandbox Sandbox instance. */
interface SandboxInstance {
  runCommand(
    cmd: string,
    args: string[],
    options?: Record<string, unknown>,
  ): Promise<CommandResult>;
  writeFile(path: string, content: string): Promise<void>;
  stop(): Promise<void>;
}

/** Internal type for command execution results. */
interface CommandResult {
  stdout: string | (() => string);
  stderr: string | (() => string);
  exitCode?: number;
  exit_code?: number;
  durationMs?: number;
  duration_ms?: number;
}
