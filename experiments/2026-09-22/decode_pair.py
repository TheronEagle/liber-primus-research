#!/usr/bin/env python3
"""
Simple decoder for the two 8-word runs (page 22 word 45 and page 47 word 11)
using an autokey‑style Vigenère decode with one run as the key for the other.
Compute dictionary hit rates and compare to random‑control baselines.
"""

import sys, json, pathlib, random
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import *

def load_transcription_blocks(path):
    """Read the rtdk transcription file and split into blocks by '%' delimiter."""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('\n%')
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def get_word_runes(block, idx):
    """Return (rune_str, values) for the word at 0‑based index idx."""
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    if idx >= len(raw_words):
        return None, None
    rune_word = raw_words[idx]
    vals = [RUNE_TO_VAL[ch] for ch in rune_word if ch in RUNE_TO_VAL]
    return rune_word, vals

def decode_key(cipher_vals, key_vals, shift_up=True):
    """Vigenère‑style decode; shift_up=True means subtract key."""
    out = []
    for i, v in enumerate(cipher_vals):
        k = key_vals[i % len(key_vals)]
        out.append((v - k) % 29 if shift_up else (v + k) % 29)
    return out

def dict_score(candidate_words, wordset):
    """Count how many candidate words appear in the reference wordset."""
    return sum(1 for w in candidate_words if w in wordset)

def random_control_score(vals, word_lengths, wordset, seed=42):
    """Shuffle and recompute dict_score as a noise baseline."""
    rng = random.Random(seed)
    shuffled = vals[:]
    rng.shuffle(shuffled)
    # Re‑split into words according to original word_lengths
    words = []
    start = 0
    for length in word_lengths:
        chunk = shuffled[start:start+length]
        start += length
        # Map each numeric value to a letter A‑Z (0→A, 1→B, …)
        letter_chunk = ''.join(chr((c % 26) + ord('A')) for c in chunk)
        words.append(letter_chunk)
    return dict_score(words, wordset)

def main():
    # --------------------------------------------------------------
    # Load transcription blocks
    # --------------------------------------------------------------
    transcription_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    blocks = load_transcription_blocks(transcription_path)
    # Page 22 ≈ block 5, Page 47 ≈ block 30 (per page‑catalog.md)
    p22_block = blocks[5]   # page 22
    p47_block = blocks[30]  # page 47
    
    # Target word indices (0‑based)
    start22 = 44  # word 45 (1‑based)
    start47 = 10  # word 11 (1‑based)
    
    # Extract runs
    _, vals22 = get_word_runes(p22_block, start22)
    _, vals47 = get_word_runes(p47_block, start47)
    if not vals22 or not vals47:
        print('Failed to extract one of the runs.')
        return
    
    # --------------------------------------------------------------
    # Load a simple English word list
    # --------------------------------------------------------------
    try:
        wordset = set()
        with open('/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/data/words_alpha.txt', encoding='utf-8') as f:
            for line in f:
                w = line.strip().upper()
                if len(w) >= 3:
                    wordset.add(w)
    except FileNotFoundError:
        print('Dictionary file not found – skipping dictionary scoring.')
        wordset = set()
    
    # --------------------------------------------------------------
    # Autokey decode (use page‑22 run as the key)
    # --------------------------------------------------------------
    decoded_up   = decode_key(vals47, vals22, shift_up=True)   # subtract key
    decoded_down = decode_key(vals47, vals22, shift_up=False)  # add key
    
    # --------------------------------------------------------------
    # Convert numeric values to letters A‑Z (mod 26)
    # --------------------------------------------------------------
    def to_letters(vals):
        return ''.join(chr((c % 26) + ord('A')) for c in vals)
    
    up_letters   = to_letters(decoded_up)
    down_letters = to_letters(decoded_down)
    
    # --------------------------------------------------------------
    # Scoring (dictionary hit rates)
    # --------------------------------------------------------------
    score_up   = None
    score_down = None
    ctrl_up    = None
    ctrl_down  = None
    if wordset:
        # Treat the whole decoded string as a single “word” for scoring
        score_up   = dict_score([up_letters],   wordset)
        score_down = dict_score([down_letters],  wordset)
        # Random‑control baseline (shuffle numeric values, map to letters, treat as single “word”)
        ctrl_up    = random_control_score(vals47, [len(up_letters)],   wordset)
        ctrl_down  = random_control_score(vals47, [len(down_letters)], wordset)
    
    # Reference good‑solve rate (page 73 solved 9/22 ≈ 41 %)
    REF_GOOD_RATIO = 9 / 22  # ≈ 41 %
    
    # --------------------------------------------------------------
    # Output
    # --------------------------------------------------------------
    print('\n=== Decoding Results ===')
    print(f'Page 47 decoded (shift‑up)   : {up_letters}')
    print(f'  Length (chars)               : {len(up_letters)}')
    print(f'Page 47 decoded (shift‑down) : {down_letters}')
    print(f'  Length (chars)               : {len(down_letters)}')
    if wordset:
        print(f'Random‑control baseline (up)   : {ctrl_up}')
        print(f'Random‑control baseline (down) : {ctrl_down}')
        print(f'Reference good‑solve rate (page 73) ≈ {REF_GOOD_RATIO:.2%}')
        if score_up is not None and (score_up > REF_GOOD_RATIO or score_down > REF_GOOD_RATIO):
            print('>>> ***Potential signal*** – decoded hit‑rate exceeds known good solve! <<<')
        else:
            print('>>> No signal exceeding known good solve <<<')
    else:
        print('Dictionary not loaded – skipping hit calculations.')
    
    # --------------------------------------------------------------
    # Save a tiny JSON report for future inspection
    # --------------------------------------------------------------
    report_path = pathlib.Path('experiments/2026-09-22/decode_report.json')
    report = {
        'run_page47_values'   : vals47,
        'decoded_up'          : up_letters,
        'decoded_down'        : down_letters,
        'reference_good_rate' : REF_GOOD_RATIO
    }
    if wordset:
        report.update({
            'dict_scores_up'    : score_up,
            'dict_scores_down'  : score_down,
            'random_control_up' : ctrl_up,
            'random_control_down': ctrl_down
        })
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f'\nReport written to {report_path}')

if __name__ == '__main__':
    main()