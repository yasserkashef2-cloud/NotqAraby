#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the interactive book:  python3 -I build.py   (run from anywhere)
reads  data/source.json, structure.py, media_map.py, vocab.py, edu_*.py, data_flags.py
writes ../index.html  ../assets/js/data.js  ../assets/img/*  (css/js/fonts/media are prepared by their own scripts)"""
import os, sys, re, json, html, shutil, zipfile, hashlib, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import render as R
from render import SRC, esc, clean, norm_ar, render_item_source, render_table, flagify, FLAG_USED, DIAC
from structure import *
from media_map import MEDIA
from data_flags import FLAGS
from vocab import ALL as VOC, GL_USED
import edu_items as EI, edu_units as EU, edu_gloss as EG

PAGES = {}          # route -> dict(t, te, h, k)
ORDER = []          # reading order of routes
BLOCK_ROUTE = {}    # source block -> route it is displayed on
QTEXT = {}          # localStorage key -> question text (for the downloadable answers file)
SEARCH = []         # [label, route, haystack]
REPORT_INFO = {'gloss_found': {}, 'gloss_missing': {}, 'jump_checks': 0}
ITEM = {it['id']: it for it in ITEMS}

AI_LABEL = 'educational'


# ---------------------------------------------------------------------------------------------------------------------
# small components
def bi(ar, en, cls='', tag='p'):
    return '<%s class="bi %s"><span class="ar" lang="ar">%s</span><span class="en" lang="en" dir="ltr">%s</span></%s>' % (tag, cls, ar, esc(en) if '<' not in en else en, tag)


def b_src():
    return '<span class="badge src-b">من مواد المقرر · From the course materials</span>'


def b_edu():
    return '<span class="badge edu-b">إضافة تعليمية · Educational addition</span>'


def route_href(r):
    return '#/' + r if r else '#/'


def link(route, text, cls=''):
    return '<a class="%s" href="%s">%s</a>' % (cls, route_href(route), text)


def _split_small(m):
    inner = m.group(1)
    mm = re.search(r' · (?=[A-Z"(])', inner)
    if not mm or not re.search('[\u0600-\u06FF]', inner[:mm.start()]):
        return m.group(0)
    return '<p class="small bi"><span class="ar" lang="ar">%s</span><span class="en" lang="en" dir="ltr">%s</span></p>' % (inner[:mm.start()], inner[mm.end():])


def register(route, title, title_en, html_, kind='page'):
    html_ = re.sub(r'<p class="small">(.*?)</p>', _split_small, html_, flags=re.S)
    PAGES[route] = dict(t=title, te=title_en, h=html_, k=kind)
    ORDER.append(route)


def render_range(a, b, route, item_id='front'):
    for i in range(a, b):
        BLOCK_ROUTE[i] = route
    return render_item_source(dict(id=item_id, rng=(a, b)))


def bullets_of(a, b, skip=('الدرس', 'أهداف', 'بيان', 'قصيدة')):
    res = []
    for i in range(a, b):
        bl = SRC.get(i)
        if not bl or bl['k'] != 'p':
            continue
        t = clean(bl['text'])
        if not t or t.startswith(skip):
            continue
        res.append((i, t.lstrip('- ').strip()))
    return res


def unit_objectives():
    t = SRC[18]
    out = {}
    for r in t['rows']:
        for c in r:
            lines = [clean(x) for x in c['text'].split('\n') if clean(x)]
            if any('المفخمات' in l for l in lines):
                out['1'] = [l.lstrip('- ').strip() for l in lines]
            elif any('نصوص طويلة' in l for l in lines):
                out['2'] = [l.lstrip('- ').strip() for l in lines]
    return out


UOBJ = unit_objectives()
assert len(UOBJ['1']) == 5 and len(UOBJ['2']) == 2, UOBJ


# ---------------------------------------------------------------------------------------------------------------------
# glossary highlighter (build time, first occurrence per entry, diacritic-insensitive)
NORM_MAP = {'إ': 'ا', 'أ': 'ا', 'آ': 'ا', 'ٱ': 'ا', 'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'}
ARL = re.compile('[ء-ي]')


PREFIX = re.compile('^(و|ف)?(ب|ل|ك)?(ال)?$')


def apply_glossary(htm, entries):
    found, missing = [], []

    def norm_seg(seg):
        n, idx = [], []
        for pos, ch in enumerate(seg):
            if DIAC.match(ch):
                continue
            n.append(NORM_MAP.get(ch, ch)); idx.append(pos)
        return ''.join(n), idx

    for word, gloss, note in entries:
        key = norm_ar(word)
        parts = re.split(r'(<[^>]+>)', htm)
        hit = False
        in_gl = False
        for k, seg in enumerate(parts):
            if seg.startswith('<'):
                if seg.startswith('<span class="gl"'):
                    in_gl = True
                elif seg == '</span>' and in_gl:
                    in_gl = False
                continue
            if in_gl or not seg.strip():
                continue
            n, idx = norm_seg(seg)
            start = 0
            while True:
                p = n.find(key, start)
                if p < 0:
                    break
                e = p + len(key)
                ws = p
                while ws > 0 and ARL.match(n[ws - 1]):
                    ws -= 1
                before_ok = ws == p or (not key.startswith('ال') and PREFIX.match(n[ws:p]) and n[ws:p]) or (key.startswith('ال') and False)
                if ws != p and n[ws:p] and PREFIX.match(n[ws:p]):
                    before_ok = True
                after_ok = e >= len(n) or not ARL.match(n[e])
                if before_ok and after_ok:
                    a = idx[p]
                    z = idx[e - 1] + 1
                    while z < len(seg) and DIAC.match(seg[z]):
                        z += 1
                    tip = gloss + ((' (' + note + ')') if note else '')
                    parts[k] = seg[:a] + '<span class="gl" tabindex="0" data-gl="%s">%s</span>' % (esc(tip), seg[a:z]) + seg[z:]
                    hit = True
                    break
                start = p + 1
            if hit:
                break
        if hit:
            htm = ''.join(parts)
        (found if hit else missing).append(word)
    return htm, found, missing


# ---------------------------------------------------------------------------------------------------------------------
# go-targets for questions
def resolve_go(go, item_html, iid):
    """returns (element id to scroll to, media id for seek or None, yt id or None)"""
    if not go:
        return None, None, None
    kind, _, rest = go.partition(':')
    if kind == 'm':
        el = 'm-' + rest
        assert 'id="%s"' % el in item_html, ('missing media element', go, iid)
        return el, rest, None
    if kind == 'b':
        el = 'b' + rest
        assert 'id="%s"' % el in item_html, ('missing block element', go, iid)
        return el, None, None
    if kind == 'p':
        blk, n = rest.split(':')
        el = 'b%s-p%s' % (blk, n)
        assert 'id="%s"' % el in item_html, ('missing paragraph', go, iid)
        return el, None, None
    if kind == 'yt':
        vid = YOUTUBE[int(rest)]
        el = 'yt-' + vid
        assert 'id="%s"' % el in item_html, ('missing yt', go, iid)
        return el, None, vid
    raise SystemExit('bad go ' + go)


def hms(ts):
    p = ts.split(':')
    return int(p[0]) * 60 + int(p[1])


def question_list(iid, qs, item_html, prefix='q'):
    out = ['<ol class="questions">']
    for n, q in enumerate(qs, 1):
        key = 'sa.ans.%s.%d' % (iid, n)
        QTEXT[key] = '%s | %s' % (q['ar'], q['en'])
        el, mid, vid = resolve_go(q['go'], item_html, iid)
        REPORT_INFO['jump_checks'] += 1 if el else 0
        tl_ar, tl_en = EI.QTYPES[q['t']]
        btn = ''
        if el:
            lab = 'الانتقال إلى المصدر · jump to the source'
            if q['ts'] and mid:
                btn = '<button type="button" class="chip jump" data-go="%s" data-media="%s" data-seek="%d">⏱ %s — %s</button>' % (el, mid, hms(q['ts']), q['ts'], lab)
            else:
                btn = '<button type="button" class="chip jump" data-go="%s">↪ %s</button>' % (el, lab)
        out.append('<li class="q"><div class="qhead"><span class="qtype" data-t="%s">%s · %s</span>%s</div>'
                   '<p class="qar" lang="ar">%s</p><p class="qen" lang="en" dir="ltr">%s</p>'
                   '<label class="sr-only" for="a-%s-%d">الإجابة · answer</label>'
                   '<textarea id="a-%s-%d" class="ans" data-key="%s" rows="3" placeholder="اكتبوا إجابتكم هنا… · write your answer here…"></textarea></li>'
                   % (q['t'], tl_ar, tl_en, btn, esc(q['ar']), esc(q['en']), iid.replace('.', '-'), n, iid.replace('.', '-'), n, key))
    out.append('</ol>')
    return ''.join(out)


def prompt_list(iid, items, kind):
    out = ['<ul class="prompts">']
    for n, p in enumerate(items, 1):
        key = 'sa.%s.%s.%d' % (kind, iid, n)
        QTEXT[key] = '%s | %s' % (p['ar'], p['en'])
        out.append('<li><p class="qar" lang="ar">%s</p><p class="qen" lang="en" dir="ltr">%s</p>'
                   '<label class="sr-only" for="p-%s-%s-%d">الإجابة · answer</label>'
                   '<textarea id="p-%s-%s-%d" class="ans" data-key="%s" rows="2" placeholder="…"></textarea></li>' % (
                       esc(p['ar']), esc(p['en']), kind, iid.replace('.', '-'), n, kind, iid.replace('.', '-'), n, key))
    out.append('</ul>')
    return ''.join(out)


# ---------------------------------------------------------------------------------------------------------------------
def vocab_section(it):
    v = VOC[it['id']]
    cards, verbs = v['cards'], v['verbs']
    parts = []
    sayings = []
    if it['id'] == '4.2':
        for b, (lab_ar, lab_en, gl) in EG.SAYINGS.items():
            sayings.append((b, clean(SRC[b]['text']).lstrip('- ').strip(), lab_ar, lab_en, gl))
    if not (cards or verbs or sayings):
        return ''
    parts.append('<section class="vocab" aria-labelledby="v-%s"><h2 id="v-%s">المفردات قبل الفقرة · Vocabulary before the item</h2>' % (it['id'].replace('.', '-'), it['id'].replace('.', '-')))
    parts.append('<p class="small">%s الكلمات من جداول الملف المصدري، والمعاني الإنجليزية إضافة تعليمية (قد يكون للكلمة غير المشكولة أكثر من قراءة). اضغطوا على البطاقة لقلبها، وعلّموا النجمة للكلمات التي تعلّمتموها. · Words come from the course tables; English glosses are an educational addition (undiacritised words can have other readings). Click a card to flip it; star the ones you have learned.</p>' % (b_src() + b_edu(),))
    if cards:
        grp = {}
        for n, c in enumerate(cards):
            grp.setdefault(c['ctx'], []).append((n, c))
        parts.append('<div class="vgroups">')
        for ctx, lst in grp.items():
            parts.append('<details class="vgroup"%s><summary><span lang="ar">%s</span> <span class="count">%d</span></summary><div class="cards">' % (' open' if len(grp) <= 3 or len(lst) <= 12 else '', esc(ctx), len(lst)))
            for n, c in lst:
                back = []
                if c['gloss']:
                    back.append('<span class="gl-en" lang="en" dir="ltr">%s</span>' % esc(c['gloss']))
                else:
                    back.append('<span class="gl-en none" lang="en" dir="ltr">(no gloss added)</span>')
                if c['partner']:
                    back.append('<span class="pair" lang="ar">↔ %s</span>' % esc(c['partner']))
                if c['srcnote']:
                    back.append('<span class="srcnote" lang="ar">%s</span>' % esc(c['srcnote']))
                parts.append('<div class="fc" data-star="%s"><button type="button" class="fc-flip" aria-pressed="false" aria-label="قلب البطاقة · flip card">'
                             '<span class="fc-front" lang="ar">%s</span><span class="fc-back">%s</span></button>'
                             '<button type="button" class="fc-star" aria-pressed="false" aria-label="تعلّمتها · mark as learned" title="تعلّمتها · learned">☆</button></div>'
                             % ('sa.star.%s.%d' % (it['id'], n), esc(c['w']), ''.join(back)))
            parts.append('</div></details>')
        parts.append('</div>')
    if verbs:
        parts.append('<details class="vgroup verbs-q"><summary>الأفعال في جدول هذه الفقرة · Verbs of this item <span class="count">%d</span></summary><div class="tablewrap"><table class="src qverbs"><thead><tr>'
                     '<th>الوزن</th><th>الفصحى</th><th>العامية / الدارجة</th><th>IPA</th><th>English</th></tr></thead><tbody>' % len(verbs))
        for x in verbs:
            ipa = ' → '.join(z for z in (x['ipa_f'], x['ipa_a']) if z)
            parts.append('<tr><td lang="ar">%s</td><td lang="ar">%s</td><td lang="ar">%s</td><td dir="ltr" class="lat">%s</td><td dir="ltr">%s</td></tr>' % (
                esc(x['pattern']), esc(x['fusha']), esc(x['amiya']), esc(ipa), esc(x['gloss'])))
        parts.append('</tbody></table></div><p class="small">الجدول مأخوذ من جداول الملف المصدري؛ عمود English إضافة تعليمية. · Table taken from the course tables; the English column is an educational addition.</p></details>')
    if sayings:
        parts.append('<div class="sayings"><h3>عبارات من التمرين · Expressions from the exercise</h3><div class="cards">')
        for b, txt, lab_ar, lab_en, gl in sayings:
            parts.append('<div class="fc"><button type="button" class="fc-flip" aria-pressed="false"><span class="fc-front" lang="ar">%s</span><span class="fc-back"><span class="srcnote" lang="ar">%s</span><span class="gl-en" lang="en" dir="ltr">%s — %s</span></span></button></div>'
                         % (esc(txt), esc(lab_ar), esc(lab_en), esc(gl)))
        parts.append('</div></div>')
    parts.append('</section>')
    return ''.join(parts)


def gloss_section(iid):
    ent = EG.GLOSSARY.get(iid)
    if not ent:
        return ''
    out = ['<section class="glossary-sec"><h2>معجم النص · Glossary of the text %s</h2>' % b_edu(),
           '<p class="small">الكلمات المظلّلة في النص لها شرح عند الضغط عليها. التغطية آلية: أول ورود لكل كلمة. · Underlined words in the text show a gloss on click or focus. Coverage is automatic: the first occurrence of each entry.</p><dl class="gloss">']
    for w, g, note in ent:
        out.append('<div><dt lang="ar">%s</dt><dd lang="en" dir="ltr">%s%s</dd></div>' % (esc(w), esc(g), (' <em>(%s)</em>' % esc(note)) if note else ''))
    out.append('</dl></section>')
    return ''.join(out)


def lesson_objective_chips(lid):
    L = LESSONS[lid]
    bl = bullets_of(*L['obj'])
    for i, _ in bl:
        BLOCK_ROUTE.setdefault(i, 'lesson/' + lid)
    return bl


def item_page(it):
    iid = it['id']
    e = EI.item_edu(iid)
    L = LESSONS[it['lesson']]
    cls = 'type-listen' if it['type'] == 'listen' else 'type-read'
    src_html = render_item_source(it)
    for i in range(*it['rng']):
        BLOCK_ROUTE[i] = 'item/' + iid
    ent = EG.GLOSSARY.get(iid)
    if ent:
        src_html, found, missing = apply_glossary(src_html, ent)
        REPORT_INFO['gloss_found'][iid] = len(found)
        REPORT_INFO['gloss_missing'][iid] = missing
    o = []
    o.append('<article class="page item %s" data-item="%s" data-target="%s">' % (cls, iid, esc(it['target'])))
    o.append('<nav class="crumbs" aria-label="breadcrumb">%s › %s › <span>%s</span></nav>' % (
        link('', 'الغلاف · Cover'), link('lesson/' + L['id'], esc(L['ar'])), esc(iid)))
    o.append('<header class="item-head"><p class="kicker">%s · %s</p><h1 class="item-title %s" lang="ar">%s</h1><p class="item-en" lang="en" dir="ltr">%s</p></header>' % (
        'استماع · Listening' if it['type'] == 'listen' else 'قراءة وإلقاء · Reading &amp; recitation', iid, cls, esc(it['ar']), esc(it['en'])))
    o.append('<div class="intro-box">%s%s</div>' % (b_edu(), bi(esc(e['intro'][0]), e['intro'][1])))
    o.append(vocab_section(it))
    o.append(gloss_section(iid))
    o.append('<section class="pre"><h2>قبل أن تبدؤوا · Before you start %s</h2><ul>%s</ul></section>' % (
        b_edu(), ''.join('<li>%s</li>' % bi(esc(p['ar']), p['en'], tag='span') for p in e['pre'])))
    tools = ('<div class="toolbar-i" role="group" aria-label="tools">'
             '<button type="button" class="chip tgl-hl" aria-pressed="false" data-letters="%s">تظليل الصوت المستهدف · highlight target sound (<span lang="ar" dir="rtl">%s</span>)</button>%s</div>' % (
                 esc(it['target']), esc(it['target']),
                 '<button type="button" class="chip tgl-gl" aria-pressed="true">شرح الكلمات · word glosses</button>' if ent else ''))
    o.append('<section class="source hl-scope"><h2>النص والتمارين · The course material %s</h2>%s<div class="src-body" dir="rtl">%s</div></section>' % (b_src(), tools, src_html))
    o.append('<section class="questions-sec"><h2>أسئلة للمناقشة · Questions %s</h2>'
             '<p class="small">ستة أسئلة مفتوحة من أنواع مختلفة. تُحفظ إجاباتكم في هذا المتصفح فقط. · Six open questions of different types. Answers are saved in this browser only.</p>%s</section>' % (
                 b_edu(), question_list(iid, e['qs'], src_html)))
    o.append('<section class="culture"><h2>مقارنة ثقافية · Cultural comparison %s</h2>%s</section>' % (b_edu(), prompt_list(iid, e['cult'], 'cult')))
    o.append('<section class="done-sec"><label class="done"><input type="checkbox" class="done-cb" data-key="sa.done.%s"> أنهيتُ هذه الفقرة · I have finished this item</label></section>' % iid)
    o.append('</article>')
    html_ = ''.join(o)
    register('item/' + iid, it['ar'], it['en'], html_, 'item')
    SEARCH.append([it['ar'] + ' — ' + it['en'], 'item/' + iid, norm_ar(it['ar'] + ' ' + it['en'] + ' ' + it['target'])])
    return html_


# ---------------------------------------------------------------------------------------------------------------------
def objective_list(unit_id):
    return ''.join('<li lang="ar">%s</li>' % esc(t) for t in UOBJ[unit_id])


def lesson_page(lid):
    L = LESSONS[lid]
    U = next(u for u in UNITS if u['id'] == L['unit'])
    first = L['items'][0]
    o = ['<article class="page lesson">']
    o.append('<nav class="crumbs">%s › %s › <span>%s</span></nav>' % (link('', 'الغلاف'), link('unit/' + U['id'], esc(U['ar'])), esc(L['ar'])))
    o.append('<h1 lang="ar" class="ttl">%s</h1><p class="item-en" lang="en" dir="ltr">%s</p>' % (esc(L['ar']), esc(L['en'])))
    # source blocks of the lesson front matter (objectives + title pages), shown verbatim
    front = LESSON_FRONT[lid]
    o.append('<section class="objectives"><h2>أهداف الدرس · Lesson objectives %s</h2>%s</section>' % (b_src(), ''.join(render_range(a, b, 'lesson/' + lid) for a, b in front)))
    o.append('<section class="items-list"><h2>فقرات الدرس · Items in this lesson</h2><ul class="toc-items">')
    for iid in L['items']:
        it = ITEM[iid]
        o.append('<li class="%s"><a href="%s"><span class="num">%s</span> <span lang="ar">%s</span><span class="en" lang="en" dir="ltr">%s</span></a><span class="mark" data-done="%s" aria-hidden="true"></span></li>' % (
            'type-listen' if it['type'] == 'listen' else 'type-read', route_href('item/' + iid), iid, esc(it['ar']), esc(it['en']), iid))
    o.append('</ul></section></article>')
    register('lesson/' + lid, L['ar'], L['en'], ''.join(o), 'lesson')
    SEARCH.append([L['ar'], 'lesson/' + lid, norm_ar(L['ar'] + ' ' + L['en'])])


LESSON_FRONT = {
    'L1': [(30, 40), (80, 85)],
    'L2': [(40, 50), (419, 423)], 'L3': [(50, 60), (594, 597)], 'L4': [(60, 70), (702, 705)], 'L5': [(70, 80), (831, 835)],
    'L6': [(1028, 1036)], 'L7': [(1036, 1044)], 'L8': [(1044, 1052)],
}


def unit_page(u):
    uid = u['id']
    o = ['<article class="page unit">']
    o.append('<nav class="crumbs">%s › <span>%s</span></nav>' % (link('', 'الغلاف'), esc(u['ar'])))
    o.append('<h1 lang="ar" class="ttl">%s</h1><p class="sub-ar" lang="ar">%s</p><p class="item-en" lang="en" dir="ltr">%s — %s</p>' % (esc(u['ar']), esc(u['sub_ar']), esc(u['en']), esc(u['sub_en'])))
    if uid == '1':
        front = render_range(29, 30, 'unit/1')
    else:
        front = render_range(1026, 1028, 'unit/2') + render_range(1052, 1077, 'unit/2')
    o.append('<div class="src-body" dir="rtl">%s</div>' % front)
    o.append('<section><h2>أهداف الوحدة · Unit objectives %s</h2><ul class="uobj">%s</ul><p class="small">النص نفسه في صفحة <a href="#/intro">مقدمة المقرر</a> · The same text is in the course introduction.</p></section>' % (b_src(), objective_list(uid)))
    o.append('<section><h2>دروس الوحدة · Lessons</h2><ul class="toc-items">')
    for lid in u['lessons']:
        L = LESSONS[lid]
        o.append('<li><a href="%s"><span lang="ar">%s</span><span class="en" lang="en" dir="ltr">%s</span></a></li>' % (route_href('lesson/' + lid), esc(L['ar']), esc(L['en'])))
    o.append('</ul></section>')
    o.append('<section class="actions"><h2>أدوات الوحدة · Unit tools %s</h2><p>%s %s %s</p></section>' % (
        b_edu(), link('unit/%s/map' % uid, 'خريطة الكفاءة · Proficiency map', 'btn'), link('unit/%s/task' % uid, 'المهمة الختامية · Final task', 'btn'),
        link('expressions', 'عبارات للمناقشة · Expressions', 'btn')))
    o.append('</article>')
    register('unit/' + uid, u['ar'], u['en'], ''.join(o), 'unit')
    SEARCH.append([u['ar'] + ': ' + u['sub_ar'], 'unit/' + uid, norm_ar(u['ar'] + ' ' + u['sub_ar'] + ' ' + u['sub_en'])])


def map_page(u):
    uid = u['id']
    rows = EU.MAPS[uid]['rows']
    o = ['<article class="page map"><nav class="crumbs">%s › %s › <span>خريطة الكفاءة</span></nav>' % (link('', 'الغلاف'), link('unit/' + uid, esc(u['ar'])))]
    o.append('<h1 class="ttl" lang="ar">خريطة الكفاءة — %s</h1><p class="item-en" lang="en" dir="ltr">Proficiency map — %s</p>' % (esc(u['ar']), esc(u['en'])))
    o.append('<div class="note-box">%s%s</div>' % (b_edu(), bi(EU.MAP_NOTE[0], EU.MAP_NOTE[1])))
    o.append('<div class="map-sum" aria-live="polite" data-unit="%s"></div>' % uid)
    o.append('<div class="maprows">')
    for k, r in enumerate(rows):
        s = r['src']
        if s[0] == 'u':
            q = UOBJ[s[1]][s[2]]; rt = 'intro'
        else:
            q = clean(SRC[s[1]]['text']).lstrip('- ').strip(); rt = BLOCK_ROUTE.get(s[1], 'intro')
        key_r = 'sa.refl.%s.%d' % (uid, k)
        QTEXT[key_r] = '%s | %s' % (r['ref_ar'], r['ref_en'])
        o.append('<section class="maprow"><h2 class="skill" data-skill="%s">%s</h2>' % (esc(r['skill']), esc(r['skill'])))
        o.append('<blockquote class="objq" lang="ar">%s<footer>%s — <a href="%s">%s</a></footer></blockquote>' % (esc(q), 'هدف من المقرر · course objective', route_href(rt), 'المصدر · source'))
        o.append('<p class="cando">%s %s</p>' % (b_edu(), bi(esc(r['can_ar']), r['can_en'], tag='span')))
        o.append('<fieldset class="self"><legend><span lang="ar">أين أنتم الآن؟</span> <span class="en" lang="en" dir="ltr">Where are you now?</span></legend>')
        for v, a, e in EU.SELF_LEVELS:
            o.append('<label><input type="radio" name="self-%s-%d" value="%s" data-key="sa.self.%s.%d"> <span lang="ar">%s</span> <span class="en" dir="ltr">%s</span></label>' % (uid, k, v, uid, k, a, e))
        o.append('</fieldset>')
        o.append('<p class="qar" lang="ar">%s</p><p class="qen" lang="en" dir="ltr">%s</p><label class="sr-only" for="r-%s-%d">تأمل · reflection</label><textarea id="r-%s-%d" class="ans" data-key="%s" rows="2"></textarea></section>' % (
            esc(r['ref_ar']), esc(r['ref_en']), uid, k, uid, k, key_r))
    o.append('</div></article>')
    register('unit/%s/map' % uid, 'خريطة الكفاءة — ' + u['ar'], 'Proficiency map — ' + u['en'], ''.join(o), 'map')


def task_page(u):
    uid = u['id']
    F = EU.FINAL[uid]
    o = ['<article class="page task"><nav class="crumbs">%s › %s › <span>المهمة الختامية</span></nav>' % (link('', 'الغلاف'), link('unit/' + uid, esc(u['ar'])))]
    o.append('<h1 class="ttl" lang="ar">%s</h1><p class="item-en" lang="en" dir="ltr">%s</p>' % (esc(F['title_ar']), esc(F['title_en'])))
    o.append('<div class="intro-box">%s%s</div>' % (b_edu(), bi(esc(F['brief_ar']), F['brief_en'])))
    o.append('<h2>الخطوات · Steps</h2><ol class="steps">%s</ol>' % ''.join('<li>%s</li>' % bi(esc(a), e, tag='span') for a, e in F['steps']))
    o.append('<h2>قائمة التحقق · Checklist</h2><ul class="check">')
    for k, (a, e) in enumerate(F['check']):
        o.append('<li><label><input type="checkbox" class="chk" data-key="sa.chk.%s.%d"> <span lang="ar">%s</span> <span class="en" dir="ltr">%s</span></label></li>' % (uid, k, esc(a), esc(e)))
        QTEXT['sa.chk.%s.%d' % (uid, k)] = '%s | %s' % (a, e)
    o.append('</ul><h2>ملاحظاتي · My notes</h2>')
    key = 'sa.note.%s' % uid
    QTEXT[key] = F['title_ar'] + ' — ملاحظات'
    o.append('<label class="sr-only" for="n-%s">ملاحظات</label><textarea id="n-%s" class="ans" data-key="%s" rows="4"></textarea></article>' % (uid, uid, key))
    register('unit/%s/task' % uid, F['title_ar'], F['title_en'], ''.join(o), 'task')


# ---------------------------------------------------------------------------------------------------------------------
def intro_page():
    o = ['<article class="page intro"><nav class="crumbs">%s › <span>مقدمة المقرر</span></nav>' % link('', 'الغلاف')]
    o.append('<h1 class="ttl" lang="ar">مقدمة المقرر</h1><p class="item-en" lang="en" dir="ltr">Course introduction</p>')
    o.append('<section class="howto"><h2>كيف تستعملون هذا الكتاب · How to use this book %s</h2><ul>' % b_edu())
    for ar, en in [
        ('الشارات تبيّن مصدر كل جزء: «من مواد المقرر» نص الملف الأصلي كما ورد، و«إضافة تعليمية» ما أُضيف لهذه النسخة.', 'Badges show where each part comes from: "From the course materials" is the original file text as supplied; "Educational addition" was written for this edition.'),
        ('العلامة ⚑ بجانب كلمة تعني أن الملف الأصلي فيه خطأ محتمل؛ النص يبقى كما ورد، والتصحيح المقترح يظهر عند الضغط عليها.', 'A ⚑ beside a word marks a probable error in the original file; the text stays as supplied and the proposed fix appears when you click it.'),
        ('تُحفظ إجاباتكم وتقدّمكم في هذا المتصفح فقط، ويمكنكم تنزيلها من القائمة.', 'Your answers and progress are saved in this browser only; you can download them from the menu.'),
        ('مفتاح لوحة المفاتيح: Esc يغلق القوائم، وزر القائمة يفتح الفهرس.', 'Keyboard: Esc closes panels; the menu button opens the table of contents.')]:
        o.append('<li>%s</li>' % bi(ar, en, tag='span'))
    o.append('</ul></section>')
    o.append('<section class="src-sec"><h2>من ملف المقرر · From the course file %s</h2><div class="src-body" dir="rtl">%s</div></section>' % (b_src(), render_range(1, 29, 'intro')))
    o.append('</article>')
    register('intro', 'مقدمة المقرر', 'Course introduction', ''.join(o), 'page')
    SEARCH.append(['مقدمة المقرر · الأهداف العامة · مجموعات الطلاب', 'intro', norm_ar('مقدمة المقرر الأهداف العامة المجموعة أ ب ج')])


def contents_page():
    o = ['<article class="page contents"><h1 class="ttl" lang="ar">الفهرس</h1><p class="item-en" lang="en" dir="ltr">Contents</p>']
    o.append('<ul class="toc-top"><li>%s</li></ul>' % link('intro', 'مقدمة المقرر · Course introduction'))
    for u in UNITS:
        o.append('<section><h2><a href="%s">%s — %s</a></h2>' % (route_href('unit/' + u['id']), esc(u['ar']), esc(u['sub_ar'])))
        for lid in u['lessons']:
            L = LESSONS[lid]
            o.append('<h3><a href="%s">%s</a></h3><ul class="toc-items">' % (route_href('lesson/' + lid), esc(L['ar'])))
            for iid in L['items']:
                it = ITEM[iid]
                o.append('<li class="%s"><a href="%s"><span class="num">%s</span> <span lang="ar">%s</span><span class="en" lang="en" dir="ltr">%s</span></a><span class="mark" data-done="%s" aria-hidden="true"></span></li>' % (
                    'type-listen' if it['type'] == 'listen' else 'type-read', route_href('item/' + iid), iid, esc(it['ar']), esc(it['en']), iid))
            o.append('</ul>')
        o.append('<p>%s %s</p></section>' % (link('unit/%s/map' % u['id'], 'خريطة الكفاءة · Proficiency map', 'btn'), link('unit/%s/task' % u['id'], 'المهمة الختامية · Final task', 'btn')))
    o.append('<section><h2>صفحات مساعدة · Reference pages</h2><ul class="toc-items">')
    for r, a, e in [('phonetics', 'مرجع النطق', 'Articulation reference'), ('expressions', 'عبارات للمناقشة', 'Expressions for discussion'),
                    ('appendix/framework', 'ملحق: الإطار المرجعي', 'Appendix: proficiency framework'), ('appendix/vocab', 'ملحق: فهرس المفردات', 'Appendix: vocabulary index'),
                    ('appendix/glossary', 'ملحق: المعجم', 'Appendix: glossary'), ('appendix/report', 'ملحق: تقرير المصادر', 'Appendix: sources report'),
                    ('appendix/tech', 'ملحق: ملاحظات تقنية', 'Appendix: technical notes')]:
        o.append('<li><a href="%s"><span lang="ar">%s</span><span class="en" lang="en" dir="ltr">%s</span></a></li>' % (route_href(r), a, e))
    o.append('</ul></section></article>')
    register('contents', 'الفهرس', 'Contents', ''.join(o), 'page')


def cover_page():
    m = META
    o = ['<article class="page cover">']
    o.append('<div class="cover-art" aria-hidden="true"><svg viewBox="0 0 400 120" width="100%" focusable="false" role="presentation"><g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">'
            + ''.join('<path d="M%d %d v%d" />' % (10 + k * 10, 60 - h // 2, h) for k, h in enumerate([8, 18, 34, 20, 52, 30, 70, 44, 90, 60, 100, 70, 84, 54, 96, 66, 76, 50, 62, 40, 56, 30, 40, 22, 30, 14, 22, 10, 16, 8, 12, 6, 10, 6, 8, 4, 6, 4, 6, 4]))
            + '</g></svg></div>')
    o.append('<h1 class="cover-title" lang="ar">%s</h1><p class="cover-sub" lang="ar">%s</p>' % (esc(m['title_ar']), esc(m['subtitle_ar'])))
    o.append('<p class="cover-en" lang="en" dir="ltr"><strong>%s</strong><br>%s</p>' % (esc(m['title_en']), esc(m['subtitle_en'])))
    o.append('<p class="cover-by" lang="ar">%s</p><p class="cover-by-en" lang="en" dir="ltr">%s</p>' % (esc(m['curator_line_ar']), esc(m['curator_line_en'])))
    o.append('<p class="cover-term">%s · %s</p>' % (esc(m['term_line']), esc(m['term_line_en'])))
    o.append('<p class="cover-actions"><a class="btn big" href="#/intro" id="start-btn">ابدؤوا · Start</a> <a class="btn" href="#/contents">الفهرس · Contents</a> <a class="btn" id="resume-btn" href="#/contents" hidden>متابعة · Continue where you left off</a></p>')
    o.append('</article>')
    register('', 'الغلاف', 'Cover', ''.join(o), 'cover')


def expressions_page():
    o = ['<article class="page expr"><nav class="crumbs">%s › <span>عبارات</span></nav><h1 class="ttl" lang="ar">عبارات للمناقشة</h1><p class="item-en" lang="en" dir="ltr">Expressions for discussion — the book\'s equivalent of a connectors page</p>' % link('', 'الغلاف')]
    o.append('<div class="note-box">%s<p class="small">لا يضم ملف المقرر صفحة روابط (أدوات ربط). هذه عبارات مساعدة لمناقشة الأصوات والنصوص بصوت عالٍ، مبنية على ما تدرّب عليه المقرر. · The course file has no connectors page. These are helper phrases for discussing sounds and texts aloud, built around what the course trains.</p></div>' % b_edu())
    for k, s in EU.EXPR.items():
        o.append('<section class="expr-set"><h2>%s <span class="en" dir="ltr">%s</span></h2><table class="src expr-t"><tbody>' % (s['ar'], s['en']))
        for a, e in s['rows']:
            o.append('<tr><td lang="ar">%s</td><td lang="en" dir="ltr">%s</td></tr>' % (esc(a), esc(e)))
        o.append('</tbody></table></section>')
    o.append('</article>')
    register('expressions', 'عبارات للمناقشة', 'Expressions for discussion', ''.join(o), 'page')


def flag_again(block, text):
    saved = {k: v for k, v in FLAG_USED.items() if k[0] == block}
    for k in saved:
        del FLAG_USED[k]
    h = flagify(block, text)
    FLAG_USED.update(saved)
    return h


def phonetics_page():
    o = ['<article class="page phon"><nav class="crumbs">%s › <span>مرجع النطق</span></nav><h1 class="ttl" lang="ar">مرجع النطق</h1><p class="item-en" lang="en" dir="ltr">Articulation reference</p>' % link('', 'الغلاف')]
    o.append('<div class="note-box">%s<p class="small">تجمع هذه الصفحة وصف المخرج الذي ورد في كل درس، مجموعاً حسب الصفات. الوصف نص الملف المصدري بلا تغيير، والتمرين في آخر الصفحة إضافة تعليمية. · This page gathers each lesson\'s own articulation description, grouped by feature. The descriptions are the file\'s text unchanged; the exercise at the end is an educational addition.</p></div>' % b_edu())
    for g_ar, g_en, ids in EU.PHON_GROUPS:
        o.append('<section class="phon-group"><h2>%s <span class="en" dir="ltr">%s</span></h2>' % (g_ar, g_en))
        for iid in ids:
            hb = EU.PHON_HOW[iid]
            it = ITEM[iid]
            if isinstance(hb, tuple):
                lines = [(0, '')] + [(k, clean(SRC[k]['text'])) for k in range(*hb) if clean(SRC[k]['text'])]
                j = 10 ** 9
            else:
                lines = [(hb, clean(SRC[hb]['text']))]
                j = hb + 1
            while j in SRC and not isinstance(hb, tuple) and SRC[j]['k'] == 'p' and not R.HEAD_EX.match(clean(SRC[j]['text'])) and not clean(SRC[j]['text']).startswith(('انظر', 'استمع', 'ملحوظة')) and j < hb + 14:
                t = clean(SRC[j]['text'])
                if t and not (R.HEAD_HOW.match(t)):
                    lines.append((j, t))
                j += 1
            o.append('<div class="phon-card"><h3 lang="ar"><a href="%s">%s</a></h3><ul class="src" dir="rtl">%s</ul></div>' % (
                route_href('item/' + iid), esc(it['ar']), ''.join('<li lang="ar">%s</li>' % flag_again(b, t) for b, t in lines[1:])))
        o.append('</section>')
    o.append('<section class="cloze"><h2>تمرين: أكملوا الجملة · Exercise: complete the statement %s</h2><p class="small">اختاروا الإجابة الصحيحة؛ يظهر بعدها نص الملف الذي يؤيدها. · Pick the answer; the supporting line from the course file then appears.</p><ol>' % b_edu())
    for k, c in enumerate(EU.CLOZE):
        ev = clean(SRC[c['src']]['text'])
        o.append('<li class="cz" data-ok="%d" data-key="sa.cloze.%d"><p class="qar" lang="ar">%s</p><p class="qen" lang="en" dir="ltr">%s</p><div class="opts" role="group">%s</div>'
                 '<p class="fb" hidden aria-live="polite"></p><p class="ev" hidden lang="ar">%s <a href="%s">المصدر · source</a></p></li>' % (
                     c['ok'], k, esc(c['ar']), esc(c['en']),
                     ''.join('<button type="button" class="chip opt" data-i="%d" lang="ar">%s</button>' % (n, esc(t)) for n, t in enumerate(c['opts'])),
                     esc(ev), route_href(BLOCK_ROUTE.get(c['src'], 'phonetics'))))
    o.append('</ol></section>')
    o.append('<section><h2>عبارات للمقارنة · Phrases for comparing %s</h2><table class="src expr-t"><tbody>%s</tbody></table></section>' % (
        b_edu(), ''.join('<tr><td lang="ar">%s</td><td lang="en" dir="ltr">%s</td></tr>' % (esc(a), esc(e)) for a, e in EU.PHON_EXPR)))
    o.append('</article>')
    register('phonetics', 'مرجع النطق', 'Articulation reference', ''.join(o), 'page')
    SEARCH.append(['مرجع النطق · مخارج الأصوات', 'phonetics', norm_ar('مرجع النطق مخارج الأصوات articulation')])


def framework_page():
    o = ['<article class="page appendix"><nav class="crumbs">%s › <span>الإطار المرجعي</span></nav><h1 class="ttl" lang="ar">ملحق: الإطار المرجعي للكفاءة</h1><p class="item-en" lang="en" dir="ltr">Appendix: proficiency framework</p>' % link('', 'الغلاف')]
    o.append('<div class="note-box"><p><strong>ما الذي لم يُقدَّم؟ · What was not supplied</strong></p>'
             '<p lang="en" dir="ltr">No framework document (such as ACTFL guidelines) was attached to the materials, so this book quotes none of its descriptors and makes no claim that its maps are aligned to any framework. The maps in this book (Unit 1 and Unit 2) are built from the course\'s own objectives, quoted verbatim, and are for self-reflection only. If you supply the framework PDFs, the maps can be re-aligned in a later build.</p>'
             '<p lang="ar">لم تُرفق وثيقة إطار مرجعي (مثل إرشادات ACTFL) مع المواد، فلا يقتبس هذا الكتاب أي وصف منها ولا يدّعي أن خرائطه مطابقة لإطار بعينه. بُنيت الخرائط على أهداف المقرر نفسها وهي للتأمل الذاتي فقط.</p></div>')
    o.append('<section><h2>مستويات الطلاب في المقرر · The course\'s own learner groups %s</h2><div class="src-body" dir="rtl">%s</div><p class="small">الفقرات من مقدمة الأستاذ في الملف المصدري. · From the teacher\'s introduction in the supplied file.</p></section>' % (b_src(), ''.join(
        '<p class="src" lang="ar">%s</p>' % esc(clean(SRC[i]['text'])) for i in (5, 6, 7))))
    o.append('<section><h2>خرائط الكفاءة · Proficiency maps</h2><p>%s %s</p></section></article>' % (link('unit/1/map', 'الوحدة الأولى · Unit 1', 'btn'), link('unit/2/map', 'الوحدة الثانية · Unit 2', 'btn')))
    register('appendix/framework', 'ملحق: الإطار المرجعي', 'Appendix: proficiency framework', ''.join(o), 'appendix')


def vocab_index_page():
    o = ['<article class="page appendix"><nav class="crumbs">%s › <span>فهرس المفردات</span></nav><h1 class="ttl" lang="ar">ملحق: فهرس المفردات</h1><p class="item-en" lang="en" dir="ltr">Appendix: vocabulary index (words from the course tables)</p>' % link('', 'الغلاف')]
    o.append('<p class="small">%s %s الكلمات من جداول الملف، والمعاني إضافة تعليمية. · Words come from the course tables; glosses are an educational addition.</p>' % (b_src(), b_edu()))
    o.append('<label class="sr-only" for="vq">بحث</label><input type="search" id="vq" class="vsearch" placeholder="ابحثوا عن كلمة أو معنى… · search a word or meaning…" autocomplete="off">')
    o.append('<p class="small" id="vcount" aria-live="polite"></p><div class="tablewrap"><table class="src vindex"><thead><tr><th>الكلمة</th><th>English</th><th>السياق</th><th>الفقرة</th></tr></thead><tbody>')
    n = 0
    for it in ITEMS:
        v = VOC[it['id']]
        for c in v['cards']:
            o.append('<tr data-q="%s %s"><td lang="ar">%s</td><td dir="ltr" lang="en">%s</td><td lang="ar">%s</td><td><a href="%s">%s</a></td></tr>' % (
                esc(norm_ar(c['w'])), esc(c['gloss'].lower()), esc(c['w']), esc(c['gloss']), esc(c['ctx']), route_href('item/' + it['id']), it['id']))
            SEARCH.append([c['w'] + ' — ' + c['gloss'] if c['gloss'] else c['w'], 'item/' + it['id'], norm_ar(c['w']) + ' ' + c['gloss'].lower()])
            n += 1
        for x in v['verbs']:
            if x['fusha']:
                o.append('<tr data-q="%s %s"><td lang="ar">%s ← %s</td><td dir="ltr" lang="en">%s</td><td lang="ar">فعل · %s</td><td><a href="%s">%s</a></td></tr>' % (
                    esc(norm_ar(x['fusha'] + ' ' + x['amiya'])), esc(x['gloss'].lower()), esc(x['fusha']), esc(x['amiya']), esc(x['gloss']), esc(x['pattern']), route_href('item/' + it['id']), it['id']))
                n += 1
    o.append('</tbody></table></div><p class="small">%d</p></article>' % n)
    register('appendix/vocab', 'ملحق: فهرس المفردات', 'Appendix: vocabulary index', ''.join(o), 'appendix')
    return n


def glossary_page():
    o = ['<article class="page appendix"><nav class="crumbs">%s › <span>المعجم</span></nav><h1 class="ttl" lang="ar">ملحق: المعجم</h1><p class="item-en" lang="en" dir="ltr">Appendix: glossary</p>' % link('', 'الغلاف')]
    o.append('<div class="note-box"><p lang="en" dir="ltr">The supplied Word file has no glossary section. The glossaries below were written for this book from the words of the longer texts; each is an educational addition and can be wrong in places — poetry and colloquial words in particular have more than one possible sense. Item 7.1 has none because its text is not reproduced.</p></div>')
    for iid, ent in EG.GLOSSARY.items():
        it = ITEM[iid]
        o.append('<section><h2><a href="%s">%s %s</a></h2><dl class="gloss">' % (route_href('item/' + iid), iid, esc(it['ar'])))
        for w, g, note in ent:
            o.append('<div><dt lang="ar">%s</dt><dd lang="en" dir="ltr">%s%s</dd></div>' % (esc(w), esc(g), (' <em>(%s)</em>' % esc(note)) if note else ''))
            SEARCH.append([w + ' — ' + g, 'item/' + iid, norm_ar(w) + ' ' + g.lower()])
        o.append('</dl></section>')
    o.append('</article>')
    register('appendix/glossary', 'ملحق: المعجم', 'Appendix: glossary', ''.join(o), 'appendix')


# ---------------------------------------------------------------------------------------------------------------------
def copy_images():
    zf = zipfile.ZipFile(os.path.join(HERE, 'source', 'sawti-arabi-source.docx'))
    os.makedirs(os.path.join(ROOT, 'assets', 'img'), exist_ok=True)
    n = 0
    for nm in zf.namelist():
        if nm.startswith('word/media/'):
            fn = nm.split('/')[-1]
            with open(os.path.join(ROOT, 'assets', 'img', 'docx-' + fn), 'wb') as f:
                f.write(zf.read(nm))
            n += 1
    return n


def main():
    nimg = copy_images()
    # private text slots (optional): _generator/data/private_texts/<key>.txt replaces a withheld card
    cover_page()
    intro_page()
    for u in UNITS:
        unit_page(u)
        for lid in u['lessons']:
            lesson_page(lid)
            for iid in LESSONS[lid]['items']:
                item_page(ITEM[iid])
        map_page(u)
        task_page(u)
    phonetics_page()
    expressions_page()
    framework_page()
    nvocab = vocab_index_page()
    glossary_page()
    contents_page()
    from report import build_reports
    build_reports(globals())
    # --- order for prev/next
    order = ['', 'intro', 'contents']
    for u in UNITS:
        order.append('unit/' + u['id'])
        for lid in u['lessons']:
            order.append('lesson/' + lid)
            order += ['item/' + i for i in LESSONS[lid]['items']]
        order += ['unit/%s/map' % u['id'], 'unit/%s/task' % u['id']]
    order += ['phonetics', 'expressions', 'appendix/framework', 'appendix/vocab', 'appendix/glossary', 'appendix/report', 'appendix/tech']
    assert set(order) == set(PAGES), (set(order) ^ set(PAGES))
    toc = []
    for u in UNITS:
        toc.append(dict(r='unit/' + u['id'], ar=u['ar'], en=u['en'], lessons=[
            dict(r='lesson/' + lid, ar=LESSONS[lid]['ar'], en=LESSONS[lid]['en'], items=[dict(r='item/' + i, id=i, ar=ITEM[i]['ar'], en=ITEM[i]['en'], ty=ITEM[i]['type']) for i in LESSONS[lid]['items']])
            for lid in u['lessons']], extra=[dict(r='unit/%s/map' % u['id'], ar='خريطة الكفاءة', en='Proficiency map'), dict(r='unit/%s/task' % u['id'], ar='المهمة الختامية', en='Final task')]))
    book = dict(meta=META, order=order, toc=toc, qtext=QTEXT, items=[i['id'] for i in ITEMS],
                titles={r: [PAGES[r]['t'], PAGES[r]['te']] for r in PAGES}, search=SEARCH,
                built=datetime.date.today().isoformat())
    pages = {r: PAGES[r]['h'] for r in PAGES}
    os.makedirs(os.path.join(ROOT, 'assets', 'js'), exist_ok=True)
    with open(os.path.join(ROOT, 'assets', 'js', 'data.js'), 'w', encoding='utf8') as f:
        f.write('/* generated by _generator/build.py — do not edit */\nwindow.BOOK=%s;\nwindow.PAGES=%s;\n' % (
            json.dumps(book, ensure_ascii=False, separators=(',', ':')), json.dumps(pages, ensure_ascii=False, separators=(',', ':'))))
    unused = [(k, FLAGS[k[1]]['text']) for k in [(f['block'], n) for n, f in enumerate(FLAGS)] if k not in FLAG_USED]
    info = dict(pages=len(PAGES), images=nimg, vocab_rows=nvocab, flags_total=len(FLAGS), flags_unused=unused,
                gloss_found=REPORT_INFO['gloss_found'], gloss_missing=REPORT_INFO['gloss_missing'], jump_checks=REPORT_INFO['jump_checks'])
    json.dump(info, open(os.path.join(HERE, 'data', 'build_info.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump({r: PAGES[r]['h'] for r in PAGES}, open(os.path.join(HERE, 'data', 'pages_dump.json'), 'w', encoding='utf8'), ensure_ascii=False)
    print(json.dumps(info, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
