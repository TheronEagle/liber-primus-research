#!/usr/bin/env python3
"""
Deep analysis of the page 22 / page 47 word-length match (Open-Leads #0).
1. Extract exact rune sequences at the matching positions
2. Compare Gematria values directly
3. Try autokey/running-key tests
4. Check for shorter length matches (n=6,7)
5. Search globally for the target pattern [6,7,6,3,6,4,3,3]
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

def find_all_occurrences(seq, target):
    """Return all start indices where target occurs as contiguous subsequence."""
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
    
    p22_words = get_words_and_values(p22_block)
    p47_words = get_words_and_values(p47_block)
    
    p22_lens = get_word_lengths(p22_block)
    p47_lens = get_word_lengths(p47_block)
    
    print(f"Page 22 (block 5): {len(p22_words)} words")
    print(f"Page 47 (block 30): {len(p47_words)} words")
    
    # Target pattern from open-leads
    target = [6,7,6,3,6,4,3,3]
    print(f"\n=== SEARCHING FOR TARGET PATTERN: {target} ===")
    
    # Search in page 22
    occ22 = find_all_occurrences(p22_lens, target)
    print(f"Page 22 occurrences of target: {occ22}")
    
    # Search in page 47
    occ47 = find_all_occurrences(p47_lens, target)
    print(f"Page 47 occurrences of target: {occ47}")
    
    # Search globally
    print(f"\n=== GLOBAL SEARCH FOR TARGET PATTERN ===")
    all_blocks = blocks[:55]
    all_lens = []
    block_boundaries = []
    offset = 0
    for idx, block in enumerate(all_blocks):
        lens = get_word_lengths(block)
        block_boundaries.append((idx, offset, offset + len(lens)))
        all_lens.extend(lens)
        offset += len(lens)
    
    global_occ = find_all_occurrences(all_lens, target)
    print(f"Global occurrences of target: {len(global_occ)}")
    for occ in global_occ[:10]:
        for b_idx, start, end in block_boundaries:
            if start <= occ < end:
                local = occ - start
                print(f"  Position {occ} -> Block {b_idx} (page ~{b_idx+17}), local word {local+1}")
                break
    
    # Now check the specific positions mentioned in open-leads
    print(f"\n=== POSITIONS MENTIONED IN OPEN-LEADS ===")
    print(f"Open-leads mentions: word 45 of page 22, word 11 of page 47")
    
    w22_idx = 44  # 0-indexed for word 45
    w47_idx = 10  # 0-indexed for word 11
    
    if w22_idx < len(p22_words) and w47_idx < len(p47_words):
        p22_words_data = get_words_and_values(p22_block)
        p47_words_data = get_words_and_values(p47_block)
        
        print(f"\nPage 22 word 45 (index {w22_idx}):")
        print(f"  Rune: {p22_words_data[w22_idx][0]}")
        print(f"  Values: {p22_words_data[w22_idx][1]}")
        print(f"  Length: {p22_words_data[w22_idx][2]}")
        
        print(f"\nPage 47 word 11 (index {w47_idx}):")
        print(f"  Rune: {p47_words_data[w47_idx][0]}")
        print(f"  Values: {p47_words_data[w47_idx][1]}")
        print(f"  Length: {p47_words_data[w47_idx][2]}")
        
        # Show surrounding context
        print(f"\nPage 22 context (words 40-50):")
        for i in range(max(0, w22_idx-5), min(len(p22_words), w22_idx+6)):
            marker = " <-- WORD 45" if i == w22_idx else ""
            print(f"  Word {i+1}: len={p22_lens[i]}, rune={p22_words_data[i][0]}{marker}")
        
        print(f"\nPage 47 context (words 6-16):")
        for i in range(max(0, w47_idx-5), min(len(p47_words), w47_idx+6)):
            marker = " <-- WORD 11" if i == w47_idx else ""
            print(f"  Word {i+1}: len={p47_lens[i]}, rune={p47_words_data[i][0]}{marker}")
    
    # Now get the actual 8-word length sequences starting at those positions
    print(f"\n=== 8-WORD LENGTH SEQUENCES AT OPEN-LEADS POSITIONS ===")
    if w22_idx + 8 <= len(p22_lens):
        seq22 = p22_lens[w22_idx:w22_idx+8]
        print(f"Page 22 words 45-52: {seq22}")
    else:
        print(f"Page 22: not enough words for 8-word sequence at position 45")
        seq22 = p22_lens[w22_idx:]
        print(f"  Available: {seq22}")
    
    if w47_idx + 8 <= len(p47_lens):
        seq47 = p47_lens[w47_idx:w47_idx+8]
        print(f"Page 47 words 11-18: {seq47}")
    else:
        print(f"Page 47: not enough words for 8-word sequence at position 11")
        seq47 = p47_lens[w47_idx:]
        print(f"  Available: {seq47}")
    
    print(f"Target: {target}")
    print(f"Page 22 matches target? {seq22 == target}")
    print(f"Page 47 matches target? {seq47 == target}")
    
    # Search for any 8-length matches globally
    print(f"\n=== GLOBAL REPEATED 8-GRAMS ===")
    grams = defaultdict(list)
    for i in range(len(all_lens) - 7):
        grams[tuple(all_lens[i:i+8])].append(i)
    repeated = {k: v for k, v in grams.items() if len(v) > 1}
    print(f"Total repeated 8-grams globally: {len(repeated)}")
    for gram, positions in list(repeated.items())[:5]:
        print(f"  Gram {gram}: {len(positions)} occurrences")
        for pos in positions[:3]:
            for b_idx, start, end in block_boundaries:
                if start <= pos < end:
                    local = pos - start
                    print(f"    Position {pos} -> Block {b_idx} (page ~{b_idx+17}), local word {local+1}")
                    break
    
    # Check for the second match mentioned in open-leads: [5,4,7,3,6,3,7,4] between pages 43 and 58
    print(f"\n=== SECOND MATCH FROM OPEN-LEADS ===")
    target2 = [5,4,7,3,6,3,7,4]
    print(f"Target 2: {target2}")
    occ43 = find_all_occurrences(get_word_lengths(blocks[43-17]), target2) if 43-17 < len(blocks) else []
    occ58 = find_all_occurrences(get_word_lengths(blocks[58-17]), target2) if 58-17 < len(blocks) else []
    print(f"Page 43 (block {43-17}) occurrences: {occ43}")
    print(f"Page 58 (block {58-17}) occurrences: {occ58}")
    
    # Also check n=6 and n=7 matches between pages 22 and 47
    print(f"\n=== N=6 AND N=7 MATCHES BETWEEN PAGES 22 AND 47 ===")
    for n in [6, 7]:
        grams22 = defaultdict(list)
        grams47 = defaultdict(list)
        for i in range(len(p22_lens) - n + 1):
            grams22[tuple(p22_lens[i:i+n])].append(i)
        for i in range(len(p47_lens) - n + 1):
            grams47[tuple(p47_lens[i:i+n])].append(i)
        common = set(grams22.keys()) & set(grams47.keys())
        common = {k: v for k, v in common.items() if len(grams22[k]) > 0 and len(grams47[k]) > 0}
        print(f"  n={n}: {len(common)} common repeated {n}-grams between pages 22 and 47")
        if common:
            for gram in list(common)[:3]:
                print(f"    Gram {gram}:")
                print(f"      Page 22: {grams22[gram]}")
                print(f"      Page 47: {grams47[gram]}")

if __name__ == '__main__':
    main()