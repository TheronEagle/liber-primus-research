# Session note — 2026-09-30

## Summary

Two results, both negative for the puzzle and positive for the repo's integrity:

1. **A real off-by-14 in the block→page mapping**, which invalidated the
   reasoning behind the repo's top-priority lead. The original 2026-09-22 claim
   was right all along.
2. **Extended the strongest existing negative result from key lengths 1–20 out
   to 1–80**, with a properly calibrated positive control.

No page was solved. 55 of 56 unsolved LP2 pages remain unsolved.

---

## 1. The off-by-14

`ruled-out.md` and `open-leads.md` both referred to "block N" throughout. Those
block numbers came from:

```python
blocks = [b.strip() for b in content.split('\n%')[1:] if b.strip()]
```

with an assumed `blocks[0] = page 17`. The transcription file in the repo
(`data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt`) is the
**whole book** — LP1 included. The real mapping is:

    sequential_page = raw_block_index + 3

Verified two independent ways in `extended_friedman.py::resolve_alignment()`,
which raises rather than reporting numbers if the mapping doesn't hold:

- All 57 of `page-catalog.md`'s 15-letter previews match exactly one block, and
  every block's rune count equals the catalog's recorded rune count.
- `raw[70]` = "An End" (page 73) and `raw[71]` = "A Parable" (page 74), adjacent
  and where the solved-pages reference says they should be. +3 holds throughout.

**Impact.** `open-leads.md` item 0 carried a 2026-09-24 "correction" that moved
the word-length-pattern lead from pages 22/47 to "blocks 19/44" and declared the
original claim false. But 19+3=22 and 44+3=47 — the correction analysed the same
two pages it claimed to have replaced. The claim it refuted was the correct one.

The negative *results* at those positions (values differ; autokey and
running-key produce gibberish) were computed on pages 22/47 and are therefore
probably still valid, so the lead's conclusion likely stands. But that hasn't
been re-run since the fix, so `open-leads.md` item 0 is re-opened 🟡 rather than
closed 🔴.

**Also found:** `raw[64]` is an empty segment — sequential page 67 was never
transcribed. The unsolved corpus is **55 pages / 12,956 runes**, not the
"56 pages / 13,051 runes" that the Kasiski entry in `ruled-out.md` reports.

## 2. Extended Friedman sweep, L=1–80

**The gap:** the recorded Friedman test stops at key length 20. L=21+ was never
tested, and at ~230 runes/page a per-page test cannot resolve L=40 (≈6 samples
per column). This pools columns across the whole corpus and sweeps 1–80.

| test | best L | best IC | margin over null |
|---|---|---|---|
| Positive control (real English + DIVINITY, true L=8) | 80 | 0.0728 | **+0.0380** |
| Null control (values shuffled) | 77 | 0.0348 | — |
| **Observed** (unsolved LP2) | 60 | 0.0349 | **+0.0005** |

Observed mean IC across all 80 key lengths = 0.0345, the random 29-symbol
baseline. The largest observed margin is 1/76th of the positive control's, at
z=2.76 — the upward bias expected from taking a max over 80 candidates.

**Verdict: a single repeating Vigenère key running continuously through the book
is ruled out for L=1–80**, not just 1–20.

This says nothing about a *per-page* key (each page carrying its own key is
invisible to a pooled-column IC test) or about non-Vigenère families.

## 3. A methodology note worth more than the result

The first version of the positive control encrypted **the observed LP2 corpus**
with DIVINITY and looked for a spike. There was none — correctly, because the LP2
runes are already near-random (IC 0.0345), so encrypting them leaves them
near-random. The script refused to interpret the result rather than reporting a
number, which is the only reason the error was caught.

That failure mode is nastier than a missing control: a broken control reads as
"this estimator can't see anything" and invites discarding a real signal. IC
key-length detection works only because each ciphertext column is a monoalphabetic
substitution of *English*; the plaintext has to be non-random for there to be
anything to detect. Rebuilt on `download/kjv_gutenberg.txt`, the control spikes
properly (+0.0380) and the result becomes interpretable. Logged as meta-lesson 4.

## 4. Side findings (not LP2 leads, not pursued)

- `iddqd/2012/01/final.jpg` (added as a submodule this session) has 61 bytes of
  data appended after the JPEG EOF marker:
  `TIBERIVS CLAVDIVS CAESAR says "lxxt>33m2mqkyv2gsq3q=w]O2ntk"`. Shifting every
  character by −4 in ASCII decodes it to `http://i.imgur.com/m9sYK.jpg`. The
  sibling file `m9sYK.jpg` is byte-identical (SHA256 verified against the live
  URL). Classic appended-payload stego, but from rtkd/iddqd's 2012 material, not
  from the Liber Primus — no bearing on the 56 unsolved pages.
- `iddqd/2012/02/mabinogion_{transcript,translation}` are a 23-character Vigenère
  pair (`kcohtgsmhirathosotnabca`) that holds for the first ~46 letters and then
  breaks, likely from line-wrap misalignment between the two files. Not resolved.

## Files

- `experiments/2026-09-30/extended_friedman.py` — alignment resolver + IC sweep
- `experiments/2026-09-30/extended_friedman.json` — raw output
- `experiments/2026-09-30/session-note.md` — this file
- Updated `skill/cicada-3301-solver/references/ruled-out.md` and `open-leads.md`

## Recommended next steps

1. Re-run the word-length pattern search on the verified mapping and record real
   page numbers (lead 0, currently 🟡).
2. Transcribe page 67 to close the 55/56 gap, then re-check the Kasiski figure.
3. A per-page-key test: pooled IC can't see it, but per-page *word-length*
   structure is a separate channel worth a look.
4. Stop using raw block indices in prose. Use page numbers, or call
   `resolve_alignment()`.
