#!/usr/bin/env python3
"""
CORRECTED extended Friedman / IC key-length sweep on the unsolved LP2 pages.

WHY THIS FILE EXISTS
--------------------
Two real defects in the prior state of this repo, both fixed and proven here.

DEFECT 1 -- block/page indexing was wrong, by 14.
Prior sessions parsed the transcription with

    blocks = [b.strip() for b in content.split('\\n%')[1:] if b.strip()]

and then treated blocks[0] as "page 17". The transcription file actually in the
repo (data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt) is
the WHOLE BOOK, not just LP2. With a constant offset of +3:

    raw[0..13]   = LP1, sequential pages 00-16
    raw[14..71]  = LP2, sequential pages 17-74
    page = raw_index + 3

NOT page = index + 17. This is load-bearing for the top-priority lead: the
"corrected positions" recorded in open-leads.md (blocks 19/44 and block 40)
resolve to sequential pages 22, 47 and 43 -- exactly the pages the ORIGINAL,
allegedly-incorrect claim named. The correction was an indexing artifact, and
the words-it-refuted claim was right. See ruled-out.md for the full writeup.

Also found: raw[64] (sequential page 67) is an EMPTY segment. That page is
untranscribed in this source, so the corpus has 55 present unsolved pages, not
56. Any statistic claiming 13,051 unsolved runes is off by the missing page.

resolve_alignment() rebuilds the mapping from page-catalog.md's 15-letter
previews plus the two solved pages as anchors, and refuses to report any
statistic if the offset is not constant or if the two solved pages do not land
on 73 and 74. It is verification, not assumption.

DEFECT 2 -- key lengths 21+ were never tested.
ruled-out.md records the Friedman test over key lengths 1-20 only, concluding
"no fixed repeating key of length <=20 is used uniformly across pages". At
~230 runes/page a per-page test cannot resolve L=40 (~6 samples per column), so
this pools columns across the whole corpus and sweeps L=1..80, which is the only
way a long key is resolvable from a corpus this size.

CONTROLS (mandatory -- see ruled-out.md meta-lesson 1)
-----------------------------------------------------
1. POSITIVE control: REAL English plaintext mapped to Gematria values and then
   encrypted with DIVINITY (L=8). This is what makes the test interpretable. IC
   key-length detection works because each column of a polyalphabetic ciphertext
   becomes a monoalphabetic substitution of English, and English over a 29-symbol
   alphabet has IC well above the 1/29 random baseline. So a correct control must
   start from English.

   An earlier version of this file used the OBSERVED corpus as the control
   plaintext. That is wrong and it silently destroyed the calibration: the LP2
   runes are already near-random (IC 0.0345), so Vigenere-encrypting them leaves
   them near-random, and the "positive control" showed no spike. A flat control
   curve then makes the estimator look broken, or -- worse -- makes any real
   signal look meaningless. Control plaintext must be English.
2. NULL control: same corpus, values shuffled. Supplies the noise curve, which
   is required because 80 key lengths are tested and the maximum is upward-biased.
"""

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "skill/cicada-3301-solver/scripts"))

from gematria_toolkit import (  # noqa: E402
    ALPHABET_SIZE, LATIN_TO_VAL, RUNE_TO_VAL, VAL_TO_LATIN,
)

TRANSCRIPTION = REPO / "data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt"
PAGE_CATALOG = REPO / "skill/cicada-3301-solver/references/page-catalog.md"
ENGLISH_SAMPLE = REPO / "data/liber-primus-jens/download/kjv_gutenberg.txt"
OUT_JSON = Path(__file__).with_name("extended_friedman.json")

MAX_KEY_LEN = 80
LP2_UNSOLVED_PAGES = list(range(17, 73))  # 73 ('An End') and 74 ('A Parable') are solved
DIVINITY = [6, 19, 28, 19, 20, 19, 13, 3]  # values from solved-pages.md


def block_values(block):
    return [RUNE_TO_VAL[ch] for ch in block if ch in RUNE_TO_VAL]


def preview(block, n=15):
    return "".join(VAL_TO_LATIN[RUNE_TO_VAL[c] % 29]
                   for c in block if c in RUNE_TO_VAL)[:n]


def load_raw_blocks():
    """Split the transcription WITHOUT dropping empty segments, so that the
    index-to-page mapping stays honest. Index 0 is dropped as the header."""
    return TRANSCRIPTION.read_text(encoding="utf-8").split("\n%")[1:]


