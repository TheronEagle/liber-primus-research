#!/usr/bin/env python3
"""
Check baseline dictionary hit rate for raw (unscrambled) transliteration.
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

def dict_score(candidate_words, wordset):
    return sum(1 for w in candidate_words if w in wordset)

def main():
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    unsolved_blocks = blocks[:55]
    
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
    
    total_hits = 0
    total_words = 0
    for block in unsolved_blocks:
        flat_vals = get_page_vals(block)
        if not flat_vals:
            continue
        word_lengths = get_word_lengths(block)
        words = vals_to_words(flat_vals, word_lengths)
        hits = dict_score(words, wordset)
        total_hits += hits
        total_words += len(words)
    
    rate = total_hits / total_words if total_words else 0
    print(f"Raw transliteration (no decryption): {total_hits}/{total_words} = {rate:.4f}")
    print(f"Reference good-solve rate (page 73): 9/22 = {9/22:.4f}")

if __name__ == '__main__':
    main()