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
        filepath: Union[str, Path],
        ignore_case: bool = False,
        line_numbers: bool = False,
        invert: bool = False,
    ) -> List[str]:
        """
        Search for pattern in file (like grep command).

        Args:
            pattern: Regular expression pattern to search
            filepath: Path to file to search in
            ignore_case: Case-insensitive search (default: False)
            line_numbers: Include line numbers in output (default: False)
            invert: Return non-matching lines (default: False)

        Returns:
            List of matching lines
        """
        flags = re.IGNORECASE if ignore_case else 0
        compiled_pattern = re.compile(pattern, flags)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                results = []
                for line_num, line in enumerate(file, 1):
                    line = line.rstrip("\n")
                    matches = bool(compiled_pattern.search(line))

                    if matches != invert:  # XOR logic for invert
                        if line_numbers:
                            results.append(f"{line_num}:{line}")
                        else:
                            results.append(line)

                return results
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found")

    @staticmethod
    def nl(
        filepath: Union[str, Path], start: int = 1, skip_empty: bool = True
    ) -> List[str]:
        """
        Add line numbers to file content (like nl command).

        Args:
            filepath: Path to file to number
            start: Starting line number (default: 1)
            skip_empty: Skip empty lines for numbering (default: True)

        Returns:
            List of numbered lines
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

                return results
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found")

    @staticmethod
    def sort_lines(
        lines: List[str], reverse: bool = False, numeric: bool = False
    ) -> List[str]:
        """
        Sort lines of text (like sort command).

        Args:
            lines: List of lines to sort
            reverse: Sort in reverse order (default: False)
            numeric: Sort numerically (default: False)

        Returns:
            Sorted list of lines
        """
        if numeric:
            try:
                return sorted(lines, key=lambda x: float(x.strip()), reverse=reverse)
            except ValueError:
                # Fall back to string sorting if numeric fails
                pass

        return sorted(lines, reverse=reverse)

    @staticmethod
    def uniq(lines: List[str], count: bool = False) -> List[str]:
        """
        Remove duplicate consecutive lines (like uniq command).

        Args:
            lines: List of lines to process
            count: Include count of occurrences (default: False)

        Returns:
            List with duplicates removed
        """
        if not lines:
            return []

        result = []
        current_line = lines[0]
        current_count = 1

        for line in lines[1:]:
            if line == current_line:
                current_count += 1
            else:
                if count:
                    result.append(f"{current_count:>7} {current_line}")
                else:
                    result.append(current_line)
                current_line = line
                current_count = 1

        # Add the last line
        if count:
            result.append(f"{current_count:>7} {current_line}")
        else:
            result.append(current_line)

        return result

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
    def word_count(text: str) -> dict:
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
