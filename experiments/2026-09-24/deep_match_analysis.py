#!/usr/bin/env python3
"""
Deep analysis of the page 22 / page 47 word-length match (Open-Leads #0).
1. Extract exact rune sequences at the matching positions
2. Compare Gematria values directly
3. Try autokey/running-key tests
4. Check for shorter length matches (n=6,7)
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

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    
    # Page 22 ≈ block 5, Page 47 ≈ block 30
    p22_block = blocks[5]
    p47_block = blocks[30]
    
    p22_words = get_words_and_values(p22_block)
    p47_words = get_words_and_values(p47_block)
    
    print(f"Page 22: {len(p22_words)} words")
    print(f"Page 47: {len(p47_words)} words")
    
    # Target indices (1-indexed from open-leads)
    w22_idx = 44  # word 45 (0-indexed)
    w47_idx = 10  # word 11 (0-indexed)
    
    print(f"\n=== EXACT RUNE SEQUENCES AT MATCH POSITIONS ===")
    print(f"\nPage 22, word 45 (index {w22_idx}):")
    print(f"  Rune: {p22_words[w22_idx][0]}")
    print(f"  Values: {p22_words[w22_idx][1]}")
    print(f"  Length: {p22_words[w22_idx][2]}")
    print(f"  Letters: {vals_to_letters(p22_words[w22_idx][1])}")
    
    print(f"\nPage 47, word 11 (index {w47_idx}):")
    print(f"  Rune: {p47_words[w47_idx][0]}")
    print(f"  Values: {p47_words[w47_idx][1]}")
    print(f"  Length: {p47_words[w47_idx][2]}")
    print(f"  Letters: {vals_to_letters(p47_words[w47_idx][1])}")
    
    # Get the 8-word sequences
    print(f"\n=== 8-WORD SEQUENCES (VALUES) ===")
    seq22_vals = [item[1] for item in p22_words[w22_idx:w22_idx+8]]
    seq47_vals = [item[1] for item in p47_words[w47_idx:w47_idx+8]]
    
    print(f"\nPage 22 words 45-52 values:")
    for i, vals in enumerate(seq22_vals):
        print(f"  Word {w22_idx+i+1}: {vals} (len={len(vals)})")
    
    print(f"\nPage 47 words 11-18 values:")
    for i, vals in enumerate(seq47_vals):
        print(f"  Word {w47_idx+i+1}: {vals} (len={len(vals)})")
    
    # Compare values directly
    print(f"\n=== DIRECT VALUE COMPARISON ===")
    all_match = True
    for i in range(8):
        if seq22_vals[i] == seq47_vals[i]:
            print(f"  Position {i}: MATCH")
        else:
            print(f"  Position {i}: DIFFERENT")
            print(f"    Page 22: {seq22_vals[i]}")
            print(f"    Page 47: {seq47_vals[i]}")
            all_match = False
    
    if all_match:
        print("  ALL 8 WORDS HAVE IDENTICAL VALUES!")
    else:
        print("  Values differ - not the same plaintext phrase")
    
    # Try autokey: use page 22 runes as key for page 47
    print(f"\n=== AUTOKYE/ RUNNING-KEY TESTS ===")
    
    # Flatten the 8-word sequences
    flat22 = [v for vals in seq22_vals for v in vals]
    flat47 = [v for vals in seq47_vals for v in vals]
    
    print(f"\nPage 22 flat values (len={len(flat22)}): {flat22}")
    print(f"Page 47 flat values (len={len(flat47)}): {flat47}")
    
    # Test 1: Page 22 as key to decode Page 47 (shift up)
    decoded = [(v - k) % 29 for v, k in zip(flat47, flat22)]
    letters = vals_to_letters(decoded)
    print(f"\nAutokey: Page22 as key for Page47 (shift up): {letters}")
    
    # Test 2: Page 47 as key to decode Page 22 (shift up)
    decoded2 = [(v - k) % 29 for v, k in zip(flat22, flat47)]
    letters2 = vals_to_letters(decoded2)
    print(f"Autokey: Page47 as key for Page22 (shift up): {letters2}")
    
    # Test 3: Shift down (add instead of subtract)
    decoded3 = [(v + k) % 29 for v, k in zip(flat47, flat22)]
    letters3 = vals_to_letters(decoded3)
    print(f"Autokey: Page22 as key for Page47 (shift down): {letters3}")
    
    decoded4 = [(v + k) % 29 for v, k in zip(flat22, flat47)]
    letters4 = vals_to_letters(decoded4)
    print(f"Autokey: Page47 as key for Page22 (shift down): {letters4}")
    
    # Now check for shorter length matches (n=6,7)
    print(f"\n=== KASISKI ON WORD LENGTHS (n=6,7) ===")
    
    p22_lens = get_word_lengths(blocks[5])
    p47_lens = get_word_lengths(blocks[30])
    
    def find_ngram_matches(lens, n):
        matches = defaultdict(list)
        for i in range(len(lens) - n + 1):
            matches[tuple(lens[i:i+n])].append(i)
        return {k: v for k, v in matches.items() if len(v) > 1}
    
    for n in [6, 7]:
        grams22 = find_ngram_matches(p22_lens, n)
        grams47 = find_ngram_matches(p47_lens, n)
        common = set(grams22.keys()) & set(grams47.keys())
        print(f"\n  n={n}: {len(common)} common repeated {n}-grams")
        if common:
            for gram in list(common)[:3]:
                print(f"    Gram {gram}:")
                print(f"      Page 22 positions: {grams22[gram]}")
                print(f"      Page 47 positions: {grams47[gram]}")
    
    # Also check globally across all pages
    print(f"\n=== GLOBAL KASISKI ON ALL PAGES (n=6,7,8) ===")
    all_blocks = blocks[:55]  # unsolved pages
    all_lens = []
    block_boundaries = []
    offset = 0
    for idx, block in enumerate(all_blocks):
        lens = get_word_lengths(block)
        block_boundaries.append((idx, offset, offset + len(lens)))
        all_lens.extend(lens)
        offset += len(lens)
    
    print(f"Total words across 55 pages: {len(all_lens)}")
    
    for n in [6, 7, 8]:
        grams = defaultdict(list)
        for i in range(len(all_lens) - n + 1):
            grams[tuple(all_lens[i:i+n])].append(i)
        repeated = {k: v for k, v in grams.items() if len(v) > 1}
        if repeated:
            print(f"\n  n={n}: {len(repeated)} repeated {n}-grams globally")
            # Show top 3
            for gram, positions in list(repeated.items())[:3]:
                print(f"    Gram {gram}: {len(positions)} occurrences at positions {positions[:10]}")
                # Map to page/word
                for pos in positions[:3]:
                    for b_idx, start, end in block_boundaries:
                        if start <= pos < end:
                            local_word = pos - start
                            print(f"      Position {pos} -> Page {b_idx} (block {b_idx}), word {local_word+1}")
                            break

if __name__ == '__main__':
    main()