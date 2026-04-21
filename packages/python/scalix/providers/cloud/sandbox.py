"""Scalix Sandbox provider — wraps the existing scalix-sandbox SDK.

Provides Firecracker microVM isolation and GPU compute.
This is a thin wrapper that delegates to the existing scalix-sandbox package.

The scalix-sandbox SDK is already async, so we delegate directly.
"""

from __future__ import annotations

import logging
from typing import Any

from scalix.config import ScalixConfig, get_config
from scalix.exceptions import AuthenticationError, ProviderError, SandboxError
from scalix.providers.base import SandboxProvider
from scalix.types import SandboxResult

logger = logging.getLogger("scalix.providers.cloud.sandbox")

# Map SDK runtime names to scalix-sandbox runtime identifiers
RUNTIME_MAP = {
    "python": "python3.12",
    "python3.12": "python3.12",
    "python3.13": "python3.13",
    "node": "node22",
    "node22": "node22",
    "node24": "node24",
    "go": "go1.22",
    "go1.22": "go1.22",
    "rust": "rust-latest",
    "rust-latest": "rust-latest",
}

# Map SDK runtime names to the command used to execute code
RUNTIME_EXEC_CMD = {
    "python": ("python3", "-c"),
    "python3.12": ("python3", "-c"),
    "python3.13": ("python3", "-c"),
    "node": ("node", "-e"),
    "node22": ("node", "-e"),
    "node24": ("node", "-e"),
    "go": None,  # File-based
    "go1.22": None,
    "rust": None,  # File-based
    "rust-latest": None,
}


class ScalixSandboxProvider(SandboxProvider):
    """Execute code in Scalix Sandbox — Firecracker microVMs with GPU support.

    Wraps the existing `scalix-sandbox` Python SDK.
    Requires a Scalix API key (cloud mode).

    Advantages over DockerSandbox:
    - Firecracker microVM isolation (production-grade security)
    - GPU access (T4, A100, H100)
    - Persistent snapshots
    - Resource monitoring and metrics
    - Auto-scaling
    """

    def __init__(self, config: ScalixConfig | None = None) -> None:
        self._config = config or get_config()
        if not self._config.is_cloud_mode:
            raise AuthenticationError(
                "Scalix Sandbox requires an API key. "
                "Call scalix.configure(api_key='...') first."
            )
        self._sandbox_configured = False

    def _ensure_configured(self) -> None:
        """Ensure the scalix-sandbox SDK is configured with our API key."""
        if self._sandbox_configured:
            return

        try:
            from scalix_sandbox import configure
        except ImportError:
            raise ProviderError(
                "scalix-sandbox package not installed. "
                "Run: pip install scalix[cloud]"
            )

        configure(
            api_key=self._config.api_key,
            base_url=self._config.base_url,
        )
        self._sandbox_configured = True

    async def execute(
        self,
        code: str,
        runtime: str = "python",
        timeout: int = 30,
        gpu: str | None = None,
    ) -> SandboxResult:
        """Execute code in a Scalix Sandbox Firecracker microVM.

        Creates an ephemeral sandbox, runs the code, captures output,
        and cleans up. For long-running workloads, use the scalix-sandbox
        SDK directly.

        Args:
            code: Source code to execute.
            runtime: Language runtime ("python", "node", "go", "rust").
            timeout: Max execution time in seconds.
            gpu: GPU type ("t4", "a100", "h100") or None for CPU-only.
        """
        self._ensure_configured()

        from scalix_sandbox import Sandbox

        # Map runtime to scalix-sandbox format
        sandbox_runtime = RUNTIME_MAP.get(runtime)
        if not sandbox_runtime:
            raise SandboxError(
                f"Unsupported runtime '{runtime}'. "
                f"Supported: {', '.join(RUNTIME_MAP.keys())}"
            )

        # Build GPU config if requested
        gpu_config = None
        if gpu:
            from scalix_sandbox.types import GpuConfig
            gpu_config = GpuConfig(type=gpu, count=1)

        # Create sandbox
        logger.debug(
            "Creating Scalix Sandbox: runtime=%s, gpu=%s, timeout=%ds",
            sandbox_runtime, gpu, timeout,
        )

        sandbox = await Sandbox.create(
            runtime=sandbox_runtime,
            timeout_ms=timeout * 1000,
            gpu=gpu_config,
        )

        try:
            # Determine how to execute the code
            exec_cmd = RUNTIME_EXEC_CMD.get(runtime)

            if exec_cmd:
                # Inline execution (python -c, node -e)
                cmd, flag = exec_cmd
                result = await sandbox.run_command(cmd, [flag, code])
            else:
                # File-based execution (go, rust)
                ext_map = {"go": ".go", "go1.22": ".go", "rust": ".rs", "rust-latest": ".rs"}
                ext = ext_map.get(runtime, ".txt")
                file_path = f"/tmp/code{ext}"

                await sandbox.write_file(file_path, code)

                if runtime in ("go", "go1.22"):
                    result = await sandbox.run_command("go", ["run", file_path])
                elif runtime in ("rust", "rust-latest"):
                    result = await sandbox.run_command(
                        "sh", ["-c", f"rustc {file_path} -o /tmp/out && /tmp/out"]
                    )
                else:
                    result = await sandbox.run_command("cat", [file_path])

            # Convert to our SandboxResult format
            stdout = result.stdout() if callable(getattr(result, "stdout", None)) else str(getattr(result, "stdout", ""))
            stderr = result.stderr() if callable(getattr(result, "stderr", None)) else str(getattr(result, "stderr", ""))
            exit_code = getattr(result, "exit_code", 0)
            duration_ms = getattr(result, "duration_ms", None)

            return SandboxResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                duration_ms=duration_ms,
            )

        finally:
            # Always clean up the sandbox
            try:
                await sandbox.stop()
            except Exception as e:
                logger.warning("Failed to stop sandbox: %s", e)
