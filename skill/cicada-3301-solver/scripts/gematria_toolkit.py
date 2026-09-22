#!/usr/bin/env python3
"""
gematria_toolkit.py — reusable Cicada 3301 / Liber Primus cryptanalysis toolkit.

This module bundles everything needed to transcribe, statistically analyze, and
brute-force candidate decryptions of Gematria Primus rune text, so future sessions
don't rewrite this from scratch. See ../references/ruled-out.md for what's already
been tried with this toolkit, and ../references/open-leads.md for what to try next.

Usage as a library:
    from gematria_toolkit import *
    vals = runes_to_values(some_rune_string)
    print(index_of_coincidence(vals))

Usage from CLI:
    python3 gematria_toolkit.py --help
"""

import argparse
import random
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Gematria Primus table (see ../references/gematria-primus.md for full detail)
# ---------------------------------------------------------------------------

GEMATRIA_PRIMUS = [
    # (rune, primary_latin, value/index, prime)
    ('ᚠ', 'F', 0, 2), ('ᚢ', 'U', 1, 3), ('ᚦ', 'TH', 2, 5), ('ᚩ', 'O', 3, 7),
    ('ᚱ', 'R', 4, 11), ('ᚳ', 'C', 5, 13), ('ᚷ', 'G', 6, 17), ('ᚹ', 'W', 7, 19),
    ('ᚻ', 'H', 8, 23), ('ᚾ', 'N', 9, 29), ('ᛁ', 'I', 10, 31), ('ᛄ', 'IO', 11, 37),
    ('ᛇ', 'EO', 12, 41), ('ᛈ', 'P', 13, 43), ('ᛉ', 'X', 14, 47), ('ᛋ', 'S', 15, 53),
    ('ᛏ', 'T', 16, 59), ('ᛒ', 'B', 17, 61), ('ᛖ', 'E', 18, 67), ('ᛗ', 'M', 19, 71),
    ('ᛚ', 'L', 20, 73), ('ᛝ', 'NG', 21, 79), ('ᛟ', 'OE', 22, 83), ('ᛞ', 'D', 23, 89),
    ('ᚪ', 'A', 24, 97), ('ᚫ', 'AE', 25, 101), ('ᚣ', 'Y', 26, 103), ('ᛡ', 'EA', 27, 107),
    ('ᛠ', 'Q', 28, 109),
]

RUNE_TO_VAL = {r: v for r, l, v, p in GEMATRIA_PRIMUS}
VAL_TO_RUNE = {v: r for r, l, v, p in GEMATRIA_PRIMUS}
VAL_TO_LATIN = {v: l for r, l, v, p in GEMATRIA_PRIMUS}
VAL_TO_PRIME = {v: p for r, l, v, p in GEMATRIA_PRIMUS}
LATIN_TO_VAL = {}
for r, l, v, p in GEMATRIA_PRIMUS:
    LATIN_TO_VAL.setdefault(l, v)
# Register alias spellings so word_to_key_values() doesn't silently drop letters
# that share a rune with their primary spelling (this was a real bug found and
# fixed during round-2 testing: 'V' has no rune of its own, it shares ᚢ with 'U',
# but word_to_key_values('DIVINITY') was silently skipping the V entirely instead
# of mapping it to U's value, corrupting every key derived from a V-containing
# word). See references/ruled-out.md for why this matters — any earlier session's
# results for keys containing V/K/Z/J were derived with this bug and should be
# treated with suspicion until re-run.
LATIN_TO_VAL.setdefault('V', LATIN_TO_VAL['U'])
LATIN_TO_VAL.setdefault('K', LATIN_TO_VAL['C'])
LATIN_TO_VAL.setdefault('Z', LATIN_TO_VAL['S'])
LATIN_TO_VAL.setdefault('J', LATIN_TO_VAL['I'])
LATIN_TO_VAL.setdefault('IA', LATIN_TO_VAL['IO'])
ALPHABET_SIZE = 29