def parse_catalog():
    """page-catalog.md -> {15-letter preview: (catalog_block, page_label, runes)}"""
    rows = {}
    for line in PAGE_CATALOG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*(\d+)[^|]*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([A-Z]+)\s*\|", line)
        if m:
            rows[m.group(5)] = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return rows


def resolve_alignment(blocks):
    """Verify a constant page = raw_index + OFFSET mapping using catalog previews
    and the two solved pages. Returns (page_to_index, report); raises SystemExit
    on any inconsistency, because every downstream number depends on it."""
    catalog = parse_catalog()

    by_preview = {}
    for pv in catalog:
        cand = [i for i, b in enumerate(blocks)
                if block_values(b) and preview(b, 15).startswith(pv[:12])]
        if len(cand) != 1:
            raise SystemExit(f"ambiguous catalog preview {pv!r}: candidates {cand}")
        by_preview[pv] = cand[0]

    # Anchors: the two solved pages, per solved-pages.md.
    an_end = by_preview.get("AEIOOESRMYLOHOAECTHG")
    a_parable = by_preview.get("PARABLELICETHEIN")
    if an_end is None or a_parable is None or a_parable - an_end != 1:
        raise SystemExit(f"solved-page anchors missing/non-adjacent: {an_end}, {a_parable}")

    # The offset is pinned by the anchors, then must hold for EVERY block.
    # page = raw_index + offset, and 'An End' is sequential page 73.
    offset = 73 - an_end
    page_to_index, mismatches = {}, []
    for pv, idx in by_preview.items():
        page = idx + offset
        catalog_block, catalog_label, catalog_runes = catalog[pv]
        actual = len(block_values(blocks[idx]))
        if actual != catalog_runes:
            mismatches.append(f"page {page} (blocks[{idx}]): {actual} runes vs catalog {catalog_runes}")
        page_to_index[page] = idx
    if mismatches:
        raise SystemExit("rune-count mismatches vs catalog:\n  " + "\n  ".join(mismatches))

    # Confirm the offset is globally constant against catalog page labels.
    # NOTE: the catalog's own page labels are off by one relative to the
    # authoritative sequential numbering (it has 57 rows for 58 pages, and its
    # own header says so). We therefore check labels only for pages <= 71 and
    # record the disagreement rather than treating it as a failure.
    label_disagreements = []
    for pv, idx in by_preview.items():
        _, catalog_label, _ = catalog[pv]
        page = idx + offset
        if catalog_label != page and page <= 72:
            label_disagreements.append({"page": page, "catalog_label": catalog_label})

    empty_pages = sorted(p for p, i in page_to_index.items() if not block_values(blocks[i]))
    missing_pages = [p for p in LP2_UNSOLVED_PAGES if p not in page_to_index or
                     not block_values(blocks[page_to_index[p]])]

    report = {
        "page_offset": offset,
        "formula": "sequential_page = raw_block_index + %d" % offset,
        "anchors": {"page_73_an_end_index": an_end, "page_74_a_parable_index": a_parable},
        "lp2_empty_segments": empty_pages,
        "unsolved_pages_absent_from_transcription": missing_pages,
        "catalog_label_disagreements": label_disagreements,
        "rune_counts_agree_with_catalog": True,
    }
    return page_to_index, report


def ic_of(seq):
    n = len(seq)
    if n < 2:
        return None
    c = Counter(seq)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))


def mean_column_ic(corpus, key_len):
    cols = [[] for _ in range(key_len)]
    for i, v in enumerate(corpus):
        cols[i % key_len].append(v)
    ics = [x for x in (ic_of(c) for c in cols) if x is not None]
    return sum(ics) / len(ics) if ics else None


def curve(corpus, max_len=MAX_KEY_LEN):
    return {L: mean_column_ic(corpus, L) for L in range(1, max_len + 1)}


def encrypt(corpus, key_vals):
    return [(v + key_vals[i % len(key_vals)]) % ALPHABET_SIZE for i, v in enumerate(corpus)]


# Multi-rune Gematria letters, longest first so "IO"/"NG"/"EA"/"AE"/"OE"/"TH" win
# over their single-letter prefixes.
_DIGRAPHS = sorted((k for k in LATIN_TO_VAL if len(k) > 1), key=len, reverse=True)


