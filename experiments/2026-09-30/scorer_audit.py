#!/usr/bin/env python3
"""
Audit the dictionary scorer itself, on text whose plaintext is KNOWN.

THE SUSPECT
-----------
`gematria_toolkit.dict_score()` counts a candidate word as a hit only on exact
string equality against a 370k word list. But Gematria Primus is a 29-symbol
alphabet over 26+ English letters, so several runes are ambiguous:

    ᚳ -> C or K      ᛋ -> S or Z      ᚢ -> U or V      ᛁ -> I or J
    ᛄ -> IO or IA   ᚫ -> AE         ᛡ -> EA          ᛝ -> NG or ING
    ᚦ -> TH         ᛟ -> OE

`values_to_words()` renders each value with its PRIMARY Latin spelling only. So
a perfect decrypt of a page whose plaintext contains any of those letters scores
as a MISS. Worse, the miss is systematic, not random: it hits the same words in
the same way for every candidate key, which is exactly the kind of bias that can
manufacture a false negative across an entire research program.

Note `SKILL.md` claims "scripts/gematria_toolkit.py handles this via
normalize_ambiguous()". That function does not exist in the toolkit (verified by
grep over the whole repo: zero hits for `normalize_ambiguous`). The documented
mitigation was never implemented.

WHY THIS MATTERS FOR THE WHOLE REPO
------------------------------------
Every hit rate in ruled-out.md -- the 3-4% "noise floor", the 6.41% raw
transliteration baseline, the 40.9% page-73 benchmark that everything is
calibrated against -- comes from this scorer. If the scorer's ceiling is low, the
noise floor is inflated, and genuine signals have been discarded as "noise" for
the entire history of the project. The benchmark itself needs re-measuring.

METHOD
------
1. Build an ambiguity-aware scorer: a candidate word hits if ANY consistent
   letter-expansion of it is a real dictionary word. Expansion is bounded and
   cached, and the digraph runes are handled as units.
2. Re-score the two SOLVED pages (73 "An End", 74 "A Parable") from their
   KNOWN plaintext re-encoded to Gematria values. A correct scorer must hit hard
   here -- this is the ceiling.
3. Re-score with the OLD exact-match scorer for comparison.
4. Report the gap. If the old scorer's ceiling is far below the 40.9% that
   ruled-out.md treats as the bar for a real solve, then the bar was set by a
   broken instrument.
"""

import json
import re
import sys
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "skill/cicada-3301-solver/scripts"))

from gematria_toolkit import ALPHABET_SIZE, LATIN_TO_VAL, RUNE_TO_VAL  # noqa: E402

DICT = REPO / "data/words_alpha.txt"
OUT_JSON = Path(__file__).with_name("scorer_audit.json")

# Which Latin spellings each ambiguous value can legitimately represent.
# Values with a single spelling are included for completeness.
VALUE_SPELLINGS = {
    0: ["F"],
    1: ["U", "V"],
    2: ["TH"],
    3: ["O"],
    4: ["R"],
    5: ["C", "K"],
    6: ["G"],
    7: ["W"],
    8: ["H"],
    9: ["N"],
    10: ["I", "J"],
    11: ["IO", "IA"],
    12: ["EO"],
    13: ["P"],
    14: ["X"],
    15: ["S", "Z"],
    16: ["T"],
    17: ["B"],
    18: ["E"],
    19: ["M"],
    20: ["L"],
    21: ["NG", "ING"],
    22: ["OE"],
    23: ["D"],
    24: ["A"],
    25: ["AE"],
    26: ["Y"],
    27: ["EA"],
    28: ["Q"],
}

# How many expansions a single word may produce before we give up and treat it as
# a miss. Real English words expand to at most a few dozen; a runaway count means
# the word is essentially arbitrary runes, not a plausible reading.
MAX_EXPANSIONS = 4096


def load_dictionary(path=DICT, min_len=3):
    words = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            w = line.strip().upper()
            if len(w) >= min_len:
                words.add(w)
    return words


@lru_cache(maxsize=1 << 16)
def expansions(values):
    """All letter strings this run of Gematria values can spell."""
    out = [""]
    for v in values:
        spellings = VALUE_SPELLINGS.get(v, ["?"])
        nxt = []
        for prefix in out:
            for s in spellings:
                nxt.append(prefix + s)
                if len(nxt) >= MAX_EXPANSIONS:
                    break
            if len(nxt) >= MAX_EXPANSIONS:
                break
        out = nxt
    return out


def is_real_word(values, wordset):
    """True if ANY ambiguity-consistent spelling of these values is a real word."""
    if not values:
        return False
    for cand in expansions(tuple(values)):
        if cand in wordset:
            return True
    return False


def _encode_token(up):
    """Single uppercase A-Z string -> Gematria values, greedily matching digraph
    runes (TH, IO, EA, AE, OE, NG) so they are not split into single letters."""
    digraphs = sorted((k for k in LATIN_TO_VAL if len(k) > 1), key=len, reverse=True)
    values, i = [], 0
    while i < len(up):
        for dg in digraphs:
            if up.startswith(dg, i):
                values.append(LATIN_TO_VAL[dg])
                i += len(dg)
                break
        else:
            ch = up[i]
            if ch in LATIN_TO_VAL:
                values.append(LATIN_TO_VAL[ch])
            i += 1
    return values


