"""Docker-based sandbox — local code execution using Docker containers.

Used in local mode as a free alternative to Scalix Sandbox.
No Firecracker isolation, no GPU — but good enough for development.

Falls back to subprocess execution if Docker is not available.
"""

from __future__ import annotations

import asyncio
import logging
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any

from scalix.providers.base import SandboxProvider
from scalix.types import SandboxResult

logger = logging.getLogger("scalix.providers.docker_sandbox")


class DockerSandbox(SandboxProvider):
    """Execute code in Docker containers on the developer's machine.

    Cost to Scalix: $0 (runs entirely on developer's hardware).

    Falls back to subprocess execution if Docker is unavailable,
    with a warning that code runs without container isolation.
    """

    RUNTIME_IMAGES = {
        "python": "python:3.12-slim",
        "node": "node:22-slim",
        "go": "golang:1.23-alpine",
        "rust": "rust:1.83-slim",
    }

    RUNTIME_COMMANDS = {
        "python": ["python", "-c"],
        "node": ["node", "-e"],
        "go": None,  # Requires file-based execution
        "rust": None,  # Requires file-based execution
    }

    RUNTIME_FILE_EXT = {
        "python": ".py",
        "node": ".js",
        "go": ".go",
        "rust": ".rs",
    }

    def __init__(self, timeout: int = 30, use_docker: bool | None = None) -> None:
        self.timeout = timeout
        self._use_docker = use_docker
        self._docker_available: bool | None = None

    async def _check_docker(self) -> bool:
        """Check if Docker daemon is available."""
        if self._docker_available is not None:
            return bool(self._docker_available)

        if self._use_docker is False:
            self._docker_available = False
            return False

        available = False
        try:
            proc = await asyncio.create_subprocess_exec(
                "docker", "info",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await asyncio.wait_for(proc.wait(), timeout=5.0)
            available = proc.returncode == 0
        except (FileNotFoundError, asyncio.TimeoutError):
            available = False

        self._docker_available = available

        if not available:
            logger.warning(
                "Docker not available — falling back to subprocess execution. "
                "Code will run without container isolation."
            )

        return available

    async def execute(
        self,
        code: str,
        runtime: str = "python",
        timeout: int | None = None,
        gpu: str | None = None,
    ) -> SandboxResult:
        """Execute code in a Docker container or subprocess fallback.

        Args:
            code: Source code to execute.
            runtime: Language runtime ("python", "node", "go", "rust").
            timeout: Max execution time in seconds.
            gpu: Ignored in local mode (GPU requires Scalix Sandbox).
        """
        if gpu:
            from scalix.exceptions import SandboxResourceError

            raise SandboxResourceError(
                f"GPU '{gpu}' is not available in local mode. "
                "Configure scalix.configure(api_key='...') to use Scalix Sandbox with GPU support."
            )

        if runtime not in self.RUNTIME_IMAGES:
            from scalix.exceptions import SandboxError

            raise SandboxError(
                f"Unsupported runtime '{runtime}'. "
                f"Supported: {', '.join(self.RUNTIME_IMAGES.keys())}"
            )

        effective_timeout = timeout or self.timeout
        docker_available = await self._check_docker()

        if docker_available:
            return await self._execute_docker(code, runtime, effective_timeout)
        else:
            return await self._execute_subprocess(code, runtime, effective_timeout)

    async def _execute_docker(
        self, code: str, runtime: str, timeout: int
    ) -> SandboxResult:
        """Execute code inside a Docker container."""
        image = self.RUNTIME_IMAGES[runtime]
        start_time = time.monotonic()

        # Create a temp file with the code
        ext = self.RUNTIME_FILE_EXT[runtime]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=ext, delete=False, prefix="scalix_"
        ) as f:
            f.write(code)
            code_path = f.name

        try:
            # Build Docker run command
            container_code_path = f"/tmp/code{ext}"
            run_cmd = self._get_docker_run_command(runtime, container_code_path)

            cmd = [
                "docker", "run",
                "--rm",
                "--network=none",  # No network access for security
                "--memory=512m",  # Memory limit
                "--cpus=1",  # CPU limit
                "-v", f"{code_path}:{container_code_path}:ro",
                image,
            ] + run_cmd

            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    proc.communicate(), timeout=timeout
                )
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                duration = (time.monotonic() - start_time) * 1000
                return SandboxResult(
                    stdout="",
                    stderr=f"Execution timed out after {timeout}s",
                    exit_code=124,
                    duration_ms=duration,
                )

            duration = (time.monotonic() - start_time) * 1000
            return SandboxResult(
                stdout=stdout_bytes.decode("utf-8", errors="replace"),
                stderr=stderr_bytes.decode("utf-8", errors="replace"),
                exit_code=proc.returncode or 0,
                duration_ms=duration,
            )
        finally:
            Path(code_path).unlink(missing_ok=True)

    async def _execute_subprocess(
        self, code: str, runtime: str, timeout: int
    ) -> SandboxResult:
        """Execute code via subprocess (fallback when Docker unavailable)."""
        start_time = time.monotonic()

        # For inline-capable runtimes (python, node), use -c/-e flag
        inline_cmd = self.RUNTIME_COMMANDS.get(runtime)
        code_path: str | None = None

        if inline_cmd:
            binary = inline_cmd[0]
            if not shutil.which(binary):
                from scalix.exceptions import SandboxError

                raise SandboxError(
                    f"Runtime '{runtime}' not found. "
                    f"Install '{binary}' or use Docker for sandboxed execution."
                )

            cmd = inline_cmd + [code]
        else:
            # File-based execution for go/rust
            ext = self.RUNTIME_FILE_EXT[runtime]
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=ext, delete=False, prefix="scalix_"
            ) as f:
                f.write(code)
                code_path = f.name

            cmd = self._get_subprocess_command(runtime, code_path)
            binary = cmd[0]
            if not shutil.which(binary):
                Path(code_path).unlink(missing_ok=True)
                from scalix.exceptions import SandboxError

                raise SandboxError(
                    f"Runtime '{runtime}' not found. "
                    f"Install '{binary}' or use Docker for sandboxed execution."
                )

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    proc.communicate(), timeout=timeout
                )
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                duration = (time.monotonic() - start_time) * 1000
                return SandboxResult(
                    stdout="",
                    stderr=f"Execution timed out after {timeout}s",
                    exit_code=124,
                    duration_ms=duration,
                )

            duration = (time.monotonic() - start_time) * 1000
            return SandboxResult(
                stdout=stdout_bytes.decode("utf-8", errors="replace"),
                stderr=stderr_bytes.decode("utf-8", errors="replace"),
                exit_code=proc.returncode or 0,
                duration_ms=duration,
            )
        finally:
            if code_path:
                Path(code_path).unlink(missing_ok=True)

    def _get_docker_run_command(self, runtime: str, code_path: str) -> list[str]:
        """Get the command to execute code inside a Docker container."""
        if runtime == "python":
            return ["python", code_path]
        elif runtime == "node":
            return ["node", code_path]
        elif runtime == "go":
            return ["go", "run", code_path]
        elif runtime == "rust":
            return ["sh", "-c", f"rustc {code_path} -o /tmp/out && /tmp/out"]
        return ["sh", "-c", f"cat {code_path}"]

    def _get_subprocess_command(self, runtime: str, code_path: str) -> list[str]:
        """Get the subprocess command for file-based runtimes."""
        if runtime == "go":
            return ["go", "run", code_path]
        elif runtime == "rust":
            return ["sh", "-c", f"rustc {code_path} -o /tmp/scalix_out && /tmp/scalix_out"]
        return ["cat", code_path]
