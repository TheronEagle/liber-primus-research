#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/skill/cicada-3301-solver/scripts')
from gematria_toolkit import *

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    # Find the line that starts with 'Page     : %' to know where header ends
    # Actually, after the header, we have blocks separated by a line that is exactly '%'
    # Let's just join and split by '%\n' (but note the header may have % too)
    content = ''.join(lines)
    # The header ends before the first '%' line that is alone? Let's split by '\n%' and then adjust.
    # Simpler: split by '\n%' and then each block starts after that.
    # We'll do a naive split and then skip the first part if it's header.
    parts = content.split('\n%')
    # The first part is the header (up to the line before the first '%' line)
    blocks = []
    for i, part in enumerate(parts[1:]):  # skip header
        # Each block may have a trailing newline, but we'll strip
        block = part.strip()
        if block:
            blocks.append(block)
    return blocks

def get_word_runes_from_block(block, word_idx):
    # block is the raw string of a page (with delimiters: '-', '/', newline?)
    # According to the file, delimiters are defined at top: Word: -, Clause: ., Paragraph: &, Segment: $
    # But the runes-text.txt in the original archive uses '-' as word separator and '/' and newline as line-continuation.
    # The RTKD file might have different? Let's assume same as original: word separator '-', and '/' and '\n' are just line continuations to be removed.
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
    # Page numbers: the index file says block i corresponds to page 17+i? Let's check the index file.
    # We'll just assume block 0 is page 0 of LP2? Actually the open-leads says page 22 and page 47 of LP2.
    # In the transcription, we have 57 blocks? Let's see.
    # We'll map: block index 0 -> page 0 of LP2 (which is page 17 overall?).
    # But the lead is about LP2 pages, so we'll use block index = page number in LP2.
    # So page 22 -> block 22, page 47 -> block 47.
    if len(blocks) <= 47:
        print(f"Not enough blocks: have {len(blocks)}, need at least 48")
        return
    p22_block = blocks[22]
    p47_block = blocks[47]
    # parse word lengths for whole page (for Kasiski context)
    p22_vals, p22_lens = parse_page_block(p22_block)
    p47_vals, p47_lens = parse_page_block(p47_block)
    print(f"Page 22 (block 22): {len(p22_lens)} words, total runes {len(p22_vals)}")
    print(f"Page 47 (block 47): {len(p47_lens)} words, total runes {len(p47_vals)}")
    # target words (using 1-index as per open-leads: word 45 of page 22 and word 11 of page 47)
    w22_idx = 45  # 1-indexed
    w47_idx = 11
    # convert to 0-index
    w22 = w22_idx - 1
    w47 = w47_idx - 1
    if w22 < 0 or w22 >= len(p22_lens) or w47 < 0 or w47 >= len(p47_lens):
        print(f"word indices out of range: w22={w22} (max {len(p22_lens)-1}), w47={w47} (max {len(p47_lens)-1})")
        return
    rune22, vals22 = get_word_runes_from_block(p22_block, w22)
    rune47, vals47 = get_word_runes_from_block(p47_block, w47)
    if rune22 is None or rune47 is None:
        print("could not extract word")
        return
    print(f"\nTesting 1-indexed word positions (LP2 pages 22 and 47):")
    print(f"Page 22 word {w22_idx}: runes='{rune22}' values={vals22}")
    print(f"Page 47 word {w47_idx}: runes='{rune47}' values={vals47}")
    # compare lengths
    print(f"Lengths: {len(vals22)} vs {len(vals47)} -> {'match' if len(vals22)==len(vals47) else 'mismatch'}")
    # compare values
    if vals22 == vals47:
        print("VALUES IDENTICAL")
    else:
        print(f"Values differ: {vals22} vs {vals47}")
    # try to see if they are same after shifting? maybe key?
    # compute difference mod 29
    if len(vals22) == len(vals47):
        diffs = [(v2 - v4) % 29 for v2, v4 in zip(vals22, vals47)]
        print(f"Value differences (p22 - p47) mod 29: {diffs}")
        # if all same diff, could be Caesar shift
        if len(set(diffs)) == 1:
            print(f"Constant shift detected: {diffs[0]}")
        else:
            print("No constant shift")
    # also get Latin letters
    lat22 = ''.join(VAL_TO_LATIN[v % 29] for v in vals22)
    lat47 = ''.join(VAL_TO_LATIN[v % 29] for v in vals47)
    print(f"Latin letters: '{lat22}' vs '{lat47}'")

if __name__ == '__main__':
    main()