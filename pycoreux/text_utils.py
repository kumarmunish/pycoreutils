"""
Text processing utilities for string manipulation and pattern matching.
"""

import re
from pathlib import Path
from typing import List, Union


class TextUtils:
    """Text processing utilities similar to Unix text tools."""

    @staticmethod
    def echo(*args: str, sep: str = " ", end: str = "\n") -> str:
        """
        Join and return arguments as string (like echo command).

        Args:
            *args: Arguments to join
            sep: Separator between arguments (default: space)
            end: End character (default: newline)

        Returns:
            Joined string
        """
        return sep.join(str(arg) for arg in args) + end

    @staticmethod
    def grep(
        pattern: str,
        filepath: Union[str, Path] = None,
        content: str = None,
        ignore_case: bool = False,
        line_numbers: bool = False,
        invert: bool = False,
    ) -> str:
        """
        Search for pattern in file or content (like grep command).

        Args:
            pattern: Regular expression pattern to search
            filepath: Path to file to search in (mutually exclusive with content)
            content: String content to search in (mutually exclusive with filepath)
            ignore_case: Case-insensitive search (default: False)
            line_numbers: Include line numbers in output (default: False)
            invert: Return non-matching lines (default: False)

        Returns:
            String containing matching lines (one per line)
        """
        if filepath is None and content is None:
            raise ValueError("Either filepath or content must be provided")
        if filepath is not None and content is not None:
            raise ValueError("filepath and content are mutually exclusive")

        flags = re.IGNORECASE if ignore_case else 0
        compiled_pattern = re.compile(pattern, flags)

        # Get lines from either file or content
        if filepath is not None:
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    lines = [line.rstrip("\n") for line in file]
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{filepath}' not found")
        else:
            lines = content.split("\n")

        results = []
        for line_num, line in enumerate(lines, 1):
            matches = bool(compiled_pattern.search(line))

            if matches != invert:  # XOR logic for invert
                if line_numbers:
                    results.append(f"{line_num}: {line}")
                else:
                    results.append(line)

        return "\n".join(results)

    @staticmethod
    def nl(filepath: Union[str, Path], start: int = 1, skip_empty: bool = True) -> str:
        """
        Add line numbers to file content (like nl command).

        Args:
            filepath: Path to file to number
            start: Starting line number (default: 1)
            skip_empty: Skip empty lines for numbering (default: True)

        Returns:
            String containing numbered lines
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                results = []
                line_num = start

                for line in file:
                    line = line.rstrip("\n")

                    if skip_empty and not line.strip():
                        results.append(line)
                    else:
                        results.append(f"\t{line_num} {line}")
                        line_num += 1

                return "\n".join(results)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found")

    @staticmethod
    def sort(lines: List[str], reverse: bool = False, numeric: bool = False) -> str:
        """
        Sort lines of text (like sort command).

        Args:
            lines: List of lines to sort
            reverse: Sort in reverse order (default: False)
            numeric: Sort numerically (default: False)

        Returns:
            String containing sorted lines (one per line)
        """
        if numeric:
            try:

                def numeric_key(line):
                    # Handle uniq -c format (leading whitespace + number + text)
                    stripped = line.strip()
                    if not stripped:
                        return 0.0

                    # Check if line starts with a number (possibly after whitespace)
                    parts = stripped.split(
                        None, 1
                    )  # Split on any whitespace, max 1 split
                    if parts:
                        try:
                            return float(parts[0])
                        except ValueError:
                            # If first part isn't a number, try to parse the
                            # whole line as a number
                            return float(stripped)
                    return 0.0

                sorted_lines = sorted(lines, key=numeric_key, reverse=reverse)
                return "\n".join(sorted_lines)
            except ValueError:
                # Fall back to string sorting if numeric fails
                pass

        sorted_lines = sorted(lines, reverse=reverse)
        return "\n".join(sorted_lines)

    @staticmethod
    def uniq(lines: List[str], count: bool = False) -> str:
        """
        Remove duplicate consecutive lines (like uniq command).

        Args:
            lines: List of lines to process
            count: Include count of occurrences (default: False)

        Returns:
            String with duplicates removed (one line per line)
        """
        if not lines:
            return ""

        result = []
        current_line = lines[0]
        current_count = 1

        for line in lines[1:]:
            if line == current_line:
                current_count += 1
            else:
                if count:
                    result.append(f"{current_count: >7} {current_line}")
                else:
                    result.append(current_line)
                current_line = line
                current_count = 1

        # Add the last line
        if count:
            result.append(f"{current_count: >7} {current_line}")
        else:
            result.append(current_line)

        return "\n".join(result)

    @staticmethod
    def cut(line: str, delimiter: str = "\t", fields: Union[int, List[int]] = 1) -> str:
        """
        Extract fields from line (like cut command).

        Args:
            line: Line to process
            delimiter: Field delimiter (default: tab)
            fields: Field number(s) to extract (1-indexed)

        Returns:
            Extracted fields joined by delimiter
        """
        parts = line.split(delimiter)

        if isinstance(fields, int):
            fields = [fields]

        result_parts = []
        for field_num in fields:
            if 1 <= field_num <= len(parts):
                result_parts.append(parts[field_num - 1])

        return delimiter.join(result_parts)

    @staticmethod
    def replace(
        text: str,
        pattern: str,
        replacement: str,
        count: int = 0,
        ignore_case: bool = False,
    ) -> str:
        """
        Replace pattern in text (like sed s/// command).

        Args:
            text: Text to process
            pattern: Pattern to replace
            replacement: Replacement text
            count: Maximum number of replacements (0 = all)
            ignore_case: Case-insensitive replacement

        Returns:
            Text with replacements made
        """
        flags = re.IGNORECASE if ignore_case else 0
        return re.sub(pattern, replacement, text, count=count, flags=flags)

    @staticmethod
    def wc(text: str) -> dict:
        """
        Count words, lines, and characters in text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with counts
        """
        return {
            "lines": text.count("\n"),
            "words": len(text.split()),
            "chars": len(text),
            "bytes": len(text.encode("utf-8")),
        }

    @staticmethod
    def pipe(*functions):
        """
        Create a pipeline of functions for chaining operations.

        Args:
            *functions: Functions to chain together

        Returns:
            A function that applies all functions in sequence

        Example:
            pipeline = TextUtils.pipe(
                lambda x: x.split('\n'),
                lambda lines: [line for line in lines if "ERROR" in line],
                lambda lines: sorted(lines),
                lambda lines: '\n'.join(lines[:5])
            )
            result = pipeline(content)
        """
        from functools import reduce

        return lambda x: reduce(lambda acc, f: f(acc), functions, x)
