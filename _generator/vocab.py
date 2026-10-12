# -*- coding: utf-8 -*-
"""Collects the vocabulary lists SUPPLIED in the Word file for each item (word tables, contexts, practice lists, verb tables)
and attaches English glosses (educational addition, data/glosses.txt)."""
import os, re, itertools
from render import SRC, clean, norm_ar, PAIR_TABLES, CONTEXT_TABLES, GRID_TABLES, VERB_TABLES, PRACTICE_RUNS, cell_lines
from structure import ITEMS

HERE = os.path.dirname(os.path.abspath(__file__))
GL = {}
for line in open(os.path.join(HERE, 'data', 'glosses.txt'), encoding='utf8'):
    if line.startswith('#') or '|' not in line:
        continue
    w, g = [x.strip() for x in line.split('|', 1)]
    k = norm_ar(w)
    if k in GL and g not in GL[k]:
        GL[k] = GL[k] + '; also: ' + g
    elif k not in GL:
        GL[k] = g
GL_USED = set()


def gloss(w):
    k = norm_ar(w)
    if k in GL:
        GL_USED.add(k)
        return GL[k]
    return ''


def split_paren(s):
    m = re.match(r'^([^(]+)\((.+)\)\s*$', s)
    if m:
        return clean(m.group(1)), clean(m.group(2))
    m = re.match(r'^(\S+)\s+["\u201c](.+)["\u201d]\s*$', s)       # word "note"
    if m:
        return clean(m.group(1)), clean(m.group(2))
    return clean(s), ''


SYLL = re.compile(r'^(.+?)\s*\((.+)\)\s*\.?$')
SYLL_BLOCKS = list(range(961, 967)) + list(range(968, 971)) + list(range(973, 976)) + list(range(978, 982))


def in_range(item, i):
    return item['rng'][0] <= i < item['rng'][1]


def build_vocab(item):
    a, b = item['rng']
    cards, seen = [], set()

    def add(word, ctx, kind, src, partner='', srcnote=''):
        word = clean(word).strip(' .،:-')
        if not word or not re.search('[ء-ي]', word):
            return
        key = (norm_ar(word), ctx)
        if key in seen:
            return
        seen.add(key)
        cards.append(dict(w=word, ctx=ctx, kind=kind, src=src, partner=partner, srcnote=srcnote, gloss=gloss(word)))

    verbs = []
    for i in range(a, b):
        bl = SRC.get(i)
        if not bl:
            continue
        if bl['k'] == 't':
            rows = bl['rows']
            if i in PAIR_TABLES:
                h = [clean(c['text']) for c in rows[0]]
                for r in rows[1:]:
                    ws = [cell_lines(c) for c in r]
                    for k, cell in enumerate(ws):
                        for line in cell:
                            w, note = split_paren(line)
                            partner = ' / '.join(split_paren(x)[0] for kk, c2 in enumerate(ws) if kk != k for x in c2)
                            add(w, 'أزواج صغرى: %s ↔ %s' % (h[0], h[1]) if len(h) > 1 else 'أزواج', 'pair', 'b%d' % i, partner, note)
            elif i in CONTEXT_TABLES:
                for r in rows[1:]:
                    label = clean(r[1]['text']) if len(r) > 1 else ''
                    for line in cell_lines(r[0]):
                        w, note = split_paren(line)
                        add(w, 'سياق: ' + label, 'context', 'b%d' % i, '', note)
            elif i in GRID_TABLES:
                head = [clean(c['text']) for c in rows[0]]
                for r in rows[1:]:
                    for k, c in enumerate(r):
                        lab = head[k] if k < len(head) and head[k] else ''
                        for line in cell_lines(c):
                            w, note = split_paren(line)
                            add(w, 'سياق: ' + lab if lab else 'سياق', 'context', 'b%d' % i, '', note)
            elif i in VERB_TABLES:
                for r in rows[2:]:
                    pat = ' '.join(cell_lines(r[0]))
                    pat_c = ' '.join(cell_lines(r[1]))
                    f, am, pf, pa = cell_lines(r[2]), cell_lines(r[3]), cell_lines(r[4]), cell_lines(r[5])
                    extra = [clean(c['text']) for c in r[6:10]]
                    n = max(len(f), len(am), len(pf), len(pa))
                    for k in range(n):
                        verbs.append(dict(pattern=pat, pattern_c=pat_c,
                                          fusha=f[k] if k < len(f) else '', amiya=am[k] if k < len(am) else '',
                                          ipa_f=pf[k] if k < len(pf) else '', ipa_a=pa[k] if k < len(pa) else '',
                                          gloss=gloss(f[k]) if k < len(f) else '', extra=extra if k == 0 else [], src='b%d' % i))
        else:
            t = clean(bl['text'])
            if any(x <= i < y for x, y in PRACTICE_RUNS) and t and len(t.split()) <= 3:
                add(t, 'تدريب في الصف', 'practice', 'b%d' % i)
            elif i in SYLL_BLOCKS:
                m = SYLL.match(t)
                if m:
                    add(m.group(1), 'تقسيم مقطعي: ' + clean(m.group(2)), 'syll', 'b%d' % i)
    return dict(cards=cards, verbs=verbs)


ALL = {it['id']: build_vocab(it) for it in ITEMS}

if __name__ == '__main__':
    tot = 0; nog = []
    for k, v in ALL.items():
        n = len(v['cards']); g = sum(1 for c in v['cards'] if c['gloss'])
        print(k, 'cards', n, 'glossed', g, 'verbs', len(v['verbs']), 'verbs glossed', sum(1 for x in v['verbs'] if x['gloss']))
        nog += [c['w'] for c in v['cards'] if not c['gloss']] + ['V:' + x['fusha'] for x in v['verbs'] if not x['gloss'] and x['fusha']]
    print('missing glosses:', len(nog)); print(' | '.join(sorted(set(nog))))
    print('unused glosses:', [k for k in GL if k not in GL_USED][:50])
