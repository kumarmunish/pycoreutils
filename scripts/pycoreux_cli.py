#!/usr/bin/env python3
"""
Command-line interface for pycoreux.
Provides CLI wrappers for the library functions.
"""

import argparse
import sys
from pathlib import Path

# Add the parent directory to sys.path to import pycoreux
sys.path.insert(0, str(Path(__file__).parent.parent))

from pycoreux import FileOps, ProcessUtils, TextUtils


def cmd_cat():
    """Cat command implementation."""
    parser = argparse.ArgumentParser(description="Display file contents")
    parser.add_argument("files", nargs="+", help="Files to display")
    args = parser.parse_args(sys.argv[2:])

    for filepath in args.files:
        try:
            content = FileOps.cat(filepath)
            print(content, end="")
        except Exception as e:
            print(f"cat: {e}", file=sys.stderr)
            sys.exit(1)


def cmd_head():
    """Head command implementation."""
    parser = argparse.ArgumentParser(description="Display first lines of file")
    parser.add_argument(
        "-n", "--lines", type=int, default=10, help="Number of lines to show"
    )
    parser.add_argument("file", help="File to read")
    args = parser.parse_args(sys.argv[2:])

    try:
        output = FileOps.head(args.file, args.lines)
        print(output)
    except Exception as e:
        print(f"head: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_tail():
    """Tail command implementation."""
    parser = argparse.ArgumentParser(description="Display last lines of file")
    parser.add_argument(
        "-n", "--lines", type=int, default=10, help="Number of lines to show"
    )
    parser.add_argument("file", help="File to read")
    args = parser.parse_args(sys.argv[2:])

    try:
        output = FileOps.tail(args.file, args.lines)
        print(output)
    except Exception as e:
        print(f"tail: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_wc():
    """Word count command implementation."""
    parser = argparse.ArgumentParser(description="Count lines, words, and characters")
    parser.add_argument(
        "-l", "--lines", action="store_true", help="Show only line count"
    )
    parser.add_argument(
        "-w", "--words", action="store_true", help="Show only word count"
    )
    parser.add_argument(
        "-c", "--chars", action="store_true", help="Show only character count"
    )
    parser.add_argument("files", nargs="+", help="Files to count")
    args = parser.parse_args(sys.argv[2:])

    for filepath in args.files:
        try:
            lines, words, chars = FileOps.wc(filepath)

            output = []
            if args.lines or not (args.words or args.chars):
                output.append(str(lines))
            if args.words or not (args.lines or args.chars):
                output.append(str(words))
            if args.chars or not (args.lines or args.words):
                output.append(str(chars))

            if not (args.lines or args.words or args.chars):
                print(f"{lines:>8} {words:>8} {chars:>8} {filepath}")
            else:
                print(f"{' '.join(output)} {filepath}")

        except Exception as e:
            print(f"wc: {e}", file=sys.stderr)
            sys.exit(1)


def cmd_ls():
    """List directory command implementation."""
    parser = argparse.ArgumentParser(description="List directory contents")
    parser.add_argument("-a", "--all", action="store_true", help="Show hidden files")
    parser.add_argument(
        "-l", "--long", action="store_true", help="Use long listing format"
    )
    parser.add_argument("paths", nargs="*", default=["."], help="Directories to list")
    args = parser.parse_args(sys.argv[2:])

    for path in args.paths:
        try:
            output = FileOps.ls(path, show_hidden=args.all, long_format=args.long)
            print(output)
        except Exception as e:
            print(f"ls: {e}", file=sys.stderr)
            sys.exit(1)


def cmd_echo():
    """Echo command implementation."""
    parser = argparse.ArgumentParser(description="Display line of text")
    parser.add_argument(
        "-n", action="store_true", help="Do not output trailing newline"
    )
    parser.add_argument("text", nargs="*", help="Text to display")
    args = parser.parse_args(sys.argv[2:])

    end_char = "" if args.n else "\n"
    result = TextUtils.echo(*args.text, end=end_char)
    print(result, end="")


def cmd_grep():
    """Grep command implementation."""
    parser = argparse.ArgumentParser(description="Search for patterns in files")
    parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Ignore case distinctions"
    )
    parser.add_argument(
        "-n", "--line-number", action="store_true", help="Show line numbers"
    )
    parser.add_argument(
        "-v",
        "--invert-match",
        action="store_true",
        help="Invert match (show non-matching lines)",
    )
    parser.add_argument("pattern", help="Pattern to search for")
    parser.add_argument("files", nargs="+", help="Files to search in")
    args = parser.parse_args(sys.argv[2:])

    for filepath in args.files:
        try:
            output = TextUtils.grep(
                args.pattern,
                filepath,
                ignore_case=args.ignore_case,
                line_numbers=args.line_number,
                invert=args.invert_match,
            )
            if output:  # Only print if there are matches
                if len(args.files) > 1:
                    for line in output.split("\n"):
                        print(f"{filepath}:{line}")
                else:
                    print(output)
        except Exception as e:
            print(f"grep: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: pycoreux <command> [args...]")
        print("Commands: cat, head, tail, wc, ls, echo, grep")
        sys.exit(1)

    command = sys.argv[1]

    commands = {
        "cat": cmd_cat,
        "head": cmd_head,
        "tail": cmd_tail,
        "wc": cmd_wc,
        "ls": cmd_ls,
        "echo": cmd_echo,
        "grep": cmd_grep,
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        print("Available commands:", ", ".join(commands.keys()))
        sys.exit(1)

    commands[command]()


if __name__ == "__main__":
    main()
