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
            output = FileOps.head(temp_path, 5)
            lines = output.split("\n")
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
            output = FileOps.tail(temp_path, 5)
            lines = output.split("\n")
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

    def test_ls(self):
        """Test ls functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            (Path(temp_dir) / "file1.txt").touch()
            (Path(temp_dir) / "file2.txt").touch()
            (Path(temp_dir) / ".hidden").touch()

            # Test basic ls
            output = FileOps.ls(temp_dir)
            files = output.split("\n")
            assert "file1.txt" in files
            assert "file2.txt" in files
            assert ".hidden" not in files

            # Test ls with hidden files
            output_hidden = FileOps.ls(temp_dir, show_hidden=True)
            files_hidden = output_hidden.split("\n")
            assert ".hidden" in files_hidden

    def test_head_with_content(self):
        """Test head functionality with content parameter."""
        content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6"
        output = FileOps.head(content=content, lines=3)
        lines = output.split("\n")
        assert len(lines) == 3
        assert lines[0] == "Line 1"
        assert lines[2] == "Line 3"

    def test_pipeline_chaining(self):
        """Test chaining operations using content parameters."""
        content = "ERROR: something bad\nINFO: normal log\nERROR: another error\nWARN: warning"

        # Chain: grep ERROR -> head 1
        error_lines = TextUtils.grep("ERROR", content=content)
        first_error = FileOps.head(content=error_lines, lines=1)

        assert first_error == "ERROR: something bad"

    def test_pipe_function(self):
        """Test pipe function for chaining operations."""
        content = "ERROR: bad thing\nINFO: good thing\nERROR: another bad thing\nWARN: warning"

        # Create a pipeline: split -> filter errors -> sort -> take first 2 -> join
        pipeline = TextUtils.pipe(
            lambda x: x.split("\n"),
            lambda lines: [line for line in lines if "ERROR" in line],
            lambda lines: sorted(lines),
            lambda lines: lines[:1],
            lambda lines: "\n".join(lines),
        )

        result = pipeline(content)
        assert result == "ERROR: another bad thing"


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
            output = TextUtils.grep("ap", temp_path)
            lines = output.split("\n")
            assert len(lines) == 2
            assert "apple" in lines
            assert "apricot" in lines
        finally:
            os.unlink(temp_path)

    def test_grep_with_content(self):
        """Test grep functionality with content parameter."""
        content = "apple\nbanana\ncherry\napricot\norange"
        output = TextUtils.grep("ap", content=content)
        lines = output.split("\n")
        assert len(lines) == 2
        assert "apple" in lines
        assert "apricot" in lines

    def test_nl(self):
        """Test line numbering functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("first line\n\nsecond line\n")
            temp_path = f.name

        try:
            output = TextUtils.nl(temp_path)
            lines = output.split("\n")
            assert len(lines) == 3
            assert lines[0] == "\t1 first line"
            assert lines[1] == ""  # Empty line not numbered
            assert lines[2] == "\t2 second line"
        finally:
            os.unlink(temp_path)

    def test_sort_lines(self):
        """Test line sorting functionality."""
        lines = ["zebra", "apple", "banana"]
        output = TextUtils.sort(lines)
        sorted_lines = output.split("\n")
        assert sorted_lines == ["apple", "banana", "zebra"]

        reverse_output = TextUtils.sort(lines, reverse=True)
        reverse_sorted_lines = reverse_output.split("\n")
        assert reverse_sorted_lines == ["zebra", "banana", "apple"]

    def test_uniq(self):
        """Test uniq functionality."""
        lines = ["apple", "apple", "banana", "banana", "banana", "cherry"]
        output = TextUtils.uniq(lines)
        result_lines = output.split("\n")
        assert result_lines == ["apple", "banana", "cherry"]

        # Test with count
        output_count = TextUtils.uniq(lines, count=True)
        count_lines = output_count.split("\n")
        assert "      2 apple" in count_lines
        assert "      3 banana" in count_lines
        assert "      1 cherry" in count_lines

    def test_sort_numeric_with_count_format(self):
        """Test numeric sorting with uniq -c format."""
        lines = ["      2 10.0.0.1", "      3 192.168.1.1", "      1 8.8.8.8"]
        output = TextUtils.sort(lines, reverse=True, numeric=True)
        sorted_lines = output.split("\n")
        assert sorted_lines == [
            "      3 192.168.1.1",
            "      2 10.0.0.1",
            "      1 8.8.8.8",
        ]

        # Test regular numeric sort
        numeric_lines = ["10", "2", "1"]
        numeric_output = TextUtils.sort(numeric_lines, numeric=True)
        numeric_sorted = numeric_output.split("\n")
        assert numeric_sorted == ["1", "2", "10"]


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
