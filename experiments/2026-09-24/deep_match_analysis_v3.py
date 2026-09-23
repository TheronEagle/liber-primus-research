#!/usr/bin/env python3
"""
Deep analysis of the page 22 / page 47 word-length match (Open-Leads #0).
Fixed bug in common set handling.
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

def get_word_lengths(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    return [len([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]) for w in raw_words]

def get_words_and_values(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    result = []
    for w in raw_words:
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        result.append((w, vals, len(vals)))
    return result

def find_all_occurrences(seq, target):
    n = len(target)
    occ = []
    for i in range(len(seq) - n + 1):
        if seq[i:i+n] == target:
            occ.append(i)
    return occ

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    
    # Page 22 ≈ block 5, Page 47 ≈ block 30
    p22_block = blocks[5]
    p47_block = blocks[30]
    
    p22_lens = get_word_lengths(p22_block)
    p47_lens = get_word_lengths(p47_block)
    
    # Target pattern from open-leads
    target = [6,7,6,3,6,4,3,3]
    target2 = [5,4,7,3,6,3,7,4]
    
    print(f"=== TARGET PATTERN: {target} ===")
    print(f"=== SECOND TARGET: {target2} ===")
    
    # Search in specific blocks
    occ22 = find_all_occurrences(p22_lens, target)
    occ47 = find_all_occurrences(p47_lens, target)
    print(f"Page 22 (block 5) occurrences: {occ22}")
    print(f"Page 47 (block 30) occurrences: {occ47}")
    
    occ22_2 = find_all_occurrences(p22_lens, target2)
    occ47_2 = find_all_occurrences(p47_lens, target2)
    print(f"Page 22 target2 occurrences: {occ22_2}")
    print(f"Page 47 target2 occurrences: {occ47_2}")
    
    # Global search
    print(f"\n=== GLOBAL SEARCH ===")
    all_blocks = blocks[:55]
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
        print(f"\n  n={n}: {len(repeated)} repeated {n}-grams globally")
        if repeated:
            for gram, positions in list(repeated.items())[:3]:
                print(f"    Gram {gram}: {len(positions)} occurrences")
                for pos in positions[:3]:
                    for b_idx, start, end in block_boundaries:
                        if start <= pos < end:
                            local = pos - start
                            print(f"      Position {pos} -> Block {b_idx} (page ~{b_idx+17}), local word {local+1}")
                            break
    
    # Check the open-leads positions
    print(f"\n=== OPEN-LEADS POSITIONS ===")
    w22_idx = 44  # word 45
    w47_idx = 10  # word 11
    
    if w22_idx < len(p22_lens) and w47_idx < len(p47_lens):
        p22_words_data = get_words_and_values(blocks[5])
        p47_words_data = get_words_and_values(blocks[30])
        
        seq22 = p22_lens[w22_idx:w22_idx+8] if w22_idx + 8 <= len(p22_lens) else p22_lens[w22_idx:]
        seq47 = p47_lens[w47_idx:w47_idx+8] if w47_idx + 8 <= len(p47_lens) else p47_lens[w47_idx:]
        
        print(f"\nAt open-leads positions:")
        print(f"  Page 22 word 45 (index {w22_idx}): {seq22}")
        print(f"  Page 47 word 11 (index {w47_idx}): {seq47}")
        print(f"  Target: {target}")
    
    # Check target2 globally
    print(f"\n=== SEARCHING FOR SECOND TARGET: {target2} ===")
    occ_t2 = []
    for i in range(len(all_lens) - len(target2) + 1):
        if all_lens[i:i+len(target2)] == target2:
            occ_t2.append(i)
    print(f"Global occurrences of target2: {len(occ_t2)}")
    for occ in occ_t2[:10]:
        for b_idx, start, end in block_boundaries:
            if start <= occ < end:
                local = occ - start
                print(f"  Position {occ} -> Block {b_idx} (page ~{b_idx+17}), local word {local+1}")
                break
    
    # Check target globally
    print(f"\n=== TARGET GLOBAL OCCURRENCES ===")
    occ_t = []
    for i in range(len(all_lens) - len(target) + 1):
        if all_lens[i:i+len(target)] == target:
            occ_t.append(i)
    print(f"Global occurrences of target: {len(occ_t)}")
    for occ in occ_t:
        for b_idx, start, end in block_boundaries:
            if start <= occ < end:
                local = occ - start
                print(f"  Position {occ} -> Block {b_idx} (page ~{b_idx+17}), local word {local+1}")
                break

if __name__ == '__main__':
    main()