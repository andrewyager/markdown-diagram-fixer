# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-08

### Changed
- **BREAKING CHANGE**: Restructured codebase to use src/ layout for improved packaging
  - Moved `precision_diagram_fixer.py` and `pandoc_preprocessor.py` to `src/` directory
  - Updated all import paths and documentation references
  - Console scripts (`diagram-fixer`, `pandoc-diagram-fixer`, `pandoc-diagram-filter`) remain unchanged
- Applied comprehensive code formatting with black, isort, and flake8
- Improved code quality and removed unused imports
- Updated all documentation files for new src/ structure
- Enhanced GitHub issue and PR templates with src/ paths
- Cleaned up redundant pandoc_filter.py (functionality integrated into pandoc_preprocessor.py)

### Fixed
- Resolved all PEP 8 compliance issues
- Fixed import organization across all Python files
- Corrected test import paths for new structure

### Improved
- Better project structure following Python packaging best practices
- Cleaner codebase with consistent formatting
- More maintainable code organization
- Updated development workflow documentation

## [1.0.1] - 2024-12-XX

### Fixed
- Security contact information in README
- Python publishing workflow improvements

### Improved  
- Major improvements to pandoc filter integration
- Enhanced pandoc filter functionality

## [1.0.0] - 2024-12-XX

### Added
- Initial release of markdown-diagram-fixer
- Precision matrix-based diagram fixing algorithm
- Pandoc integration with multiple entry points
- Console script commands for CLI usage
- Comprehensive test suite
- Documentation and examples

### Features
- Automatic ASCII diagram alignment and formatting
- Unicode box-drawing character support
- Quiet operation with optional verbose debugging
- Robust algorithm handling complex nested diagrams
- No external dependencies (standard library only)