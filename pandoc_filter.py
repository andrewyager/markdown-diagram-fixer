#!/usr/bin/env python3
"""
Proper pandoc filter for precision diagram fixer.
Works with pandoc's AST format, not raw markdown.

Copyright (c) 2025 Andrew Yager, Real World Technology Solutions Pty Ltd
MIT License - see LICENSE file for details.
"""

import json
import sys
import os

from precision_diagram_fixer import PrecisionDiagramFixer


def walk_ast(obj, action):
    """Walk through pandoc AST and apply action to matching elements."""
    if isinstance(obj, dict):
        if obj.get('t') == 'CodeBlock':
            # Check if this is a diagram code block
            attr, content = obj.get('c', [None, ''])
            if attr and isinstance(content, str):
                # Check if content contains diagram characters
                diagram_chars = '┌┐└┘├┤┬┴┼─│┄┅┆┇┈┉┊┋'
                ascii_art_chars = '+|\\-/'
                if (any(char in content for char in diagram_chars) or 
                    any(char in content for char in ascii_art_chars)):
                    # This is a diagram, process it
                    fixed_content = action(content)
                    if fixed_content != content:
                        obj['c'][1] = fixed_content
                        if not os.environ.get('DIAGRAM_FIXER_QUIET'):
                            print(f"diagram-fixer: Fixed diagram in code block", file=sys.stderr)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                walk_ast(value, action)
        elif isinstance(obj, list):
            for item in obj:
                walk_ast(item, action)
    elif isinstance(obj, list):
        for item in obj:
            walk_ast(item, action)


def fix_diagram_content(content):
    """Fix diagram content using PrecisionDiagramFixer."""
    try:
        fixer = PrecisionDiagramFixer(debug=False)
        lines = content.strip().split('\n')
        fixed_lines = fixer.fix_diagram(lines)
        return '\n'.join(fixed_lines)
    except Exception as e:
        if not os.environ.get('DIAGRAM_FIXER_QUIET'):
            print(f"diagram-fixer error: {e}", file=sys.stderr)
        return content


def main():
    """Main pandoc filter function."""
    try:
        # Read JSON from stdin (pandoc AST)
        doc = json.load(sys.stdin)
        
        # Process the AST
        walk_ast(doc, fix_diagram_content)
        
        # Output modified JSON
        json.dump(doc, sys.stdout, separators=(',', ':'))
        
    except Exception as e:
        if not os.environ.get('DIAGRAM_FIXER_QUIET'):
            print(f"pandoc filter error: {e}", file=sys.stderr)
        # On error, pass through original input
        sys.stdin.seek(0)
        sys.stdout.write(sys.stdin.read())


if __name__ == '__main__':
    main()