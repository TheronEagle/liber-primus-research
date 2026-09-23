#!/usr/bin/env python3
"""
Final focused analysis on lead #0 at CORRECTED positions:
1. Pattern 1: Blocks 19 & 44 (word-length match) - try autokey/running-key
2. Pattern 2: Block 40 unique global occurrence - try as key with proper alignment
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

def vals_to_words(vals, word_lengths):
    words = []
    start = 0
    for length in word_lengths:
        chunk = vals[start:start+length]
        start += length
        word = ''.join(VAL_TO_LATIN[c % ALPHABET_SIZE] for c in chunk)
        words.append(word)
    return words

def get_page_vals(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    flat_vals = []
    for w in raw_words:
        flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
    return flat_vals

def get_word_lengths(block):
    return [item[2] for item in get_words_and_values(block)]

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
        return
    
    # ============================================================
    # PATTERN 1: Blocks 19 & 44 - autokey/running-key tests
    # ============================================================
    print("=" * 70)
    print("PATTERN 1: Blocks 19 & 44 - AUTOKYE/RUNNING-KEY TESTS")
    print("=" * 70)
    
    block19 = blocks[19]  # page ~36
    block44 = blocks[44]  # page ~61
    
    b19_words = get_words_and_values(block19)
    b44_words = get_words_and_values(block44)
    b19_lens = get_word_lengths(block19)
    b44_lens = get_word_lengths(block44)
    
    w19_idx = 46  # 0-indexed for word 47
    w44_idx = 11  # 0-indexed for word 12
    
    # Get the 8-word sequences
    seq19_vals = [b19_words[i][1] for i in range(w19_idx, w19_idx+8)]
    seq44_vals = [b44_words[i][1] for i in range(w44_idx, w44_idx+8)]
    seq19_runes = [b19_words[i][0] for i in range(w19_idx, w19_idx+8)]
    seq44_runes = [b44_words[i][0] for i in range(w44_idx, w44_idx+8)]
    
    flat19 = [v for vals in seq19_vals for v in vals]
    flat44 = [v for vals in seq44_vals for v in vals]
    
    print(f"Block 19 words 47-54: {len(flat19)} runes")
    print(f"Block 44 words 12-19: {len(flat44)} runes")
    
    # Test 1: Autokey - use one as key for the other
    print("\n--- AUTOKYE TESTS ---")
    
    # Block 19 as key for Block 44
    def autokey_decode(cipher, key, shift_up=True):
        """Autokey: key extends with ciphertext (or plaintext)"""
        key = list(key)
        decoded = []
        for i, v in enumerate(cipher):
            if i < len(key):
                k = key[i]
            else:
                # Autokey: use previous ciphertext as key
                k = cipher[i - len(key)]
            decoded.append((v - k) % 29 if shift_up else (v + k) % 29)
        return decoded
    
    # Test 1a: Block 19 as key for Block 44 (autokey)
    decoded = autokey_decode(flat44, flat19, True)
    letters = vals_to_letters(decoded)
    print(f"Autokey: Block19 key for Block44 (shift up): {letters}")
    
    decoded = autokey_decode(flat44, flat19, False)
    letters = vals_to_letters(decoded)
    print(f"Autokey: Block19 key for Block44 (shift down): {letters}")
    
    # Test 1b: Block 44 as key for Block 19 (autokey)
    decoded = autokey_decode(flat19, flat44, True)
    letters = vals_to_letters(decoded)
    print(f"Autokey: Block44 key for Block19 (shift up): {letters}")
    
    decoded = autokey_decode(flat19, flat44, False)
    letters = vals_to_letters(decoded)
    print(f"Autokey: Block44 key for Block19 (shift down): {letters}")
    
    # Test 2: Running key - continuous across the 8 words
    print("\n--- RUNNING KEY (continuous) ---")
    
    # Use Block 19 as running key for Block 44
    key = flat19
    decoded = [(v - k) % 29 for v, k in zip(flat44, (key * ((len(flat44)//len(key))+1))[:len(flat44)])]
    letters = vals_to_letters(decoded)
    print(f"Running key Block19->Block44 (shift up): {vals_to_letters(decoded)}")
    
    decoded = [(v + k) % 29 for v, k in zip(flat44, (flat19 * ((len(flat44)//len(flat19))+1))[:len(flat44)])]
    print(f"Running key Block19->Block44 (shift down): {vals_to_letters(decoded)}")
    
    # Reverse
    decoded = [(v - k) % 29 for v, k in zip(flat19, (flat44 * ((len(flat19)//len(flat44))+1))[:len(flat19)])]
    print(f"Running key Block44->Block19 (shift up): {vals_to_letters(decoded)}")
    
    decoded = [(v + k) % 29 for v, k in zip(flat19, (flat44 * ((len(flat19)//len(flat44))+1))[:len(flat19)])]
    print(f"Running key Block44->Block19 (shift down): {vals_to_letters(decoded)}")
    
    # Test 3: Try using the shared n-grams as keys
    print("\n--- SHARED N-GRAMS AS KEYS ---")
    # The shared n-grams at positions:
    # n=6: (7,6,3,6,4,3) at Block19:47, Block44:12
    # n=6: (6,3,6,4,3,3) at Block19:48, Block44:13
    # n=6: (6,7,6,3,6,4) at Block19:46, Block44:11
    # n=7: (7,6,3,6,4,3,3) at Block19:47, Block44:12
    # n=7: (6,7,6,3,6,4,3) at Block19:46, Block44:11
    
    # Get the rune values for the shared n-gram at Block19:47 (word 47) which is 6 runes
    # Word 47 in block 19 is 6 runes: [16, 23, 25, 13, 3, 11]
    shared_6gram_19 = [16, 23, 25, 13, 3, 11]  # Word 47
    shared_6gram_44 = [6, 5, 23, 28, 27, 5]    # Word 12
    
    print(f"\nShared 6-gram at Block19 word 47: {shared_6gram_19}")
    print(f"Shared 6-gram at Block44 word 12: {shared_6gram_44}")
    
    # Use as Vigenère keys
    for name, key in [("Block19_word47", shared_6gram_19), ("Block44_word12", shared_6gram_44)]:
        for block, flat_vals in [("Block44_8words", flat44), ("Block19_8words", flat19)]:
            for shift_up in [True, False]:
                decoded = [(v - k) % 29 for v, k in zip(flat_vals, (key * ((len(flat_vals)//len(key))+1))[:len(flat_vals)])] if shift_up else [(v + k) % 29 for v, k in zip(flat_vals, (key * ((len(flat_vals)//len(key))+1))[:len(flat_vals)])]
                letters = vals_to_letters(decoded)
                print(f"  {name} key on {block} ({'up' if shift_up else 'down'}): {letters[:50]}...")
    
    # ============================================================
    # PATTERN 2: Block 40 unique pattern - proper alignment test
    # ============================================================
    print("\n" + "=" * 70)
    print("PATTERN 2: BLOCK 40 UNIQUE PATTERN - PROPER ALIGNMENT")
    print("=" * 70)
    
    block40 = blocks[40]
    b40_words = get_words_and_values(block40)
    b40_lens = get_word_lengths(block40)
    
    # Pattern at words 42-49 (indices 41-48)
    pattern_vals = []
    for i in range(41, 49):
        if i < len(b40_words):
            pattern_vals.extend(b40_words[i][1])
    
    print(f"\nPattern length: {len(pattern_vals)} values")
    print(f"Pattern: {pattern_vals}")
    
    # Test with proper alignment: use pattern as key for the SAME block (self-decrypt)
    block40_vals = get_page_vals(block40)
    b40_word_lengths = get_word_lengths(block40)
    
    # Try different starting offsets within the pattern
    for offset in range(len(pattern_vals)):
        rotated = pattern_vals[offset:] + pattern_vals[:offset]
        
        # Self-decrypt
        decoded = [(v - k) % 29 for v, k in zip(block40_vals, (rotated * ((len(block40_vals)//len(rotated))+1))[:len(block40_vals)])]
        words = vals_to_words(decoded, b40_word_lengths)
        
        # Score
        try:
            wordset = set()
            with open('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/words_alpha.txt', encoding='utf-8') as f:
                for line in f:
                    w = line.strip().upper()
                    if len(w) >= 3:
                        wordset.add(w)
        except:
            wordset = set()
        
        hits = dict_score(words, wordset)
        rate = hits / len(words) if words else 0
        
        if rate > 0.05:
            print(f"  Self-decrypt offset {offset}: {hits}/{len(words)} = {rate:.4f}")

if __name__ == '__main__':
    main()