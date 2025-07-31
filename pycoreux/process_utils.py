"""
Process and subprocess utilities for executing commands and managing processes.
"""

import shlex
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class ProcessResult:
    """Result of a process execution."""

    stdout: str
    stderr: str
    returncode: int
    command: str

    @property
    def success(self) -> bool:
        """Whether the process completed successfully."""
        return self.returncode == 0

    def __str__(self) -> str:
        return self.stdout


class ProcessUtils:
    """Utilities for executing processes and managing subprocesses."""

    @staticmethod
    def run(
        command: Union[str, List[str]],
        shell: bool = True,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        capture_output: bool = True,
    ) -> ProcessResult:
        """
        Execute a command and return the result.

        Args:
            command: Command to execute (string or list)
            shell: Whether to use shell (default: True)
            cwd: Working directory for command
            env: Environment variables
            timeout: Timeout in seconds
            capture_output: Whether to capture stdout/stderr

        Returns:
            ProcessResult object with execution details
        """
        if isinstance(command, str) and not shell:
            command = shlex.split(command)

        try:
            result = subprocess.run(
                command,
                shell=shell,
                cwd=cwd,
                env=env,
                timeout=timeout,
                capture_output=capture_output,
                text=True,
            )

            return ProcessResult(
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                returncode=result.returncode,
                command=str(command),
            )

        except subprocess.TimeoutExpired as e:
            return ProcessResult(
                stdout=e.stdout or "",
                stderr=f"Command timed out after {timeout} seconds",
                returncode=-1,
                command=str(command),
            )
        except Exception as e:
            return ProcessResult(
                stdout="", stderr=str(e), returncode=-1, command=str(command)
            )

    @staticmethod
    def pipe(commands: List[str], shell: bool = True) -> ProcessResult:
        """
        Chain commands together with pipes (like shell | operator).

        Args:
            commands: List of commands to chain
            shell: Whether to use shell

        Returns:
            ProcessResult of the final command
        """
        if not commands:
            raise ValueError("At least one command is required")

        if len(commands) == 1:
            return ProcessUtils.run(commands[0], shell=shell)

        processes = []

        try:
            processes = ProcessUtils._create_pipeline(commands, shell)
            return ProcessUtils._execute_pipeline(processes, commands)

        except Exception as e:
            ProcessUtils._cleanup_processes(processes)
            return ProcessResult(
                stdout="", stderr=str(e), returncode=-1, command=" | ".join(commands)
            )

    @staticmethod
    def _create_pipeline(commands: List[str], shell: bool) -> List:
        """Create a pipeline of processes."""
        processes = []

        # Start the first process
        first_proc = ProcessUtils._start_first_process(commands[0], shell)
        processes.append(first_proc)

        # Chain the middle processes
        for cmd in commands[1:-1]:
            proc = ProcessUtils._start_middle_process(cmd, shell, processes[-1])
            processes.append(proc)

        # Start the final process
        if len(commands) > 1:
            last_proc = ProcessUtils._start_last_process(
                commands[-1], shell, processes[-1]
            )
            processes.append(last_proc)

        return processes

    @staticmethod
    def _start_first_process(cmd: str, shell: bool):
        """Start the first process in the pipeline."""
        if not shell:
            cmd = shlex.split(cmd)
        return subprocess.Popen(
            cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

    @staticmethod
    def _start_middle_process(cmd: str, shell: bool, prev_proc):
        """Start a middle process in the pipeline."""
        if not shell:
            cmd = shlex.split(cmd)
        proc = subprocess.Popen(
            cmd,
            shell=shell,
            stdin=prev_proc.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        prev_proc.stdout.close()
        return proc

    @staticmethod
    def _start_last_process(cmd: str, shell: bool, prev_proc):
        """Start the last process in the pipeline."""
        if not shell:
            cmd = shlex.split(cmd)
        proc = subprocess.Popen(
            cmd,
            shell=shell,
            stdin=prev_proc.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        prev_proc.stdout.close()
        return proc

    @staticmethod
    def _execute_pipeline(processes: List, commands: List[str]) -> ProcessResult:
        """Execute the pipeline and return results."""
        # Wait for the final process and get output
        last_proc = processes[-1]
        stdout, stderr = last_proc.communicate()

        # Wait for all processes to complete
        for proc in processes:
            proc.wait()

        return ProcessResult(
            stdout=stdout,
            stderr=stderr,
            returncode=last_proc.returncode,
            command=" | ".join(commands),
        )

    @staticmethod
    def _cleanup_processes(processes: List):
        """Clean up any running processes."""
        for proc in processes:
            try:
                proc.terminate()
            except Exception:
                pass

    @staticmethod
    def capture(command: Union[str, List[str]], **kwargs) -> str:
        """
        Execute command and return just the stdout.

        Args:
            command: Command to execute
            **kwargs: Additional arguments for run()

        Returns:
            Command output as string
        """
        result = ProcessUtils.run(command, **kwargs)
        return result.stdout

    @staticmethod
    def which(program: str) -> Optional[str]:
        """
        Find the full path of a program (like which command).

        Args:
            program: Program name to find

        Returns:
            Full path to program or None if not found
        """
        import shutil

        return shutil.which(program)

    @staticmethod
    def kill(pid: int, signal: int = 15) -> bool:
        """
        Send signal to process (like kill command).

        Args:
            pid: Process ID
            signal: Signal number (default: 15 = SIGTERM)

        Returns:
            True if signal was sent successfully
        """
        try:
            import os

            os.kill(pid, signal)
            return True
        except (OSError, ProcessLookupError):
            return False

    @staticmethod
    def ps() -> List[Dict[str, Any]]:
        """
        List running processes (simplified ps command).

        Returns:
            List of process information dictionaries
        """
        try:
            # Optional dependency - provides enhanced process information
            import psutil  # type: ignore

            processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent"]
            ):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return processes
        except ImportError:
            # Fallback using subprocess if psutil not available
            result = ProcessUtils.run("ps aux", shell=True)
            if result.success:
                lines = result.stdout.strip().split("\n")[1:]  # Skip header
                processes = []
                for line in lines:
                    parts = line.split(None, 10)
                    if len(parts) >= 11:
                        processes.append(
                            {
                                "pid": int(parts[1]),
                                "name": parts[10],
                                "cpu_percent": float(parts[2]),
                                "memory_percent": float(parts[3]),
                            }
                        )
                return processes
            return []
