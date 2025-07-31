"""
Pycoreutils - A Python library for shell-like utilities.

This package provides Pythonic interfaces to common shell operations
like file processing, text manipulation, and subprocess management.
"""

from .archive_utils import ArchiveUtils
from .file_ops import FileOps
from .path_utils import PathUtils
from .process_utils import ProcessUtils
from .text_utils import TextUtils

__version__ = "0.1.0"
__author__ = "Munish Kumar"
__email__ = "your-email@example.com"

__all__ = [
    "FileOps",
    "TextUtils",
    "ProcessUtils",
    "PathUtils",
    "ArchiveUtils",
]
