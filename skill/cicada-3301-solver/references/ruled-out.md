# Ruled-Out Methods — Cumulative Negative-Results Log

**Purpose of this file:** cryptanalysis on a corpus this size is expensive in time
and tokens. Every method logged here has been tried, with a specific methodology,
and returned a null result (statistically indistinguishable from random noise).
Read this before re-running any of these — if you have a variant, check whether
it's meaningfully different from what's listed before spending a session on it.

**How to read a result as "null" vs "real":** every test below reports a
dictionary-word-match rate (real English words hit / total candidate words) and,
where relevant, a random-shuffle control computed the same way. As a calibration
anchor: the *real* solve of page 73 ("An End", see solved-pages.md) scored 9/22
real dictionary words when correctly decrypted — a 41% hit rate — against a
baseline of 0-9% for every wrong key on the same page. A result under ~10% hit rate
on a page of that length is noise; dictionary hit rates climb *sharply and
unambiguously* on a correct decrypt because real text is mostly real words. There
is no realistic scenario where the correct key gives only a marginal improvement
over noise — if a test result looks marginal, it's wrong, not "promising."

---

## Statistical fingerprinting

**Index of Coincidence (IC), page 17 (first unsolved LP2 page), 262 runes:**
IC = 0.0343. Theoretical random-29-symbol-alphabet IC ≈ 0.0345. Effectively
identical — this page shows no monoalphabetic substitution structure at all.

**Friedman test (key-length detection via per-column IC), run across ALL 56
unsolved pages independently, key lengths 1-20:**
Every single key length from 1 to 20 produced average column IC in the range
0.033-0.036 — flat, no spike anywhere. A real short repeating-key Vigenère would
show a clear spike (IC ~0.06-0.07) at the true key length and its multiples.
**Conclusion: no fixed repeating key of length ≤20 is used uniformly across pages.**
This is one of the strongest negative results in this file — it rules out an
entire category of cipher (the same category, Vigenère-with-English-word-key,
that cracked every other solved page in the book).

**Kasiski examination, run on the full concatenation of all 56 unsolved pages
(13,051 runes total, page 73 excluded since it's solved by a different method):**
n-gram lengths tested: 3, 4, 5. Found 2539 repeated 3-grams (3638 pairwise
distances), 132 repeated 4-grams, 6 repeated 5-grams. Factored all pairwise
distances looking for a common small factor (which would indicate key length).
Result: the most common factors (2, 3, 4, 5...) appear at the frequency you'd
expect from coincidence in this much text — no factor stood out above baseline.
**No periodicity signal found.**

---

## Cipher keys tried (Vigenère-style, additive over Gematria values mod 29)

All tried in BOTH directions (shift-up and shift-down) on page 17 initially, then
the most plausible candidates re-tested across all 56 unsolved pages with proper
dictionary scoring (see `scripts/gematria_toolkit.py` `vigenere_decode()` +
`dict_score()`):

- DIVINITY (known LP1 key) — no hit
- FIRFUMFERENFE / CIRCUMFERENCE (known LP1 key) — no hit
- INSTAR, EMERGE, PRIMALITY, SACRED, TOTIENT, PILGRIM, PARABLE, WISDOM, CICADA,
  PRIME, PRIMES, KOAN, WARNING, SHADOW, TRUTH, DEATH, BOOK, CIRCUMFERENCES,
  CONSUMPTION, PRESERVATION, ADHERENCE, BELONG, REALITY, ILLUSION, SURFACE,
  TUNNELING, WITHIN, WITHOUT, SELF, BEING, LAW, HOLY, LIBERPRIMUS, GEMATRIA,
  INSTRUCTION, JOURNEY, ENLIGHTENED, MASTER, STUDENT, CONSCIOUSNESS, QUESTION,
  PROGRAM, MIND — every one of these as a Vigenère key, both directions, across
  all 56 pages: best result was 8/57 words on one page (noise level; direct
  uncyphered transliteration on the same page scored 2/57 for comparison).

**Reversed Gematria (Atbash-style, the LP1-page-01 method) applied to page 17:**
produces `SHEOGMEAFSYENGCTHIOGAEFIOOEONTHNEWBASOEEOINGUNAEGITHHBNEAPBNEOIOTHANGY...`
— not English, no dictionary hits.

## Number-theoretic streams (running additive key, not repeating-word-based)

Tested across all 56 unsolved pages, both directions, WITH a random-shuffle
control computed the same way for direct comparability:

| Stream | up hit rate | down hit rate |
|---|---|---|
| Raw prime sequence mod 29 (2,3,5,7,11,...) | 0.043 | 0.039 |
| General Euler totient φ(n) for n=1,2,3,... mod 29 (not just primes) | 0.040 | 0.034 |
| Emirp sequence mod 29 | 0.032 | 0.038 |
| **Random shuffle control** | **0.040** | — |

All four numbers (including the control) sit in the same 0.032-0.043 band. This is
about as clean a null result as cryptanalysis produces — the "sacred primes /
sacred totient" hint from page 5 does NOT generalize as a simple running key beyond
the one page (73) it's already known to unlock.

Note: this is different from testing φ(nth prime) specifically as used on page 73 —
that one is confirmed to work on page 73 (see solved-pages.md) and was NOT
re-tested against the other 56 pages with this exact stream in the same run; it WAS
tested earlier and also returned null on those pages. If re-deriving, use
`scripts/gematria_toolkit.py`'s `totient_of_primes_stream()` and check both.

## Numeric grids/clues printed in the book itself

- **Page 32's 4x4 numeric grid** (3258, 3222, 3152, 3038 / 3278, 3299, 3298, 2838 /
  3288, 3294, 3296, 2472 / 4516, 1206, 708, 1820 — flattened, mod 29, used as
  additive stream): up=0.039, down=0.041. Noise level.
