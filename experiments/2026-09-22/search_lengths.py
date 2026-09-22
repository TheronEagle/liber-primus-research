#!/usr/bin/env python3
target = [6,7,6,3,6,4,3,3]
with open('data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt', encoding='utf-8') as f:
    content = f.read()
blocks = content.split('%')
found = False
for idx, block in enumerate(blocks):
    clean = block.replace('/', '').replace('\n', '')
    words = [w for w in clean.split('-') if w]
    lengths = [len(w) for w in words]
    for i in range(len(lengths) - len(target) + 1):
        if lengths[i:i+len(target)] == target:
            print(f'Found target at block {idx} (1-indexed block number {idx+1}), starting at word {i+1}')
            words = [w for w in clean.split('-') if w]
            for j in range(max(0, i-2), min(len(words), i+len(target)+3)):
                marker = ' <--' if j == i else ''
                print(f'  [{j+1}] {words[j]}{marker}')
            found = True
if not found:
    print('Pattern not found.')