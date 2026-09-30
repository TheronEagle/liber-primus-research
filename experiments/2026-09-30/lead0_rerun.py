#!/usr/bin/env python3
"""
Lead #0 re-run under the CORRECTED page mapping and the ambiguity-aware scorer.

WHY
---
Lead 0 was closed on 2026-09-24 by a "correction" that moved the word-length
pattern from pages 22/47 to "blocks 19/44". The 2026-09-30 session showed that
correction was an off-by-14 artifact: blocks 19/44 ARE pages 22/47. So the
original claim was right and the follow-up analysis was a re-run of the same two
pages under a different label. The negative result may still hold, but it was
reached through invalid reasoning and with a scorer that has a known systematic
bias (see scorer_audit.py: every V renders as U, so DIVINITY->DIUINITY and scores
as a miss).

This script redoes the lead from scratch on verified pages, with:
  - the page mapping re-derived from anchors, not assumed
  - an ambiguity-aware dictionary scorer as the primary metric
  - a random-shuffle control on the SAME scorer
  - the old exact-match scorer reported alongside for continuity

The question being asked: does the 8-word length pattern [6,7,6,3,6,4,3,3] occur
at pages 22 and 47, do the runes there differ, and does any cross-page key
(autokey / running / xor / difference) turn that difference into English?
"""

import json
import random
import sys
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "skill/cicada-3301-solver/scripts"))

from gematria_toolkit import ALPHABET_SIZE, RUNE_TO_VAL, VAL_TO_LATIN  # noqa: E402

TRANSCRIPTION = REPO / "data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt"
DICT = REPO / "data/words_alpha.txt"
OUT_JSON = Path(__file__).with_name("lead0_rerun.json")

PAGE_OFFSET = 3  # verified 2026-09-30 against page-catalog.md previews + solved pages
PATTERN = [6, 7, 6, 3, 6, 4, 3, 3]
PATTERN2 = [5, 4, 7, 3, 6, 3, 7, 4]

VALUE_SPELLINGS = {
    0: ["F"], 1: ["U", "V"], 2: ["TH"], 3: ["O"], 4: ["R"], 5: ["C", "K"],
    6: ["G"], 7: ["W"], 8: ["H"], 9: ["N"], 10: ["I", "J"], 11: ["IO", "IA"],
    12: ["EO"], 13: ["P"], 14: ["X"], 15: ["S", "Z"], 16: ["T"], 17: ["B"],
    18: ["E"], 19: ["M"], 20: ["L"], 21: ["NG", "ING"], 22: ["OE"], 23: ["D"],
    24: ["A"], 25: ["AE"], 26: ["Y"], 27: ["EA"], 28: ["Q"],
}
MAX_EXPANSIONS = 4096


def load_blocks():
    return TRANSCRIPTION.read_text(encoding="utf-8").split("\n%")[1:]


def block_values(b):
    return [RUNE_TO_VAL[c] for c in b if c in RUNE_TO_VAL]


def words_of(block):
    """Split a page into words of values, using the transcription's delimiters
    (- word, . clause, / line, & paragraph, $ segment)."""
    out = []
    for chunk in block.split("-"):
        vals = block_values(chunk)
        if vals:
            out.append(vals)
    return out


def word_lengths(page_words):
    return [len(w) for w in page_words]


def find_pattern(lengths, pat):
    """All start indices where pat occurs as a contiguous run."""
    n, m = len(lengths), len(pat)
    return [i for i in range(n - m + 1) if lengths[i:i + m] == pat]


def find_subsequence(lengths, pat):
    """Greedy leftmost subsequence match (gaps allowed)."""
    hits = []
    for start in range(len(lengths)):
        j = 0
        i = start
        while i < len(lengths) and j < len(pat):
            if lengths[i] == pat[j]:
                j += 1
            i += 1
        if j == len(pat):
            hits.append(start)
    return hits


@lru_cache(maxsize=1 << 16)
def expansions(values):
    out = [""]
    for v in values:
        nxt = []
        for pre in out:
            for s in VALUE_SPELLINGS.get(v, ["?"]):
                nxt.append(pre + s)
                if len(nxt) >= MAX_EXPANSIONS:
                    break
            if len(nxt) >= MAX_EXPANSIONS:
                break
        out = nxt
    return out


