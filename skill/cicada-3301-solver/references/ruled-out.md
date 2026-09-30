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
4. **A positive control's plaintext must be English, not the corpus under test.**
   This bit hard in the 2026-09-30 session. The first version of the extended
   Friedman test used the observed LP2 corpus as the plaintext for its positive
   control and then Vigenere-encrypted it. But the LP2 runes are already
   near-random (IC 0.0345 ≈ the 1/29 baseline), so encrypting them leaves them
   near-random: the "positive control" showed no spike, and the script correctly
   refused to interpret the result. This is a subtler failure than a missing
   control, because a broken control reads as "the estimator can't see anything"
   and invites dismissing a real signal. Polyalphabetic key-length detection only
   works if the underlying plaintext is non-random; each ciphertext column has to
   be a monoalphabetic substitution of English. **Calibrate on English
   (`download/kjv_gutenberg.txt`), never on the mystery text.**
5. **Re-derive the block→page mapping from anchors; don't inherit it.** See the
   off-by-14 below. Every "block N" in this repo's older results is off, and the
   error was invisible because internal indices are self-consistent.

---

## CORRECTION (2026-09-30): the block/page mapping was wrong by 14, and it invalidated the top-priority lead

**This supersedes the positional claims in `open-leads.md` item 0. Read it before
citing any "block N" from an older commit.**

Every prior session parsed the transcription as:

```python
blocks = [b.strip() for b in content.split('\n%')[1:] if b.strip()]
```

and then assumed `blocks[0]` is page 17. But
`data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt` is the
**whole book**, not just LP2. The correct mapping is:

| raw index | contents |
|---|---|
| 0–13 | LP1, sequential pages 00–16 |
| 14–71 | LP2, sequential pages 17–74 |
| 72 | empty trailing segment |

**`sequential_page = raw_block_index + 3`**, not `+ 17`.

Verified two independent ways in `experiments/2026-09-30/extended_friedman.py`
(`resolve_alignment()`), which refuses to report any statistic unless the mapping
checks out:

1. All 57 rows of `page-catalog.md`'s 15-letter previews each match exactly one
   block, and every block's rune count equals the catalog's recorded count.
2. The two solved pages pin the constant: `raw[70]` = "An End" (page 73),
   `raw[71]` = "A Parable" (page 74). Page = index + 3 holds for every block.

### What this breaks

`open-leads.md` item 0 records a 2026-09-24 "correction" that moved the
word-length-pattern lead from **pages 22 and 47** to "blocks 19/44" on the
grounds that the pattern doesn't occur at pages 22/47. But blocks 19 and 44 *are*
pages 22 and 47 (19+3, 44+3). The correction chased the same two pages under a
different label and concluded the original claim was false when it was right.
The separate "unique pattern" was at block 40 = page 43, not a 43/58 pair.

So: **the 8-word length pattern `[6,7,6,3,6,4,3,3]` does occur at pages 22 and
47, exactly as first reported.** The "corrected positions" and the follow-up
negative results in `open-leads.md` item 0 are not evidence about a different
pair of pages — they are a re-run of the original pair. The values there still
differ and autokey/running-key still yields gibberish, so the *conclusion* of
that lead is unaffected; but the reasoning that "the original claim was false"
was wrong and must not be cited again.

**Re-verified 2026-09-30** (`experiments/2026-09-30/lead0_rerun.py`): both
patterns land exactly where first claimed — `[6,7,6,3,6,4,3,3]` at page 22
word 47 and page 47 word 12; `[5,4,7,3,6,3,7,4]` at page 43 word 42 and page 58
word 47. The 2026-09-24 correction was wrong on both patterns. Lead 0 is now
closed 🔴 with a permutation test behind it (p=0.113), not just with a
"no dictionary hits" observation.

### Also: page 67 is absent from the transcription

`raw[64]` is an **empty segment** — sequential page 67 was never transcribed in
this source. Consequences:

- The unsolved corpus is **55 pages / 12,956 runes**, not "56 pages / 13,051
  runes" as stated in the Kasiski entry above. That Kasiski run's "13,051" is 95
  runes too high — about one short page, consistent with page 67 being counted
  but not transcribed. Its conclusion (no periodicity) is unaffected by 95 runes,
  but the number is wrong.
- Any future test claiming 56 unsolved pages is testing 55.

---

## Scorer defect (2026-09-30): the documented ambiguity handling does not exist

`gematria-primus.md` and `SKILL.md` both state that the scorer handles the
alphabet's ambiguous runes "via `normalize_ambiguous()`". **That function does not
exist.** Grepping the entire repo for `normalize_ambiguous` returns zero hits.

`dict_score()` is exact string equality, and `VAL_TO_LATIN` renders each value with
its PRIMARY spelling only. So a word is scored a **miss** if its true spelling
contains any ambiguous rune. Measured on the two known-solved pages, where the
plaintext is certain and the answer is known:

