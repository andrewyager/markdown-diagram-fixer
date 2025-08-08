#!/usr/bin/env python3
"""
Pandoc preprocessor wrapper for precision diagram fixer.
Reads markdown from stdin, processes diagrams, and outputs to stdout.

Copyright (c) 2025 Andrew Yager, Real World Technology Solutions Pty Ltd
MIT License - see LICENSE file for details.
"""

import sys
import os
from pathlib import Path

# Add the current directory to path to find precision_diagram_fixer
sys.path.insert(0, str(Path(__file__).parent))
from precision_diagram_fixer import PrecisionDiagramFixer

def detect_diagrams_in_content(content):
    """Detect diagram blocks in markdown content.
    
    Returns:
        List of tuples (start_line, end_line, diagram_content) where line numbers are 0-indexed
    """
    diagram_blocks = []
    lines = content.split('\n')
    in_code_block = False
    current_block = []
    block_start = 0
    
    for i, line in enumerate(lines):
        if line.strip() == '```':
            if in_code_block:
                # End of code block
                block_content = '\n'.join(current_block)
                # Check if it contains box drawing characters OR ASCII art (likely a diagram)
                diagram_chars = '┌┐└┘├┤┬┴┼─│┄┅┆┇┈┉┊┋'  # Unicode box drawing chars
                ascii_art_chars = '+|\\-/'  # ASCII art style diagrams
                if (any(char in block_content for char in diagram_chars) or 
                    any(char in block_content for char in ascii_art_chars)):
                    diagram_blocks.append((block_start, i, block_content))
                current_block = []
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
                block_start = i + 1  # Content starts on next line
        elif in_code_block:
            current_block.append(line)
    
    return diagram_blocks

def main():
    # Read all input from stdin
    input_content = sys.stdin.read()
    
    if not input_content.strip():
        return
    
    try:
        # Create precision diagram fixer instance
        fixer = PrecisionDiagramFixer(debug=False)
        
        # Detect diagrams in the content
        diagrams = detect_diagrams_in_content(input_content)
        
        if not diagrams:
            # No diagrams found, output original content
            sys.stdout.write(input_content)
            return
        
        # Process diagrams from end to start to preserve line numbers
        modified_content = input_content
        for start_line, end_line, diagram_content in reversed(diagrams):
            diagram_lines = diagram_content.split('\n')
            fixed_lines = fixer.fix_diagram(diagram_lines)
            fixed_diagram = '\n'.join(fixed_lines)
            
            # Replace the diagram in the content
            lines = modified_content.split('\n')
            lines[start_line:end_line + 1] = fixed_diagram.split('\n')
            modified_content = '\n'.join(lines)
        
        # Output the fixed content
        sys.stdout.write(modified_content)
        
        # Log to stderr for debugging (pandoc will ignore this)
        # Set DIAGRAM_FIXER_QUIET=1 to suppress this message
        if not os.environ.get('DIAGRAM_FIXER_QUIET'):
            sys.stderr.write(f"diagram-fixer: Fixed {len(diagrams)} diagrams\n")
        
    except Exception as e:
        # On any error, output original content and log error
        sys.stdout.write(input_content)
        if not os.environ.get('DIAGRAM_FIXER_QUIET'):
            sys.stderr.write(f"diagram-fixer error: {e}\n")

if __name__ == '__main__':
    main()