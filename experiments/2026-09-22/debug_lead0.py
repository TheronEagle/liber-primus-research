#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/skill/cicada-3301-solver/scripts')
from gematria_toolkit import *

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    content = ''.join(lines)
    parts = content.split('\n%')
    blocks = []
    for part in parts[1:]:
        block = part.strip()
        if block:
            blocks.append(block)
    return blocks

def word_lengths_from_block(block):
    clean = block.replace('/', '').replace('\n', '')
    words = [w for w in clean.split('-') if w]
    lengths = []
    for w in words:
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        lengths.append(len(vals))
    return lengths

def get_word_runes_from_block(block, word_idx):
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
    # Let's examine page 22 and page 47 (0-indexed blocks)
    p22_lengths = word_lengths_from_block(blocks[22])
    p47_lengths = word_lengths_from_block(blocks[47])
    print(f"Page 22 word lengths (1-indexed positions):")
    for i, l in enumerate(p22_lengths, start=1):
        print(f"  {i}: {l}")
    print(f"Page 47 word lengths (1-indexed positions):")
    for i, l in enumerate(p47_lengths, start=1):
        print(f"  {i}: {l}")
    # Now look for the 8-gram [6,7,6,3,6,4,3,3] in each
    target = [6,7,6,3,6,4,3,3]
    def find(seq, target):
        n = len(target)
        for i in range(len(seq) - n + 1):
            if seq[i:i+n] == target:
                return i
        return -1
    idx22 = find(p22_lengths, target)
    idx47 = find(p47_lengths, target)
    print(f"\nTarget {target} found in page 22 at word index (0-index) {idx22} -> 1-indexed {idx22+1 if idx22!=-1 else 'not found'}")
    print(f"Target {target} found in page 47 at word index (0-index) {idx47} -> 1-indexed {idx47+1 if idx47!=-1 else 'not found'}")
    if idx22 != -1 and idx47 != -1:
        print("MATCH FOUND!")
        # Show the actual words (runes) for that span
        print("\nPage 22 span:")
        for offset in range(8):
            widx = idx22 + offset
            rune, vals = get_word_runes_from_block(blocks[22], widx)
            print(f"  Word {widx+1}: runes='{rune}' values={vals} len={len(vals)}")
        print("\nPage 47 span:")
        for offset in range(8):
            widx = idx47 + offset
            rune, vals = get_word_runes_from_block(blocks[47], widx)
            print(f"  Word {widx+1}: runes='{rune}' values={vals} len={len(vals)}")
    else:
        print("No exact match found. Let's see if there are any similar length-8 matches.")
        # Maybe the lead is about a match of length 8 but not necessarily that exact pattern? Let's compute all 8-grams and see intersections.
        from collections import defaultdict
        def get_ngrams(seq, n):
            d = defaultdict(list)
            for i in range(len(seq) - n + 1):
                d[tuple(seq[i:i+n])].append(i)
            return {k:v for k,v in d.items() if len(v) > 1}
        grams22 = get_ngrams(p22_lengths, 8)
        grams47 = get_ngrams(p47_lengths, 8)
        common = set(grams22.keys()) & set(grams47.keys())
        print(f"Common 8-grams between pages: {len(common)}")
        if common:
            for gram in list(common)[:5]:
                print(f"  Gram {gram}: pages 22 at {grams22[gram]}, page 47 at {grams47[gram]}")

if __name__ == '__main__':
    main()