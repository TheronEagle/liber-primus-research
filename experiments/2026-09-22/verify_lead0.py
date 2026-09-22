#!/usr/bin/env python3
"""
Verify the page 22 / page 47 word-length match from open-leads.md item 0.
"""
import sys
sys.path.insert(0, '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/skill/cicada-3301-solver/scripts')
from gematria_toolkit import *

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    content = ''.join(lines)
    # Split by '%' lines that are on their own (the delimiter for pages)
    # We'll split by '\n%' and then each part after the first is a page block.
    parts = content.split('\n%')
    # The first part is the header (up to the first '%' line)
    blocks = []
    for part in parts[1:]:
        block = part.strip()
        if block:
            blocks.append(block)
    return blocks

def word_lengths_from_block(block):
    """Return list of word lengths (number of runes per word) for a block."""
    clean = block.replace('/', '').replace('\n', '')
    words = [w for w in clean.split('-') if w]
    lengths = []
    for w in words:
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        lengths.append(len(vals))
    return lengths

def get_word_runes_from_block(block, word_idx):
    """Return (rune_string, values) for the word at word_idx (0-index)."""
    clean = block.replace('/', '').replace('\n', '')
    words = [w for w in clean.split('-') if w]
    if word_idx >= len(words):
        return None, None
    rune_word = words[word_idx]
    vals = [RUNE_TO_VAL[ch] for ch in rune_word if ch in RUNE_TO_VAL]
    return rune_word, vals

def main():
    blocks = load_transcription_blocks('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt')
    print(f"Number of blocks (pages): {len(blocks)}")
    # Assuming block index 0 corresponds to LP2 page 0 (i.e., page 17 overall).
    # The lead is about LP2 pages 22 and 47, so we use block indices 22 and 47.
    if len(blocks) <= 47:
        print(f"ERROR: Not enough blocks: have {len(blocks)}, need at least 48")
        return
    p22_block = blocks[22]
    p47_block = blocks[47]
    p22_lens = word_lengths_from_block(p22_block)
    p47_lens = word_lengths_from_block(p47_block)
    print(f"Page 22 (block 22): {len(p22_lens)} words")
    print(f"Page 47 (block 47): {len(p47_lens)} words")
    # Target word indices from lead: word 45 of page 22 and word 11 of page 47 (1-indexed)
    w22_idx_1based = 45
    w47_idx_1based = 11
    w22_idx = w22_idx_1based - 1  # to 0-index
    w47_idx = w47_idx_1based - 1
    if w22_idx < 0 or w22_idx >= len(p22_lens) or w47_idx < 0 or w47_idx >= len(p47_lens):
        print(f"ERROR: word indices out of range: w22={w22_idx} (max {len(p22_lens)-1}), w47={w47_idx} (max {len(p47_lens)-1})")
        return
    # Extract the 8-word length sequence starting at those indices
    target = [6,7,6,3,6,4,3,3]
    def get_seq(lengths, start, n=8):
        return lengths[start:start+n]
    seq22 = get_seq(p22_lens, w22_idx, 8)
    seq47 = get_seq(p47_lens, w47_idx, 8)
    print(f"\nTarget pattern: {target}")
    print(f"Page 22 lengths starting at word {w22_idx_1based}: {seq22}")
    print(f"Page 47 lengths starting at word {w47_idx_1based}: {seq47}")
    match22 = seq22 == target
    match47 = seq47 == target
    print(f"Page 22 match? {match22}")
    print(f"Page 47 match? {match47}")
    if match22 and match47:
        print("\nSUCCESS: The exact 8-word-length match exists!")
        # Now get the actual rune strings and values for those words
        print("\n--- Page 22 span (words 45-52) ---")
        for offset in range(8):
            widx = w22_idx + offset
            rune, vals = get_word_runes_from_block(p22_block, widx)
            print(f"  Word {widx+1}: runes='{rune}' values={vals}")
        print("\n--- Page 47 span (words 11-18) ---")
        for offset in range(8):
            widx = w47_idx + offset
            rune, vals = get_word_runes_from_block(p47_block, widx)
            print(f"  Word {widx+1}: runes='{rune}' values={vals}")
        # Check if the values are identical
        vals22_list = []
        vals47_list = []
        for offset in range(8):
            _, vals22 = get_word_runes_from_block(p22_block, w22_idx + offset)
            _, vals47 = get_word_runes_from_block(p47_block, w47_idx + offset)
            vals22_list.append(vals22)
            vals47_list.append(vals47)
        if vals22_list == vals47_list:
            print("\nThe Gematria VALUES of the two spans are IDENTICAL.")
        else:
            print("\nThe Gematria VALUES differ.")
            # Check for constant shift (Caesar-like)
            if all(len(v) == len(w) for v, w in zip(vals22_list, vals47_list)):
                # Compute difference per position (should be same length)
                diffs = []
                for vlist, wlist in zip(vals22_list, vals47_list):
                    if len(vlist) == len(wlist):
                        diffs.append([(v - w) % 29 for v, w in zip(vlist, wlist)])
                    else:
                        diffs.append(None)
                # Flatten and see if all differences are the same number
                flat_diffs = [d for sublist in diffs if sublist is not None for d in sublist]
                if flat_diffs and len(set(flat_diffs)) == 1:
                    print(f"Constant shift detected: {flat_diffs[0]} (i.e., page22 values = page47 values + {flat_diffs[0]} mod 29)")
                else:
                    print("No constant shift across the span.")
            else:
                print("Word lengths differ within the span (should not happen if length sequence matched).")
    else:
        print("\nFAILURE: The exact 8-word-length match was NOT found.")
        print("Let's see if there are any 8-length matches at all in each page.")
        from collections import defaultdict
        def ngram_dict(lengths, n):
            d = defaultdict(list)
            for i in range(len(lengths) - n + 1):
                d[tuple(lengths[i:i+n])].append(i)
            return {k:v for k,v in d.items() if len(v) > 1}
        grams22 = ngram_dict(p22_lens, 8)
        grams47 = ngram_dict(p47_lens, 8)
        print(f"Page 22 has {len(grams22)} repeated 8-grams.")
        print(f"Page 47 has {len(grams47)} repeated 8-grams.")
        common = set(grams22.keys()) & set(grams47.keys())
        print(f"Number of common repeated 8-grams between pages: {len(common)}")
        if common:
            print("Examples of common 8-grams:")
            for gram in list(common)[:3]:
                print(f"  Gram {gram}")
                print(f"    Page 22 positions: {grams22[gram]}")
                print(f"    Page 47 positions: {grams47[gram]}")

if __name__ == '__main__':
    main()