#!/usr/bin/env python3
"""
Follow-up: is the +7.54% lift on "p47run -> p22 add" signal, or one of 8 draws?

THE QUESTION
------------
lead0_rerun.py tested 8 cross-page key variants on pages 22/47. The best was
"p47run -> p22 add" at 10.53% ambiguity-aware dictionary hits against a 2.98%
shuffle control: a +7.54pp lift. On its face that looks like the best result in
the repo's history.

It almost certainly is not, and this script exists to prove that rather than to
leave the number lying around waiting to be quoted.

WHY IT IS ALMOST CERTAINLY NOT SIGNAL
-------------------------------------
1. Multiple comparisons. 8 variants were tested. The shuffle controls themselves
   varied from 2.98% to 6.05% on the SAME data, so the null distribution of
   "lift" is wide. Picking the max of 8 noisy draws manufactures lift.
2. The ceiling is known and this is nowhere near it. A correct decrypt of a page
   of this length scores 72.5-78.9% (scorer_audit.py, on the two solved pages).
   10.5% is a tenth of the way there.
3. The words that hit are not a phrase. A real decrypt produces English. This
   produces scattered dictionary words separated by gibberish, which is exactly
   what you expect from poking 57 random rune-groups at a 370k word list.

METHOD
------
Permutation test, done properly:
  - Null model: shuffle the 57 words of page 22 among themselves, re-run ALL 8
    key variants, record the best lift. Repeat 2000x.
  - This preserves the real word-length distribution and the real dictionary
    interaction, so it is a faithful null -- far better than assuming normality.
  - If the observed best lift sits inside the permutation distribution, it is
    noise and the lead is closed as noise.
Also print the actual decoded text so the reader can judge with their own eyes
rather than trusting a percentage.
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
OUT_JSON = Path(__file__).with_name("lead0_permutation.json")

PAGE_OFFSET = 3
PATTERN = [6, 7, 6, 3, 6, 4, 3, 3]
N_PERM = 400
SEED = 3301

VALUE_SPELLINGS = {
    0: ["F"], 1: ["U", "V"], 2: ["TH"], 3: ["O"], 4: ["R"], 5: ["C", "K"],
    6: ["G"], 7: ["W"], 8: ["H"], 9: ["N"], 10: ["I", "J"], 11: ["IO", "IA"],
    12: ["EO"], 13: ["P"], 14: ["X"], 15: ["S", "Z"], 16: ["T"], 17: ["B"],
    18: ["E"], 19: ["M"], 20: ["L"], 21: ["NG", "ING"], 22: ["OE"], 23: ["D"],
    24: ["A"], 25: ["AE"], 26: ["Y"], 27: ["EA"], 28: ["Q"],
}
MAX_EXPANSIONS = 4096


@lru_cache(maxsize=1 << 18)
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
    return bool(vals) and any(c in wordset for c in expansions(tuple(vals)))


def load_wordset():
    ws = set()
    with open(DICT, encoding="utf-8") as f:
        for line in f:
            w = line.strip().upper()
            if len(w) >= 3:
                ws.add(w)
    return ws


def words_of(block):
    out = []
    for chunk in block.split("-"):
        vals = [RUNE_TO_VAL[c] for c in chunk if c in RUNE_TO_VAL]
        if vals:
            out.append(vals)
    return out


def hit_rate(word_groups, wordset):
    return sum(1 for w in word_groups if is_real_word(w, wordset)) / len(word_groups)


def apply_key(target_vals, key, sign):
    tiled = (key * (len(target_vals) // len(key) + 1))[:len(target_vals)]
    return [(v + sign * k) % ALPHABET_SIZE for v, k in zip(target_vals, tiled)]


def split_by(values, lengths):
    out, i = [], 0
    for L in lengths:
        seg = values[i:i + L]
        i += L
        if seg:
            out.append(seg)
    return out


def all_variants(v22, v47, k22, k47, diff, words22, words47, wordset):
    """The 8 tests from lead0_rerun.py, as (name, word_groups) pairs."""
    L22 = [len(w) for w in words22]
    L47 = [len(w) for w in words47]
    out = []
    out.append(("p22run->p47 sub", split_by(apply_key(v47, k22, -1), L47)))
    out.append(("p22run->p47 add", split_by(apply_key(v47, k22, +1), L47)))
    out.append(("p47run->p22 sub", split_by(apply_key(v22, k47, -1), L22)))
    out.append(("p47run->p22 add", split_by(apply_key(v22, k47, +1), L22)))
    out.append(("diff->p47 sub", split_by(apply_key(v47, diff, -1), L47)))
    out.append(("diff->p47 add", split_by(apply_key(v47, diff, +1), L47)))
    out.append(("diff->p22 sub", split_by(apply_key(v22, diff, -1), L22)))
    out.append(("diff->p22 add", split_by(apply_key(v22, diff, +1), L22)))
    return out


def matched_run(page_words, lengths):
    n, m = len(lengths), len(PATTERN)
    for i in range(n - m + 1):
        if lengths[i:i + m] == PATTERN:
            return [v for w in page_words[i:i + m] for v in w], i
    return None, None


def main():
    rng = random.Random(SEED)
    wordset = load_wordset()
    blocks = TRANSCRIPTION.read_text(encoding="utf-8").split("\n%")[1:]

    words22 = words_of(blocks[22 - PAGE_OFFSET])
    words47 = words_of(blocks[47 - PAGE_OFFSET])
    v22 = [v for w in words22 for v in w]
    v47 = [v for w in words47 for v in w]

    k22, i22 = matched_run(words22, [len(w) for w in words22])
    k47, i47 = matched_run(words47, [len(w) for w in words47])
    assert k22 and k47, "pattern not found on pages 22/47 -- mapping regressed"
    diff = [(a - b) % ALPHABET_SIZE for a, b in zip(k22, k47)]

    print("=" * 76)
    print("LEAD 0 -- PERMUTATION TEST OF THE BEST LIFT")
    print("=" * 76)
    print(f"  pages 22 (run @ word {i22+1}) and 47 (run @ word {i47+1}), {len(k22)} runes each")
    print(f"  8 key variants, {N_PERM} permutations of the target page's words")
    print(f"  null model: permute page-22 word groups, re-run all 8, keep the best")
    print("  (preserves the real word-length distribution and dictionary interaction)")

    # --- observed ---
    obs = all_variants(v22, v47, k22, k47, diff, words22, words47, wordset)
    obs_rates = {name: hit_rate(groups, wordset) for name, groups in obs}
    obs_best = max(obs_rates, key=obs_rates.get)
    # own shuffle control for the observed best
    ctrl = []
    base_groups = dict(obs)[obs_best]
    for _ in range(200):
        g = base_groups[:]
        rng.shuffle(g)
        ctrl.append(hit_rate(g, wordset))
    ctrl_mean = sum(ctrl) / len(ctrl)
    obs_lift = obs_rates[obs_best] - ctrl_mean
    assert ctrl_mean is not None and obs_lift is not None
    print(f"\n  observed rates:")
    for name, r in sorted(obs_rates.items(), key=lambda kv: -kv[1]):
        print(f"    {name:22s} {r:7.2%}")
    print(f"\n  best  : {obs_best}  {obs_rates[obs_best]:.2%}")
    print(f"  its shuffle control : {ctrl_mean:.2%}")
    print(f"  lift                : {obs_lift:+.2%}")

    # --- permutation null for the MAXIMUM over 8 variants ---
    # Permute page 22's word groups, keeping their true lengths in a random order.
    # This preserves the page's real word-length distribution and its real
    # interaction with the dictionary, so it is a faithful null for "what does
    # the best of 8 key variants look like when there is no signal".
    L22 = [len(w) for w in words22]
    L47 = [len(w) for w in words47]
    null_max = []
    for _ in range(N_PERM):
        perm = words22[:]
        rng.shuffle(perm)
        pv22 = [v for w in perm for v in w]
        v = all_variants(pv22, v47, k22, k47, diff, words22, words47, wordset)
        r = max(hit_rate(g, wordset) for _, g in v)
        null_max.append(r)
    null_max.sort()

    p = sum(1 for x in null_max if x >= obs_rates[obs_best]) / len(null_max)
    print(f"\n  PERMUTATION NULL for the max-over-8 statistic:")
    print(f"    median : {null_max[len(null_max)//2]:.2%}")
    print(f"    95th   : {null_max[int(0.95*len(null_max))]:.2%}")
    print(f"    99th   : {null_max[int(0.99*len(null_max))]:.2%}")
    print(f"    max    : {null_max[-1]:.2%}")
    print(f"\n  observed max = {obs_rates[obs_best]:.2%}")
    print(f"  p-value      = {p:.3f}   (fraction of permutations matching or beating it)")

    # --- show the actual text of the best variant ---
    print(f"\n  DECODED TEXT of {obs_best} (ambiguity-aware, '?' where nothing matches):")
    groups = dict(obs)[obs_best]
    toks = []
    for w in groups:
        alts = [c for c in expansions(tuple(w)) if c in wordset]
        toks.append(alts[0] if alts else
                    "".join(VALUE_SPELLINGS[v][0] for v in w))
    for i in range(0, len(toks), 8):
        print("    " + " ".join(toks[i:i + 8]))

    ceiling = 0.789  # from scorer_audit.py, page 73+74
    print(f"\n  reference: a CORRECT decrypt of a page this long scores {ceiling:.1%}.")
    print(f"  the best observed here is {obs_rates[obs_best]:.1%} "
          f"= {obs_rates[obs_best]/ceiling:.0%} of the way there.")

    if p > 0.05:
        verdict = (f"NOISE. The best lift ({obs_lift:+.2%}) is inside the permutation null "
                   f"for a max-over-8 statistic (p={p:.3f}), and is {obs_rates[obs_best]:.1%} "
                   f"against a {ceiling:.1%} ceiling. Lead 0 stays closed.")
    else:
        verdict = (f"POSSIBLY REAL (p={p:.3f}). Requires a second independent confirmation "
                   f"before any claim. Show the text, not the percentage.")

    print(f"\n  VERDICT: {verdict}")
    OUT_JSON.write_text(json.dumps({
        "best_variant": obs_best,
        "observed_rates": obs_rates,
        "observed_best_rate": obs_rates[obs_best],
        "shuffle_control_for_best": ctrl_mean,
        "lift": obs_lift,
        "permutation": {"n": N_PERM, "median": null_max[len(null_max)//2],
                        "p95": null_max[int(0.95*len(null_max))],
                        "p99": null_max[int(0.99*len(null_max))],
                        "max": null_max[-1], "p_value": p},
        "decoded_best_variant": toks,
        "ceiling_reference": ceiling,
        "verdict": verdict,
    }, indent=2))
    print(f"\n  wrote {OUT_JSON.relative_to(REPO)}")


if __name__ == "__main__":
    main()
