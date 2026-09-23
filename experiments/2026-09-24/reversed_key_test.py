#!/usr/bin/env python3
"""
Test reversed key text as running key across all 56 unsolved pages.
Cicada uses reversed gematria on solved pages 06-09, so reversed key text is high-prior.
"""

import sys, json, pathlib, random
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import RUNE_TO_VAL, VAL_TO_LATIN, ALPHABET_SIZE, LATIN_TO_VAL

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

def text_to_key_stream(text):
    """Convert text to a stream of Gematria values."""
    stream = []
    for ch in text.upper():
        if ch in LATIN_TO_VAL:
            stream.append(LATIN_TO_VAL[ch])
    return stream

def dict_score(candidate_words, wordset):
    return sum(1 for w in candidate_words if w in wordset)

def random_control_score(vals, word_lengths, wordset, seed=42):
    rng = random.Random(seed)
    shuffled = vals[:]
    rng.shuffle(shuffled)
    words = []
    start = 0
    for length in word_lengths:
        chunk = shuffled[start:start+length]
        start += length
        letter_chunk = ''.join(chr((c % 26) + ord('A')) for c in chunk)
        words.append(letter_chunk)
    return dict_score(words, wordset)

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
        print('Dictionary file not found')
        return
    
    # Load key texts
    key_texts = {}
    download_dir = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download'
    
    try:
        with open(f'{download_dir}/kjv_gutenberg.txt', encoding='utf-8') as f:
            key_texts['KJV'] = f.read()
        with open(f'{download_dir}/liber_al_vel_legis.txt', encoding='utf-8') as f:
            key_texts['Liber_AL'] = f.read()
        with open(f'{download_dir}/mabinogion.txt', encoding='utf-8') as f:
            key_texts['Mabinogion'] = f.read()
        with open(f'{download_dir}/blake_marriage_of_heaven_and_hell.txt', encoding='utf-8') as f:
            key_texts['Blake'] = f.read()
    except FileNotFoundError as e:
        print(f"Key text file not found: {e}")
        return
    
    # Test both forward and reversed
    best_result = {'rate': 0}
    all_results = []
    
    for text_name, text_content in key_texts.items():
        for reverse in (False, True):
            text = text_content[:200]
            
            if reverse:
                text = text[::-1]
            
            key_stream = []
            for ch in text.upper():
                if ch in LATIN_TO_VAL:
                    key_stream.append(LATIN_TO_VAL[ch])
            
            if not key_stream:
                continue
            
            total_hits = 0
            total_words = 0
            for block in unsolved_blocks:
                flat_vals = get_page_vals(block)
                if not flat_vals:
                    continue
                word_lengths = get_word_lengths(block)
                
                decoded_vals = []
                for i, v in enumerate(flat_vals):
                    k = key_stream[i % len(key_stream)]
                    decoded_vals.append((v - k) % ALPHABET_SIZE)
                
                words = vals_to_words(decoded_vals, word_lengths)
                hits = dict_score(words, wordset)
                total_hits += hits
                total_words += len(words)
            
            if total_words == 0:
                continue
            rate = total_hits / total_words
            direction = 'reversed' if reverse else 'forward'
            all_results.append({
                'text': text_name,
                'direction': direction,
                'hits': total_hits,
                'total_words': total_words,
                'rate': rate
            })
            
            if rate > best_result['rate']:
                best_result = {
                    'text': text_name,
                    'direction': direction,
                    'rate': rate,
                    'hits': total_hits,
                    'total_words': total_words
                }
            
            print(f"{text_name} {direction}: {total_hits}/{total_words} = {rate:.4f}")
    
    print(f"\nBest result: {best_result}")
    print(f"Reference good-solve rate (page 73): 9/22 = {9/22:.4f}")
    
    # Save all results
    report_path = pathlib.Path('experiments/2026-09-24/reversed_key_test.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump({
            'best': best_result,
            'all_results': all_results,
            'reference_rate': 9/22
        }, f, indent=2)
    print(f"Report written to {report_path}")

if __name__ == '__main__':
    main()