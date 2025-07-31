# pycoreux

<div align="center">
  <img src="pycoreux.png" alt="pycoreux - Python Unix Core Utilities" />
</div>

[![Build Status](https://github.com/kumarmunish/pycoreux/workflows/CI/badge.svg)](https://github.com/kumarmunish/pycoreux/actions)
[![PyPI version](https://img.shields.io/pypi/v/pycoreux.svg)](https://pypi.org/project/pycoreux/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycoreux.svg)](https://pypi.org/project/pycoreux/)
[![Tests](https://img.shields.io/github/actions/workflow/status/kumarmunish/pycoreux/ci.yml?label=tests&logo=pytest)](https://github.com/kumarmunish/pycoreux/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
---

**A modern Python library that provides shell-like utilities for file operations, text processing, and subprocess management. Inspired by Unix coreutils, pycoreux offers a Pythonic API for building portable, scriptable command-line workflows with ease.**

## Features

- **File Operations**: Read, write, and manipulate files with ease
- **Text Processing**: Count lines/words, search patterns, head/tail operations
- **Process Management**: Execute subprocesses with simple APIs
- **String Utilities**: Pattern matching, text manipulation
- **Path Operations**: Directory listing, file system navigation
- **Archive Operations**: Create and extract tar/zip archives
- **Pipeline Support**: Chain operations together like shell pipes

## Installation

```bash
pip install pycoreux
```

## Quick Start: Unix Equivalents

If you're already familiar with shell scripting and the Unix toolset, here is a comprehensive guide to the equivalent pycoreux operation for each Unix command:

| Unix / shell | pycoreux equivalent |
|--------------|-------------------|
| `cat file.txt` | `FileOps.cat("file.txt")` |
| `head -n 10 file.txt` | `FileOps.head("file.txt", 10)` |
| `tail -n 10 file.txt` | `FileOps.tail("file.txt", 10)` |
| `wc file.txt` | `FileOps.wc("file.txt")` |
| `ls -la` | `FileOps.ls(".", show_hidden=True, long_format=True)` |
| `grep pattern file.txt` | `TextUtils.grep("pattern", "file.txt")` |
| `grep -i pattern file.txt` | `TextUtils.grep("pattern", "file.txt", ignore_case=True)` |
| `grep -n pattern file.txt` | `TextUtils.grep("pattern", "file.txt", line_numbers=True)` |
| `grep -v pattern file.txt` | `TextUtils.grep("pattern", "file.txt", invert=True)` |
| `sort file.txt` | `TextUtils.sort(lines)` |
| `sort -r file.txt` | `TextUtils.sort(lines, reverse=True)` |
| `sort -n file.txt` | `TextUtils.sort(lines, numeric=True)` |
| `uniq file.txt` | `TextUtils.uniq(lines)` |
| `uniq -c file.txt` | `TextUtils.uniq(lines, count=True)` |
| `nl file.txt` | `TextUtils.nl("file.txt")` |
| `echo "hello world"` | `TextUtils.echo("hello", "world")` |
| `cut -d',' -f1 file.txt` | `TextUtils.cut(line, delimiter=",", fields=1)` |
| `sed 's/old/new/g' file.txt` | `TextUtils.replace(text, "old", "new")` |
| `find . -name "*.txt"` | `PathUtils.find(".", name="*.txt")` |
| `find . -type f` | `PathUtils.find(".", type_filter="f")` |
| `which python` | `ProcessUtils.which("python")` |
| `ps aux` | `ProcessUtils.ps()` |
| `tar -czf archive.tar.gz files/` | `ArchiveUtils.tar_create("archive.tar.gz", ["files/"], "gz")` |
| `tar -xzf archive.tar.gz` | `ArchiveUtils.tar_extract("archive.tar.gz")` |
| `gzip file.txt` | `ArchiveUtils.gzip_file("file.txt")` |
| `gunzip file.txt.gz` | `ArchiveUtils.gunzip_file("file.txt.gz")` |

## Some Examples

Let's see some simple examples. Suppose you want to read the contents of a file as a string:

```python
from pycoreux import FileOps

content = FileOps.cat("test.txt")
```

That looks straightforward enough, but suppose you now want to count the lines in that file:

```python
lines, words, chars = FileOps.wc("test.txt")
print(f"File has {lines} lines")
```

For something a bit more challenging, let's try finding all lines in the file that contain "Error":

```python
from pycoreux import TextUtils

error_lines = TextUtils.grep("Error", "test.txt")
print(error_lines)
```

Want to get just the first 10 lines of a file?

```python
first_ten = FileOps.head("test.txt", 10)
print(first_ten)
```

Let's combine operations - read a file, find lines containing "Error", and get only the first 5 matches:

```python
# Read file and split into lines
content = FileOps.cat("test.txt")
lines = content.split('\n')

# Filter for error lines
error_lines = [line for line in lines if "Error" in line]

# Get first 5
first_five_errors = error_lines[:5]
print('\n'.join(first_five_errors))

# Or using grep directly for the same result
error_output = TextUtils.grep("Error", "test.txt")
error_lines = error_output.split('\n')
first_five = error_lines[:5]
print('\n'.join(first_five))
```

Want to sort some data? No problem:

```python
lines = ["zebra", "apple", "banana", "cherry"]
sorted_output = TextUtils.sort(lines)
print(sorted_output)
# Output:
# apple
# banana
# cherry
# zebra
```

Let's try something more complex - count unique occurrences:

```python
lines = ["apple", "apple", "banana", "apple", "cherry", "banana"]
unique_output = TextUtils.uniq(lines, count=True)
print(unique_output)
# Output:
#       2 apple
#       1 banana
#       1 apple
#       1 cherry
#       1 banana
```

Running external commands:

```python
from pycoreux import ProcessUtils

# Simple command execution
result = ProcessUtils.run("ls -la")
if result.success:
    print(result.stdout)

# Capture output directly
output = ProcessUtils.capture("date")
print(f"Current date: {output.strip()}")

# Find executable location
python_path = ProcessUtils.which("python3")
print(f"Python is at: {python_path}")
```

Working with archives:

```python
from pycoreux import ArchiveUtils

# Create a tar.gz archive
ArchiveUtils.tar_create("backup.tar.gz", ["important_files/"], compression="gz")

# Extract it later
extracted_files = ArchiveUtils.tar_extract("backup.tar.gz", "restore/")
print(f"Extracted: {extracted_files}")

# Compress a single file
compressed_file = ArchiveUtils.gzip_file("large_file.txt")
print(f"Compressed to: {compressed_file}")
```

## A Realistic Use Case

Let's use pycoreux to write a program that system administrators might actually need. Suppose we want to analyze web server logs to find the most frequent visitors. Given an Apache log file, we want to extract IP addresses and count their occurrences.

In a shell script, you might do:

```bash
cut -d' ' -f 1 access.log | sort | uniq -c | sort -rn | head -10
```

Here's the equivalent using pycoreux:

```python
from pycoreux import FileOps, TextUtils

# Direct pipeline style - each step mirrors the Unix command
def analyze_access_log(log_file):
    content = FileOps.cat(log_file)                                    # cat access.log
    ips = [TextUtils.cut(line, ' ', 1) for line in content.split('\n') if line.strip()]  # cut -d' ' -f 1
    sorted_ips = TextUtils.sort(ips)                                   # sort
    unique_counts = TextUtils.uniq(sorted_ips.split('\n'), count=True) # uniq -c
    reverse_sorted = TextUtils.sort(unique_counts.split('\n'), reverse=True, numeric=True)  # sort -rn
    return FileOps.head(content=reverse_sorted, lines=10)             # head -10

# Usage
print(analyze_access_log("access.log"))

# Or using the TextUtils.pipe function for functional composition:
from functools import partial

pipeline = TextUtils.pipe(
    FileOps.cat,
    lambda content: [TextUtils.cut(line, ' ', 1) for line in content.split('\n') if line.strip()],
    TextUtils.sort,
    lambda ips: TextUtils.uniq(ips.split('\n'), count=True),
    lambda counts: TextUtils.sort(counts.split('\n'), reverse=True, numeric=True),
    lambda sorted_counts: FileOps.head(content=sorted_counts, lines=10)
)
result = pipeline("access.log")
```

Output:

```text
      16 176.182.2.191
       7 212.205.21.11
       1 190.253.121.1
       1 90.53.111.17
```

## Pipeline-Style Operations

You can chain operations together for powerful data processing, mimicking Unix shell pipelines:

```python
from pycoreux import FileOps, TextUtils

# Example 1: Simple one-liner chaining
# Shell equivalent: cat app.log | grep "ERROR" | head -5
first_errors = FileOps.head(content=TextUtils.grep("ERROR", content=FileOps.cat("app.log")), lines=5)
print(first_errors)

# Example 2: Multi-step chaining (easier to read)
# Shell equivalent: cat app.log | grep "ERROR" | sort | head -3
content = FileOps.cat("app.log")                           # cat app.log
errors = TextUtils.grep("ERROR", content=content)          # | grep "ERROR"
sorted_errors = TextUtils.sort(errors.split('\n'))         # | sort
top_errors = FileOps.head(content=sorted_errors, lines=3)  # | head -3
print(top_errors)

# Example 3: Processing multiple files
# Shell equivalent: cat *.log | grep "WARN" | head -10
import glob
all_logs = '\n'.join([FileOps.cat(f) for f in glob.glob("*.log")])  # cat *.log
warnings = TextUtils.grep("WARN", content=all_logs)                 # | grep "WARN"
first_warnings = FileOps.head(content=warnings, lines=10)           # | head -10
print(first_warnings)
```

## CLI Usage

pycoreux also provides command-line tools:

```bash
# Using the CLI scripts
python -m pycoreux.scripts.pycoreux_cli cat myfile.txt
python -m pycoreux.scripts.pycoreux_cli head -n 5 myfile.txt
python -m pycoreux.scripts.pycoreux_cli grep "pattern" myfile.txt
python -m pycoreux.scripts.pycoreux_cli wc myfile.txt
```

## API Reference

### FileOps

- `cat(filepath)` - Read and return file contents
- `head(filepath=None, lines=10, content=None)` - Return first N lines as string (from file or content)
- `tail(filepath, lines=10)` - Return last N lines as string
- `ls(path=".", show_hidden=False, long_format=False)` - List directory contents
- `wc(filepath)` - Count lines, words, and characters
- `touch(filepath)` - Create empty file or update timestamp
- `mkdir(dirpath, parents=False)` - Create directory
- `rm(filepath, recursive=False)` - Remove files or directories

### TextUtils

- `echo(*args, sep=" ", end="\n")` - Join and return arguments as string
- `grep(pattern, filepath=None, content=None, ignore_case=False, line_numbers=False, invert=False)` - Search for patterns (in file or content)
- `nl(filepath, start=1, skip_empty=True)` - Add line numbers
- `sort(lines, reverse=False, numeric=False)` - Sort lines
- `uniq(lines, count=False)` - Remove duplicate consecutive lines
- `cut(line, delimiter="\t", fields=1)` - Extract fields from line
- `replace(text, pattern, replacement, count=0, ignore_case=False)` - Replace patterns in text
- `wc(text)` - Count words, lines, characters in text
- `pipe(*functions)` - Create a pipeline of functions for chaining operations

### ProcessUtils

- `run(command, shell=True, **kwargs)` - Execute command and return ProcessResult
- `capture(command, **kwargs)` - Execute command and return stdout
- `pipe(commands)` - Chain commands with pipes
- `which(program)` - Find program in PATH
- `kill(pid, signal=15)` - Send signal to process
- `ps()` - List running processes

### PathUtils

- `find(path=".", name=None, type_filter=None, max_depth=None)` - Find files and directories
- `which_all(program)` - Find all instances of program in PATH
- `du(path, human_readable=False)` - Calculate disk usage
- `chmod(path, mode)` - Change file permissions
- `stat_info(path)` - Get detailed file information
- `copy(src, dst, recursive=False)` - Copy files or directories
- `move(src, dst)` - Move/rename files or directories
- `symlink(target, link_name)` - Create symbolic link
- `readlink(path)` - Read symbolic link target

### ArchiveUtils

- `tar_create(archive_path, files, compression=None)` - Create tar archive
- `tar_extract(archive_path, extract_to=".")` - Extract tar archive
- `tar_list(archive_path)` - List tar archive contents
- `zip_create(archive_path, files, compression_level=6)` - Create zip archive
- `zip_extract(archive_path, extract_to=".")` - Extract zip archive
- `zip_list(archive_path)` - List zip archive contents
- `gzip_file(file_path, output_path=None)` - Compress file with gzip
- `gunzip_file(file_path, output_path=None)` - Decompress gzip file
- `compress_file(file_path, method="gz")` - Compress with specified method
- `decompress_file(file_path)` - Auto-detect and decompress file

## Development

```bash
# Clone the repository
git clone https://github.com/kumarmunish/pycoreux.git
cd pycoreux

# Install in development mode
pip install -e ".[dev]"

# Set up pre-commit hooks (optional)
pre-commit install

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy pycoreux

# Run all checks (like CI)
black --check .
isort --check-only .
flake8 pycoreux
mypy pycoreux
pytest
```

## Package Information

**pycoreux** is published on PyPI and can be installed using pip:

```bash
pip install pycoreux
```

### Package Details

- **Latest Version**: 0.1.1
- **License**: MIT
- **Python Support**: 3.8+
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Dependencies**: No external dependencies required for core functionality

### Development Status

- **Status**: Alpha
- **Intended Audience**: Developers, System Administrators, DevOps Engineers
- **Use Cases**: Shell scripting in Python, file processing, log analysis, automation

### Release History

- **v0.1.1** (2025-07-31): Refactored to renamed functions for consistency
- **v0.1.0** (2025-07-31): Initial release with core shell-like utilities

## License

MIT License – see [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
