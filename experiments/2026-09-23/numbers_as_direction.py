#!/usr/bin/env python3
"""
Test "numbers as direction" - different interpretations.
1. Use solved page 73's totient stream as directions on other pages
2. Use page numbers as offsets into other pages
3. Use prime/totient sequences as navigation
"""

import sys, json, pathlib, random
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import RUNE_TO_VAL, VAL_TO_LATIN, ALPHABET_SIZE, totient_of_primes_stream

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

def use_stream_as_vigenere(cipher_vals, key_stream):
    """Apply key stream as Vigenère key (subtract)."""
    result = []
    for i, v in enumerate(cipher_vals):
        k = key_stream[i % len(key_stream)]
        result.append((v - k) % ALPHABET_SIZE)
    return result

def vals_to_words(vals, word_lengths):
    words = []
    start = 0
    for length in word_lengths:
        chunk = vals[start:start+length]
        start += length
        word = ''.join(VAL_TO_LATIN[c % ALPHABET_SIZE] for c in chunk)
        words.append(word)
    return words

def get_word_lengths(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    word_lengths = [len([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]) for w in raw_words]
    return word_lengths

def dict_score(candidate_words, wordset):
    return sum(1 for w in candidate_words if w in wordset)

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
    
    # Get totient stream (the confirmed key for page 73)
    # Page 73 has 85 runes, so we need at least that many
    totient_stream = totient_of_primes_stream(200)  # generate extra
    
    print("=== Testing Totient Stream as Continuous Key Across Pages ===")
    
    # Test: use totient stream as a continuous key across all pages
    # (continuing where each page left off)
    stream_pos = 0
    total_hits = 0
    total_words = 0
    
    for block in unsolved_blocks:
        flat_vals = get_page_vals(block)
        if not flat_vals:
            continue
        word_lengths = get_word_lengths(block)
        
        # Extract key segment for this page
        key_segment = totient_stream[stream_pos:stream_pos + len(flat_vals)]
        stream_pos += len(flat_vals)
        
        if len(key_segment) < len(flat_vals):
            # Extend if needed
            extra = totient_of_primes_stream(len(flat_vals) - len(key_segment))
            key_segment = totient_stream[stream_pos - len(flat_vals):]  # regenerate from pos
            # Actually just use modular
            key_segment = [totient_stream[(stream_pos - len(flat_vals) + i) % len(totient_stream)] for i in range(len(flat_vals))]
        
        # Decode
        decoded = use_stream_as_vigenere(flat_vals, key_segment)
        words = vals_to_words(decoded, word_lengths)
        hits = dict_score(words, wordset)
        total_hits += hits
        total_words += len(words)
    
    rate = total_hits / total_words if total_words else 0
    print(f"Continuous totient stream (carrying position across pages): {total_hits}/{total_words} = {rate:.4f}")
    
    # Test 2: Use totient stream as directions for reading order (permutation)
    print("\n=== Testing Totient Stream as Permutation Indices ===")
    # For each page, use first N totient values as permutation of word order
    total_hits = 0
    total_words = 0
    for block in unsolved_blocks:
        flat_vals = get_page_vals(block)
        if not flat_vals:
            continue
        word_lengths = get_word_lengths(block)
        
        # Use totient to permute the words
        n_words = len(word_lengths)
        perm = [totient_stream[i] % n_words for i in range(n_words)]
        # Apply permutation to word order (reconstruct words in permuted order)
        # First get the words in original order
        words = []
        start = 0
        for length in word_lengths:
            chunk = flat_vals[start:start+length]
            start += length
            word = ''.join(VAL_TO_LATIN[c % ALPHABET_SIZE] for c in chunk)
            words.append(word)
        
        # Permute words
        permuted_words = [words[i % n_words] for i in perm]
        
        hits = dict_score(permuted_words, wordset)
        total_hits += hits
        total_words += len(permuted_words)
    
    rate = total_hits / total_words if total_words else 0
    print(f"Totient permutation of word order: {total_hits}/{total_words} = {rate:.4f}")
    
    # Test 3: Use page numbers as offsets into the totient stream
    print("\n=== Testing Page Numbers as Totient Stream Offsets ===")
    # Page 17 (block 0) uses offset 17, page 18 uses 18, etc.
    total_hits = 0
    total_words = 0
    for page_idx, block in enumerate(unsolved_blocks):
        flat_vals = get_page_vals(block)
        if not flat_vals:
            continue
        word_lengths = get_word_lengths(block)
        
        page_num = 17 + page_idx  # actual page number
        offset = page_num * 10  # some scaling
        
        key_segment = [totient_stream[(offset + i) % len(totient_stream)] for i in range(len(flat_vals))]
        decoded = use_stream_as_vigenere(flat_vals, key_segment)
        words = vals_to_words(decoded, word_lengths)
        hits = dict_score(words, wordset)
        total_hits += hits
        total_words += len(words)
    
    rate = total_hits / total_words if total_words else 0
    print(f"Page-numbered totient offsets: {total_hits}/{total_words} = {rate:.4f}")

    # Test 4: Use values from solved page 73 as a key for other pages
    print("\n=== Testing Solved Page 73 Values as Key ===")
    # Block 55 is page 73 (solved)
    if len(blocks) > 55:
        solved_vals = get_page_vals(blocks[55])
        print(f"Solved page 73 has {len(solved_vals)} runes")
        
        total_hits = 0
        total_words = 0
        for block in unsolved_blocks:
            flat_vals = get_page_vals(block)
            if not flat_vals:
                continue
            word_lengths = get_word_lengths(block)
            
            # Use solved page values as repeating key
            decoded = use_stream_as_vigenere(flat_vals, solved_vals)
            words = vals_to_words(decoded, word_lengths)
            hits = dict_score(words, wordset)
            total_hits += hits
            total_words += len(words)
        
        rate = total_hits / total_words if total_words else 0
        print(f"Solved page 73 values as key: {total_hits}/{total_words} = {rate:.4f}")

    # Test 5: Prime numbers themselves as key (not totient)
    print("\n=== Testing Prime Sequence as Key ===")
    import sympy
    primes = list(sympy.primerange(2, 5000))[:200]
    prime_stream = [p % ALPHABET_SIZE for p in primes]
    
    total_hits = 0
    total_words = 0
    for block in unsolved_blocks:
        flat_vals = get_page_vals(block)
        if not flat_vals:
            continue
        word_lengths = get_word_lengths(block)
        
        decoded = use_stream_as_vigenere(flat_vals, prime_stream)
        words = vals_to_words(decoded, word_lengths)
        hits = dict_score(words, wordset)
        total_hits += hits
        total_words += len(words)
    
    rate = total_hits / total_words if total_words else 0
    print(f"Prime sequence mod 29 as key: {total_hits}/{total_words} = {rate:.4f}")

    print("\nReference good-solve rate (page 73): 9/22 = {:.4f}".format(9/22))

if __name__ == '__main__':
    main()