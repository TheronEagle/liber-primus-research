#!/usr/bin/env python3
"""
Test diagonal and spiral orderings of the page 5 magic square as Vigenère keys.
The row-major and column-major were already tested and ruled out.
The square's symmetry means row-major and column-major are similar,
but diagonal and spiral traversals would be genuinely different sequences.
"""

import sys, json, pathlib
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
    
    # Page 5 magic square (5x5)
    # Values from ruled-out.md
    square = [
        [272, 138, 341, 131, 151],
        [366, 199, 130, 320, 18],
        [226, 245, 91, 245, 226],
        [18, 320, 130, 199, 366],
        [151, 131, 341, 138, 272]
    ]
    
    # Mod 29 for Vigenère
    square_mod = [[v % 29 for v in row] for row in square]
    print("Magic square (mod 29):")
    for row in square_mod:
        print(f"  {row}")
    
    # Different traversal orders
    def diagonal_main(sq):
        """Main diagonal (top-left to bottom-right)"""
        return [sq[i][i] for i in range(len(sq))]
    
    def diagonal_anti(sq):
        """Anti-diagonal (top-right to bottom-left)"""
        n = len(sq)
        return [sq[i][n-1-i] for i in range(n)]
    
    def spiral_clockwise(sq):
        """Clockwise spiral from top-left"""
        n = len(sq)
        result = []
        top, bottom = 0, n-1
        left, right = 0, n-1
        while top <= bottom and left <= right:
            # top row
            for j in range(left, right+1):
                result.append(sq[top][j])
            top += 1
            # right column
            for i in range(top, bottom+1):
                result.append(sq[i][right])
            right -= 1
            # bottom row
            if top <= bottom:
                for j in range(right, left-1, -1):
                    result.append(sq[bottom][j])
                bottom -= 1
            # left column
            if left <= right:
                for i in range(bottom, top-1, -1):
                    result.append(sq[i][left])
                left += 1
        return result
    
    def spiral_counterclockwise(sq):
        """Counter-clockwise spiral from top-left"""
        n = len(sq)
        result = []
        top, bottom = 0, n-1
        left, right = 0, n-1
        while top <= bottom and left <= right:
            # left column
            for i in range(top, bottom+1):
                result.append(sq[i][left])
            left += 1
            # bottom row
            for j in range(left, right+1):
                result.append(sq[bottom][j])
            bottom -= 1
            # right column
            if left <= right:
                for i in range(bottom, top-1, -1):
                    result.append(sq[i][right])
                right -= 1
            # top row
            if top <= bottom:
                for j in range(right, left-1, -1):
                    result.append(sq[top][j])
                top += 1
        return result
    
    def zigzag_rows(sq):
        """Zigzag row traversal"""
        result = []
        for i, row in enumerate(sq):
            if i % 2 == 0:
                result.extend(row)
            else:
                result.extend(reversed(row))
        return result
    
    def zigzag_cols(sq):
        """Zigzag column traversal"""
        result = []
        n = len(sq)
        for j in range(n):
            col = [sq[i][j] for i in range(n)]
            if j % 2 == 0:
                result.extend(col)
            else:
                result.extend(reversed(col))
        return result
    
    traversals = {
        'diagonal_main': diagonal_main(square_mod),
        'diagonal_anti': diagonal_anti(square_mod),
        'spiral_clockwise': spiral_clockwise(square_mod),
        'spiral_counterclockwise': spiral_counterclockwise(square_mod),
        'zigzag_rows': zigzag_rows(square_mod),
        'zigzag_cols': zigzag_cols(square_mod),
    }
    
    print("Traversal sequences:")
    for name, seq in traversals.items():
        print(f"  {name}: {seq}")
    
    # Load transcription and dictionary
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
    
    best_result = {'rate': 0}
    all_results = []
    
    for name, key_vals in traversals.items():
        print(f"\n=== Testing {name} ===")
        print(f"  Key: {key_vals}")
        
        total_hits = 0
        total_words = 0
        for block in unsolved_blocks:
            flat_vals = get_page_vals(block)
            if not flat_vals:
                continue
            word_lengths = get_word_lengths(block)
            
            decoded = [(v - k) % 29 for v, k in zip(flat_vals, (key_vals * ((len(flat_vals)//len(key_vals))+1))[:len(flat_vals)])]
            words = vals_to_words(decoded, word_lengths)
            hits = dict_score(words, wordset)
            total_hits += hits
            total_words += len(words)
        
        if total_words == 0:
            continue
        rate = total_hits / total_words
        
        # Also test shift-down (add key)
        total_hits_down = 0
        for block in unsolved_blocks:
            flat_vals = get_page_vals(block)
            if not flat_vals:
                continue
            word_lengths = get_word_lengths(block)
            
            decoded = [(v + k) % 29 for v, k in zip(flat_vals, (key_vals * ((len(flat_vals)//len(key_vals))+1))[:len(flat_vals)])]
            words = vals_to_words(decoded, get_word_lengths(block))
            hits = dict_score(words, wordset)
            total_hits_down += hits
        
        rate_down = total_hits_down / total_words if total_words else 0
        
        print(f"  Shift up: {total_hits}/{total_words} = {total_hits/total_words:.4f}")
        print(f"  Shift down: {total_hits_down}/{total_words} = {rate_down:.4f}")
        
        for direction, hits, rate in [('up', total_hits, total_hits/total_words), ('down', total_hits_down, rate_down)]:
            all_results.append({
                'traversal': name,
                'direction': direction,
                'hits': hits,
                'total_words': total_words,
                'rate': rate
            })
            
            if rate > best_result['rate']:
                best_result = {
                    'traversal': name,
                    'direction': direction,
                    'rate': rate,
                    'hits': hits,
                    'total_words': total_words
                }
    
    print(f"\n=== BEST RESULT ===")
    print(f"Best: {best_result}")
    print(f"Reference good-solve rate (page 73): 9/22 = {9/22:.4f}")
    
    # Save all results
    report_path = pathlib.Path('experiments/2026-09-24/magic_square_diagonal_spiral.json')
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

if __name__ == '__main__':
    main()