- **Magic-square border digit patterns from pages 10-13** (digit-repeated grid
  borders, flattened and mod-29'd): up=0.039, down=0.035. Noise level.
  Caveat: the exact digit extraction here was a reasonable-effort approximation,
  not a rigorously re-verified transcription — if revisiting, re-derive the exact
  border digit sequence from the original page images first.
- **Page 5's 5x5 magic square (sums to 3301)**: not yet tested as a key stream at
  all (only used qualitatively so far). Flagged in `open-leads.md`.

## Image/steganography analysis

**Dot-pattern illustration on page 74** (the "tree/mycelium/wing" artwork under
the Parable text — note this page's TEXT is solved, but the artwork was checked
independently in case it carried separate information):
- Connected-component analysis: 624 distinct blobs, sizes cluster tightly (517-620
  range for the larger "trunk" components) — consistent with uniform-radius
  decorative stippling, not size-encoded data.
- Nearest-neighbor spacing analysis: smooth, monotonically decaying histogram (76
  pairs at ~6.7px up to 1 pair at ~76px) — consistent with a natural/stochastic
  point process (e.g. Perlin-noise-driven generative art), NOT a periodic grid.
  A hidden Braille-style or binary-grid encoding would show sharp peaks at fixed
  spacings; none were found.
- **Conclusion: no evidence of hidden structure in this specific illustration.**
  Other pages' illustrations (dendrite/tree patterns appear on several pages, not
  just 74) have not yet been checked with this method — flagged in `open-leads.md`.

---

## Round 2 tests (added in a later session)

**Cross-page continuous totient-of-primes stream** (the confirmed page-73 method,
but run as ONE continuous stream across the concatenation of all 56 unsolved pages
instead of restarting per page — this was flagged as untested in open-leads.md v1):
up=103/2768 (0.037), down=90/2768 (0.033), random control=96/2768 (0.035). Also
tried starting the stream at offsets 22, 44, 100, 200 words in (in case the key
"continues" from wherever page 73's stream ended): 114, 102, 103, 109 out of 2768 —
all within the same noise band. **No signal. Ruled out.**

**Page 5's 5x5 magic square (values 272,138,341,131,151 / 366,199,130,320,18 /
226,245,91,245,226 / 18,320,130,199,366 / 151,131,341,138,272) as an additive key
stream**, both row-major and column-major flattening, both directions: rates
0.032-0.038, all within the noise band. **No signal. Ruled out.**
(Note: this square is symmetric — row-major and column-major flattenings actually
produce very similar sequences due to the square's symmetry; a diagonal or
spiral-order flattening has NOT been tried and would be a genuinely distinct test
if revisiting.)