# Ambiguous mappings — a decoded rune value's "letter" may plausibly be rendered
# multiple ways. Use when scoring against a dictionary so real hits aren't missed.
AMBIGUOUS_EQUIV = {
    'C': ['C', 'K'], 'K': ['C', 'K'],
    'S': ['S', 'Z'], 'Z': ['S', 'Z'],
    'U': ['U', 'V'], 'V': ['U', 'V'],
    'IO': ['IO', 'IA'],
}


# ---------------------------------------------------------------------------
# Transcription helpers
# ---------------------------------------------------------------------------

def runes_to_values(rune_text):
    """Strip non-rune characters (delimiters, whitespace) and return Gematria values."""
    return [RUNE_TO_VAL[ch] for ch in rune_text if ch in RUNE_TO_VAL]


def parse_page_block(raw_block):
    """
    Parse a raw transcription block (as found in runes-text.txt, which uses
    '-' as word separator, '/' and newlines as line-continuation markers) into
    (flat_values, word_lengths). word_lengths lets you reconstruct word
    boundaries after applying a cipher.
    """
    clean = raw_block.replace('/', '').replace('\n', '')
    words = [w for w in clean.split('-') if w]
    word_vals = [[RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL] for w in words]
    word_vals = [w for w in word_vals if w]  # drop empty (e.g. pure-punctuation) tokens
    flat = [v for w in word_vals for v in w]
    lens = [len(w) for w in word_vals]
    return flat, lens


def values_to_words(vals, word_lengths):
    """Reconstruct a list of Latin-letter 'words' from decrypted values + word lengths."""
    letters = [VAL_TO_LATIN[v % ALPHABET_SIZE] for v in vals]
    out, i = [], 0
    for length in word_lengths:
        out.append(''.join(letters[i:i + length]))
        i += length
    return out


# ---------------------------------------------------------------------------
# Statistical analysis
# ---------------------------------------------------------------------------

def index_of_coincidence(vals):
    """
    Standard IC over the 29-symbol Gematria alphabet.
    Reference baselines (see references/ruled-out.md):
      - random 29-symbol text: ~0.0345
      - monoalphabetic-substituted English (scaled to 29 symbols): ~0.06-0.07
    """
    n = len(vals)
    if n < 2:
        return 0.0
    counts = Counter(vals)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator if denominator else 0.0


def friedman_test(pages_of_vals, max_key_length=20):
    """
    Test candidate Vigenère key lengths 1..max_key_length by average per-column IC,
    computed independently per page (key assumed to restart each page) then
    averaged. Returns dict {key_length: avg_ic}. A real key length should show a
    clear spike well above the random baseline (~0.0345); see ruled-out.md for the
    result of running this against all 56 unsolved LP2 pages (flat everywhere,
    no spike found for lengths 1-20).
    """
    results = {}
    for keylen in range(1, max_key_length + 1):
        page_ics = []
        for vals in pages_of_vals:
            if len(vals) < keylen * 3:
                continue
            cols = [[vals[i] for i in range(c, len(vals), keylen)] for c in range(keylen)]
            col_ics = [index_of_coincidence(c) for c in cols if len(c) > 1]
            if col_ics:
                page_ics.append(sum(col_ics) / len(col_ics))
        results[keylen] = sum(page_ics) / len(page_ics) if page_ics else 0.0
    return results


