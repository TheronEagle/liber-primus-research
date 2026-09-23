#!/usr/bin/env python3
"""
Test rail fence (zigzag) transposition on all 56 unsolved pages.
Test various numbers of rails (2-10) and both directions.
"""

import sys, json, pathlib, random
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import RUNE_TO_VAL, VAL_TO_LATIN, ALPHABET_SIZE

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('\n%')
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def get_page_vals(block):
    """Return flat list of rune values for a block."""
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    flat_vals = []
    for w in raw_words:
        flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
    return flat_vals

def get_word_lengths(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    word_lengths = [len([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]) for w in raw_words]
    return word_lengths

def vals_to_words(vals, word_lengths):
    words = []
    start = 0
    for length in word_lengths:
        chunk = vals[start:start+length]
        start += length
        word = ''.join(VAL_TO_LATIN[c % ALPHABET_SIZE] for c in chunk)
        words.append(word)
    return words

def rail_fence_encrypt(plaintext, num_rails):
    """Encrypt using rail fence (zigzag) cipher."""
    if num_rails <= 1:
        return plaintext
    
    rails = [[] for _ in range(num_rails)]
    rail = 0
    direction = 1  # 1 = down, -1 = up
    
    for char in plaintext:
        rails[rail].append(char)
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
    
    # Concatenate rails
    ciphertext = []
    for rail_chars in rails:
        ciphertext.extend(rail_chars)
    return ciphertext

def rail_fence_decrypt(ciphertext, num_rails):
    """Decrypt using rail fence (zigzag) cipher."""
    if num_rails <= 1:
        return ciphertext
    
    n = len(ciphertext)
    
    # Determine the length of each rail
    rail_lengths = [0] * num_rails
    rail = 0
    direction = 1
    for _ in range(n):
        rail_lengths[rail] += 1
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
    
    # Split ciphertext into rails
    rails = []
    idx = 0
    for length in rail_lengths:
        rails.append(ciphertext[idx:idx+length])
        idx += length
    
    # Reconstruct plaintext by walking the zigzag
    rail_indices = [0] * num_rails
    result = []
    rail = 0
    direction = 1
    for _ in range(n):
        result.append(rails[rail][rail_indices[rail]])
        rail_indices[rail] += 1
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
    
    return result

def dict_score(candidate_words, wordset):
    return sum(1 for w in candidate_words if w in wordset)

def test_single_rail(block, wordset, num_rails):
    """Test a single rail count on one block."""
    flat_vals = get_page_vals(block)
    if not flat_vals:
        return 0, 0
    word_lengths = get_word_lengths(block)
    
    # Decrypt with rail fence
    decrypted_vals = rail_fence_decrypt(flat_vals, num_rails)
    words = vals_to_words(decrypted_vals, word_lengths)
    hits = dict_score(words, wordset)
    return hits, len(words)

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    unsolved_blocks = blocks[:55]  # blocks 0-54
    
    # Load dictionary
    try:
        wordset = set()
        with open('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/words_alpha.txt', encoding='utf-8') as f:
            for line in f:
                w = line.strip().upper()
                if len(w) >= 3:
                    wordset.add(w)
    except FileNotFoundError:
        print('Dictionary file not found')
        return
    
    # Rail counts to test
    rail_counts = list(range(2, 11))  # 2 to 10 rails
    
    best_result = {'rate': 0}
    all_results = []
    
    for num_rails in rail_counts:
        total_hits = 0
        total_words = 0
        for block in unsolved_blocks:
            hits, words = test_single_rail(block, wordset, num_rails)
            total_hits += hits
            total_words += words
        
        if total_words == 0:
            continue
        rate = total_hits / total_words
        all_results.append({
            'num_rails': num_rails,
            'hits': total_hits,
            'total_words': total_words,
            'rate': rate
        })
        
        if rate > best_result['rate']:
            best_result = {
                'num_rails': num_rails,
                'rate': rate,
                'hits': total_hits,
                'total_words': total_words
            }
        
        print(f"Rails: {num_rails}, hits: {total_hits}/{total_words} = {rate:.4f}")
    
    print(f"\nBest result: {best_result}")
    print(f"Reference good-solve rate (page 73): 9/22 = {9/22:.4f}")
    
    # Save all results
    report_path = pathlib.Path('experiments/2026-09-24/rail_fence_test.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump({
            'best': best_result,
            'all_results': all_results,
            'reference_rate': 9/22
        }, f, indent=2)
    print(f"Report written to {report_path}")

def load_transcription_blocks(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('\n%')
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def get_page_vals(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    flat_vals = []
    for w in raw_words:
        flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
    return flat_vals

if __name__ == '__main__':
    main()