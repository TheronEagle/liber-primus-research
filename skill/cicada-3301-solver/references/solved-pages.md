# Solved Pages — Full Reference

## Page numbering crosswalk (IMPORTANT — easy to get wrong)

The Liber Primus has 75 pages total, sequentially numbered `00.jpg` through `74.jpg`
in the modern community archive (this is the "primary"/authoritative numbering — use
it when talking to the user or citing a page).

It was released in two parts:
- **LP1**: pages `00`-`16` (17 pages). Released 2014, all 17 pages solved.
- **LP2**: pages `17`-`74` (58 pages). Released 2014-2016. Internally, LP2 also has
  its own numbering `0.jpg`-`57.jpg` which you'll see in older community sources
  (e.g. "page 57.jpg" in old forum posts = sequential page `74`). **When a source
  says "page 57" check whether it means the internal LP2 numbering (=sequential 74)
  or is just wrong** — this has caused confusion before (an earlier session in this
  skill's history initially misidentified the book's final page as unsolved before
  correcting itself — see the postmortem note at the bottom of this file).
- Of LP2's 58 pages, only **2 are solved**: sequential pages `73` ("An End") and
  `74` ("A Parable"). The other 56 (`17`-`72`) are unsolved as of this writing.

Verified via: pixel-identical comparison of page images against the
`krisyotam/cicada3301` GitHub archive, cross-checked against that archive's own
page-index file (`liber-primus__index.txt`) which explicitly labels each page's
title and both numbering schemes.

## LP1 (pages 00-16) — ALL SOLVED

Chapter 1 ("Intus" = "within"), consisting of: a warning, a welcome/pilgrimage
passage, "some wisdom" + a 5x5 magic square (all rows/columns/diagonals sum to
3301), a koan ("A Man Decided..."), "the loss of divinity" (three behaviors —
consumption, preservation, adherence), a second koan ("The I"), and a closing
instruction.

Ciphers used across LP1 (all cracked within weeks of release in 2014):
- Direct Gematria substitution (no additional cipher) — pages 00, 02, 05, 10-13, 16
- Reversed Gematria Primus (Atbash-style, 2014 variant) — page 01
- Vigenère cipher, key **DIVINITY** (key values 6,19,28,19,20,19,13,3), shift-up,
  with the rule that the plaintext letter F (→ rune ᚠ) must be SKIPPED during
  decoding (F can't be encrypted with this key) — pages 03-04
- Shift-3-down reversed Gematria — pages 06-09
- Vigenère cipher, key **FIRFUMFERENFE** (a deliberately-corrupted spelling of
  "CIRCUMFERENCE" — the F-substitution is itself a hint about the F-skip rule
  above), shift-up — pages 14-15

Full LP1 plaintext is long; fetch it from `data-sources.md`'s archive link
(`liber-primus/decoded/DECODED-PAGES.md` in the krisyotam archive) rather than
duplicating it all here. Key excerpt, page 01 ("A Warning") — worth keeping close
at hand since its instruction is thematically load-bearing for the whole book:

```
A WARNING
BELIEVE NOTHING FROM THIS BOOK EXCEPT WHAT YOU KNOW TO BE TRUE
TEST THE KNOWLEDGE, FIND YOUR TRUTH, EXPERIENCE YOUR DEATH
DO NOT EDIT OR CHANGE THIS BOOK OR THE MESSAGE CONTAINED WITHIN
EITHER THE WORDS OR THEIR NUMBERS, FOR ALL IS SACRED
```

## LP2 solved page 1 of 2 — Page 73, "An End"

Cipher: stream cipher using **φ(nth prime) = (nth prime − 1), mod 29**, applied as
a running additive key (shift-down direction), NOT restarting per line. This is the
"totient function is sacred" hint made concrete. Stream starts:
`1,2,4,6,10,12,16,18,22,28,1,7,11,13,...` (i.e. (2-1),(3-1),(5-1),(7-1),(11-1)...
each mod 29).

Plaintext:
```
AN END
WITHIN THE DEEP WEB
THERE EXISTS A PAGE THAT HASHES TO
36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a
8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4
IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE
```

Note: the referenced SHA-512 hash has never been found/matched to any known page or
service, as far as any archive reviewed for this skill records.

## LP2 solved page 2 of 2 — Page 74, "A Parable" (the book's final page)

This is the page shown in the artwork with a red first line and a stippled
tree/mycelium/wing illustration beneath the text — visually striking and often
mistaken (including by an earlier pass in this skill's own history) for one of
the deliberately unsolved pages, because it LOOKS as elaborate as the hard ones.
It isn't hard: it's a **direct, uncipher transliteration** — straight rune-to-letter,
no key at all.

Runes (5 lines, from the community-verified transcription):
```
ᛈᚪᚱᚪᛒᛚᛖ.ᛚᛁᚳᛖ-ᚦᛖ-ᛁᚾᛋᛏᚪᚱ-ᛏ
ᚢᚾᚾᛖᛚᛝ-ᛏᚩ-ᚦᛖ-ᛋᚢᚱᚠᚪᚳᛖ.
ᚹᛖ-ᛗᚢᛋᛏ-ᛋᚻᛖᛞ-ᚩᚢᚱ-ᚩᚹᚾ-ᚳ
ᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖᛋ.ᚠᛁᚾᛞ-ᚦ
ᛖ-ᛞᛁᚢᛁᚾᛁᛏᚣ-ᚹᛁᚦᛁᚾ-ᚪᚾᛞ-ᛖᛗᛖᚱᚷᛖ.
```

Plaintext:
```
A PARABLE.
LIKE THE INSTAR, TUNNELING TO THE SURFACE.
WE MUST SHED OUR OWN CIRCUMFERENCES.
FIND THE DIVINITY WITHIN, AND EMERGE.
```

This directly echoes "The Instar Emergence" poem quoted back in the 2013 puzzle
stage, thematically closing the loop: the book ends on the same image (shedding a
false/circumference self to "emerge") that it opened with in the LP1 welcome text.

## Postmortem note (keep for future sessions' calibration)

An earlier working session on this puzzle initially assumed the book's final page
(page 74, "A Parable") was one of the unsolved mystery pages, based on surface
pattern-matching to other famous "final page is the hardest" narratives about this
puzzle. It was corrected only after actually cloning the community archive and
checking the page-index file directly. **Lesson for future sessions: don't assume
which pages are hard/easy from vibes or which one "looks most mysterious" — always
verify against the archive's index before characterizing a page's solve status.**
