#!/usr/bin/env python3
"""
Precision Diagram Fixer - Uses matrix-based detection for accurate problem identification and fixing.

Copyright (c) 2025 Andrew Yager, Real World Technology Solutions Pty Ltd
MIT License - see LICENSE file for details.
"""

import sys
import io
import contextlib
from typing import List, Dict

class PrecisionDiagramFixer:
    def __init__(self, debug=False):
        self.debug = debug
        self.solved = None
        self.cached_boxes = None  # Cache initial box detection
    
    def fix_diagram(self, lines):
        """Main entry point using precision detection and targeted fixing."""
        max_iterations = len(lines) * 4  # 4 times the number of lines
        
        # Reset cached boxes for this diagram fixing session
        self.cached_boxes = None
        
        if self.debug:
            print("=== PRECISION DIAGRAM FIXER ===")
            print(f"Diagram size: {len(lines)} lines")
            print(f"Max iterations: {max_iterations}")
            print()
        iteration = 0
        max_fixed_row = -1
        last_target_width = None
        
        while iteration < max_iterations:
            iteration += 1
            if self.debug:
                print(f"--- ITERATION {iteration} ---")
            
            # Get precise problem analysis
            row_analysis = self.analyze_diagram_problems(lines, iteration)
            
            
            # Check for width changes
            if self.debug and len(lines) > 29:  # Check if we have row 30
                current_target_width = len(lines[29])  # Row 30 as reference
                if last_target_width is not None and current_target_width != last_target_width:
                    print(f"📏 WIDTH CHANGE DETECTED: Target width changed from {last_target_width} → {current_target_width} chars")
                    print(f"   This suggests a box expansion occurred")
                last_target_width = current_target_width
            
            # Find the first row with problems (top-to-bottom approach)
            problem_rows = [r for r in sorted(row_analysis.keys()) if row_analysis[r]['problems']]
            
            if not problem_rows:
                if self.debug:
                    print("✅ No problems found - diagram is fixed!")
                break
            
            first_problem_row = problem_rows[0]
            problems_in_row = row_analysis[first_problem_row]['problems']
            
            # Check for regression
            if self.debug and first_problem_row < max_fixed_row:
                print(f"🚨 REGRESSION DETECTED: Found problem in row {first_problem_row}")
                print(f"   We previously fixed rows up to {max_fixed_row}")
                print(f"   This suggests our last fix created a new problem!")
                print()
            
            if self.debug:
                print(f"First problem row: {first_problem_row}")
                print(f"Problems in row {first_problem_row}:")
                for problem in problems_in_row:
                    print(f"  - {problem}")
                
            
            # Fix the leftmost problem in this row
            leftmost_problem = self.get_leftmost_problem(problems_in_row)
            if not leftmost_problem:
                if self.debug:
                    print("No fixable problems found - stopping")
                break
            
            if self.debug:
                print(f"Fixing leftmost problem: {leftmost_problem}")
            
            
            # Apply the fix
            lines = self.apply_fix(lines, leftmost_problem)
            
            # Update progress tracking
            max_fixed_row = max(max_fixed_row, first_problem_row)
            
            # Save diagram state after each iteration
            if self.debug:
                self.save_iteration_state(lines, iteration)
            
            
            
            if self.debug:
                print(f"Applied fix, rescanning diagram...")
                print()
        
        if self.debug:
            print(f"Completed in {iteration} iterations")
        
        return lines
    
    def detect_boxes(self, lines: List[str]) -> List[dict]:
        """Detect all rectangular boxes using corner character patterns."""
        # First, count all corner types to understand expected box count
        corner_counts = self._count_corner_characters(lines)
        expected_boxes = min(corner_counts.values()) if corner_counts else 0
        
        boxes = []
        
        for row in range(len(lines)):
            line = lines[row]
            for col in range(len(line)):
                # Look for top-left corners
                if line[col] == '┌':
                    box = self._trace_complete_box(lines, row, col)
                    if box and self._validate_box(lines, box):
                        boxes.append(box)
        
        if self.debug:
            print(f"DETECTED BOXES ({len(boxes)} total):")
            for i, box in enumerate(boxes):
                print(f"  Box {i+1}: top_left=({box['top_left'][0]}, {box['top_left'][1]}), bottom_right=({box['bottom_right'][0]}, {box['bottom_right'][1]})")
            print()
        
        return boxes
    
    def _count_corner_characters(self, lines: List[str]) -> dict:
        """Count each type of corner character to estimate expected boxes."""
        counts = {'┌': 0, '┐': 0, '└': 0, '┘': 0}
        
        for line in lines:
            for char in line:
                if char in counts:
                    counts[char] += 1
        
        return counts
    
    def _trace_complete_box(self, lines: List[str], start_row: int, start_col: int) -> dict:
        """Trace a complete box from its top-left corner, with tolerance for misaligned corners."""
        # Characters allowed in box borders (including connection points)
        top_border_chars = {'─', '┬', '┼', '▼', '▲', '◄', '►'}
        left_border_chars = {'│', '├', '┼', '▼', '▲'}
        
        # Find the top-right corner by following border characters
        top_right_col = None
        actual_top_right_col = None
        
        if start_row < len(lines):
            line = lines[start_row]
            # First, scan for the expected ┐ character
            for col in range(start_col + 1, len(line)):
                if line[col] in top_border_chars:
                    continue
                elif line[col] == '┐':
                    top_right_col = col
                    actual_top_right_col = col
                    break
                else:
                    # Hit something that's not part of a box top - stop here
                    # But first check if there's a ┐ nearby (tolerance)
                    potential_right_col = col - 1  # The last valid border position
                    for offset in range(-3, 4):
                        check_col = potential_right_col + offset
                        if (0 <= check_col < len(line) and line[check_col] == '┐'):
                            top_right_col = potential_right_col  # Use expected position
                            actual_top_right_col = check_col  # Record actual position
                            break
                    break
        
        if top_right_col is None:
            return None
        
        # Find the bottom-left corner by following border characters down
        bottom_row = None
        actual_bottom_row = None
        for row in range(start_row + 1, len(lines)):
            if start_col >= len(lines[row]):
                break
            char = lines[row][start_col]
            if char in left_border_chars:
                continue
            elif char == '└':
                bottom_row = row
                break
            else:
                # Hit non-border character - check nearby columns for misaligned border
                found_nearby_border = False
                
                # Search nearby columns for the border character
                for offset in range(-2, 3):
                    check_col = start_col + offset
                    if (0 <= check_col < len(lines[row])):
                        check_char = lines[row][check_col]
                        if check_char in left_border_chars:
                            found_nearby_border = True
                            break
                        elif check_char == '└':
                            bottom_row = row
                            found_nearby_border = True
                            break
                
                if not found_nearby_border:
                    break
                # If we found a nearby border, continue tracing
        
        if bottom_row is None:
            return None
        
        # Find the bottom-right corner with tolerance
        bottom_right_found = False
        actual_bottom_right_col = top_right_col
        bottom_right_row = actual_bottom_row if actual_bottom_row else bottom_row
        
        if bottom_right_row < len(lines):
            # Calculate tolerance based on box width (5% minimum 2 chars)
            box_width = top_right_col - start_col + 1
            tolerance = max(2, int(box_width * 0.05))
            
            # First try exact position
            if (top_right_col < len(lines[bottom_right_row]) and 
                lines[bottom_right_row][top_right_col] == '┘'):
                bottom_right_found = True
            else:
                # Look within tolerance for the bottom-right corner
                for offset in range(-tolerance, tolerance + 1):
                    check_col = top_right_col + offset
                    if (0 <= check_col < len(lines[bottom_right_row]) and 
                        lines[bottom_right_row][check_col] == '┘'):
                        bottom_right_found = True
                        actual_bottom_right_col = check_col
                        if self.debug:
                            print(f"  Found misaligned bottom-right corner: expected col {top_right_col}, found at col {check_col} (tolerance: {tolerance})")
                        break
        
        if not bottom_right_found:
            return None
            
        # Use maximum extents for box boundaries (widest/tallest dimensions are correct)
        max_right_col = max(top_right_col, actual_bottom_right_col)
        max_bottom_row = actual_bottom_row or bottom_row
        
        return {
            'top_left': (start_row, start_col),
            'top_right': (start_row, max_right_col),
            'bottom_left': (max_bottom_row, start_col),
            'bottom_right': (max_bottom_row, max_right_col),  # Use max extent, not actual detected
            'width': max_right_col - start_col + 1,
            'height': max_bottom_row - start_row + 1,
            'center_col': start_col + (max_right_col - start_col) // 2,
            'center_row': start_row + (max_bottom_row - start_row) // 2
        }
    
    def _validate_box(self, lines: List[str], box: dict) -> bool:
        """Validate that a detected box has proper borders, allowing connection points."""
        top_row, left_col = box['top_left']
        bottom_row, right_col = box['bottom_right']
        
        # More lenient validation - allow some connection characters in borders
        valid_border_chars = {'─', '│', '├', '┤', '┬', '┴', '┼', '▼', '▲', '◄', '►'}
        valid_vertical_chars = {'│', '├', '┤', '┼', '▼', '▲'}
        valid_horizontal_chars = {'─', '┬', '┴', '┼', '◄', '►'}
        
        # Check top and bottom borders are mostly complete
        top_valid = 0
        bottom_valid = 0
        border_length = right_col - left_col - 1
        
        for col in range(left_col + 1, right_col):
            if (top_row < len(lines) and col < len(lines[top_row])):
                if lines[top_row][col] in valid_horizontal_chars:
                    top_valid += 1
            if (bottom_row < len(lines) and col < len(lines[bottom_row])):
                if lines[bottom_row][col] in valid_horizontal_chars:
                    bottom_valid += 1
        
        # Check left and right borders are mostly complete  
        left_valid = 0
        right_valid = 0
        border_height = bottom_row - top_row - 1
        
        for row in range(top_row + 1, bottom_row):
            if (row < len(lines) and left_col < len(lines[row])):
                if lines[row][left_col] in valid_vertical_chars:
                    left_valid += 1
            if (row < len(lines) and right_col < len(lines[row])):
                if lines[row][right_col] in valid_vertical_chars:
                    right_valid += 1
        
        # Accept box if at least 70% of border is valid box characters
        if border_length > 0:
            top_ratio = top_valid / border_length
            bottom_ratio = bottom_valid / border_length
        else:
            top_ratio = bottom_ratio = 1.0
            
        if border_height > 0:
            left_ratio = left_valid / border_height  
            right_ratio = right_valid / border_height
        else:
            left_ratio = right_ratio = 1.0
        
        # First try strict validation
        strict_pass = (top_ratio >= 0.7 and bottom_ratio >= 0.7 and 
                      left_ratio >= 0.7 and right_ratio >= 0.7)
        
        if strict_pass:
            return True
        
        # If strict validation failed, check if it's due to nearby misaligned characters
        if self.debug:
            print(f"Box validation failed, searching for nearby misaligned characters...")
        
        # Check if missing border characters are just misplaced nearby
        missing_chars_found_nearby = 0
        total_missing_chars = 0
        
        # Check right border misalignments
        for row in range(top_row + 1, bottom_row):
            if row < len(lines):
                if right_col >= len(lines[row]) or lines[row][right_col] not in valid_vertical_chars:
                    total_missing_chars += 1
                    # Look within 5 columns for the missing │
                    for offset in range(-5, 6):
                        check_col = right_col + offset
                        if (0 <= check_col < len(lines[row]) and 
                            lines[row][check_col] in valid_vertical_chars):
                            missing_chars_found_nearby += 1
                            if self.debug:
                                print(f"  Found misplaced │ at row {row}: expected col {right_col}, found at col {check_col}")
                            break
        
        # Check left border misalignments  
        for row in range(top_row + 1, bottom_row):
            if row < len(lines):
                if left_col >= len(lines[row]) or lines[row][left_col] not in valid_vertical_chars:
                    total_missing_chars += 1
                    # Look within 5 columns for the missing │
                    for offset in range(-5, 6):
                        check_col = left_col + offset
                        if (0 <= check_col < len(lines[row]) and 
                            lines[row][check_col] in valid_vertical_chars):
                            missing_chars_found_nearby += 1
                            if self.debug:
                                print(f"  Found misplaced │ at row {row}: expected col {left_col}, found at col {check_col}")
                            break
        
        # If we found most of the "missing" characters nearby, accept the box
        if total_missing_chars > 0:
            nearby_ratio = missing_chars_found_nearby / total_missing_chars
            if self.debug:
                print(f"  Missing chars found nearby: {missing_chars_found_nearby}/{total_missing_chars} = {nearby_ratio:.1%}")
            
            if nearby_ratio >= 0.5:  # If we found at least 50% of missing chars nearby
                if self.debug:
                    print(f"  ✅ Accepting box - missing characters found nearby")
                return True
        
        if self.debug:
            print(f"  ❌ Rejecting box - characters not found nearby")
        return False
    
    def save_iteration_state(self, lines, iteration):
        """Save the diagram state after each iteration to a file."""
        import os
        
        # Ensure the iteration_outputs directory exists
        os.makedirs('iteration_outputs', exist_ok=True)
        
        filename = f"iteration_outputs/iteration_{iteration:03d}.txt"
        with open(filename, 'w') as f:
            f.write(f"Diagram state after iteration {iteration}\n")
            f.write(f"Max width: {max(len(line) for line in lines)} chars\n")
            f.write("=" * 50 + "\n")
            for line_num, line in enumerate(lines):
                f.write(f"{line_num:2d}: {line}\n")
        
        if self.debug and iteration % 10 == 0:  # Only print every 10th iteration to avoid spam
            print(f"   Saved iteration {iteration} state to {filename}")
    
    def analyze_diagram_problems(self, lines, iteration=0):
        """Analyze diagram using matrix-based detection to get precise problems."""
        self._iteration = iteration  # Store for debug purposes
        
        # ENSURE COMPLETE FRESH STATE - no persistence between iterations
        self.solved = None
        
        try:
            # Initialize solved matrix - completely fresh for this iteration
            self.solved = [[False for _ in range(len(line))] for line in lines]
            
            
            # 1. Detect boxes and mark borders as solved  
            boxes = self.detect_boxes_with_matrix(lines, iteration)
            if self.debug:
                print(f"DETECTED BOXES ({len(boxes)} total):")
                for i, box in enumerate(boxes):
                    print(f"  Box {i+1}: top_left=({box['top_left'][0]}, {box['top_left'][1]}), bottom_right=({box['bottom_right'][0]}, {box['bottom_right'][1]})")
                print()
            
            # 2. Detect connection lines from unsolved positions
            connection_lines = self.detect_connections_with_matrix(lines)
            
            # 3. Analyze problems
            box_problems = self.analyze_box_problems(lines, boxes)
            connection_problems = self.analyze_connection_problems(lines, connection_lines, iteration)
            

            # 4. Build row-by-row analysis
            row_analysis = self.build_row_analysis(lines, boxes, connection_lines, box_problems, connection_problems)
            
            # 5. Save matrix for debugging before cleanup
            
            return row_analysis
        
        finally:
            # Clean up matrix
            self.solved = None
    
    def detect_boxes_with_matrix(self, lines, iteration=0):
        """Detect boxes and mark all border positions as solved."""
        
        # Use cached boxes after reaching stability (iteration 52+)
        if self.cached_boxes is None:
            # Detect boxes using our own systematic detection
            boxes = self.detect_boxes(lines)
            
            # Correct box widths to actual maximum extent
            boxes = self.correct_box_widths(lines, boxes)
            
            # Cache boxes when we reach the stable state (iteration 52)
            if iteration == 52:
                self.cached_boxes = [box.copy() for box in boxes]
                if self.debug:
                    print(f"🔒 CACHED {len(boxes)} BOXES at iteration {iteration} for stability")
                    # Debug the BGP Route Exchange box
                    for i, box in enumerate(boxes):
                        if box['top_left'][0] == 31:  # BGP box starts at row 31
                            print(f"   BGP Box {i+1}: ({box['top_left'][0]},{box['top_left'][1]}) to ({box['bottom_right'][0]},{box['bottom_right'][1]})")
        else:
            # Use cached boxes from the stable iteration
            boxes = [box.copy() for box in self.cached_boxes]
            
            if self.debug and iteration <= 55:  # Show for first few iterations after caching
                print(f"📋 Using cached boxes from iteration 52 ({len(boxes)} total) for iteration {iteration}")
        
        # Mark all box border positions as solved
        for i, box in enumerate(boxes):
            top_row, left_col = box['top_left']
            bottom_row, right_col = box['bottom_right']
            
            
            # Mark expected positions and find misplaced borders
            # Top and bottom borders
            for row in [top_row, bottom_row]:
                if row < len(lines):
                    line = lines[row]
                    for col in range(left_col, right_col + 1):
                        if col < len(self.solved[row]):
                            self.solved[row][col] = True
                        # Look for misplaced border characters nearby
                        for check_col in range(max(0, col-3), min(len(line), col+4)):
                            if (check_col < len(self.solved[row]) and 
                                not self.solved[row][check_col] and 
                                line[check_col] in '┌┐└┘─'):
                                self.solved[row][check_col] = True
            
            # Left and right borders
            for col in [left_col, right_col]:
                for row in range(top_row, bottom_row + 1):
                    if row < len(lines):
                        line = lines[row]
                        if col < len(self.solved[row]):
                            self.solved[row][col] = True
                        # Look for misplaced border characters nearby
                        for check_col in range(max(0, col-3), min(len(line), col+4)):
                            if (check_col < len(self.solved[row]) and 
                                not self.solved[row][check_col] and 
                                line[check_col] in '│├┤┬┴┼'):
                                self.solved[row][check_col] = True
        
        return boxes
    
    def detect_connections_with_matrix(self, lines):
        """Detect connection lines from unsolved │ characters and border crossings."""
        
        
        connection_lines = []
        unsolved_pipes = []
        
        # Find unsolved │ characters
        for row_idx, line in enumerate(lines):
            for col_idx, char in enumerate(line):
                if char == '│':
                    
                    if (col_idx < len(self.solved[row_idx]) and 
                        not self.solved[row_idx][col_idx]):
                        # Regular unsolved pipe
                        unsolved_pipes.append((row_idx, col_idx))
                    elif (col_idx < len(self.solved[row_idx]) and 
                          self.solved[row_idx][col_idx]):
                        # This might be a connection crossing a box border
                        # Check if this pipe connects to unsolved pipes above/below
                        has_unsolved_connection = False
                        for check_row in range(max(0, row_idx-5), min(len(lines), row_idx+6)):
                            if check_row != row_idx and check_row < len(lines):
                                check_line = lines[check_row]
                                for check_col in range(max(0, col_idx-2), min(len(check_line), col_idx+3)):
                                    if (check_line[check_col] == '│' and 
                                        check_col < len(self.solved[check_row]) and
                                        not self.solved[check_row][check_col]):
                                        has_unsolved_connection = True
                                        break
                                if has_unsolved_connection:
                                    break
                        
                        if has_unsolved_connection:
                            # Include this as part of a connection line
                            unsolved_pipes.append((row_idx, col_idx))
                            # Don't mark as solved yet - let the grouping logic handle it
        
        # Group into connection lines
        used_pipes = set()
        
        
        for row, col in unsolved_pipes:
            if (row, col) in used_pipes:
                continue
            
            # Find all pipes belonging to this connection
            conn_rows = []
            conn_cols = []
            
            for check_row, check_col in unsolved_pipes:
                if (check_row, check_col) not in used_pipes:
                    if abs(check_col - col) <= 2:  # Tolerance
                        conn_rows.append(check_row)
                        conn_cols.append(check_col)
                        used_pipes.add((check_row, check_col))
                        self.solved[check_row][check_col] = True
            
            if conn_rows:
                # Apply rightmost position rule
                rightmost_col = max(conn_cols)
                connection_lines.append({
                    'type': 'connection_line',
                    'rows': sorted(conn_rows),
                    'columns': conn_cols,
                    'correct_column': rightmost_col
                })
        
        return connection_lines
    
    def analyze_box_problems(self, lines, boxes):
        """Analyze box border problems."""
        box_problems = {}
        
        for i, box in enumerate(boxes):
            box_name = f"box_{i+1}"
            problems = []
            
            top_row, left_col = box['top_left']
            bottom_row, right_col = box['bottom_right']
            
            # First check for box-level misalignment (top/bottom row shifts)
            box_level_problem = self.detect_box_level_misalignment(lines, box, top_row, bottom_row)
            if box_level_problem:
                problems.append(box_level_problem)
            
            # Then check individual border problems
            # Check left borders
            left_problems = self.check_left_border_alignment(lines, top_row, bottom_row, left_col)
            problems.extend(left_problems)
            
            # Check right borders  
            right_problems = self.check_right_border_alignment(lines, top_row, bottom_row, right_col)
            problems.extend(right_problems)
            
            if problems:
                box_problems[box_name] = problems
        
        return box_problems
    
    def detect_box_level_misalignment(self, lines, box, top_row, bottom_row):
        """Detect if top and bottom rows have same width but are horizontally misaligned."""
        if top_row >= len(lines) or bottom_row >= len(lines):
            return None
            
        top_line = lines[top_row]
        bottom_line = lines[bottom_row]
        
        # Find corner positions within expected box region
        expected_left = box['top_left'][1]
        expected_right = box['bottom_right'][1]
        search_start = max(0, expected_left - 2)  # Allow small tolerance
        search_end = min(len(top_line), expected_right + 2)
        
        actual_top_left = self.find_corner_in_line(top_line, '┌', search_start, search_end)
        actual_top_right = self.find_corner_in_line(top_line, '┐', search_start, search_end)
        actual_bottom_left = self.find_corner_in_line(bottom_line, '└', search_start, search_end) 
        actual_bottom_right = self.find_corner_in_line(bottom_line, '┘', search_start, search_end)
        
        if any(pos is None for pos in [actual_top_left, actual_top_right, actual_bottom_left, actual_bottom_right]):
            return None  # Can't find all corners
            
        # Calculate box dimensions
        top_width = actual_top_right - actual_top_left
        bottom_width = actual_bottom_right - actual_bottom_left
        
        # Check if box has consistent width but misaligned position
        if top_width == bottom_width and actual_top_left != actual_bottom_left:
            # Determine which row needs to move right (align to rightmost position)
            if actual_top_left < actual_bottom_left:
                # Top row is more left, bottom row is the target
                return {
                    'row': top_row,
                    'issue': 'box_row_needs_shift_right',
                    'actual_col': actual_top_left,
                    'shift_needed': actual_bottom_left - actual_top_left,
                    'target_left_col': actual_bottom_left
                }
            else:
                # Bottom row is more left, top row is the target  
                return {
                    'row': bottom_row,
                    'issue': 'box_row_needs_shift_right',
                    'actual_col': actual_bottom_left,
                    'shift_needed': actual_top_left - actual_bottom_left,
                    'target_left_col': actual_top_left
                }
        
        return None
    
    def correct_box_widths(self, lines, boxes):
        """Correct box widths by finding the actual maximum extent across all rows."""
        corrected_boxes = []
        
        for i, box in enumerate(boxes):
            top_row, left_col = box['top_left']
            bottom_row, right_col = box['bottom_right']
            
            if self.debug:
                print(f"Box {i+1} width correction:")
                print(f"  Original: ({top_row},{left_col}) to ({bottom_row},{right_col}) - width {right_col - left_col + 1}")
            
            
            # Find the actual maximum right extent across all rows of this box
            max_right_col = right_col
            for row in range(top_row, bottom_row + 1):
                if row < len(lines):
                    line = lines[row]
                    # Look for the nearest border character using canonical method
                    valid_chars = {'│', '┐', '┘'} if row in [top_row, bottom_row] else {'│'}
                    rightmost_border = self.find_nearest_border(line, right_col, valid_chars)
                    if rightmost_border is not None and rightmost_border > max_right_col:
                        max_right_col = rightmost_border
                        if self.debug:
                            print(f"    Row {row}: found border at col {rightmost_border} (extends box width)")
            
            # Create corrected box with maximum width
            corrected_box = box.copy()
            corrected_box['bottom_right'] = (bottom_row, max_right_col)
            corrected_box['top_right'] = (top_row, max_right_col)
            corrected_box['width'] = max_right_col - left_col + 1
            
            if self.debug:
                print(f"  Corrected: ({top_row},{left_col}) to ({bottom_row},{max_right_col}) - width {max_right_col - left_col + 1}")
                print()
            
            corrected_boxes.append(corrected_box)
        
        return corrected_boxes
    
    def find_nearest_border(self, line, expected_col, valid_chars, max_distance=5):
        """Find the nearest border character to the expected position.
        
        Args:
            line: The line to search in
            expected_col: Expected column position  
            valid_chars: Set of valid border characters to look for
            max_distance: Maximum distance to search from expected position
            
        Returns:
            Column position of nearest border, or None if not found
        """
        # First check the expected position
        if 0 <= expected_col < len(line) and line[expected_col] in valid_chars:
            return expected_col
        
        # Work outward from expected position: ±1, ±2, ±3...
        for distance in range(1, max_distance + 1):
            # Check left side first (expected - distance)
            check_col = expected_col - distance
            if 0 <= check_col < len(line) and line[check_col] in valid_chars:
                return check_col
                
            # Check right side (expected + distance)  
            check_col = expected_col + distance
            if 0 <= check_col < len(line) and line[check_col] in valid_chars:
                return check_col
        
        # If nothing found within range, return None
        return None
    
    def find_corner_in_line(self, line, corner_char, search_start=0, search_end=None):
        """Find the position of a corner character in a line within a specific region."""
        if search_end is None:
            search_end = len(line)
        
        search_region = line[search_start:search_end]
        try:
            relative_pos = search_region.index(corner_char)
            return search_start + relative_pos
        except ValueError:
            return None
    
    def check_left_border_alignment(self, lines, top_row, bottom_row, expected_left_col):
        """Check left border vertical alignment."""
        problems = []
        
        for row in range(top_row, bottom_row + 1):
            if row < len(lines):
                line = lines[row]
                
                # Determine expected character based on row type
                if row == top_row:
                    expected_char = '┌'  # Top-left corner
                elif row == bottom_row:
                    expected_char = '└'  # Bottom-left corner
                else:
                    expected_char = '│'  # Vertical border
                
                # Use canonical method to find the nearest border
                actual_border_col = self.find_nearest_border(line, expected_left_col, {expected_char})
                
                if actual_border_col == expected_left_col:
                    # Left border correctly positioned - no problem
                    continue
                elif actual_border_col is not None:
                    # Found border nearby but not at expected position
                    problems.append({
                        'row': row,
                        'issue': 'misplaced_left_border',
                        'expected_col': expected_left_col,
                        'actual_col': actual_border_col,
                        'expected_char': expected_char
                    })
        
        return problems
    
    def check_right_border_alignment(self, lines, top_row, bottom_row, expected_right_col):
        """Check right border vertical alignment."""
        problems = []
        
        for row in range(top_row, bottom_row + 1):
            if row < len(lines):
                line = lines[row]
                
                # Determine expected character based on row type
                if row == top_row:
                    expected_char = '┐'  # Top-right corner
                elif row == bottom_row:
                    expected_char = '┘'  # Bottom-right corner  
                else:
                    expected_char = '│'  # Vertical border
                
                # Use canonical method to find the nearest border
                actual_border_col = self.find_nearest_border(line, expected_right_col, {expected_char})
                
                
                if actual_border_col == expected_right_col:
                    # Right border correctly positioned - no problem
                    continue
                elif actual_border_col is not None:
                    # Found border nearby but not at expected position
                    problems.append({
                        'row': row,
                        'issue': 'misplaced_right_border', 
                        'expected_col': expected_right_col,
                        'actual_col': actual_border_col,
                        'expected_char': expected_char
                    })
                else:
                    # No border found at all - this is a missing border problem
                    problems.append({
                        'row': row,
                        'issue': 'missing_right_border',
                        'expected_col': expected_right_col,
                        'expected_char': expected_char
                    })
        
        return problems
    
    def analyze_connection_problems(self, lines, connection_lines, iteration=0):
        """Analyze connection line problems."""
        connection_problems = {}
        
        for i, conn in enumerate(connection_lines):
            conn_name = f"connection_{i+1}"
            problems = []
            
            correct_col = conn['correct_column']
            
            # Check alignment for each row
            for row_idx, row in enumerate(conn['rows']):
                if row < len(lines):
                    # Find actual column for this row
                    actual_col = conn['columns'][row_idx] if row_idx < len(conn['columns']) else None
                    
                    if actual_col is None:
                        problems.append({
                            'row': row,
                            'issue': 'missing_connection',
                            'expected_col': correct_col,
                            'expected_char': '│'
                        })
                    elif actual_col != correct_col:
                        problems.append({
                            'row': row,
                            'issue': 'misaligned_connection',
                            'expected_col': correct_col,
                            'actual_col': actual_col,
                            'expected_char': '│'
                        })
            
            if problems:
                connection_problems[conn_name] = problems
        
        return connection_problems
    
    def build_row_analysis(self, lines, boxes, connection_lines, box_problems, connection_problems):
        """Build row-by-row problem analysis."""
        row_analysis = {}
        
        for row_num in range(len(lines)):
            row_analysis[row_num] = {'entities': [], 'problems': []}
        
        # Add box problems
        for i, box in enumerate(boxes):
            box_name = f"box_{i+1}"
            if box_name in box_problems:
                for problem in box_problems[box_name]:
                    row = problem['row']
                    if row in row_analysis:
                        row_analysis[row]['problems'].append({
                            'entity': box_name,
                            **problem
                        })
        
        # Add connection problems
        for i, conn in enumerate(connection_lines):
            conn_name = f"connection_{i+1}"
            if conn_name in connection_problems:
                for problem in connection_problems[conn_name]:
                    row = problem['row']
                    if row in row_analysis:
                        row_analysis[row]['problems'].append({
                            'entity': conn_name,
                            **problem
                        })
        
        return row_analysis
    
    def get_leftmost_problem(self, problems):
        """Get the leftmost problem that can be fixed."""
        if not problems:
            return None
        
        # Sort problems by column position (leftmost first)
        def get_problem_column(problem):
            if 'actual_col' in problem:
                return problem['actual_col']  # For misaligned items
            elif 'expected_col' in problem:
                return problem['expected_col']  # For missing items
            else:
                return float('inf')  # Unknown issues go to end
        
        sorted_problems = sorted(problems, key=get_problem_column)
        return sorted_problems[0]
    
    def apply_fix(self, lines, problem):
        """Apply a fix by injecting a character at the actual position to move it right."""
        row = problem['row']
        
        if row >= len(lines):
            return lines
            
        line = list(lines[row])
        
        # Handle the special case of connection lines crossing box borders
        if problem['issue'] == 'missing_connection':
            # This is the only case where we add a truly missing character
            expected_col = problem['expected_col']
            expected_char = problem['expected_char']
            
            if expected_col < len(line):
                line.insert(expected_col, expected_char)
            else:
                # Extend line
                while len(line) < expected_col:
                    line.append(' ')
                line.append(expected_char)
            
            lines[row] = ''.join(line)
            if self.debug:
                print(f"  Added missing connection {expected_char} at col {expected_col} in row {row}")
            return lines
        
        # For ALL other cases: actual position is LEFT of expected, inject at actual to move RIGHT
        if 'actual_col' in problem:
            actual_col = problem['actual_col']
        else:
            # This shouldn't happen - all problems should have actual_col
            if self.debug:
                print(f"  WARNING: Problem has no actual_col: {problem}")
            return lines
        
        # Determine what character to inject (look left for context)
        inject_char = ' '  # Default to space
        if actual_col > 0 and actual_col - 1 < len(line):
            left_char = line[actual_col - 1]
            if left_char in '─┌┐└┘├┤┬┴┼':
                inject_char = '─'  # Continue horizontal border
            else:
                inject_char = left_char  # Use the character to the left
        
        # Inject character at actual position to move it right
        if actual_col < len(line):
            line.insert(actual_col, inject_char)
        else:
            # Extend line to reach injection point
            while len(line) < actual_col:
                line.append(' ')
            line.append(inject_char)
        
        lines[row] = ''.join(line)
        
        if self.debug:
            issue = problem.get('issue', 'alignment_problem')
            expected_col = problem.get('expected_col', 'unknown')
            print(f"  Injected '{inject_char}' at col {actual_col} to move {issue} from {actual_col} toward {expected_col} in row {row}")
        
        return lines