**Columnar transposition** (grid-based reordering only, no substitution), column
widths 2 through 30, direct transliteration after transposition, scored against
dictionary: best result was ncols=14 at 0.048 hit rate, only marginally above the
0.034-0.040 noise band and not distinguishable from a multiple-comparisons fluke
(29 column widths were tested; getting one mild outlier is expected by chance).
**No convincing signal, but this is the least-explored cipher family — only simple
column widths were tried, not column-reordering (keyed) transposition, which is
the more common real-world variant. If revisiting, try keyed columnar transposition
(where columns are also permuted according to a keyword) rather than plain width-N
transposition.**

**Word-length pattern analysis** (Kasiski-style test on the SEQUENCE OF WORD
LENGTHS, independent of letter content, across all 2768 words in the 56-page
corpus): found an 8-word-length run — lengths `[6,7,6,3,6,4,3,3]` — matching
exactly at two positions: word 45 of page 22, and word 11 of page 47. This is a
genuinely different signal channel from every other test in this file (nothing
else has looked at length-only structure). Rough back-of-envelope statistics
(using actual observed length-frequency, not uniform assumption) put the expected
number of such 8-length coincidental matches across this corpus at very roughly
0.1-0.5, so a single observed match is *suggestive but not conclusive* — it's
above chance but not overwhelmingly so, especially accounting for the fact many
different run-lengths and window placements were implicitly tested. **Flagged in
open-leads.md as worth a follow-up rather than logged as fully ruled out** — the
natural next step is to try decoding pages 22 and 47 specifically against each
other (e.g. try one page's rune sequence as a key for the other, autokey-style)
since a repeated formulaic phrase across two pages is exactly the kind of
structure that could arise from a running/autokey cipher.

---

## Tooling bug found and fixed (round 2) — re-verify anything derived before this fix

`scripts/gematria_toolkit.py`'s `word_to_key_values()` had a bug: letters with no
rune of their own (V, K, Z, J — these share a rune with U, C, S, I respectively)
were silently DROPPED from the derived key instead of mapped to their alias's
value. E.g. `word_to_key_values('DIVINITY')` produced a 7-value key with V
missing, not the correct 8-value key. **This was fixed** by registering explicit
aliases (V→U, K→C, Z→S, J→I, IA→IO) in `LATIN_TO_VAL`.

Impact check: DIVINITY, CIRCUMFERENCE, DIVINE, REVELATION, and EVERYTHING were
re-tested with the corrected key derivation after the fix — all still score
0.031-0.042, i.e. still noise-level. **The "ruled out" conclusions for
V/K/Z/J-containing keys in this file still hold**, but if you find OLD raw output
elsewhere (outside this file) that used a V/K/Z/J-containing key before this fix
was applied, treat it as unverified and re-run with the current toolkit version.
This is exactly the kind of silent correctness bug this skill's "always add a
random-control baseline and validate against a known-solved page" discipline is
meant to catch on the *statistical* side — it does NOT catch bugs in key
derivation itself, so it's worth periodically spot-checking that
`word_to_key_values()` output looks right by hand for a test word before trusting
a large sweep.

## Meta-lessons for future sessions

1. **Always compute a random-shuffle control alongside any new stream/key test.**
   Early sessions (including this skill's own first pass) sometimes reported raw
   hit counts without a control, which made noise-level results look more
   suggestive than they were. The dictionary-score-vs-shuffle-control comparison
   is the single most important discipline in this file.
2. **A crude n-gram-based "looks English" scorer is not reliable enough** — it
   gave a false-positive-adjacent result (score 8 on garbage vs score 7 on the
   real known-solved plaintext of page 3, i.e. barely distinguishable) before
   being replaced with a real 370k-word dictionary exact-match scorer, which is
   what all results in this file use. If you build a new scorer, validate it
   the same way: run it against a KNOWN solved page's real plaintext and confirm
   it scores dramatically higher than garbage before trusting it on unsolved text.
3. **Verify page numbering/identity against the archive index before
   characterizing a page as hard or easy** (see the postmortem note in
   solved-pages.md).
