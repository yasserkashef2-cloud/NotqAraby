#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Source-fidelity check: every non-empty line of the Word file must appear (after stripping tags, unescaping, collapsing whitespace)
in the text of the built pages, except blocks deliberately withheld. Also checks that all media files and docx images are used."""
import os, sys, re, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from render import SRC, clean, blocks_text_lines
from structure import WITHHELD
from media_map import MEDIA

pages = json.load(open(os.path.join(HERE, 'data', 'pages_dump.json'), encoding='utf8'))
priv = os.path.join(HERE, 'data', 'private_texts')


def text_of(h):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<br\s*/?>', ' ', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    return clean(html.unescape(h))


def key(s):
    return re.sub(r'\s+', '', s)        # ignore whitespace differences between spans


ALL = key(' '.join(text_of(h) for h in pages.values()))
missing, checked, withheld = [], 0, []
for i, b in SRC.items():
    for line in blocks_text_lines(i):
        if i in WITHHELD:
            wh = WITHHELD[i]
            if not os.path.exists(os.path.join(priv, wh['key'] + '.txt')):
                withheld.append((i, line[:40]))
                continue
        checked += 1
        if line.startswith('http'):
            tok = line.split('v=')[-1] if 'v=' in line else line.replace('http://', '').replace('https://', '')
            if key(tok) not in ALL:
                missing.append((i, line[:80]))
            continue
        # verse separators (*** / ... / wide gaps) are layout, not text: check every hemistich
        parts = [p for p in re.split(r'\s*(?:\*{3,4}|\.{2,}|…+)\s*|\s{3,}', line) if p.strip()]
        for p in parts or []:
            if key(clean(p)) not in ALL:
                missing.append((i, p[:80]))
res = dict(lines_checked=checked, missing=missing, withheld_lines=len(withheld))
# media
used = set(re.findall(r'data-media="([^"]+)"', ' '.join(pages.values())))
unused_media = [m['id'] for m in MEDIA if m['id'] not in used]
files = set(os.listdir(os.path.join(ROOT, 'assets', 'media')))
declared = {m['id'] for m in MEDIA}
orphan_files = [f for f in files if f.rsplit('.', 1)[0] not in declared]
imgs = set(os.listdir(os.path.join(ROOT, 'assets', 'img')))
shown = set(re.findall(r'assets/img/(docx-[^"]+)"', ' '.join(pages.values())))
unused_imgs = sorted(imgs - shown)
res.update(media_unused=unused_media, media_orphans=orphan_files, images_unused=unused_imgs)
print(json.dumps(res, ensure_ascii=False, indent=1))
sys.exit(1 if (missing or unused_media) else 0)
