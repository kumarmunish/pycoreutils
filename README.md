# Pycoreutils

A modern Python library that provides shell-like utilities for file operations, text processing, and subprocess management. Inspired by Unix coreutils, this library offers a Pythonic API for common shell scripting tasks.

## Features

- **File Operations**: Read, write, and manipulate files with ease
- **Text Processing**: Count lines/words, search patterns, head/tail operations
- **Process Management**: Execute subprocesses with simple APIs
- **String Utilities**: Pattern matching, text manipulation
- **Path Operations**: Directory listing, file system navigation
- **Pipeline Support**: Chain operations together like shell pipes

## Installation

```bash
pip install pycoreutils
```

## Quick Start

```python
from pycoreutils import FileOps, TextUtils, ProcessUtils

# Read and process files
content = FileOps.cat("myfile.txt")
lines = FileOps.head("myfile.txt", lines=10)
word_count = TextUtils.wc("myfile.txt")

# Execute commands
result = ProcessUtils.run("ls -la")
output = ProcessUtils.pipe(["cat myfile.txt", "grep pattern", "wc -l"])

# Text processing
matches = TextUtils.grep("pattern", "myfile.txt")
numbered_lines = TextUtils.nl("myfile.txt")
```

## API Reference

### FileOps
- `cat(filepath)` - Read and return file contents
- `head(filepath, lines=10)` - Return first N lines
- `tail(filepath, lines=10)` - Return last N lines
- `ls(path=".", show_hidden=False)` - List directory contents
- `wc(filepath)` - Count lines, words, and characters

### TextUtils
- `grep(pattern, filepath, flags=0)` - Search for patterns
- `nl(filepath, start=1)` - Add line numbers
- `echo(*args)` - Print arguments
- `sort(lines, reverse=False)` - Sort lines

### ProcessUtils
- `run(command, shell=True)` - Execute command
- `pipe(commands)` - Chain commands
- `capture(command)` - Capture output

## Development

```bash
# Clone the repository
git clone https://github.com/kumarmunish/pycoreutils.git
cd pycoreutils

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .
```

## License

MIT License – see [LICENSE](./LICENSE) file for details.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.