| page | words | old exact-match | ambiguity-aware |
|---|---|---|---|
| 0 (LP1) | 12 | 58.3% | 83.3% |
| 5 (LP1) | 14 | 85.7% | 85.7% |
| 73 (LP2) | 25 | 64.0% | 72.0% |
| 74 (LP2) | 21 | 81.0% | 85.7% |

The three words it silently loses on known-correct plaintext:

    p73: "EUERY"  -> EVERY    (v = U in the primary spelling)
    p73: "SEEC"   -> SEEK     (k = C in the primary spelling)
    p74: "DIUINITY" -> DIVINITY

**Direction of the bias matters.** The error is systematic, not random: the same
words fail for every candidate key, and it penalises *correct* decrypts more than
wrong ones, because a wrong decrypt rarely produces real words at all. So this
bias suppresses signal rather than manufacturing it. The consequence is still
serious: the "3-4% noise floor" quoted throughout this file is inflated, and the
margin between noise and signal is compressed. It cannot manufacture a false
positive, but it can cause a real one to be dismissed as noise.

**Benchmarks are therefore restated:**
- Ceiling for a correct decrypt, old scorer: **72.5%** (mean of pages 73/74).
- Ceiling for a correct decrypt, ambiguity-aware: **78.9%**.
- The "40.9%" figure quoted in earlier rounds of this file is not reproducible
  under either scorer on these texts; treat 72.5-78.9% as the real bar.

Implemented and measured in `experiments/2026-09-30/scorer_audit.py` (+`.json`).
The fix is not in `gematria_toolkit.py` because changing the shared scorer would
retroactively invalidate every number already logged here; the ambiguity-aware
scorer lives in the experiment files until someone decides whether to re-baseline
the whole file.

**A note on what this does *not* do:** this is not a reason to expect the
unsolved pages are secretly readable. A 6-12pp ceiling correction does not turn
10% into 70%.

## Reading the numbers honestly: multiple comparisons, not just controls

A random control is necessary but not sufficient. Two lessons from 2026-09-30:

1. **The control must be computed on the same statistic you are reporting.**
   `lead0_rerun.py` produced a "+7.54pp lift" for its best key variant — the best
   number in this repo's history. `lead0_permutation.py` then permuted the target
   page's word groups 400×, re-ran all 8 variants, and kept the best each time.
   The shuffle control for the winning variant came out at **10.53%, identical to
   its own observed rate — a lift of exactly 0.00%**, and p=0.113 against the
   max-over-8 null. The "+7.54pp" was an artifact of comparing a rate against a
   control computed with a different word ordering.
2. **A maximum over N tests is biased upward.** With 80 key lengths the expected
   best margin sits at z≈2.8 from chance alone. Always report the permutation
   null for the *max-over-N* statistic, not a fixed threshold, and always print
   the decoded text. Gibberish with scattered 5-letter dictionary words is the
   signature of noise, and no percentage rescues it.

## Extended Friedman sweep, key lengths 1–80 (2026-09-30) — RULED OUT

**Gap filled:** the Friedman test above covers L=1–20 only, concluding "no fixed
repeating key of length ≤20 is used uniformly across pages." L=21+ was never
tested. At ~230 runes/page a per-page test can't resolve L=40 (~6 samples per
column), so this pools columns across the full corpus and sweeps L=1–80.

Method: for each L, every value at absolute corpus position *i* goes to column
(*i* mod *L*); mean the per-column IC. Script
`experiments/2026-09-30/extended_friedman.py`, raw output
`experiments/2026-09-30/extended_friedman.json`. Corpus: 55 present unsolved
pages, 12,956 runes, 29-symbol alphabet. Page boundaries are deliberately
ignored — a flat curve there is the signature of one key running continuously.

| test | best L | best IC | margin over null |
|---|---|---|---|
| **Positive control** (real English + DIVINITY, true L=8) | 80 | 0.0728 | **+0.0380** |
| **Null control** (values shuffled) | 77 | 0.0348 | — |
| **Observed** (unsolved LP2) | 60 | 0.0349 | **+0.0005** |

- English plaintext IC = 0.0725; random 29-symbol baseline = 0.0345. The gap
  between those two is the only reason key-length detection works at all.
- Observed mean IC across all 80 key lengths = 0.0345, i.e. **identical to
  random**. The largest observed margin is +0.0005 at L=40 — 1/76th of the
  positive control's margin, at z=2.76, exactly the upward bias expected from
  taking a max over 80 candidates.

**Conclusion: a single repeating Vigenère key running continuously through the
book is ruled out for all key lengths 1–80**, not just 1–20. This extends the
strongest negative result in this file. The test says nothing about a *per-page*
key (each page with its own key is invisible to this method) or about
non-Vigenère families.
