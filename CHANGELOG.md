# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-07-31

### Changed

- **BREAKING**: Refactored function return types to match Unix command behavior
  - `FileOps.head()` and `FileOps.tail()` now return strings instead of lists
  - `FileOps.ls()` now returns string output (one item per line) instead of list
  - `TextUtils.grep()`, `TextUtils.nl()`, `TextUtils.sort_lines()`, `TextUtils.uniq()` now return strings
  - `PathUtils.find()` and `PathUtils.which_all()` now return strings (one item per line)
  - `ArchiveUtils.tar_extract()` and `ArchiveUtils.zip_extract()` now return strings
- **BREAKING**: Renamed functions for Unix consistency:
  - `TextUtils.sort_lines()` → `TextUtils.sort()`
  - `TextUtils.word_count()` → `TextUtils.wc()`
- Improved `FileOps.wc()` line counting to match Unix `wc` behavior (handles files without trailing newlines)
- Updated CLI scripts to work with new string return types
- Updated examples and documentation to reflect new API

### Fixed

- Line counting in `FileOps.wc()` now properly handles files that don't end with newlines
- All functions now behave consistently with their Unix counterparts

## [0.1.0] - 2025-07-31

### Added

- Initial release of pycoreux package
- Core functionality for shell-like operations in Python
- Support for Python 3.7+
- MIT License
- Comprehensive documentation
