---
name: cicada-3301-solver
description: "Cumulative research toolkit and knowledge base for Cicada 3301's Liber Primus, the unsolved rune manuscript. Use this skill whenever the user asks about Cicada 3301, the Liber Primus, Gematria Primus, or wants to analyze, decode, transcribe, or cryptanalyze runic pages from the puzzle. ALSO use it before trying any cipher, key, or statistical test on Liber Primus text — check references/ruled-out.md first so you don't repeat work already proven not to work. Trigger this proactively any time runic (Futhorc/ᚠᚢᚦ-style) text or Cicada 3301 imagery appears, even if the user doesn't name the puzzle explicitly. This skill is meant to accumulate — every session that does new analysis should add its findings back into references/ before finishing."
---

# Cicada 3301 / Liber Primus Research Toolkit

This skill exists because solving the Liber Primus (if it's solvable at all) is not a
one-session task. It has resisted a decade of sustained effort by the global
cryptography community. The point of this skill is to make each new attempt
**additive** rather than repetitive — every session should read what's already been
ruled in/out before doing new work, and should append its own findings before ending.

**Be honest with the user throughout.** Don't present noise-level statistical results
as breakthroughs. See `references/ruled-out.md` for calibration on what a real signal
looks like vs. noise (it includes worked examples of both).

## Before doing anything else

1. Read `references/ruled-out.md` in full. It's a growing log of every cipher, key,
   and statistical test that has been tried and failed, with the exact methodology,
   so you don't waste a session re-deriving a negative result.
2. Read `references/solved-pages.md` to know what's already cracked (so you don't
   accidentally treat solved pages as open problems) and to see worked examples of
   what a *real* solve looks like — useful for calibrating "is this signal real?"
3. Check `references/open-leads.md` for promising untried directions before inventing
   a new approach from scratch — someone (a past session, or the wider community) may
   have already scoped it out. **As of this writing, item 0 in that file (a specific
   8-word-length match between pages 22/47 and a second one between 43/58) is the
   highest-priority concrete lead — it's an actual coordinate, not just a technique
   to try, and the next 2-3 concrete steps are spelled out there.**

## Core reference files

- `references/gematria-primus.md` — the full 29-rune cipher table (rune, Unicode
  codepoint, prime value, Latin letter mapping). Needed for every transcription task.
- `references/solved-pages.md` — full plaintext + cipher method for every page that
  IS solved (pages 0-16 = LP1, all solved; pages 73 and 74 = LP2's only 2 solved
  pages). Includes the page-numbering crosswalk between the sequential scheme
  (00.jpg-74.jpg) and the internal LP2 scheme (0.jpg-57.jpg) — these are easy to
  confuse and previous sessions have gotten this wrong.
- `references/ruled-out.md` — every cipher/key/statistical test tried on the 56
  unsolved pages, with results. All results as of this writing are null (statistically
  indistinguishable from random). Read this BEFORE re-running Vigenère brute force,
  Kasiski, Friedman, or trying "primes as a key" — it's been done.
- `references/open-leads.md` — untried or partially-explored directions, ranked by
  plausibility. Update this as leads get tried and ruled out or confirmed.
- `references/data-sources.md` — where to get page images, transcriptions, and the
  wider community's live research (which changes over time and isn't in any static
  file).
- `references/page-catalog.md` — per-page metadata (rune count, word count, a
  15-letter direct-transliteration preview) for all 57 transcribed blocks, with a
  caveat about block/page-number alignment. Useful for quickly finding a specific
  page's basic stats without re-parsing the raw transcription file.

## Toolkit scripts

`scripts/gematria_toolkit.py` is a working, tested Python module with:
- Rune ↔ Latin letter ↔ Gematria value conversion (handles the ambiguous mappings:
  C/K, S/Z, IO/IA, TH, NG, OE, EA properly)
- Index of Coincidence (IC) calculator, with the correct baseline for a 29-symbol
  alphabet (~0.0345 for random text — NOT the ~0.067 English baseline people
  sometimes wrongly assume)
- Friedman test (key-length detection via per-column IC)
- Kasiski examination (repeated n-gram distance/factor analysis)
- Vigenère encode/decode over the 29-symbol Gematria alphabet, both directions
- A dictionary-based scorer for evaluating candidate decryptions against real English
  words (critical: use this, not a vague "does it look English" judgment call —
  see ruled-out.md for why naive n-gram scoring gives false positives)
- A random-shuffle control generator — ALWAYS compute this baseline before claiming
  a result is signal, not noise

Run `python3 scripts/gematria_toolkit.py --help` for usage, or import it directly.
It needs the page transcriptions and an English word list — see
`references/data-sources.md` for where to fetch both (they're too large to bundle).

## Workflow for a new session

1. Read `references/ruled-out.md` and `references/open-leads.md`.
2. Pick an untried lead, or propose a new one and check it's not a rephrasing of
   something already ruled out.
3. Use `scripts/gematria_toolkit.py` rather than rewriting cipher/statistics code.
4. ALWAYS compute a random-control baseline alongside any new test — a result is
   only worth reporting if it clears the baseline by a wide margin (see
   `references/ruled-out.md` for what a real hit looks like: the totient-stream
   decode of page 73 scored 9/22 real dictionary words against a baseline of 0-5/22
   for everything else — that's the bar).
5. Before ending the session, **append your results to `references/ruled-out.md`**
   (if negative) or write up the solve properly in `references/solved-pages.md` (if
   you get a real, verified hit) or `references/open-leads.md` (if you found a
   partially-promising but inconclusive direction).
6. Tell the user honestly whether anything new was found. Most sessions will
   correctly find nothing — that's expected and still valuable if logged, because it
   narrows the search space for the next attempt.

## Honesty guardrails

- Never claim a decode is correct without a dictionary-word-match score well above
  the random-shuffle baseline for that same page/method.
- Never fabricate a "translation" to satisfy a user's hope for progress. If nothing
  is found, say so plainly — see the example closing statements in
  `references/ruled-out.md` for tone/calibration.
- The book is real, actively studied by a large community, and genuinely
  unsolved as of this skill's last update. Treat claims of a full solve (from
  the user, from web sources, or from your own analysis) with high skepticism
  and verify against `references/solved-pages.md` and independent dictionary
  scoring before believing them.
