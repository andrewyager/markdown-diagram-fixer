#!/usr/bin/env python3
"""
Installation and command-line interface tests.
"""

import subprocess
import sys
from pathlib import Path


def test_console_scripts_available():
    """Test that console scripts are available after installation."""
    # Test diagram-fixer command
    try:
        result = subprocess.run(['diagram-fixer'], capture_output=True, text=True)
        assert 'Usage:' in result.stdout
        print("✓ diagram-fixer command available")
    except FileNotFoundError:
        print("✗ diagram-fixer command not found - package may not be installed")
        return False
    
    # Test pandoc-diagram-fixer command  
    try:
        result = subprocess.run(['pandoc-diagram-fixer'], 
                              input="", capture_output=True, text=True)
        # Should complete without error (empty input is valid)
        assert result.returncode == 0
        print("✓ pandoc-diagram-fixer command available")
    except FileNotFoundError:
        print("✗ pandoc-diagram-fixer command not found - package may not be installed")
        return False
    
    return True


def test_diagram_fixer_with_test_file():
    """Test diagram-fixer with a simple test file."""
    test_file = Path(__file__).parent / 'simple_diagram.txt'
    
    if not test_file.exists():
        print("✗ Test file not found")
        return False
    
    try:
        result = subprocess.run(['diagram-fixer', str(test_file)], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert '✅' in result.stdout
        print("✓ diagram-fixer processes test file successfully")
        return True
    except FileNotFoundError:
        print("✗ diagram-fixer command not available")
        return False


def test_pandoc_integration():
    """Test pandoc integration if pandoc is available."""
    test_content = '''# Test

```
┌─────┐
│ Test│
└─────┘
```
'''
    
    try:
        # Test our filter directly
        result = subprocess.run(['pandoc-diagram-fixer'], 
                              input=test_content, capture_output=True, text=True)
        assert result.returncode == 0
        assert '┌─────┐' in result.stdout
        print("✓ pandoc-diagram-fixer processes markdown successfully")
        
        # Test with actual pandoc if available
        try:
            pandoc_result = subprocess.run(['pandoc', '--filter', 'pandoc-diagram-fixer', '-t', 'html'],
                                         input=test_content, capture_output=True, text=True)
            if pandoc_result.returncode == 0:
                print("✓ Full pandoc integration works")
            else:
                print("⚠ pandoc integration failed, but filter works standalone")
        except FileNotFoundError:
            print("ℹ pandoc not available for full integration test")
            
        return True
        
    except FileNotFoundError:
        print("✗ pandoc-diagram-fixer command not available")
        return False


if __name__ == '__main__':
    print("Running installation tests...")
    print("Note: These tests require the package to be installed (pip install -e .)")
    print()
    
    tests_passed = 0
    
    if test_console_scripts_available():
        tests_passed += 1
        
    if test_diagram_fixer_with_test_file():
        tests_passed += 1
        
    if test_pandoc_integration():
        tests_passed += 1
    
    print(f"\n{tests_passed}/3 installation tests passed")
    
    if tests_passed == 3:
        print("🎉 All installation tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed - check installation")
        sys.exit(1)