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
    # According to page-catalog.md, block 5 = page 22, block 30 = page 47
    if len(blocks) <= 30:
        print(f"Not enough blocks: have {len(blocks)}")
        return
    p22_block = blocks[5]
    p47_block = blocks[30]
    p22_lens = word_lengths_from_block(p22_block)
    p47_lens = word_lengths_from_block(p47_block)
    print(f"Page 22 (block 5): {len(p22_lens)} words")
    print(f"Page 47 (block 30): {len(p47_lens)} words")
    # Print word lengths with indices
    print("\nPage 22 word lengths (index: length):")
    for i, l in enumerate(p22_lens):
        print(f"  {i}: {l}", end=' ')
        if (i+1) % 10 == 0:
            print()
    print()
    print("\nPage 47 word lengths (index: length):")
    for i, l in enumerate(p47_lens):
        print(f"  {i}: {l}", end=' ')
        if (i+1) % 10 == 0:
            print()
    print()
    # Check around word 45 (1-indexed) -> index 44
    w22_idx = 44  # 0-indexed
    w47_idx = 10  # 0-indexed
    print(f"\nChecking around word 45 of page 22 (index {w22_idx}):")
    start = max(0, w22_idx - 5)
    end = min(len(p22_lens), w22_idx + 5 + 8)  # show a few before and after the 8-word window
    for i in range(start, end):
        marker = ' -->' if i == w22_idx else ''
        print(f"  Word {i+1}: length={p22_lens[i]}{marker}")
    print(f"\nThe 8-word sequence starting at word 45: {p22_lens[w22_idx:w22_idx+8]}")
    print(f"Checking around word 11 of page 47 (index {w47_idx}):")
    start = max(0, w47_idx - 5)
    end = min(len(p47_lens), w47_idx + 5 + 8)
    for i in range(start, end):
        marker = ' <--' if i == w47_idx else ''
        print(f"  Word {i+1}: length={p47_lens[i]}{marker}")
    print(f"\nThe 8-word sequence starting at word 11: {p47_lens[w47_idx:w47_idx+8]}")
    target = [6,7,6,3,6,4,3,3]
    print(f"\nTarget pattern: {target}")
    if p22_lens[w22_idx:w22_idx+8] == target:
        print("Page 22 matches!")
    else:
        print("Page 22 does NOT match.")
    if p47_lens[w47_idx:w47_idx+8] == target:
        print("Page 47 matches!")
    else:
        print("Page 47 does NOT match.")
    # Also, let's see if the target appears anywhere else in each page
    def find_all(seq, target):
        n = len(target)
        matches = []
        for i in range(len(seq) - n + 1):
            if seq[i:i+n] == target:
                matches.append(i)
        return matches
    matches22 = find_all(p22_lens, target)
    matches47 = find_all(p47_lens, target)
    print(f"\nAll occurrences of target in page 22: {matches22}")
    print(f"All occurrences of target in page 47: {matches47}")

if __name__ == '__main__':
    main()