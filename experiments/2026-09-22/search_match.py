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
    # Print first 60 word lengths for each
    print("\nPage 22 word lengths (index: length):")
    for i in range(min(60, len(p22_lens))):
        print(f"  {i}: {p22_lens[i]}", end=' ')
        if (i+1) % 10 == 0:
            print()
    print()
    print("\nPage 47 word lengths (index: length):")
    for i in range(min(60, len(p47_lens))):
        print(f"  {i}: {p47_lens[i]}", end=' ')
        if (i+1) % 10 == 0:
            print()
    print()
    # Now let's slide a window of size 8 and see if we find the target
    target = [6,7,6,3,6,4,3,3]
    print(f"Searching for target {target} in page 22 word lengths:")
    matches22 = []
    for i in range(len(p22_lens) - len(target) + 1):
        if p22_lens[i:i+len(target)] == target:
            matches22.append(i)
    print(f"  Found at indices: {matches22}")
    print(f"Searching for target {target} in page 47 word lengths:")
    matches47 = []
    for i in range(len(p47_lens) - len(target) + 1):
        if p47_lens[i:i+len(target)] == target:
            matches47.append(i)
    print(f"  Found at indices: {matches47}")
    if matches22 and matches47:
        print("\nMatch found! Now extracting the rune sequences for those positions.")
        def get_word_runes_from_block(block, word_idx):
            clean = block.replace('/', '').replace('\n', '')
            words = [w for w in clean.split('-') if w]
            if word_idx >= len(words):
                return None, None
            rune_word = words[word_idx]
            vals = [RUNE_TO_VAL[ch] for ch in rune_word if ch in RUNE_TO_VAL]
            return rune_word, vals
        if matches22:
            idx = matches22[0]
            print(f"\nPage 22 match at word index {idx} (1-indexed word {idx+1}):")
            for offset in range(len(target)):
                widx = idx + offset
                rune, vals = get_word_runes_from_block(p22_block, widx)
                print(f"  Word {widx+1}: runes='{rune}' values={vals}")
        if matches47:
            idx = matches47[0]
            print(f"\nPage 47 match at word index {idx} (1-indexed word {idx+1}):")
            for offset in range(len(target)):
                widx = idx + offset
                rune, vals = get_word_runes_from_block(p47_block, widx)
                print(f"  Word {widx+1}: runes='{rune}' values={vals}")

if __name__ == '__main__':
    main()