#!/usr/bin/env python3
"""
Test "numbers as direction" hypothesis from Open-Leads #4.
Interpret Gematria values as turtle graphics / grid navigation instructions.
"""

import sys, json, pathlib, random
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import RUNE_TO_VAL, VAL_TO_LATIN, ALPHABET_SIZE

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('\n%')
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def get_page_vals(block):
    """Return flat list of rune values for a block."""
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    flat_vals = []
    for w in raw_words:
        flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
    return flat_vals

def turtle_walk(vals, grid_size=5):
    """
    Interpret values as turtle graphics directions.
    Map each value to a direction (mod 4):
      0: right, 1: down, 2: left, 3: up
    Walk on a grid, recording visited cells.
    """
    x, y = 0, 0
    visited = set()
    visited.add((x, y))
    
    for v in vals:
        direction = v % 4
        if direction == 0:  # right
            x += 1
        elif direction == 1:  # down
            y += 1
        elif direction == 2:  # left
            x -= 1
        else:  # up
            y -= 1
        # Wrap around if needed
        x = x % grid_size
        y = y % grid_size
        visited.add((x, y))
    
    return visited

def grid_to_string(visited, grid_size=5):
    """Convert visited grid cells to a string representation."""
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y in visited:
        grid[y][x] = 'X'
    return '\n'.join(''.join(row) for row in grid)

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    
    # Test on a few unsolved pages
    test_blocks = blocks[:10]  # first 10 pages
    
    print("=== Turtle Graphics Test ===")
    print("Interpreting rune values as directions (mod 4): 0=right, 1=down, 2=left, 3=up")
    print()
    
    for idx, block in enumerate(test_blocks):
        vals = get_page_vals(block)
        if not vals:
            continue
        visited = turtle_walk(vals, grid_size=5)
        print(f"Page {idx+1} (block {idx}): {len(vals)} runes, {len(visited)} unique cells visited")
        print(grid_to_string(visited, grid_size=5))
        print()
    
    # Also test with different grid sizes
    print("\n=== Different Grid Sizes ===")
    vals = get_page_vals(blocks[0])
    for size in [3, 4, 5, 6, 7, 8]:
        visited = turtle_walk(vals, grid_size=size)
        print(f"Grid size {size}: {len(visited)} unique cells out of {size*size}")
    
    # Try interpreting values as offsets into a magic square
    print("\n=== Magic Square Indexing Test ===")
    # Page 5 magic square values
    square = [
        [272, 138, 341, 131, 151],
        [366, 199, 130, 320, 18],
        [226, 245, 91, 245, 226],
        [18, 320, 130, 199, 366],
        [151, 131, 341, 138, 272]
    ]
    
    # Use rune values mod 5 to index into the square
    vals = get_page_vals(blocks[0])
    indices = [(v % 5, v // 5 % 5) for v in vals[:25]]  # first 25 values
    print(f"First 25 rune values mod 5 indexing into 5x5 magic square:")
    for i, (row, col) in enumerate(indices):
        if row < 5 and col < 5:
            print(f"  {vals[i]} -> ({row},{col}) = {square[row][col]}")
        else:
            print(f"  {vals[i]} -> ({row},{col}) = OUT OF RANGE")

if __name__ == '__main__':
    main()