#!/usr/bin/env python3
"""
Test diagonal and spiral orderings of the page 5 magic square as Vigenère keys
across all 56 unsolved pages. Compare dictionary hit rates against random control.
"""

import sys, json, pathlib, random
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import *

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('\n%')
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def get_page_vals(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    flat_vals = []
    for w in raw_words:
        flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
    return flat_vals

def diagonal_order(square):
    """Return values in diagonal order (top-left to bottom-right)."""
    n = len(square)
    vals = []
    for i in range(n):
        vals.append(square[i][i])
    return vals

def anti_diagonal_order(square):
    """Return values in anti-diagonal order (top-right to bottom-left)."""
    n = len(square)
    vals = []
    for i in range(n):
        vals.append(square[i][n-1-i])
    return vals

def spiral_order(square):
    """Return values in clockwise spiral order starting from top-left."""
    n = len(square)
    if n == 0:
        return []
    vals = []
    top, bottom = 0, n-1
    left, right = 0, n-1
    while top <= bottom and left <= right:
        # top row
        for j in range(left, right+1):
            vals.append(square[top][j])
        top += 1
        # right column
        for i in range(top, bottom+1):
            vals.append(square[i][right])
        right -= 1
        # bottom row
        if top <= bottom:
            for j in range(right, left-1, -1):
                vals.append(square[bottom][j])
            bottom -= 1
        # left column
        if left <= right:
            for i in range(bottom, top-1, -1):
                vals.append(square[i][left])
            left += 1
    return vals

def decode_key(cipher_vals, key_vals, shift_up=True):
    """Vigenère decode: subtract key if shift_up=True, otherwise add."""
    out = []
    for i, v in enumerate(cipher_vals):
        k = key_vals[i % len(key_vals)]
        out.append((v - k) % 29 if shift_up else (v + k) % 29)
    return out

def dict_score(candidate_words, wordset):
    return sum(1 for w in candidate_words if w in wordset)

def random_control_score(vals, word_lengths, wordset, seed=42):
    rng = random.Random(seed)
    shuffled = vals[:]
    rng.shuffle(shuffled)
    words = []
    start = 0
    for length in word_lengths:
        chunk = shuffled[start:start+length]
        start += length
        letter_chunk = ''.join(chr((c % 26) + ord('A')) for c in chunk)
        words.append(letter_chunk)
    return dict_score(words, wordset)

def main():
    # Load transcription blocks
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    # Exclude solved pages: block 55 (page 73) and block 56 (page 74)
    unsolved_blocks = blocks[:55]  # blocks 0-54 = pages 17-71 (56 pages)
    
    # Page 5 magic square values (from ruled-out.md)
    square = [
        [272, 138, 341, 131, 151],
        [366, 199, 130, 320, 18],
        [226, 245, 91, 245, 226],
        [18, 320, 130, 199, 366],
        [151, 131, 341, 138, 272]
    ]
    
    # Generate candidate key streams
    keys = {
        'diagonal': diagonal_order(square),
        'anti_diagonal': anti_diagonal_order(square),
        'spiral': spiral_order(square)
    }
    
    # Load dictionary
    try:
        wordset = set()
        with open('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/words_alpha.txt', encoding='utf-8') as f:
            for line in f:
                w = line.strip().upper()
                if len(w) >= 3:
                    wordset.add(w)
    except FileNotFoundError:
        print('Dictionary file not found')
        return
    
    results = {}
    for key_name, key_vals in keys.items():
        print(f"\n=== Testing key: {key_name} ===")
        for shift_up in (True, False):
            total_hits = 0
            total_words = 0
            for block in unsolved_blocks:
                flat_vals = get_page_vals(block)
                if not flat_vals:
                    continue
                # Get word lengths for this block
                clean = block.replace('/', '').replace('\n', '')
                raw_words = [w for w in clean.split('-') if w]
                word_lengths = [len([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]) for w in raw_words]
                # Decode
                decoded_vals = decode_key(flat_vals, key_vals, shift_up=shift_up)
                # Convert to words
                words = []
                start = 0
                for length in word_lengths:
                    chunk = decoded_vals[start:start+length]
                    start += length
                    word = ''.join(VAL_TO_LATIN[c % 29] for c in chunk)
                    words.append(word)
                # Score
                hits = dict_score(words, wordset)
                total_hits += hits
                total_words += len(words)
            rate = total_hits / total_words if total_words else 0
            # Random control
            ctrl_vals = []
            for block in unsolved_blocks:
                flat_vals = get_page_vals(block)
                if flat_vals:
                    ctrl_vals.extend(flat_vals)
            ctrl_rate = random_control_score(ctrl_vals, [len(unsolved_blocks)], wordset)
            direction = 'up' if shift_up else 'down'
            print(f"  Shift {direction}: {total_hits}/{total_words} = {rate:.4f} (control: {ctrl_rate})")
            results[f"{key_name}_{direction}"] = {
                'hits': total_hits,
                'total_words': total_words,
                'rate': rate,
                'control_rate': ctrl_rate
            }
    
    # Save results
    report_path = pathlib.Path('experiments/2026-09-22/magic_square_test.json')
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nReport written to {report_path}")

if __name__ == '__main__':
    main()