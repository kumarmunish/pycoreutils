"""Tests for pycoreux package."""

import os
import tempfile
from pathlib import Path

import pytest

from pycoreux import FileOps, ProcessUtils, TextUtils


class TestFileOps:
    """Test FileOps functionality."""

    def test_cat(self):
        """Test cat functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("Hello, World!\nSecond line")
            temp_path = f.name

        try:
            content = FileOps.cat(temp_path)
            assert content == "Hello, World!\nSecond line"
        finally:
            os.unlink(temp_path)

    def test_head(self):
        """Test head functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            for i in range(20):
                f.write(f"Line {i+1}\n")
            temp_path = f.name

        try:
            lines = FileOps.head(temp_path, 5)
            assert len(lines) == 5
            assert lines[0] == "Line 1"
            assert lines[4] == "Line 5"
        finally:
            os.unlink(temp_path)

    def test_tail(self):
        """Test tail functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            for i in range(20):
                f.write(f"Line {i+1}\n")
            temp_path = f.name

        try:
            lines = FileOps.tail(temp_path, 5)
            assert len(lines) == 5
            assert lines[0] == "Line 16"
            assert lines[4] == "Line 20"
        finally:
            os.unlink(temp_path)

    def test_wc(self):
        """Test word count functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("Hello world\nSecond line\n")
            temp_path = f.name

        try:
            lines, words, chars = FileOps.wc(temp_path)
            assert lines == 2
            assert words == 4  # "Hello", "world", "Second", "line"
            assert chars == 24  # Including newlines
        finally:
            os.unlink(temp_path)


class TestTextUtils:
    """Test TextUtils functionality."""

    def test_echo(self):
        """Test echo functionality."""
        result = TextUtils.echo("Hello", "World")
        assert result == "Hello World\n"

    def test_grep(self):
        """Test grep functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("apple\nbanana\ncherry\napricot\n")
            temp_path = f.name

        try:
            matches = TextUtils.grep("ap", temp_path)
            assert len(matches) == 2
            assert "apple" in matches
            assert "apricot" in matches
        finally:
            os.unlink(temp_path)

    def test_nl(self):
        """Test line numbering functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("first line\n\nsecond line\n")
            temp_path = f.name

        try:
            numbered = TextUtils.nl(temp_path)
            assert len(numbered) == 3
            assert numbered[0] == "\t1 first line"
            assert numbered[1] == ""  # Empty line not numbered
            assert numbered[2] == "\t2 second line"
        finally:
            os.unlink(temp_path)

    def test_sort_lines(self):
        """Test line sorting functionality."""
        lines = ["zebra", "apple", "banana"]
        sorted_lines = TextUtils.sort_lines(lines)
        assert sorted_lines == ["apple", "banana", "zebra"]

        reverse_sorted = TextUtils.sort_lines(lines, reverse=True)
        assert reverse_sorted == ["zebra", "banana", "apple"]


class TestProcessUtils:
    """Test ProcessUtils functionality."""

    def test_run_simple_command(self):
        """Test running a simple command."""
        result = ProcessUtils.run("echo 'Hello World'")
        assert result.success
        assert "Hello World" in result.stdout

    def test_capture(self):
        """Test capturing command output."""
        output = ProcessUtils.capture("echo 'Test output'")
        assert "Test output" in output

    def test_which(self):
        """Test which functionality."""
        # Test finding a common system command
        ls_path = ProcessUtils.which("ls")
        assert ls_path is not None
        assert "ls" in ls_path

        # Test non-existent command
        fake_path = ProcessUtils.which("nonexistentcommand12345")
        assert fake_path is None


if __name__ == "__main__":
    pytest.main([__file__])
