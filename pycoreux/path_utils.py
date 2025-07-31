"""
Path and filesystem utilities for working with files and directories.
"""

import fnmatch
import os
import shutil
import stat
from pathlib import Path
from typing import Optional, Union


class PathUtils:
    """Utilities for path and filesystem operations."""

    @staticmethod
    def find(
        path: Union[str, Path] = ".",
        name: Optional[str] = None,
        type_filter: Optional[str] = None,
        max_depth: Optional[int] = None,
    ) -> str:
        """
        Find files and directories (like find command).

        Args:
            path: Starting directory for search
            name: Filename pattern to match (supports wildcards)
            type_filter: File type filter ('f' for files, 'd' for directories)
            max_depth: Maximum search depth

        Returns:
            String containing matching paths (one per line)
        """
        finder = PathUtils._FileFinder(name, type_filter, max_depth)
        return finder.search(Path(path))

    class _FileFinder:
        """Helper class to handle file finding logic."""

        def __init__(
            self,
            name: Optional[str],
            type_filter: Optional[str],
            max_depth: Optional[int],
        ):
            self.name = name
            self.type_filter = type_filter
            self.max_depth = max_depth
            self.results = []

        def search(self, start_path: Path) -> str:
            """Search for files and return results."""
            self._search_recursive(start_path, 0)
            return "\n".join(sorted(self.results))

        def _search_recursive(self, current_path: Path, depth: int):
            """Recursively search directories."""
            if self.max_depth is not None and depth > self.max_depth:
                return

            try:
                for item in current_path.iterdir():
                    if self._item_matches(item):
                        self.results.append(str(item))

                    if item.is_dir():
                        self._search_recursive(item, depth + 1)

            except PermissionError:
                pass  # Skip directories we can't read

        def _item_matches(self, item: Path) -> bool:
            """Check if an item matches all filters."""
            return self._matches_type_filter(item) and self._matches_name_pattern(item)

        def _matches_type_filter(self, item: Path) -> bool:
            """Check if item matches the type filter."""
            if self.type_filter == "f":
                return item.is_file()
            elif self.type_filter == "d":
                return item.is_dir()
            return True

        def _matches_name_pattern(self, item: Path) -> bool:
            """Check if item matches the name pattern."""
            return self.name is None or fnmatch.fnmatch(item.name, self.name)

    @staticmethod
    def which_all(program: str) -> str:
        """
        Find all instances of a program in PATH.

        Args:
            program: Program name to find

        Returns:
            String containing full paths to the program (one per line)
        """
        paths = []
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            if not path_dir:
                continue

            program_path = Path(path_dir) / program
            if program_path.is_file() and os.access(program_path, os.X_OK):
                paths.append(str(program_path))

        return "\n".join(paths)

    @staticmethod
    def du(path: Union[str, Path], human_readable: bool = False) -> dict:
        """
        Calculate disk usage (like du command).

        Args:
            path: Path to analyze
            human_readable: Format sizes in human readable format

        Returns:
            Dictionary with size information
        """
        path_obj = Path(path)
        total_size = 0
        file_count = 0
        dir_count = 0

        if path_obj.is_file():
            total_size = path_obj.stat().st_size
            file_count = 1
        elif path_obj.is_dir():
            for item in path_obj.rglob("*"):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                        file_count += 1
                    except (OSError, FileNotFoundError):
                        pass
                elif item.is_dir():
                    dir_count += 1

        result = {
            "total_bytes": total_size,
            "files": file_count,
            "directories": dir_count,
        }

        if human_readable:
            result["human_readable"] = PathUtils._format_size(total_size)

        return result

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format byte size in human readable format."""
        for unit in ["B", "K", "M", "G", "T"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}P"

    @staticmethod
    def chmod(path: Union[str, Path], mode: Union[str, int]) -> None:
        """
        Change file permissions (like chmod command).

        Args:
            path: Path to file/directory
            mode: Permission mode (octal integer or string like '755')
        """
        if isinstance(mode, str):
            mode = int(mode, 8)  # Convert octal string to int

        os.chmod(path, mode)

    @staticmethod
    def stat_info(path: Union[str, Path]) -> dict:
        """
        Get detailed file information (like stat command).

        Args:
            path: Path to examine

        Returns:
            Dictionary with file statistics
        """
        path_stat = Path(path).stat()

        return {
            "size": path_stat.st_size,
            "mode": oct(path_stat.st_mode),
            "uid": path_stat.st_uid,
            "gid": path_stat.st_gid,
            "atime": path_stat.st_atime,
            "mtime": path_stat.st_mtime,
            "ctime": path_stat.st_ctime,
            "is_file": stat.S_ISREG(path_stat.st_mode),
            "is_dir": stat.S_ISDIR(path_stat.st_mode),
            "is_link": stat.S_ISLNK(path_stat.st_mode),
        }

    @staticmethod
    def copy(
        src: Union[str, Path], dst: Union[str, Path], recursive: bool = False
    ) -> None:
        """
        Copy files or directories (like cp command).

        Args:
            src: Source path
            dst: Destination path
            recursive: Copy directories recursively
        """
        src_path = Path(src)
        dst_path = Path(dst)

        if src_path.is_file():
            shutil.copy2(src_path, dst_path)
        elif src_path.is_dir() and recursive:
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        elif src_path.is_dir():
            raise IsADirectoryError(
                f"'{src}' is a directory. Use recursive=True to copy it."
            )

    @staticmethod
    def move(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        Move/rename files or directories (like mv command).

        Args:
            src: Source path
            dst: Destination path
        """
        shutil.move(str(src), str(dst))

    @staticmethod
    def symlink(target: Union[str, Path], link_name: Union[str, Path]) -> None:
        """
        Create symbolic link (like ln -s command).

        Args:
            target: Target path to link to
            link_name: Name of the symbolic link to create
        """
        Path(link_name).symlink_to(target)

    @staticmethod
    def readlink(path: Union[str, Path]) -> str:
        """
        Read symbolic link target (like readlink command).

        Args:
            path: Path to symbolic link

        Returns:
            Target path of the symbolic link
        """
        import os

        return str(os.readlink(path))