def is_real_word(vals, wordset):
    if not vals:
        return False
    return any(c in wordset for c in expansions(tuple(vals)))


def score(vals, word_lengths_, wordset):
    """Score a decrypted value stream, re-split by the known word lengths."""
    words, i = [], 0
    for L in word_lengths_:
        seg = vals[i:i + L]
        i += L
        if seg:
            words.append(seg)
    aware = sum(1 for w in words if is_real_word(w, wordset))
    strict = sum(1 for w in words
                 if "".join(VALUE_SPELLINGS[v][0] for v in w) in wordset)
    return {"n_words": len(words), "aware_hits": aware, "strict_hits": strict,
            "aware_rate": aware / len(words) if words else 0.0,
            "strict_rate": strict / len(words) if words else 0.0}


def load_wordset():
    ws = set()
    with open(DICT, encoding="utf-8") as f:
        for line in f:
            w = line.strip().upper()
            if len(w) >= 3:
                ws.add(w)
    return ws


def main():
    rng = random.Random(3301)
    wordset = load_wordset()
    blocks = load_blocks()

    print("=" * 76)
    print("LEAD 0 RE-RUN -- corrected page mapping + ambiguity-aware scorer")
    print("=" * 76)

    # ---- sanity: anchors ----
    p73 = 73 - PAGE_OFFSET
    p74 = 74 - PAGE_OFFSET
    a = "".join(VAL_TO_LATIN[v] for v in block_values(blocks[p73]))
    b = "".join(VAL_TO_LATIN[v] for v in block_values(blocks[p74]))
    print(f"  page 73 raw[{p73}] = {a[:24]!r}  (expect 'AEIOOESRMYLOHOAECTHG')")
    print(f"  page 74 raw[{p74}] = {b[:24]!r}  (expect 'PARABLELICETHEINSTAR')")
    assert a.startswith("AEIOOESRMYLOHOAECTHG"), "page 73 anchor broken"
    assert b.startswith("PARABLELICETHEIN"), "page 74 anchor broken"
    print("  anchors OK")

    # ---- pattern search across the whole unsolved corpus, real page numbers ----
    unsolved = [p for p in range(17, 73) if p != 67]
    print(f"\n  unsolved pages scanned: {len(unsolved)} (17-66, 68-72; page 67 absent)")

    per_page = {}
    for p in unsolved:
        per_page[p] = words_of(blocks[p - PAGE_OFFSET])

    print(f"\n  CONTIGUOUS occurrences of {PATTERN}:")
    contig = []
    for p in unsolved:
        for i in find_pattern(word_lengths(per_page[p]), PATTERN):
            contig.append((p, i))
            print(f"    page {p:2d} word {i} (1-based word {i+1})")
    if not contig:
        print("    none")

    print(f"\n  CONTIGUOUS occurrences of {PATTERN2}:")
    contig2 = []
    for p in unsolved:
        for i in find_pattern(word_lengths(per_page[p]), PATTERN2):
            contig2.append((p, i))
            print(f"    page {p:2d} word {i} (1-based word {i+1})")
    if not contig:
        print("    none")

    print(f"\n  SUBSEQUENCE (gaps allowed) occurrences of {PATTERN} -- leftmost per page:")
    sub = {}
    for p in unsolved:
        h = find_subsequence(word_lengths(per_page[p]), PATTERN)
        if h:
            sub[p] = h
            print(f"    page {p:2d}: {len(h)} hit(s), first at word {h[0]}")
    print(f"    pages with a subsequence match: {sorted(sub)}")

    report = {"pattern": PATTERN, "pattern2": PATTERN2,
              "contiguous": contig, "contiguous2": contig2,
              "subsequence_pages": sorted(sub)}

    # ---- the cross-page key tests, on the two pages the lead actually names ----
    print("\n" + "=" * 76)
    print("CROSS-PAGE KEY TESTS on pages 22 and 47")
    print("=" * 76)
    p22, p47 = 22, 47
    w22, w47 = per_page[p22], per_page[p47]
    L22, L47 = word_lengths(w22), word_lengths(w47)
    v22 = [v for w in w22 for v in w]
    v47 = [v for w in w47 for v in w]
    print(f"  page 22: {len(v22)} runes, {len(w22)} words")
    print(f"  page 47: {len(v47)} runes, {len(w47)} words")

    # The matched 8-word runs, if the contiguous search found them at 22/47.
    runs = {}
    for p, (words_, L_) in ((p22, (w22, L22)), (p47, (w47, L47))):
        idxs = find_pattern(L_, PATTERN)
        if idxs:
            i = idxs[0]
            run = [v for w in words_[i:i + len(PATTERN)] for v in w]
            runs[p] = {"word_index": i, "values": run}
            print(f"  page {p}: 8-word run at word {i+1}, {len(run)} runes")

    results = []

    def record(name, vals, lengths):
        r = score(vals, lengths, wordset)
        # random control on the SAME scorer and same word splits
        ctrl_rates = []
        for _ in range(20):
            sh = vals[:]
            rng.shuffle(sh)
            ctrl_rates.append(score(sh, lengths, wordset)["aware_rate"])
        ctrl = sum(ctrl_rates) / len(ctrl_rates)
        lift = r["aware_rate"] - ctrl
        results.append({"test": name, **r, "control_rate": ctrl, "lift": lift})
        print(f"    {name:38s} aware {r['aware_hits']:3d}/{r['n_words']:3d} "
              f"= {r['aware_rate']:6.2%}  strict {r['strict_rate']:6.2%}  "
              f"ctrl {ctrl:6.2%}  lift {lift:+.2%}")
        return r

    print("\n  raw transliteration (no key):")
    record("page 22 raw", v22, L22)
    record("page 47 raw", v47, L47)

    if 22 in runs and 47 in runs:
        k22, k47 = runs[22]["values"], runs[47]["values"]
        print(f"\n  values identical at the two runs? {k22 == k47}")
        if k22 != k47:
            diff = [(a - b) % ALPHABET_SIZE for a, b in zip(k22, k47)]
            print(f"  elementwise difference (p22 - p47 mod 29): {diff}")
            print(f"  as letters: {''.join(VAL_TO_LATIN[d] for d in diff)}")

        print("\n  using one page's matched run as a key for the other:")
        # tile each run across the whole target page
        for src, dst, dvals, dlens, tag in ((k22, p47, v47, L47, "p22run->p47"),
                                            (k47, p22, v22, L22, "p47run->p22")):
            for sign, sname in ((-1, "sub"), (1, "add")):
                dec = [(v + sign * k) % ALPHABET_SIZE
                       for v, k in zip(dvals, (src * (len(dvals) // len(src) + 1))[:len(dvals)])]
                record(f"{tag} {sname}", dec, dlens)

        print("\n  difference as an additive stream over the pages:")
        for target, tval, tlen, tag in ((p47, v47, L47, "diff->p47"),
                                        (p22, v22, L22, "diff->p22")):
            tiled = (diff * (len(tval) // len(diff) + 1))[:len(tval)]
            dec = [(v - d) % ALPHABET_SIZE for v, d in zip(tval, tiled)]
            record(f"{tag} sub", dec, tlen)
            dec = [(v + d) % ALPHABET_SIZE for v, d in zip(tval, tiled)]
            record(f"{tag} add", dec, tlen)

    # ---- what the two runs actually spell, under both scorers ----
    print("\n  what the matched 8-word runs render as:")
    for p, r in runs.items():
        toks = []
        i = 0
        wvals = [v for w in per_page[p][r["word_index"]:r["word_index"] + len(PATTERN)]
                 for v in w]
        # re-split by PATTERN lengths
        i = 0
        for L in PATTERN:
            toks.append("".join(VALUE_SPELLINGS[v][0] for v in wvals[i:i + L]))
            i += L
        print(f"    page {p}: strict spelling  {toks}")
        real = []
        i = 0
        for L in PATTERN:
            seg = tuple(wvals[i:i + L])
            i += L
            real.append([c for c in expansions(seg) if c in wordset] or None)
        print(f"    page {p}: real words      {real}")

    out = {"report": report, "cross_page_results": results,
           "runs": {str(k): {kk: vv for kk, vv in v.items()} for k, v in runs.items()}}
    OUT_JSON.write_text(json.dumps(out, indent=2))
    print(f"\n  wrote {OUT_JSON.relative_to(REPO)}")


if __name__ == "__main__":
    main()