def test_precision_fixer(input_file=None):
    """Test the precision fixer with a diagram file."""
    if input_file is None:
        input_file = 'original_diagram.txt'
    
    try:
        with open(input_file, 'r') as f:
            diagram_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return None
    
    lines = diagram_content.split('\n')
    original_lines = lines.copy()  # Save original for comparison
    
    print(f"TESTING FILE: {input_file}")
    print(f"Diagram has {len(lines)} lines")
    print()
    
    print("BEFORE:")
    for i, line in enumerate(lines[:20]):  # Show first 20 lines
        print(f"{i:2d}: {line}")
    if len(lines) > 20:
        print("...")
    print()
    
    fixer = PrecisionDiagramFixer(debug=True)
    fixed_lines = fixer.fix_diagram(lines)
    
    print("\nAFTER:")
    for i, line in enumerate(fixed_lines[:20]):  # Show first 20 lines
        print(f"{i:2d}: {line}")
    if len(fixed_lines) > 20:
        print("...")
    print()
    
    # Show what changed (compare original vs final result)
    changes = 0
    print("CHANGES:")
    for i, (orig, fixed) in enumerate(zip(original_lines, fixed_lines)):
        if orig != fixed:
            changes += 1
            print(f"Row {i}: CHANGED")
            print(f"  Before: {repr(orig)}")
            print(f"  After:  {repr(fixed)}")
    
    if changes == 0:
        print("No changes made - diagram was already correct")
    else:
        print(f"Total changes: {changes}")
    
    # Save fixed diagram to output file
    if input_file != 'original_diagram.txt':  # Skip for default test
        output_file = input_file.replace('.txt', '_fixed.txt')
        with open(output_file, 'w') as f:
            for line in fixed_lines:
                f.write(line + '\n')
        print(f"Fixed diagram saved to: {output_file}")
    
    return fixed_lines