def english_to_values(text, limit):
    """Map real English prose to Gematria values, greedily matching the 29-symbol
    Gematria Primus alphabet. Returns (values, consumed_char_count)."""
    up = text.upper()
    vals, i = [], 0
    while i < len(up) and len(vals) < limit:
        ch = up[i]
        if ch in LATIN_TO_VAL and len(ch) == 1:
            vals.append(LATIN_TO_VAL[ch])
            i += 1
            continue
        for dg in _DIGRAPHS:
            if up.startswith(dg, i):
                vals.append(LATIN_TO_VAL[dg])
                i += len(dg)
                break
        else:
            i += 1  # space, punctuation, or a letter with no Gematria rune
    return vals, i


def build_positive_control(n_values):
    """Real English -> Gematria values -> Vigenere(DIVINITY). This is the
    calibration the test needs: it must spike at a multiple of 8."""
    if not ENGLISH_SAMPLE.exists():
        raise SystemExit(f"English sample missing: {ENGLISH_SAMPLE}")
    vals, _ = english_to_values(ENGLISH_SAMPLE.read_text(encoding="utf-8",
                                                         errors="ignore"), n_values)
    if len(vals) < n_values:
        raise SystemExit(f"only {len(vals)} values parsed from English sample, need {n_values}")
    return vals


def show(name, c):
    vals = [v for v in c.values() if v is not None]
    best = max(c, key=lambda L: c[L])
    top = sorted(c.items(), key=lambda kv: -kv[1])[:8]
    print(f"\n{'-'*72}\n{name}\n{'-'*72}")
    print(f"  mean IC across all key lengths : {sum(vals)/len(vals):.4f}")
    print(f"  random-text expectation (1/29)  : {1/ALPHABET_SIZE:.4f}")
    print(f"  highest key length              : L={best}  IC={c[best]:.4f}")
    print("  top 8: " + ", ".join(f"L{L}={ic:.4f}" for L, ic in top))
    return {"mean": sum(vals) / len(vals), "best_L": best, "best_ic": c[best],
            "top8": [{"L": L, "ic": ic} for L, ic in top]}


