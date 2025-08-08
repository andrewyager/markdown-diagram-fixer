# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the markdown diagram fixer.

## Installation Issues

### Package Not Found After Installation

**Problem**: After running `pip install markdown-diagram-fixer`, you get `ModuleNotFoundError: No module named 'precision_diagram_fixer'`

**Cause**: The package is installed in a different Python environment than the one being used.

**Solution**:
1. Check which Python environments you have:
   ```bash
   which python3
   /usr/bin/env python3 -c "import sys; print(sys.executable)"
   ```

2. Install the package in the correct Python environment:
   ```bash
   # If they point to different locations, use the specific Python:
   /path/to/specific/python3 -m pip install markdown-diagram-fixer
   ```

3. Test the installation:
   ```bash
   /path/to/specific/python3 -c "from precision_diagram_fixer import PrecisionDiagramFixer; print('SUCCESS')"
   ```

### Console Scripts Not Found

**Problem**: `diagram-fixer` or `pandoc-diagram-fixer` commands not found after installation.

**Solution**:
1. Check if the scripts are in your PATH:
   ```bash
   which diagram-fixer
   which pandoc-diagram-fixer
   ```

2. If not found, locate them:
   ```bash
   python3 -m pip show markdown-diagram-fixer
   # Look at the Location field
   find /opt/homebrew/bin -name "*diagram*" 2>/dev/null
   ```

3. Add the bin directory to your PATH or create symlinks.

## Pandoc Filter Issues

### Filter Not Found

**Problem**: Pandoc reports filter not found or permission denied.

**Solution**:
1. Check the console script exists:
   ```bash
   which pandoc-diagram-filter
   ```

2. If not found, verify package installation:
   ```bash
   pip list | grep markdown-diagram-fixer
   ```

3. Use full path in pandoc defaults:
   ```yaml
   filters:
     - /opt/homebrew/bin/pandoc-diagram-filter  # Use output from 'which'
   ```

### Filter Fails with Import Error

**Problem**: Filter runs but fails with Python import errors.

**Solution**: The installed console script should automatically use the correct Python environment. If it fails:

1. Check the console script:
   ```bash
   head -5 $(which pandoc-diagram-filter)
   ```

2. Test the script directly:
   ```bash
   echo '{"blocks":[],"meta":{},"pandoc-api-version":[1,23,1]}' | pandoc-diagram-filter
   ```

3. If it fails, reinstall:
   ```bash
   pip uninstall markdown-diagram-fixer
   pip install markdown-diagram-fixer
   ```

### Filter Runs But Diagrams Not Fixed

**Problem**: Pandoc verbose output shows filter completed successfully, but diagrams in output are unchanged.

**Diagnosis**:
1. Test the filter manually:
   ```bash
   echo '```
   ┌─────┐    ┌──────┐  
   │ Bad │────│ Box  │
   └─────┘    └──────┘
   ```' | pandoc -f gfm -t json | pandoc-diagram-filter | pandoc -f json -t markdown
   ```

2. Check if diagrams are detected (look for "Fixed diagram in code block" messages):
   ```bash
   # Run with stderr to see messages
   DIAGRAM_FIXER_QUIET= pandoc -d pdf your_file.md -o output.pdf --verbose
   ```

**Solutions**:
- Verify your diagrams contain detectable Unicode box drawing characters (`┌┐└┘├┤┬┴┼─│`)
- Ensure diagrams are in plain code blocks (```), not language-specific blocks (```text)
- Check that the precision diagram fixer can actually fix your diagrams by testing directly:
  ```bash
  # Save diagram to file and test
  diagram-fixer your_diagram.txt
  ```

### Multiple Python Versions Confusion

**Problem**: You have multiple Python installations and the console script doesn't work.

**Solution**: The console script automatically uses the Python environment where the package was installed. Simply reinstall in the desired Python environment:

```bash
# Use specific Python version
/opt/homebrew/bin/python3 -m pip install markdown-diagram-fixer

# Or use the default
pip install markdown-diagram-fixer
```

The installed `pandoc-diagram-filter` script will automatically use the correct Python environment.

## Testing Your Setup

### Complete Integration Test

Create a test file and verify the entire workflow:

1. **Create test file** (`test_integration.md`):
   ```markdown
   # Test Document
   
   ```
   ┌─────┐    ┌──────┐  
   │ Bad │────│ Box  │
   └─────┘    └──────┘
   ```
   ```

2. **Test command-line tool**:
   ```bash
   diagram-fixer --help
   echo '┌─────┐  │ Bad │' | pandoc-diagram-fixer
   ```

3. **Test pandoc integration**:
   ```bash
   pandoc test_integration.md -t html --filter pandoc-diagram-filter
   ```

4. **Test with your defaults**:
   ```bash
   pandoc -d pdf test_integration.md -o test.pdf --verbose
   ```

### Debug Mode

Enable debug output to see what's happening:

```bash
# For pandoc filter
DIAGRAM_FIXER_QUIET= pandoc -d pdf your_file.md -o output.pdf --verbose

# For command line tool  
diagram-fixer your_diagram.txt --verbose
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `command not found: pandoc-diagram-filter` | Console script not installed | Reinstall package with `pip install markdown-diagram-fixer` |
| `Filter returned error status 1` | Filter crashed | Test filter directly, check installation |
| `JSON parse error: Unexpected end-of-input` | Filter crashed before outputting JSON | Check filter's stderr for actual error |
| `ModuleNotFoundError` in filter | Package not properly installed | Reinstall package |

## Getting Help

If you're still having issues:

1. **Check the logs**: Look for error messages in pandoc's verbose output
2. **Test components separately**: Test the Python package, console scripts, and pandoc filter individually  
3. **Report bugs**: Create an issue at https://github.com/andrewyager/markdown-diagram-fixer/issues with:
   - Your operating system and Python version
   - Installation method used
   - Complete error messages
   - Output of the diagnostic commands above