def word_length_kasiski(word_lengths, ngram_lengths=(3, 4, 5, 6, 7, 8)):
    """
    Kasiski-style examination applied to the SEQUENCE OF WORD LENGTHS rather than
    letter/rune values. This is a genuinely different signal channel from
    kasiski_examination() (which works on letter values) — it found a real,
    specific match (an 8-word-length run shared between two pages) in round-2
    testing; see references/ruled-out.md "Round 2 tests" and
    references/open-leads.md item 0 for the actual finding and follow-up steps.

    `word_lengths` should be the GLOBAL concatenated word-length sequence across
    however many pages you want to search jointly (e.g. all 56 unsolved pages
    concatenated) — pass a (page_index, local_word_index) lookup table alongside
    if you need to map a hit back to a specific page (see the ad hoc code in this
    skill's development history / open-leads.md for the pattern).

    Returns {n: {pattern_tuple: [positions]}} for n in ngram_lengths, repeated
    patterns only (positions list length > 1).
    """
    results = {}
    for n in ngram_lengths:
        positions = defaultdict(list)
        for i in range(len(word_lengths) - n + 1):
            positions[tuple(word_lengths[i:i + n])].append(i)
        results[n] = {g: p for g, p in positions.items() if len(p) > 1}
    return results


def extend_match(seq, p1, p2):
    """Given two starting positions in seq that are known to match, extend the
    match as far as possible in both directions and return (start_offset_from_p1,
    length) — i.e. how far before p1/p2 the match also holds, and total length.
    Useful for finding the FULL extent of a repeat found by word_length_kasiski
    or kasiski_examination (which only report the seed n-gram length)."""
    # extend forward
    fwd = 0
    while p1 + fwd < len(seq) and p2 + fwd < len(seq) and seq[p1 + fwd] == seq[p2 + fwd]:
        fwd += 1
    # extend backward
    back = 0
    while p1 - back - 1 >= 0 and p2 - back - 1 >= 0 and seq[p1 - back - 1] == seq[p2 - back - 1]:
        back += 1
    return back, fwd + back


def kasiski_examination(vals, ngram_lengths=(3, 4, 5)):
    """
    Find repeated n-grams and the factors of the distances between repeats.
    Returns {n: {'num_repeated': int, 'num_distances': int, 'top_factors': [(factor, count), ...]}}.
    A spike in one factor across n-gram lengths suggests that factor is the key length.
    """
    results = {}
    for n in ngram_lengths:
        positions = defaultdict(list)
        for i in range(len(vals) - n + 1):
            positions[tuple(vals[i:i + n])].append(i)
        repeated = {g: p for g, p in positions.items() if len(p) > 1}
        distances = []
        for g, plist in repeated.items():
            for i in range(len(plist) - 1):
                for j in range(i + 1, len(plist)):
                    distances.append(plist[j] - plist[i])
        factor_counts = Counter()
        for d in distances:
            for f in range(2, 40):
                if d % f == 0:
                    factor_counts[f] += 1
        results[n] = {
            'num_repeated': len(repeated),
            'num_distances': len(distances),
            'top_factors': factor_counts.most_common(10),
        }
    return results


# ---------------------------------------------------------------------------
# Cipher operations
# ---------------------------------------------------------------------------

def vigenere_decode(vals, key_vals, shift_up=True):
    """Apply/remove an additive (Vigenère-style) key over mod-29 Gematria values."""
    out = []
    for i, v in enumerate(vals):
        k = key_vals[i % len(key_vals)]
        out.append((v + k) % ALPHABET_SIZE if shift_up else (v - k) % ALPHABET_SIZE)
    return out


def word_to_key_values(word):
    """Convert an English word (e.g. 'DIVINITY') into a Gematria key-value stream."""
    key = []
    w = word.upper()
    i = 0
    # greedily match multi-letter tokens (TH, NG, OE, EO, EA, IO, AE) before single letters
    multi = sorted([l for l in LATIN_TO_VAL if len(l) > 1], key=len, reverse=True)
    while i < len(w):
        matched = False
        for tok in multi:
            if w[i:i + len(tok)] == tok:
                key.append(LATIN_TO_VAL[tok])
                i += len(tok)
                matched = True
                break
        if not matched:
            if w[i] in LATIN_TO_VAL:
                key.append(LATIN_TO_VAL[w[i]])
            i += 1
    return key


