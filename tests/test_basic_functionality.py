#!/usr/bin/env python3
"""
Basic functionality tests for the diagram fixer.
These tests can be run with: python3 -m pytest tests/
"""

import sys
from pathlib import Path

# Add the src directory to path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandoc_preprocessor  # noqa: E402
from precision_diagram_fixer import PrecisionDiagramFixer  # noqa: E402


def test_precision_diagram_fixer_import():
    """Test that we can import and instantiate the fixer."""
    fixer = PrecisionDiagramFixer()
    assert fixer is not None
    assert fixer.debug is False


def test_basic_diagram_fixing():
    """Test basic diagram fixing functionality."""
    fixer = PrecisionDiagramFixer(debug=False)

    # Simple test diagram
    lines = ["┌─────┐", "│ Test│", "└─────┘"]

    result = fixer.fix_diagram(lines)
    assert isinstance(result, list)
    assert len(result) >= len(lines)  # Should not lose lines


def test_pandoc_preprocessor_import():
    """Test that we can import pandoc preprocessor."""
    # Just test that we can import without error
    assert pandoc_preprocessor.detect_diagrams_in_content is not None
    assert pandoc_preprocessor.main is not None


def test_diagram_detection_in_markdown():
    """Test diagram detection in markdown content."""
    content = """# Test Document

Here's a diagram:

```
┌─────┐
│ Test│
└─────┘
```

And some text.
"""

    diagrams = pandoc_preprocessor.detect_diagrams_in_content(content)
    assert len(diagrams) == 1
    start_line, end_line, diagram_content = diagrams[0]
    assert "┌─────┐" in diagram_content
    assert "│ Test│" in diagram_content
    assert "└─────┘" in diagram_content


def test_no_diagram_detection():
    """Test that regular code blocks are not detected as diagrams."""
    content = """# Test Document

Regular code:

```python
def hello():
    print("world")
```

No diagrams here.
"""

    diagrams = pandoc_preprocessor.detect_diagrams_in_content(content)
    assert len(diagrams) == 0


if __name__ == "__main__":
    print("Running basic functionality tests...")

    test_precision_diagram_fixer_import()
    print("✓ PrecisionDiagramFixer import test passed")

    test_basic_diagram_fixing()
    print("✓ Basic diagram fixing test passed")

    test_pandoc_preprocessor_import()
    print("✓ Pandoc preprocessor import test passed")

    test_diagram_detection_in_markdown()
    print("✓ Diagram detection test passed")

    test_no_diagram_detection()
    print("✓ No false diagram detection test passed")

    print("\n🎉 All tests passed!")