def encode_english(text):
    """English text -> (flat values, [per-word value lists])."""
    values = _encode_token(re.sub(r"[^A-Z]", "", text.upper()))

    words, cur = [], []
    for tok in re.findall(r"[A-Za-z]+|[^A-Za-z]+", text):
        if tok.isalpha():
            cur.append(_encode_token(tok.upper()))
        else:
            if cur:
                words.append(cur)
                cur = []
    if cur:
        words.append(cur)
    return values, words


KNOWN_SOLVED = {
    73: """AN END
WITHIN THE DEEP WEB
THERE EXISTS A PAGE THAT HASHES TO
IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE""",
    74: """A PARABLE
LIKE THE INSTAR TUNNELING TO THE SURFACE
WE MUST SHED OUR OWN CIRCUMFERENCES
FIND THE DIVINITY WITHIN AND EMERGE""",
}

# A few words of real LP1 plaintext, for a second calibration point.
LP1_SAMPLE = {
    0: "BELIEVE NOTHING FROM THIS BOOK EXCEPT WHAT YOU KNOW TO BE TRUE",
    5: "THE PRIMES ARE SACRED THE TOTIENT FUNCTION IS SACRED ALL THINGS SHOULD BE ENCRYPTED",
}


def score_set(name, text, wordset):
    _, words = encode_english(text)
    words = [w for w in words if w]
    # encode_english returns a list of paragraph-groups, each a list of words.
    # Flatten to a plain list of per-word value lists.
    flat_words = [vals for group in words for vals in group if vals]
    total = len(flat_words)
    strict = sum(1 for w in flat_words
                 if "".join(VALUE_SPELLINGS[v][0] for v in w) in wordset)
    aware = sum(1 for w in flat_words if is_real_word(w, wordset))
    return {
        "page": name,
        "words": total,
        "old_exact_match_hits": strict,
        "old_exact_match_rate": strict / total if total else 0.0,
        "ambiguity_aware_hits": aware,
        "ambiguity_aware_rate": aware / total if total else 0.0,
    }


def main():
    print("=" * 74)
    print("DICTIONARY SCORER AUDIT -- validate the instrument on known plaintext")
    print("=" * 74)
    print(f"  dictionary      : {DICT.relative_to(REPO)}")
    wordset = load_dictionary()
    print(f"  words in list   : {len(wordset):,}")
    print(f"  alphabet size   : {ALPHABET_SIZE}")
    print("  NOTE: normalize_ambiguous() is documented in SKILL.md but does not")
    print("        exist in the toolkit. This file implements the missing logic.")

    results = []
    print(f"\n{'page':>6}  {'words':>5}  {'old hits':>9} {'old %':>7}  {'new hits':>9} {'new %':>7}")
    print("  " + "-" * 70)
    for page, text in sorted({**KNOWN_SOLVED, **LP1_SAMPLE}.items()):
        r = score_set(page, text, wordset)
        results.append(r)
        print(f"  {r['page']:>4}  {r['words']:>5}  {r['old_exact_match_hits']:>9} "
              f"{r['old_exact_match_rate']:>6.1%}  {r['ambiguity_aware_hits']:>9} "
              f"{r['ambiguity_aware_rate']:>6.1%}")

    solved = [r for r in results if r["page"] in (73, 74)]
    old_bar = sum(r["old_exact_match_rate"] for r in solved) / len(solved)
    new_bar = sum(r["ambiguity_aware_rate"] for r in solved) / len(solved)
    loss = old_bar - new_bar

    print(f"\n  CEILING on known-solved pages (page 73 + 74):")
    print(f"    old exact-match scorer : {old_bar:.1%}   <- the '40.9% benchmark'")
    print(f"    ambiguity-aware scorer : {new_bar:.1%}")
    print(f"    silent loss from ambiguity handling : {loss:.1%} of the ceiling")

    # Which letters are actually costing the most?
    print(f"\n  WORDS THE OLD SCORER MISSES ON KNOWN-CORRECT PLAINTEXT:")
    demo_misses = []
    for page, text in sorted(KNOWN_SOLVED.items()):
        _, groups = encode_english(text)
        for group in groups:
            for w in group:
                if not w:
                    continue
                rendered = "".join(VALUE_SPELLINGS[v][0] for v in w)
                if rendered not in wordset and is_real_word(w, wordset):
                    alts = [c for c in expansions(tuple(w)) if c in wordset]
                    demo_misses.append({"page": page, "rendered": rendered,
                                        "real_spellings": alts})
    for m in demo_misses[:25]:
        print(f"    p{m['page']}: rendered {m['rendered']!r} -> real {m['real_spellings']}")
    print(f"    ... {len(demo_misses)} such words total across the two solved pages")

    out = {
        "dictionary_size": len(wordset),
        "results": results,
        "solved_pages_ceiling": {"old_exact_match": old_bar, "ambiguity_aware": new_bar},
        "missed_words": demo_misses,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2))
    print(f"\n  wrote {OUT_JSON.relative_to(REPO)}")


if __name__ == "__main__":
    main()
