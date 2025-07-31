"""
File operations module providing shell-like file utilities.
"""

import os
from pathlib import Path
from typing import Tuple, Union


class FileOps:
    """File operations utilities similar to Unix coreutils."""

    @staticmethod
    def cat(filepath: Union[str, Path]) -> str:
        """
        Read and return the contents of a file (like cat command).

        Args:
            filepath: Path to the file to read

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file doesn't exist
            IsADirectoryError: If path is a directory
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found")
        except IsADirectoryError:
            raise IsADirectoryError(f"'{filepath}' is a directory, not a file")

    @staticmethod
    def head(filepath: Union[str, Path], lines: int = 10) -> str:
        """
        Return the first N lines of a file (like head command).

        Args:
            filepath: Path to the file to read
            lines: Number of lines to return (default: 10)

        Returns:
            String containing the first N lines
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                result = []
                for i, line in enumerate(file):
                    if i >= lines:
                        break
                    result.append(line.rstrip("\n"))
                return "\n".join(result)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found")

    @staticmethod
    def tail(filepath: Union[str, Path], lines: int = 10) -> str:
        """
        Return the last N lines of a file (like tail command).

        Args:
            filepath: Path to the file to read
            lines: Number of lines to return (default: 10)

        Returns:
            String containing the last N lines
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                all_lines = file.readlines()
                last_lines = [line.rstrip("\n") for line in all_lines[-lines:]]
                return "\n".join(last_lines)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found")

    @staticmethod
    def ls(
        path: Union[str, Path] = ".",
        show_hidden: bool = False,
        long_format: bool = False,
    ) -> str:
        """
        List directory contents (like ls command).

        Args:
            path: Directory path to list (default: current directory)
            show_hidden: Whether to show hidden files (default: False)
            long_format: Whether to show detailed info (default: False)

        Returns:
            String containing directory contents (one per line)
        """
        try:
            items = os.listdir(path)
            if not show_hidden:
                items = [item for item in items if not item.startswith(".")]

            if long_format:
                result = []
                for item in sorted(items):
                    item_path = Path(path) / item
                    stat = item_path.stat()
                    is_dir = item_path.is_dir()
                    size = stat.st_size
                    result.append(f"{'d' if is_dir else '-'} {size:>8} {item}")
                return "\n".join(result)
            else:
                return "\n".join(sorted(items))
        except FileNotFoundError:
            raise FileNotFoundError(f"Directory '{path}' not found")

    @staticmethod
    def wc(filepath: Union[str, Path]) -> Tuple[int, int, int]:
        """
        Count lines, words, and characters in a file (like wc command).

        Args:
            filepath: Path to the file to analyze

        Returns:
            Tuple of (lines, words, characters)
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                # Count lines properly like Unix wc
                lines = content.count("\n")
                if content and not content.endswith("\n"):
                    lines += 1
                words = len(content.split())
                chars = len(content)
                return (lines, words, chars)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found")

    @staticmethod
    def touch(filepath: Union[str, Path]) -> None:
        """
        Create an empty file or update timestamp (like touch command).

        Args:
            filepath: Path to the file to create/touch
        """
        Path(filepath).touch()

    @staticmethod
    def mkdir(dirpath: Union[str, Path], parents: bool = False) -> None:
        """
        Create a directory (like mkdir command).

        Args:
            dirpath: Path to the directory to create
            parents: Whether to create parent directories (like mkdir -p)
        """
        Path(dirpath).mkdir(parents=parents, exist_ok=True)

    @staticmethod
    def rm(filepath: Union[str, Path], recursive: bool = False) -> None:
        """
        Remove files or directories (like rm command).

        Args:
            filepath: Path to remove
            recursive: Whether to remove directories recursively
        """
        path = Path(filepath)
        if path.is_file():
            path.unlink()
        elif path.is_dir() and recursive:
            import shutil

            shutil.rmtree(path)
        elif path.is_dir():
            raise IsADirectoryError(
                f"'{filepath}' is a directory. Use recursive=True to remove it."
            )
        else:
            raise FileNotFoundError(f"'{filepath}' not found")
