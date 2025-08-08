# Diagram Fixer

This is a python application that is designed to read markdown diagrams and fix the formatting/spacing in them.

Sometimes when Claude Code generates pretty block diagrams, the pipe lines that reflect the diagram don't get cleanly created, and things that clearly should line up don't.

This python app can be run over a file to clean it up.

Examples include including in a pandoc workflow to clean up before converting to another format.

## Project Structure

### Production Files (main directory)
- `precision_diagram_fixer.py` - Main production tool with matrix-based algorithm
- `pandoc_preprocessor.py` - Pandoc integration for markdown workflows
- `example_diagram.txt` - Sample diagram for testing
- `setup.py` - Python package setup (legacy)
- `pyproject.toml` - Modern Python package configuration
- `requirements.txt` - Dependencies (empty - no external deps)
- `MANIFEST.in` - Package manifest for distribution
- `tests/` - Test files and test suite
- `README.md` - Public documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `SECURITY.md` - Security policy and vulnerability reporting
- `LICENSE` - MIT license
- `CLAUDE.md` - This file (development instructions)
- `.gitignore` - Git ignore patterns
- `.github/` - GitHub issue templates and PR templates

### Development Archive (`dev-archive/`)
- `debug-tools/` - Analysis and debugging utilities
- `experiments/` - Experimental implementations and prototypes  
- `test-data/` - Test diagrams and sample data
- `iteration-debug/` - Debug output from algorithm development
- `documentation/` - Development notes and algorithm documentation

## Commands

### Development (without installation)
```bash
# Test the production tool
python3 precision_diagram_fixer.py dev-archive/test-data/extracted_doc_diagram_2.txt

# Test pandoc integration
cat dev-archive/test-data/test_quiet.md | python3 pandoc_preprocessor.py
```

### Installation Testing
```bash
# Install in development mode
pip install -e .

# Test installed commands
diagram-fixer dev-archive/test-data/extracted_doc_diagram_2.txt
cat dev-archive/test-data/test_quiet.md | pandoc-diagram-fixer

# Build package
python3 -m build

# Test distribution
pip install dist/markdown_diagram_fixer-1.0.0-py3-none-any.whl

# Run tests
python3 tests/test_basic_functionality.py
python3 tests/test_installation.py
```
