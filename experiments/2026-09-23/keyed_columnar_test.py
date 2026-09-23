#!/usr/bin/env python3
"""
Test keyed columnar transposition on all 56 unsolved pages.
Columns are permuted according to a keyword (standard columnar transposition).
Test multiple keyword candidates and column widths.
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

def get_column_order(keyword):
    """Get column reading order from keyword (alphabetical with tie-breaker by position)."""
    key_pairs = [(ch, i) for i, ch in enumerate(keyword)]
    key_pairs.sort(key=lambda x: (x[0], x[1]))
    return [pair[1] for pair in key_pairs]

def columnar_transpose_decrypt(cipher_vals, keyword):
    """
    Decrypt a columnar transposition cipher.
    The number of columns equals the keyword length.
    """
    n = len(cipher_vals)
    if n == 0:
        return []
    
    num_cols = len(keyword)
    num_rows = (n + num_cols - 1) // num_cols
    num_full_cols = n % num_cols
    if num_full_cols == 0:
        num_full_cols = num_cols
    
    col_order = get_column_order(keyword)
    col_heights = [num_rows if i < num_full_cols else num_rows - 1 for i in range(num_cols)]
    
    # Fill grid column by column in keyword order
    grid = [[None] * num_cols for _ in range(num_rows)]
    idx = 0
    for col_idx in col_order:
        height = col_heights[col_idx]
        for row in range(height):
            grid[row][col_idx] = cipher_vals[idx]
            idx += 1
    
    # Read out row by row
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            val = grid[row][col]
            if val is not None:
                result.append(val)
    return result

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

def test_single_key(block, wordset, keyword):
    """Test a single keyword on one block."""
    flat_vals = get_page_vals(block)
    if not flat_vals:
        return 0, 0
    word_lengths = get_word_lengths(block)
    decrypted_vals = columnar_transpose_decrypt(flat_vals, keyword)
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
    
    # Keyword candidates from Cicada vocabulary
    keywords = [
        'DIVINITY', 'FIRFUMFERENFE', 'INSTAR', 'EMERGE', 'PRIMALITY', 'SACRED',
        'TOTIENT', 'PILGRIM', 'PARABLE', 'WISDOM', 'CICADA', 'PRIME', 'PRIMES',
        'KOAN', 'WARNING', 'SHADOW', 'TRUTH', 'DEATH', 'BOOK', 'CIRCUMFERENCE',
        'CONSUMPTION', 'PRESERVATION', 'ADHERENCE', 'BELONG', 'REALITY', 'ILLUSION',
        'SURFACE', 'TUNNELING', 'WITHIN', 'WITHOUT', 'SELF', 'BEING', 'LAW', 'HOLY',
        'LIBERPRIMUS', 'GEMATRIA', 'INSTRUCTION', 'JOURNEY', 'ENLIGHTENED', 'MASTER',
        'STUDENT', 'CONSCIOUSNESS', 'QUESTION', 'PROGRAM', 'MIND'
    ]
    
    best_result = {'rate': 0}
    all_results = []
    
    for keyword in keywords:
        # Remove duplicate letters while preserving order for keyed transposition
        seen = set()
        clean_keyword = ''
        for ch in keyword:
            if ch not in seen:
                seen.add(ch)
                clean_keyword += ch
        if len(clean_keyword) < 2:
            continue
        
        total_hits = 0
        total_words = 0
        for block in unsolved_blocks:
            hits, words = test_single_key(block, wordset, clean_keyword)
            total_hits += hits
            total_words += words
        
        if total_words == 0:
            continue
        rate = total_hits / total_words
        all_results.append({
            'keyword': keyword,
            'clean_keyword': clean_keyword,
            'num_cols': len(clean_keyword),
            'hits': total_hits,
            'total_words': total_words,
            'rate': rate
        })
        
        if rate > best_result['rate']:
            best_result = {
                'keyword': keyword,
                'clean_keyword': clean_keyword,
                'num_cols': len(clean_keyword),
                'rate': rate,
                'hits': total_hits,
                'total_words': total_words
            }
        
        if rate > 0.05:  # Only log notable results
            print(f"Keyword: {keyword} ({clean_keyword}), cols: {len(clean_keyword)}, hits: {total_hits}/{total_words} = {rate:.4f}")
    
    # Random control
    print("\nRunning random control...")
    all_vals = []
    for block in unsolved_blocks:
        all_vals.extend(get_page_vals(block))
    ctrl_rate = random_control_score(all_vals, [len(all_vals)], wordset)
    print(f"Random control baseline: {ctrl_rate:.4f}")
    
    print(f"\nBest result: {best_result}")
    print(f"Reference good-solve rate (page 73): 9/22 = {9/22:.4f}")
    
    # Save all results
    report_path = pathlib.Path('experiments/2026-09-23/keyed_columnar_test.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump({
            'best': best_result,
            'all_results': all_results,
            'control_rate': ctrl_rate,
            'reference_rate': 9/22
        }, f, indent=2)
    print(f"Report written to {report_path}")

if __name__ == '__main__':
    main()