#!/usr/bin/env python3
"""
Deep check on the self-decrypt hit at offset 33 for block 40.
Get the actual words to see what's being matched.
"""

import sys
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import RUNE_TO_VAL, VAL_TO_LATIN, ALPHABET_SIZE

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

def get_words_and_values(block):
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    result = []
    for w in raw_words:
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        result.append((w, vals, len(vals)))
    return result

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    
    # Load dictionary
    wordset = set()
    with open('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/words_alpha.txt', encoding='utf-8') as f:
        for line in f:
            w = line.strip().upper()
            if len(w) >= 3:
                wordset.add(w)
    
    # Block 40
    block40 = blocks[40]
    block40_vals = get_page_vals(block40)
    b40_word_lengths = get_word_lengths(block40)
    b40_words = get_words_and_values(block40)
    
    # Pattern at words 42-49 (indices 41-48)
    pattern_vals = []
    for i in range(41, 49):
        if i < len(b40_words):
            pattern_vals.extend(b40_words[i][1])
    
    print(f"Pattern length: {len(pattern_vals)} values")
    
    # Test self-decrypt at offset 33 (the one that gave 5/57 hits)
    offset = 33
    rotated = pattern_vals[offset:] + pattern_vals[:offset]
    
    decoded = [(v - k) % 29 for v, k in zip(block40_vals, (pattern_vals[offset:] + pattern_vals[:offset] + pattern_vals)[:len(block40_vals)])]
    
    words = []
    start = 0
    for length in get_word_lengths(block40):
        chunk = decoded[start:start+length]
        start += length
        word = ''.join(VAL_TO_LATIN[c % ALPHABET_SIZE] for c in chunk)
        words.append(word)
    
    print(f"Total words: {len(words)}")
    print("\nDecoded words with dictionary hits:")
    hits = 0
    for i, word in enumerate(words):
        hit = word in wordset
        if hit:
            hits += 1
            print(f"  Word {i+1}: {word} <-- HIT!")
        else:
            print(f"  Word {i+1}: {word}")
    
    print(f"\nTotal hits: {hits}/{len(words)} = {hits/len(words):.4f}")
    
    # Also check raw transliteration for comparison
    print("\n=== RAW TRANSLITERATION (for comparison) ===")
    raw_words = []
    start = 0
    for length in get_word_lengths(block40):
        chunk = block40_vals[start:start+length]
        start += length
        word = ''.join(VAL_TO_LATIN[c % ALPHABET_SIZE] for c in chunk)
        raw_words.append(word)
    
    raw_hits = 0
    for i, word in enumerate(raw_words):
        hit = word in wordset
        if hit:
            raw_hits += 1
            print(f"  Word {i+1}: {word} <-- HIT!")
        else:
            print(f"  Word {i+1}: {word}")
    
    print(f"Raw hits: {raw_hits}/{len(raw_words)} = {raw_hits/len(raw_words):.4f}")
    
    # Now let's check what specific words are being matched at offset 33
    print("\n=== HITS AT OFFSET 33 ===")
    for i, word in enumerate(words):
        if word in wordset:
            print(f"  Word {i+1} (length {len(word)}): '{word}'")

if __name__ == '__main__':
    main()