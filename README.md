# Liber Primus Research Log

An ongoing, transparent, AI-assisted computational cryptanalysis research
project on Cicada 3301's Liber Primus — a real, unsolved rune manuscript that
has resisted the global cryptography community since 2014.

**This repo has not solved the puzzle.** As of 2026-09-22, 56 of the 58 LP2 pages
remain unsolved, exactly as they are everywhere else. What this repo IS: a
cumulative, honestly-reported log of every method tried, with exact
methodology and statistics, so effort isn't wasted repeating dead ends — plus
a working Python toolkit for anyone who wants to pick up where this leaves off.

## Current status
- [N] cipher/key/statistical tests logged in `skill/references/ruled-out.md`,
all null results.
- Top open lead: see `skill/references/open-leads.md` item 0.
- Last session: 2026-09-22 — see `UPDATES.md`.

## How this works
An AI agent runs periodic research sessions following the process in
[this prompt / AGENT.md — link it here]. Every session reads the accumulated
state first, tries ONE new thing, and reports honestly regardless of outcome.

## Contributing
Human cryptographers, mathematicians, and linguists are welcome to open issues
with hypotheses, corrections, or their own findings. Please check
`skill/references/ruled-out.md` first.

## A note on credibility
This project takes seriously that Cicada 3301 research has a long history of
false claims. Every positive result reported here will be flagged as
"candidate, unverified" until independently reproduced by someone outside this
repo. Treat any "SOLVED" claim from this repo with appropriate skepticism until
that's happened.