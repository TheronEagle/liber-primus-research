#!/usr/bin/env python3
"""
Systematic test of the unique pattern from block 40 as a running key.
Test all possible alignments and key lengths.
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
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    word_lengths = [len([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]) for w in raw_words]
    return word_lengths

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    unsolved_blocks = blocks[:55]
    
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
    
    # Get the unique pattern from block 40
    block40 = blocks[40]
    b40_words = []
    clean = block40.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    for w in raw_words:
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        b40_words.append(vals)
    
    # Pattern at words 42-49 (indices 41-48)
    pattern_vals = []
    for i in range(41, 49):
        if i < len(b40_words):
            pattern_vals.extend(b40_words[i])
    
    print(f"Pattern length: {len(pattern_vals)} values")
    print(f"Pattern: {pattern_vals}")
    
    # Test 1: Use pattern as repeating key (Vigenère)
    print("\n=== Test 1: Pattern as repeating Vigenère key ===")
    best_result = {'rate': 0}
    all_results = []
    
    for offset in range(len(pattern_vals)):
        # Rotate pattern by offset
        rotated = pattern_vals[offset:] + pattern_vals[:offset]
        
        total_hits = 0
        total_words = 0
        for block in blocks[:55]:
            flat_vals = []
            clean = block.replace('/', '').replace('\n', '')
            raw_words = [w for w in clean.split('-') if w]
            for w in raw_words:
                flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
            
            if not flat_vals:
                continue
            
            word_lengths = get_word_lengths(block)
            
            # Decode with rotating key
            decoded = [(v - k) % 29 for v, k in zip(flat_vals, (rotated * ((len(flat_vals)//len(rotated))+1))[:len(flat_vals)])]
            words = vals_to_words(decoded, word_lengths)
            hits = dict_score(words, wordset)
            total_hits += hits
            total_words += len(words)
        
        if total_words == 0:
            continue
        rate = total_hits / total_words
        all_results.append({
            'test': 'vigenere_rotated',
            'offset': offset,
            'hits': total_hits,
            'total_words': total_words,
            'rate': rate
        })
        
        if rate > best_result['rate']:
            best_result = {'test': 'vigenere_rotated', 'offset': offset, 'rate': rate, 'hits': total_hits, 'total_words': total_words}
        
        if rate > 0.05:
            print(f"  Offset {offset}: {total_hits}/{total_words} = {rate:.4f}")
    
    # Test 2: Use pattern as autokey (key stream = pattern + ciphertext)
    print("\n=== Test 2: Pattern as autokey seed ===")
    for offset in range(len(pattern_vals)):
        rotated = pattern_vals[offset:] + pattern_vals[:offset]
        
        total_hits = 0
        total_words = 0
        for block in blocks[:55]:
            flat_vals = []
            clean = block.replace('/', '').replace('\n', '')
            raw_words = [w for w in clean.split('-') if w]
            for w in raw_words:
                flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
            
            if not flat_vals:
                continue
            
            word_lengths = get_word_lengths(block)
            
            # Autokey: key starts with pattern, then continues with ciphertext
            key = rotated[:]
            decoded = []
            for i, v in enumerate(flat_vals):
                k = key[i % len(key)]
                decoded.append((v - k) % 29)
                if len(key) < len(flat_vals):
                    key.append(v)  # autokey: key extends with ciphertext
            
            words = vals_to_words(decoded, get_word_lengths(blocks[0]) if False else get_word_lengths(blocks[0]))  # wrong - need actual block lengths
            # Fix: use actual block word lengths
            words = vals_to_words(decoded, get_word_lengths(block))
            hits = dict_score(words, wordset)
            total_hits += hits
            total_words += len(words)
        
        if total_words == 0:
            continue
        rate = total_hits / total_words
        all_results.append({
            'test': 'autokey',
            'offset': offset,
            'hits': total_hits,
            'total_words': total_words,
            'rate': rate
        })
        
        if rate > best_result['rate']:
            best_result = {'test': 'autokey', 'offset': offset, 'rate': rate, 'hits': total_hits, 'total_words': total_words}
        
        if rate > 0.05:
            print(f"  Autokey offset {offset}: {total_hits}/{total_words} = {rate:.4f}")
    
    # Test 3: Pattern as running key with different starting positions per page
    print("\n=== Test 3: Pattern as running key with per-page offsets ===")
    for page_offset in range(20):  # Try different starting positions in pattern
        total_hits = 0
        total_words = 0
        pattern_idx = page_offset
        
        for block in blocks[:55]:
            flat_vals = []
            clean = block.replace('/', '').replace('\n', '')
            raw_words = [w for w in clean.split('-') if w]
            for w in raw_words:
                flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
            
            if not flat_vals:
                continue
            
            word_lengths = get_word_lengths(block)
            
            # Use pattern as running key, continuing across pages
            decoded = []
            idx = 0
            while idx < len(flat_vals):
                k = pattern_vals[pattern_idx % len(pattern_vals)]
                decoded.append((flat_vals[idx] - k) % 29)
                idx += 1
                pattern_idx += 1
            
            words = vals_to_words(decoded, get_word_lengths(block))
            hits = dict_score(words, wordset)
            total_hits += hits
            total_words += len(words)
        
        if total_words == 0:
            continue
        rate = total_hits / total_words
        all_results.append({
            'test': 'running_key_continuous',
            'page_offset': page_offset,
            'hits': total_hits,
            'total_words': total_words,
            'rate': rate
        })
        
        if rate > best_result['rate']:
            best_result = {'test': 'running_key_continuous', 'page_offset': page_offset, 'rate': rate, 'hits': total_hits, 'total_words': total_words}
        
        if rate > 0.05:
            print(f"  Continuous offset {page_offset}: {total_hits}/{total_words} = {rate:.4f}")
    
    # Test 4: Reverse pattern
    print("\n=== Test 4: Reversed pattern ===")
    reversed_pattern = pattern_vals[::-1]
    for offset in range(len(reversed_pattern)):
        rotated = reversed_pattern[offset:] + reversed_pattern[:offset]
        
        total_hits = 0
        total_words = 0
        for block in blocks[:55]:
            flat_vals = []
            clean = block.replace('/', '').replace('\n', '')
            raw_words = [w for w in clean.split('-') if w]
            for w in raw_words:
                flat_vals.extend([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL])
            
            if not flat_vals:
                continue
            
            word_lengths = get_word_lengths(block)
            decoded = [(v - k) % 29 for v, k in zip(flat_vals, (rotated * ((len(flat_vals)//len(rotated))+1))[:len(flat_vals)])]
            words = vals_to_words(decoded, get_word_lengths(block))
            hits = dict_score(words, wordset)
            total_hits += hits
            total_words += len(words)
        
        if total_words == 0:
            continue
        rate = total_hits / total_words
        all_results.append({
            'test': 'vigenere_reversed_rotated',
            'offset': offset,
            'hits': total_hits,
            'total_words': total_words,
            'rate': rate
        })
        
        if rate > best_result['rate']:
            best_result = {'test': 'vigenere_reversed_rotated', 'offset': offset, 'rate': rate, 'hits': total_hits, 'total_words': total_words}
        
        if rate > 0.05:
            print(f"  Reversed offset {offset}: {total_hits}/{total_words} = {rate:.4f}")
    
    print(f"\n=== BEST RESULT ===")
    print(f"Best: {best_result}")
    print(f"Reference good-solve rate (page 73): 9/22 = {9/22:.4f}")
    
    # Save all results
    report_path = pathlib.Path('experiments/2026-09-24/unique_pattern_systematic_test.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump({
            'best': best_result,
            'all_results': all_results,
            'pattern': pattern_vals,
            'reference_rate': 9/22
        }, f, indent=2)
    print(f"Report written to {report_path}")

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
        result.append(vals)
    return result

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

if __name__ == '__main__':
    main()