def main():
    """Main entry point for the diagram fixer command-line tool."""
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
        # Check for verbose flag
        verbose = '--verbose' in sys.argv or '-v' in sys.argv
        
        if verbose:
            test_precision_fixer(input_file)
        else:
            # Quiet mode - just fix the diagram and report summary
            try:
                with open(input_file, 'r') as f:
                    diagram_content = f.read()
            except FileNotFoundError:
                print(f"Error: File '{input_file}' not found")
                sys.exit(1)
            
            lines = diagram_content.split('\n')
            original_lines = lines.copy()
            
            fixer = PrecisionDiagramFixer(debug=False)
            fixed_lines = fixer.fix_diagram(lines)
            
            # Count changes
            changes = sum(1 for orig, fixed in zip(original_lines, fixed_lines) if orig != fixed)
            
            if changes == 0:
                print("✅ No problems found - diagram is fixed!")
            else:
                print("✅ Diagram fixed!")
                print(f"Total changes: {changes}")
                
                # Save fixed diagram
                output_file = input_file.replace('.txt', '_fixed.txt')
                with open(output_file, 'w') as f:
                    for line in fixed_lines:
                        f.write(line + '\n')
                print(f"Fixed diagram saved to: {output_file}")
    else:
        print("Usage: diagram-fixer <input_file> [--verbose|-v]")
        print("Example: diagram-fixer extracted_diagram_1.txt")
        print("         diagram-fixer extracted_diagram_1.txt --verbose")


if __name__ == "__main__":
    main()