def reversed_gematria(vals):
    """Atbash-style reversal used to solve LP1 page 01. reversed(v) = 28 - v."""
    return [(ALPHABET_SIZE - 1) - v for v in vals]


def totient_of_primes_stream(length):
    """
    The stream confirmed to solve LP2 page 73 ("An End"): phi(nth prime) = (nth
    prime - 1), mod 29, for the first `length` primes. Requires sympy.
    """
    import sympy
    primes = list(sympy.primerange(2, length * 20 + 100))[:length]
    return [(p - 1) % ALPHABET_SIZE for p in primes]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def load_dictionary(path='words_alpha.txt', min_len=3):
    """Load an English word list (one word per line) for dictionary-based scoring.
    See references/data-sources.md for where to download this file."""
    words = set()
    with open(path) as f:
        for line in f:
            w = line.strip().upper()
            if len(w) >= min_len:
                words.add(w)
    return words


def dict_score(candidate_words, wordset):
    """
    Count how many candidate 'words' (from values_to_words) are real dictionary
    words. ALWAYS compare this against a random-shuffle-control score computed the
    same way (see random_control_score below) before treating a result as signal —
    see references/ruled-out.md for calibration numbers.
    """
    return sum(1 for w in candidate_words if w in wordset)


def random_control_score(vals, word_lengths, wordset, seed=42):
    """Shuffle the values randomly and re-run dict_score, as a noise baseline."""
    rng = random.Random(seed)
    shuffled = vals[:]
    rng.shuffle(shuffled)
    words = values_to_words(shuffled, word_lengths)
    return dict_score(words, wordset)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--transcription', help='Path to runes-text.txt-style file')
    parser.add_argument('--wordlist', default='words_alpha.txt')
    parser.add_argument('--exclude-block', type=int, action='append', default=[],
                         help='Block index to exclude (e.g. already-solved pages)')
    parser.add_argument('--friedman', action='store_true', help='Run Friedman key-length test')
    parser.add_argument('--kasiski', action='store_true', help='Run Kasiski examination')
    parser.add_argument('--try-keys', nargs='*', default=[],
                         help='English words to try as Vigenere keys')
    args = parser.parse_args()

    if not args.transcription:
        print("Provide --transcription path/to/runes-text.txt (see references/data-sources.md)")
        return

    with open(args.transcription, encoding='utf-8') as f:
        content = f.read()
    blocks = [b for i, b in enumerate(content.split('%'))
              if b.strip() and i not in args.exclude_block]

    pages = [parse_page_block(b) for b in blocks]
    pages_vals = [p[0] for p in pages if p[0]]

    if args.friedman:
        print("Friedman test (avg column IC per key length):")
        for kl, ic in friedman_test(pages_vals).items():
            print(f"  keylen={kl:3d}  avg_ic={ic:.4f}")

    if args.kasiski:
        all_vals = [v for p in pages_vals for v in p]
        print(f"Kasiski examination on {len(all_vals)} concatenated runes:")
        for n, res in kasiski_examination(all_vals).items():
            print(f"  n={n}: {res['num_repeated']} repeated grams, "
                  f"top factors: {res['top_factors']}")

    if args.try_keys:
        try:
            wordset = load_dictionary(args.wordlist)
        except FileNotFoundError:
            print(f"Word list not found at {args.wordlist} — see references/data-sources.md")
            return
        for word in args.try_keys:
            key = word_to_key_values(word)
            for shift_up in (True, False):
                total_hits, total_words = 0, 0
                for flat, lens in pages:
                    if not flat:
                        continue
                    dec = vigenere_decode(flat, key, shift_up)
                    words = values_to_words(dec, lens)
                    total_hits += dict_score(words, wordset)
                    total_words += len(words)
                rate = total_hits / total_words if total_words else 0
                direction = 'up' if shift_up else 'down'
                print(f"key={word:16s} dir={direction:4s} hits={total_hits:4d}/{total_words:4d} rate={rate:.3f}")


if __name__ == '__main__':
    _cli()