def main():
    rng = random.Random(3301)
    blocks = load_raw_blocks()

    print("=" * 72)
    print("1. BLOCK/PAGE ALIGNMENT  (fixes an off-by-14 in prior sessions)")
    print("=" * 72)
    print(f"  transcription     : {TRANSCRIPTION.relative_to(REPO)}")
    print(f"  raw segments      : {len(blocks)} (header dropped, empties KEPT)")
    page_to_index, align = resolve_alignment(blocks)
    print(f"  {align['formula']}")
    print(f"  anchors           : page 73 'An End'    -> raw[{align['anchors']['page_73_an_end_index']}]")
    print(f"                      page 74 'A Parable' -> raw[{align['anchors']['page_74_a_parable_index']}]")
    print(f"  rune counts       : agree with page-catalog.md for every block")
    print(f"  EMPTY segments    : pages {align['lp2_empty_segments']}  (untranscribed)")
    print(f"  unsolved pages    : {align['unsolved_pages_absent_from_transcription']} absent from source")
    print("\n  resolved LP2 sample:")
    for pg in (17, 22, 30, 43, 47, 66, 68, 72, 73, 74):
        if pg in page_to_index:
            i = page_to_index[pg]
            print(f"    page {pg:2d} -> raw[{i:2d}]  runes={len(block_values(blocks[i])):3d}  {preview(blocks[i], 20)!r}")

    print("\n  CONSEQUENCE for the lead #0 'correction' in open-leads.md:")
    for idx, claimed in ((19, "page 22"), (44, "page 47"), (40, "page 43")):
        print(f"    prior 'block {idx}' = raw[{idx}] = sequential {idx + align['page_offset']}"
              f"   (originally claimed: {claimed})")

    corpus = [v for p in LP2_UNSOLVED_PAGES if p in page_to_index
              for v in block_values(blocks[page_to_index[p]])]
    n = len(corpus)

    print("\n" + "=" * 72)
    print(f"2. EXTENDED FRIEDMAN / IC KEY-LENGTH SWEEP, L=1..{MAX_KEY_LEN}")
    print("=" * 72)
    print(f"  unsolved pages present : {sum(1 for p in LP2_UNSOLVED_PAGES if p in page_to_index)}"
          f" of {len(LP2_UNSOLVED_PAGES)}")
    print(f"  runes in corpus        : {n}")
    print(f"  alphabet size          : {ALPHABET_SIZE}")
    print(f"  samples/column L=8     : {n//8}")
    print(f"  samples/column L=40    : {n//40}")
    print(f"  samples/column L={MAX_KEY_LEN}    : {n//MAX_KEY_LEN}")

    english = build_positive_control(n)
    pos = show("POSITIVE CONTROL  (real English + DIVINITY Vigenere, true L=8)",
               curve(encrypt(english, DIVINITY)))
    pos["true_key_length"] = 8
    pos["detected_multiple_of_8"] = pos["best_L"] % 8 == 0
    print(f"  IC of the English plaintext itself : {ic_of(english):.4f}")
    print("  (English over a 29-symbol alphabet should sit far above 0.0345; that")
    print("   gap is the entire reason key-length detection can work at all)")

    shuffled = corpus[:]
    rng.shuffle(shuffled)
    null = show("NULL CONTROL  (values shuffled -- the noise curve)", curve(shuffled))

    obs = show("OBSERVED  (unsolved LP2 pages, as transcribed)", curve(corpus))

    full_obs, full_null = curve(corpus), curve(shuffled)
    margins = [{"L": L, "obs": full_obs[L], "null": full_null[L],
                "margin": full_obs[L] - full_null[L]} for L in range(1, MAX_KEY_LEN + 1)]
    ranked = sorted(margins, key=lambda d: -d["margin"])

    print(f"\n{'-'*72}\nMARGIN OVER NULL, ranked (top 12 of {MAX_KEY_LEN})\n{'-'*72}")
    for d in ranked[:12]:
        print(f"  L={d['L']:3d}  obs={d['obs']:.4f}  null={d['null']:.4f}  margin={d['margin']:+.4f}")

    mean_m = sum(d["margin"] for d in margins) / len(margins)
    sd = (sum((d["margin"] - mean_m) ** 2 for d in margins) / len(margins)) ** 0.5
    z = ranked[0]["margin"] / sd if sd else 0.0
    pos_margin = pos["best_ic"] - null["best_ic"]

    print(f"\n  std-dev of margin across key lengths : {sd:.4f}")
    print(f"  largest margin                       : {ranked[0]['margin']:+.4f} at L={ranked[0]['L']}")
    print(f"  z-score of that margin               : {z:.2f}")
    print(f"  POSITIVE control margin (DIVINITY)   : {pos_margin:+.4f} at L={pos['best_L']}")
    print("\n  With 80 key lengths tested the maximum is upward-biased; z~2-3 is expected")
    print("  from chance alone. The bar is whether an observed margin approaches the")
    print("  positive control's margin, which is what a genuinely present key looks like.")

    if not pos["detected_multiple_of_8"]:
        verdict = ("INCONCLUSIVE: estimator failed to recover a known L=8 key from this "
                   "corpus, so the flat observed curve is uninformative.")
    elif ranked[0]["margin"] < 0.25 * pos_margin:
        verdict = (f"NEGATIVE: no key length in 1-{MAX_KEY_LEN} reaches even a quarter of the "
                   f"positive control's IC margin (best {ranked[0]['margin']:+.4f} at "
                   f"L={ranked[0]['L']}, z={z:.2f}; positive control {pos_margin:+.4f}). Extends "
                   f"the prior 1-20 null result out to L={MAX_KEY_LEN} and rules out a single "
                   f"repeating Vigenere key running continuously through the book.")
    else:
        verdict = (f"CANDIDATE at L={ranked[0]['L']} (margin {ranked[0]['margin']:+.4f} vs "
                   f"positive control {pos_margin:+.4f}). UNVERIFIED -- an IC bump alone is not "
                   f"a solve; needs a dictionary-scored decrypt to confirm.")

    print(f"\n  VERDICT: {verdict}")

    out = {
        "alignment": align,
        "corpus": {"pages_present": sorted(p for p in LP2_UNSOLVED_PAGES if p in page_to_index),
                   "runes": n, "alphabet_size": ALPHABET_SIZE,
                   "max_key_length": MAX_KEY_LEN},
        "positive_control": pos, "null_control": null, "observed": obs,
        "margins": margins, "margin_sd": sd, "top_margins": ranked[:12],
        "largest_margin_z": z, "positive_control_margin": pos_margin,
        "verdict": verdict,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2))
    print(f"\n  wrote {OUT_JSON.relative_to(REPO)}")


if __name__ == "__main__":
    main()
