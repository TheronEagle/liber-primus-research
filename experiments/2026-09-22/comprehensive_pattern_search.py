#!/usr/bin/env python3
"""
Comprehensive search for the 8-word-length pattern [6,7,6,3,6,4,3,3] across all blocks.
Generates a report of all occurrences (if any) and saves context for manual review.
"""
import sys
sys.path.insert(0, '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/skill/cicada-3301-solver/scripts')
from gematria_toolkit import *

def load_transcription_blocks(path):
    """Read the rtdk transcription file and split into blocks by '%' delimiter."""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    # Split on a line that contains only '%' (as it appears in the source)
    parts = content.split('\n%')
    # The first part is the header; the remaining parts are the blocks
    blocks = [p.strip() for p in parts[1:] if p.strip()]
    return blocks

def word_lengths_and_tokens(block):
    """Given a block string, return (list_of_lengths, list_of_tokens, list_of_raw_words).
    Length is the number of runes (after mapping via RUNE_TO_VAL)."""
    clean = block.replace('/', '').replace('\n', '')
    raw_words = [w for w in clean.split('-') if w]
    lengths = []
    tokens = []
    for w in raw_words:
        vals = [RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]
        lengths.append(len(vals))
        tokens.append(w)
    return lengths, tokens, raw_words

def find_all_occurrences(seq, target):
    """Return list of start indices where target occurs as a contiguous sub‑sequence."""
    n = len(target)
    occ = []
    for i in range(len(seq) - n + 1):
        if seq[i:i+n] == target:
            occ.append(i)
    return occ

def context_for_match(block, start_idx, length, tokens, raw_words):
    """Generate a human‑readable excerpt around a matched index."""
    # We'll show +/- 2 words around the match for context
    start = max(0, start_idx - 2)
    end = min(len(tokens), start_idx + length + 2)
    excerpt_tokens = tokens[start:end]
    excerpt_lengths = [len([RUNE_TO_VAL[ch] for ch in w if ch in RUNE_TO_VAL]) for w in excerpt_tokens]
    excerpt_raw = excerpt_tokens
    return {
        "start_idx": start_idx,
        "match_lengths": excerpt_lengths,
        "match_raw": excerpt_raw
    }

def main():
    # Path to the transcription file
    transcription_path = (
        '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/'
        'data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt'
    )
    blocks = load_transcription_blocks(transcription_path)
    print(f"Loaded {len(blocks)} blocks from transcription file.")

    # According to the page‑catalog, block 5 ≈ page 22, block 30 ≈ page 47.
    # We'll still scan all blocks for completeness.
    target_pattern = [6, 7, 6, 3, 6, 4, 3, 3]

    all_matches = []  # List of dicts with metadata about each match

    for idx, block in enumerate(blocks):
        lengths, tokens, raw_words = word_lengths_and_tokens(block)
        matches = find_all_occurrences(lengths, target_pattern)
        if matches:
            for match_start in matches:
                ctx = context_for_match(block, match_start, len(target_pattern), tokens, raw_words)
                all_matches.append({
                    "block_idx": idx,
                    "match_start_word_idx": match_start,
                    "target_pattern": target_pattern,
                    "context": ctx
                })

    # ----------------------------------------------------------------------
    # Reporting
    # ----------------------------------------------------------------------
    if not all_matches:
        print("No occurrences of the target pattern were found.")
    else:
        print(f"Found {len(all_matches)} occurrence(s).")
        for m in all_matches:
            print(f"\nBlock {m['block_idx']} (≈ page {idx_to_page(m['block_idx'])}):")
            print(f"  Match starts at word index {m['match_start_word_idx']} (1‑indexed {m['match_start_word_idx']+1})")
            ctx = m["context"]
            print(f"  Context (words {ctx['start_idx']+1}‑{ctx['start_idx']+len(ctx['match_lengths'])}):")
            for i, length in enumerate(ctx["match_lengths"]):
                raw_word = ctx["match_raw"][i]
                print(f"    [{i+ctx['start_idx']+1}]: length={length}, raw_word={raw_word}")

    # ----------------------------------------------------------------------
    # Helper: crude block‑to‑page approximation (per page‑catalog.md)
    # ----------------------------------------------------------------------
    def idx_to_page(block_idx):
        # Page numbers start at 17 for block 0, so page = 17 + block_idx,
        # but the catalogue notes an off‑by‑one uncertainty.
        return 17 + block_idx

    # ----------------------------------------------------------------------
    # Save a detailed JSON report for later manual inspection
    # ----------------------------------------------------------------------
    import json
    report_path = '/Users/corey.mitchell/hermes/templetutorial/liber-primus-research/experiments/2026-09-22/pattern_search_report.json'
    with open(report_path, 'w', encoding='utf-8') as jf:
        json.dump({
            "blocks_analyzed": len(blocks),
            "matches_found": len(all_matches),
            "matches": all_matches,
            "target_pattern": target_pattern
        }, jf, indent=2)
    print(f"\nDetailed report written to {report_path}")

if __name__ == '__main__':
    main()