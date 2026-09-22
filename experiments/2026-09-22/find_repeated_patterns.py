#!/usr/bin/env python3
"""
Find any 8-length contiguous pattern that appears more than once across
the transcription blocks. This could reveal a non‑random repetition.
"""

import sys, json, pathlib, collections

def load_transcription_blocks(path):
    """Read the rtdk transcription file and split into blocks by '%' delimiter."""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('\n%')
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def length_sequence(block):
    """Return list of word‑length values for a block."""
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    lengths = []
    for w in raw_words:
        # Map each rune to its numeric value
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        lengths.append(len(vals))
    return lengths

def find_repeated_8grams(path):
    """Search for any 8-length contiguous pattern that appears more than once across blocks."""
    blocks = load_transcription_blocks(path)
    # Map pattern tuple -> list of (block_idx, start_pos)
    pattern_positions = collections.defaultdict(list)
    for idx, block in enumerate(blocks):
        lengths = length_sequence(block)
        # Slide an 8‑long window
        for i in range(len(lengths) - 7):
            gram = tuple(lengths[i:i+8])
            pattern_positions[gram].append((idx, i))
    # Find grams that occur more than once
    repeated = {gram:poslist for gram, poslist in pattern_positions.items() if len(poslist) > 1}
    if not repeated:
        return []  # none found
    # Return list of (gram, positions)
    return list(repeated.items())

def main():
    path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    repeats = find_repeated_8grams(path)
    if not repeats:
        print('No repeated 8‑length patterns found.')
        return
    print(f'Found {len(repeats)} repeated 8‑length patterns.')
    for gram, poslist in repeats:
        print(f'Pattern {gram} appears in blocks at positions: {poslist}')
        # Show first occurrence details
        b_idx, start = poslist[0]
        block = load_transcription_blocks(path)[b_idx]
        lengths = length_sequence(block)
        gram_lengths = lengths[poslist[0][1]:poslist[0][1]+8]
        print(f'  First occurrence in block {b_idx} (length‑seq start {poslist[0][1]}): {gram_lengths}')
    # Output JSON for downstream processing
    report_path = pathlib.Path('experiments/2026-09-22/repeated_patterns.json')
    json.dump({'repeated_grams': repeats}, pathlib.Path(report_path).open('w'), indent=2)
    print(f'Report written to {pathlib.Path(report_path)}')

if __name__ == '__main__':
    main()