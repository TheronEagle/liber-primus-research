#!/usr/bin/env python3
"""
Deep analysis of the ACTUAL matching positions from corrected Open-Leads #0.
1. Pattern [6,7,6,3,6,4,3,3] at:
   - Block 19 (page ~36), local word 47
   - Block 44 (page ~61), local word 12
2. Pattern [5,4,7,3,6,3,7,4] at:
   - Block 40 (page ~57), local word 42 (only 1 occurrence globally!)
3. Extract rune sequences, compare values, try autokey/running-key tests
"""

import sys, json, pathlib
from collections import defaultdict
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import RUNE_TO_VAL, VAL_TO_LATIN, ALPHABET_SIZE

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('\n%')
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def get_words_and_values(block):
    """Return list of (rune_string, values, length) for each word in block."""
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    result = []
    for w in raw_words:
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        result.append((w, vals, len(vals)))
    return result

def get_word_lengths(block):
    return [item[2] for item in get_words_and_values(block)]

def vals_to_letters(vals):
    return ''.join(VAL_TO_LATIN[v % ALPHABET_SIZE] for v in vals)

def dict_score(candidate_words, wordset):
    return sum(1 for w in candidate_words if w in wordset)

def test_autokey(flat1, flat2, wordset):
    """Test both directions of autokey between two flat value lists."""
    if len(flat1) == 0 or len(flat2) == 0:
        return None
    
    # Use shorter as key, longer as ciphertext
    if len(flat1) <= len(flat2):
        key, cipher = flat1, flat2
        key_label, cipher_label = "1->2", "2"
    else:
        key, cipher = flat2, flat1
        key_label, cipher_label = "2->1", "1"
    
    # Extend key to match ciphertext length
    extended_key = (key * ((len(cipher) // len(key)) + 1))[:len(cipher)]
    
    # Shift up (subtract key)
    decoded_up = [(c - k) % 29 for c, k in zip(cipher, extended_key)]
    # Shift down (add key)
    decoded_down = [(c + k) % 29 for c, k in zip(cipher, extended_key)]
    
    # Convert to letters for inspection
    up_letters = ''.join(VAL_TO_LATIN[v % 29] for v in decoded_up)
    down_letters = ''.join(VAL_TO_LATIN[v % 29] for v in decoded_down)
    
    return {
        'key_label': key_label,
        'up_letters': up_letters,
        'down_letters': down_letters,
        'up_values': decoded_up,
        'down_values': decoded_down
    }

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    
    # Load dictionary
    try:
        wordset = set()
        with open('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/words_alpha.txt', encoding='utf-8') as f:
            for line in f:
                w = line.strip().upper()
                if len(w) >= 3:
                    wordset.add(w)
    except FileNotFoundError:
        wordset = set()
        print("Dictionary not loaded")
    
    # ============================================================
    # PATTERN 1: [6,7,6,3,6,4,3,3] at Block 19 word 47 and Block 44 word 12
    # ============================================================
    print("=" * 70)
    print("PATTERN 1: [6,7,6,3,6,4,3,3]")
    print("=" * 70)
    
    block19 = blocks[19]  # page ~36
    block44 = blocks[44]  # page ~61
    
    b19_words = get_words_and_values(block19)
    b44_words = get_words_and_values(block44)
    b19_lens = get_word_lengths(block19)
    b44_lens = get_word_lengths(block44)
    
    w19_idx = 46  # 0-indexed for word 47
    w44_idx = 11  # 0-indexed for word 12
    
    print(f"\nBlock 19 (page ~36): {len(b19_words)} words")
    print(f"Block 44 (page ~61): {len(b44_words)} words")
    
    # Verify the pattern
    seq19 = b19_lens[w19_idx:w19_idx+8] if w19_idx + 8 <= len(b19_lens) else []
    seq44 = b44_lens[w44_idx:w44_idx+8] if w44_idx + 8 <= len(b44_lens) else []
    
    print(f"Block 19 word 47-54: {seq19}")
    print(f"Block 44 word 12-19: {seq44}")
    print(f"Target: [6,7,6,3,6,4,3,3]")
    print(f"Block 19 matches: {seq19 == [6,7,6,3,6,4,3,3]}")
    print(f"Block 44 matches: {seq44 == [6,7,6,3,6,4,3,3]}")
    
    # Extract the 8-word rune sequences
    if w19_idx + 8 <= len(b19_words) and w44_idx + 8 <= len(b44_words):
        seq19_runes = [b19_words[i][0] for i in range(w19_idx, w19_idx+8)]
        seq19_vals = [b19_words[i][1] for i in range(w19_idx, w19_idx+8)]
        seq44_runes = [b44_words[i][0] for i in range(w44_idx, w44_idx+8)]
        seq44_vals = [b44_words[i][1] for i in range(w44_idx, w44_idx+8)]
        
        print(f"\nBlock 19 words 47-54 (runes):")
        for i, (rune, vals) in enumerate(zip(seq19_runes, seq19_vals)):
            print(f"  Word {w19_idx+i+1}: {rune} -> {vals} (len={len(vals)})")
        
        print(f"\nBlock 44 words 12-19 (runes):")
        for i, (rune, vals) in enumerate(zip(seq44_runes, seq44_vals)):
            print(f"  Word {w44_idx+i+1}: {rune} -> {vals} (len={len(vals)})")
        
        # Compare values directly
        print(f"\n--- Direct Value Comparison ---")
        all_match = True
        for i in range(8):
            if seq19_vals[i] == seq44_vals[i]:
                print(f"  Position {i}: MATCH")
            else:
                print(f"  Position {i}: DIFFERENT")
                print(f"    Block 19: {seq19_vals[i]}")
                print(f"    Block 44: {seq44_vals[i]}")
                all_match = False
        
        if all_match:
            print("  >>> ALL 8 WORDS HAVE IDENTICAL VALUES! <<<")
        else:
            print("  Values differ")
        
        # Autokey tests
        flat19 = [v for vals in seq19_vals for v in vals]
        flat44 = [v for vals in seq44_vals for v in vals]
        
        print(f"\nBlock 19 flat ({len(flat19)} vals): {flat19}")
        print(f"Block 44 flat ({len(flat44)} vals): {flat44}")
        
        result = test_autokey(flat19, flat44, set())
        if result:
            print(f"\nAutokey {result['key_label']}:")
            print(f"  Shift up:   {result['up_letters']}")
            print(f"  Shift down: {result['down_letters']}")
    
    # ============================================================
    # PATTERN 2: [5,4,7,3,6,3,7,4] at Block 40 word 42 (only 1 global occurrence!)
    # ============================================================
    print("\n" + "=" * 70)
    print("PATTERN 2: [5,4,7,3,6,3,7,4] - UNIQUE GLOBAL OCCURRENCE!")
    print("=" * 70)
    
    block40 = blocks[40]  # page ~57
    b40_words = get_words_and_values(block40)
    b40_lens = get_word_lengths(block40)
    
    w40_idx = 41  # 0-indexed for word 42
    
    print(f"\nBlock 40 (page ~57): {len(b40_words)} words")
    seq40 = b40_lens[w40_idx:w40_idx+8] if w40_idx + 8 <= len(b40_lens) else []
    print(f"Block 40 word 42-49: {seq40}")
    print(f"Target: [5,4,7,3,6,3,7,4]")
    print(f"Matches: {seq40 == [5,4,7,3,6,3,7,4]}")
    
    if w40_idx + 8 <= len(b40_words):
        seq40_runes = [b40_words[i][0] for i in range(w40_idx, w40_idx+8)]
        seq40_vals = [b40_words[i][1] for i in range(w40_idx, w40_idx+8)]
        
        print(f"\nBlock 40 words 42-49 (runes):")
        for i, (rune, vals) in enumerate(zip(seq40_runes, seq40_vals)):
            print(f"  Word {w40_idx+i+1}: {rune} -> {vals} (len={len(vals)})")
        
        # Since this pattern occurs only ONCE globally, it's extremely significant
        # Try using it as a key against other pages
        print(f"\n--- Testing unique pattern as key against other pages ---")
        flat40 = [v for vals in seq40_vals for v in vals]
        print(f"Block 40 flat ({len(flat40)} vals): {flat40}")
        
        # Test against a few other blocks
        test_blocks = [0, 5, 19, 30, 44, 54]  # various pages
        for b_idx in test_blocks:
            if b_idx >= len(blocks):
                continue
            test_block = blocks[b_idx]
            test_words = get_words_and_values(test_block)
            test_lens = get_word_lengths(test_block)
            flat_test = []
            for w in test_words:
                flat_test.extend(w[1])
            
            if len(flat_test) >= len(flat40):
                # Use pattern as key
                key = flat40
                cipher = flat_test[:len(flat40)]
                decoded_up = [(c - k) % 29 for c, k in zip(cipher, key)]
                decoded_down = [(c + k) % 29 for c, k in zip(cipher, key)]
                up_letters = ''.join(VAL_TO_LATIN[v % 29] for v in decoded_up)
                down_letters = ''.join(VAL_TO_LATIN[v % 29] for v in decoded_down)
                print(f"  Block {b_idx} (page ~{b_idx+17}): up='{up_letters[:30]}...' down='{down_letters[:30]}...'")
    
    # ============================================================
    # N=6,7 KASISKI ON THE MATCHING BLOCKS
    # ============================================================
    print("\n" + "=" * 70)
    print("KASISKI ON MATCHING BLOCKS (n=6,7)")
    print("=" * 70)
    
    for n in [6, 7]:
        grams19 = defaultdict(list)
        grams44 = defaultdict(list)
        for i in range(len(b19_lens) - n + 1):
            grams19[tuple(b19_lens[i:i+n])].append(i)
        for i in range(len(b44_lens) - n + 1):
            grams44[tuple(b44_lens[i:i+n])].append(i)
        common = set(grams19.keys()) & set(grams44.keys())
        print(f"\n  n={n}: {len(common)} common repeated {n}-grams between blocks 19 and 44")
        if common:
            for gram in list(common)[:3]:
                print(f"    Gram {gram}:")
                print(f"      Block 19: {grams19[gram]}")
                print(f"      Block 44: {grams44[gram]}")

if __name__ == '__main__':
    main()