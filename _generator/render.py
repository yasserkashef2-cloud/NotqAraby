# -*- coding: utf-8 -*-
"""Turns blocks of the supplied Word file into HTML, in source order, without changing any supplied text.
(Whitespace is collapsed and trimmed for display only; the QA script checks every line against the source.)"""
import html, json, os, re
from structure import *
from media_map import MEDIA
from data_flags import FLAGS

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {b['i']: b for b in json.load(open(os.path.join(HERE, 'data', 'source.json'), encoding='utf8'))}
MEDIA_BY_ID = {m['id']: m for m in MEDIA}

AR = re.compile(r'[؀-ۿ]')
LAT = re.compile(r'[A-Za-zÀ-ɏɐ-ʯᴀ-ᶿḀ-ỿ]')
DIAC = re.compile('[ً-ٰٟـ۪ٖ-ٟ]')


def esc(s):
    return html.escape(s, quote=True)


def clean(s):
    return re.sub(r'\s+', ' ', s.replace('\xa0', ' ').replace('\t', ' ')).strip()


def norm_ar(w):
    w = DIAC.sub('', w)
    w = re.sub('[إأآٱ]', 'ا', w)
    w = w.replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    return re.sub(r'\s+', ' ', w).strip()


FLAG_USED = {}


def flagify(block, text):
    """escape `text` and wrap flagged substrings (first occurrence per flag) in a visible flag marker"""
    out = esc(text)
    for k, f in enumerate(FLAGS):
        if f['block'] != block:
            continue
        e = esc(f['text'])
        if e in out and (block, k) not in FLAG_USED:
            FLAG_USED[(block, k)] = True
            out = out.replace(e, '<span class="flag" tabindex="0" role="note" data-note="%s" data-fix="%s">%s</span>' % (esc(f['note']), esc(f['fix']), e), 1)
    return out


def lang_span(line, block):
    """a table-cell line: wrap pure-Latin transcription in an LTR span"""
    h = flagify(block, line)
    if LAT.search(line) and not AR.search(line):
        return '<span class="tr" dir="ltr">%s</span>' % h
    return h


# ---------------------------------------------------------------------------------------------------------------------
IMG_ALT = {
    'image1.png': ('', ''), 'image2.png': ('', ''),
    'image3.png': ('رسم مقطعي: وضع اللسان عند س و ز', 'Sagittal diagram: tongue position for sīn / zāy'),
    'image4.png': ('رسم مقطعي: وضع اللسان عند ص', 'Sagittal diagram: tongue position for ṣād'),
    'image5.jpg': ('لقطة من فيديو تعليمي: مخرج الضاد', 'Still from a teaching video: place of articulation of ḍād'),
    'image6.jpg': ('لقطة من فيديو تعليمي: مخرج السين والزاي', 'Still from a teaching video: place of articulation of sīn and zāy'),
    'image7.png': ('رسم مقطعي: وضع اللسان عند ض', 'Sagittal diagram: tongue position for ḍād'),
    'image8.png': ('رسم مقطعي: وضع اللسان عند د و ت', 'Sagittal diagram: tongue position for dāl / tāʾ'),
    'image9.jpg': ('لقطة من فيديو تعليمي: مخرج الضاد', 'Still from a teaching video: place of articulation of ḍād'),
    'image10.png': ('رسم مقطعي: وضع اللسان عند ط', 'Sagittal diagram: tongue position for ṭāʾ'),
    'image11.jpg': ('لقطة من فيديو تعليمي: مخرج الطاء', 'Still from a teaching video: place of articulation of ṭāʾ'),
    'image12.jpg': ('لقطة من فيديو تعليمي: مقارنة بين الطاء والدال والتاء', 'Still from a teaching video: comparison of ṭāʾ, dāl and tāʾ'),
    'image13.png': ('رسم مقطعي: وضع اللسان عند ذ و ث', 'Sagittal diagram: tongue position for dhāl / thāʾ'),
    'image14.png': ('رسم مقطعي: وضع اللسان عند ظ', 'Sagittal diagram: tongue position for ẓāʾ'),
    'image15.jpg': ('لقطة من فيديو تعليمي: مخرج الظاء', 'Still from a teaching video: place of articulation of ẓāʾ'),
    'image16.jpg': ('لقطة من فيديو تعليمي: مقارنة بين أوضاع اللسان', 'Still from a teaching video: comparison of tongue positions'),
    'image17.jpeg': ('صورة مرافقة لنص الاستماع في الملف المصدري', 'Picture supplied with the listening item in the Word file'),
    'image18.jpeg': ('صورة مرافقة لأبيات أبي فراس: بيت من القصيدة فوق مشهد فارس', 'Picture supplied with the Abū Firās verses (a line of the poem over a horseman scene)'),
    'image19.png': ('رسم مقطعي: وضع اللسان عند ك', 'Sagittal diagram: tongue position for kāf'),
    'image20.png': ('رسم مقطعي: وضع اللسان عند ق', 'Sagittal diagram: tongue position for qāf'),
    'image21.jpg': ('لقطة من فيديو تعليمي: مخرج القاف', 'Still from a teaching video: place of articulation of qāf'),
    'image22.jpg': ('لقطة من فيديو تعليمي: مخرج القاف', 'Still from a teaching video: place of articulation of qāf'),
    'image23.png': ('رسم مقطعي: وضع اللسان عند ع و ء و هـ', 'Sagittal diagram: tongue position for ʿayn / hamza / hāʾ'),
    'image24.png': ('رسم مقطعي: وضع اللسان عند ح', 'Sagittal diagram: tongue position for ḥāʾ'),
    'image25.jpg': ('لقطة من فيديو تعليمي: مخرج الحاء', 'Still from a teaching video: place of articulation of ḥāʾ'),
    'image26.jpeg': ('رسم مرافق لأبيات المهلهل: فارس بسيف', 'Illustration supplied with the Muhalhil verses (a horseman with a sword)'),
    'image27.jpeg': ('صورة مرافقة للأغنية في الملف المصدري', 'Photograph supplied with the song in the Word file'),
    'image28.png': ('رسم مقطعي: وضع اللسان عند ع', 'Sagittal diagram: tongue position for ʿayn'),
    'image29.jpg': ('لقطة من فيديو تعليمي: مخرج العين', 'Still from a teaching video: place of articulation of ʿayn'),
    'image30.jpeg': ('صورة مرافقة للأغنية في الملف المصدري', 'Photograph supplied with the song in the Word file'),
    'image31.png': ('رسم مقطعي: وضع اللسان عند غ', 'Sagittal diagram: tongue position for ghayn'),
    'image32.jpg': ('لقطة من فيديو تعليمي: مخرج الغين', 'Still from a teaching video: place of articulation of ghayn'),
    'image33.jpeg': ('صورة مرافقة للأغنية في الملف المصدري', 'Photograph supplied with the song in the Word file'),
    'image34.png': ('رسم مقطعي: وضع اللسان عند خ', 'Sagittal diagram: tongue position for khāʾ'),
    'image35.jpg': ('لقطة من فيديو تعليمي: مخرج الخاء', 'Still from a teaching video: place of articulation of khāʾ'),
    'image36.jpeg': ('صورة مرافقة للمثل المغربي: رجل يحمل أكياساً ويسقي', 'Picture supplied with the Moroccan saying (a man in a yellow robe)'),
    'image37.jpeg': ('صورة مرافقة: تعويذة على شكل كف', 'Picture supplied with the sayings: a hand-shaped amulet'),
    'image38.png': ('رسم مقطعي: اللام المرققة واللام المفخمة', 'Sagittal diagrams: non-emphatic and emphatic lām'),
    'image39.jpg': ('لقطة من فيديو تعليمي: مخرج اللام', 'Still from a teaching video: place of articulation of lām'),
    'image40.jpeg': ('صورة مرافقة للأغنية في الملف المصدري', 'Photograph supplied with the song in the Word file'),
    'image41.png': ('رسم مقطعي: الراء المرققة والراء المفخمة', 'Sagittal diagrams: non-emphatic and emphatic rāʾ'),
    'image42.jpg': ('لقطة من فيديو تعليمي: شكل اللسان عند نطق الراء المفخمة والمرققة', 'Still from a teaching video: tongue shape for emphatic and non-emphatic rāʾ'),
    'image43.jpeg': ('صورة مرافقة لأبيات المتنبي: كلمات «الخيل والليل والبيداء» فوق ثلاث لقطات', 'Picture supplied with the al-Mutanabbī verses: the words "the horses, the night, the desert" over three scenes'),
    'image44.jpeg': ('صورة مرافقة للأغنية في الملف المصدري', 'Photograph supplied with the song in the Word file'),
    'image45.jpeg': ('صورة تاريخية مرافقة لبيان 23 يوليو', 'Historical photograph supplied with the 23 July statement'),
    'image46.jpeg': ('صورة مرافقة للقصيدة في الملف المصدري', 'Photograph supplied with the poem in the Word file'),
    'image47.jpeg': ('صورة مرافقة للقصيدة في الملف المصدري', 'Photograph supplied with the poem in the Word file'),
}


def img_tag(path):
    fn = path.split('/')[-1]
    ar, en = IMG_ALT.get(fn, ('صورة من الملف المصدري', 'Picture from the Word file'))
    alt = ar if not en else '%s — %s' % (ar, en)
    return '<img src="assets/img/docx-%s" alt="%s" loading="lazy" decoration="%s">' % (fn, esc(alt), 'yes' if not ar else 'no')


# ---------------------------------------------------------------------------------------------------------------------
def media_widget(m):
    fn = m['id'] + os.path.splitext(m['src'])[1].lower()
    label = os.path.splitext(os.path.basename(m['src']))[0]
    tag = 'video' if m['kind'] == 'video' else 'audio'
    seek = ''
    if m['seek']:
        seek = '<span class="seek" role="group" aria-label="Jump to a time stated in the course file">' + ''.join(
            '<button type="button" class="chip seekbtn" data-seek="%d" data-target="%s">⏱ %s</button>' % (s, m['id'], t) for t, s in m['seek']) + '</span>'
    note = ('<p class="mnote">%s</p>' % esc(m['note'])) if m['note'] else ''
    kindcls = 'vid' if tag == 'video' else 'aud'
    return ('<div class="media %s" id="m-%s" data-media="%s">'
            '<div class="media-head"><span class="mrole">%s</span><span class="mfile" dir="auto">%s</span></div>'
            '<%s controls preload="%s" src="assets/media/%s" data-media-el="%s"></%s>'
            '<div class="media-tools"><span class="rate" role="group" aria-label="Playback speed">'
            '<button type="button" class="chip ratebtn" data-rate="0.75" data-target="%s">0.75×</button>'
            '<button type="button" class="chip ratebtn" data-rate="1" data-target="%s">1×</button></span>%s'
            '<a class="direct" href="assets/media/%s" target="_blank" rel="noopener">فتح الملف في صفحة مستقلة · open in a new tab</a></div>%s</div>'
            ) % (kindcls, m['id'], m['id'], esc(m['role']), esc(label), tag, 'metadata' if tag == 'video' else 'none', fn, m['id'], tag, m['id'], m['id'], seek, fn, note)


def yt_widget(block, vid, title):
    seek = ''
    if block in YT_SEEK:
        seek = '<span class="seek">' + ''.join('<button type="button" class="chip ytseek" data-seek="%d" data-yt="%s">⏱ %s</button>' % (s, vid, t) for t, s in YT_SEEK[block]) + '</span>'
    extra = ''
    for url, note in EXTRA_LINKS.get(block + 1, []):
        extra += '<p class="mnote"><a href="%s" target="_blank" rel="noopener">%s</a></p>' % (esc(url), esc(note))
    return ('<div class="yt" id="yt-%s" data-yt="%s"><div class="media-head"><span class="mrole">YouTube</span><span class="mfile" dir="ltr">youtube.com/watch?v=%s</span></div>'
            '<div class="yt-stage"><button type="button" class="yt-load" data-yt="%s"><span class="play">▶</span> تحميل الفيديو · load the video (youtube-nocookie)</button></div>'
            '<div class="media-tools">%s<a class="direct" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">فتح الفيديو الأصلي في صفحة جديدة · open the original video in a new tab</a></div>%s</div>'
            ) % (vid, vid, vid, vid, seek, vid, extra)


def withheld_card(wh, item):
    pt = os.path.join(HERE, 'data', 'private_texts', wh['key'] + '.txt')
    if os.path.exists(pt):
        lines = [clean(x) for x in open(pt, encoding='utf8').read().split('\n') if clean(x)]
        return ('<div class="verses private" id="w-%s" dir="rtl"><p class="mnote">نص أضافه صاحب المقرر عند البناء · text added by the course author at build time</p>%s</div>' % (
            wh['key'], ''.join('<div class="verse single"><span class="vn">%d</span><span class="h h1">%s</span></div>' % (n, esc(l)) for n, l in enumerate(lines, 1))))
    if wh['kind'] == 'transcript':
        body = ('<p><strong>%s</strong></p><p class="en" dir="ltr">The Word file supplies a transcript for this listening item. It is deliberately not shown: the aim is to build listening strategies '
                '(gist first, details second). Replay the recording as often as needed.</p>' % esc(wh['label_ar']))
    else:
        body = ('<p><strong>%s</strong></p><p class="en" dir="ltr">%s. The Word file supplies this text, but it is modern copyrighted material and is not reproduced in this book. '
                'Use the YouTube link above to listen to it. The course author can add the text at build time (see README: <code>_generator/data/private_texts/%s.txt</code>).</p>'
                % (esc(wh['label_ar']), esc(wh['label_en']), wh['key']))
    return '<aside class="withheld" id="w-%s">%s</aside>' % (wh['key'], body)


# ---------------------------------------------------------------------------------------------------------------------
HEAD_EX = re.compile(r'^(التمرين|التدريب|الإستماع|الاستماع)')
HEAD_HOW = re.compile(r'^كيف ')
PRACTICE_RUNS = [(129, 137), (202, 211), (282, 290), (367, 373), (469, 475), (984, 992)]
PRACTICE_SET = {i for a, b in PRACTICE_RUNS for i in range(a, b)}
PAIR_TABLES = {104, 162, 242, 325, 328, 447, 529, 625, 797, 870, 945}
CONTEXT_TABLES = {113, 174, 259, 341, 457, 738, 808, 882, 958}
GRID_TABLES = {543, 647}
NOTE_TABLES = {279, 936}
TIP_TABLES = {550, 651}
VERB_TABLES = {379, 382, 386, 389, 486, 558, 658, 749, 817, 890, 997}
POEM_TABLES = {417}


def cell_lines(cell):
    return [clean(x) for x in cell['text'].split('\n') if clean(x)]


def render_table(i):
    t = SRC[i]
    rows = t['rows']
    if i in POEM_TABLES:
        # poetic order: first hemistich is the second cell of the row in the XML (see flags)
        out = ['<div class="verses" id="b%d" dir="rtl" role="group" aria-label="verses">' % i]
        for n, r in enumerate(rows, 1):
            h1, h2 = clean(r[1]['text']), clean(r[0]['text'])
            out.append('<div class="verse" id="b%d-v%d"><span class="vn">%d</span><span class="h h1">%s</span><span class="h h2">%s</span></div>' % (i, n, n, flagify(i, h1), flagify(i, h2)))
        out.append('</div>')
        return ''.join(out)
    if i in NOTE_TABLES:
        lines = [clean(x) for x in rows[0][0]['text'].split('\n') if clean(x)]
        return '<aside class="callout src" id="b%d">%s</aside>' % (i, ''.join('<p>%s</p>' % flagify(i, l) for l in lines))
    if i in VERB_TABLES:
        return render_verbs(i)
    cls = 'pairs' if i in PAIR_TABLES else 'contexts' if i in CONTEXT_TABLES else 'grid' if i in GRID_TABLES else 'tip' if i in TIP_TABLES else 'tbl'
    out = ['<div class="tablewrap"><table class="src %s" id="b%d" dir="rtl">' % (cls, i)]
    for n, r in enumerate(rows):
        cells = r
        if i in TIP_TABLES and len(r) == 3 and not clean(r[2]['text']):
            cells = r[:2]
        tag = 'th' if (n == 0 and cls in ('pairs', 'contexts', 'tip', 'grid')) else 'td'
        out.append('<tr>')
        for c in cells:
            ls = cell_lines(c)
            inner = '<br>'.join(lang_span(l, i) for l in ls)
            attrs = ' scope="col"' if tag == 'th' else ''
            out.append('<%s%s>%s</%s>' % (tag, attrs, inner, tag))
        out.append('</tr>')
    out.append('</table></div>')
    return ''.join(out)


def render_verbs(i):
    t = SRC[i]
    rows = t['rows']
    hdr1, hdr2, data = rows[0], rows[1], rows[2:]
    out = ['<div class="tablewrap"><table class="src verbs" id="b%d" dir="rtl"><thead>' % i, '<tr>']
    for c in hdr1:
        ls = cell_lines(c)
        txt = ' '.join(ls)
        if c['span'] > 1:
            out.append('<th colspan="%d" scope="colgroup">%s</th>' % (c['span'], esc(txt)))
        else:
            out.append('<th rowspan="2" scope="col">%s</th>' % esc(txt))
    out.append('</tr><tr>')
    for c in hdr2:
        if c['vmerge'] == 'cont':
            continue
        out.append('<th scope="col">%s</th>' % esc(clean(c['text'])))
    out.append('</tr></thead><tbody>')
    for r in data:
        out.append('<tr>')
        for k, c in enumerate(r):
            ls = cell_lines(c)
            inner = '<br>'.join(lang_span(l, i) for l in ls)
            cls = ' class="lat"' if k in (4, 5) else ''
            out.append('<td%s>%s</td>' % (cls, inner))
        out.append('</tr>')
    out.append('</tbody></table></div>')
    return ''.join(out)


# ---------------------------------------------------------------------------------------------------------------------
def split_hemi(line):
    parts = re.split(r'\s*(?:\.{2,}|…+)\s*|\s{3,}', line.replace('\xa0', ' ').strip())
    return [clean(p) for p in parts if clean(p)]


def render_verse_block(i, mode, vcount):
    text = SRC[i]['text']
    out = []
    for line in text.split('\n'):
        l = clean(line)
        if not l:
            continue
        if re.fullmatch(r'\*{3,4}', l):
            out.append('<div class="stanza-gap" aria-hidden="true"></div>')
            continue
        # hemistichs separated by *** inside a line (al-Mutanabbi block style)
        mm = re.split(r'\s*\*{3,4}\s*', l)
        if len(mm) == 1:
            mm = split_hemi(l)
        vcount[0] += 1
        n = vcount[0]
        if mode == 'lines' or len(mm) == 1:
            out.append('<div class="verse single" id="b%d-v%d"><span class="vn">%d</span><span class="h h1">%s</span></div>' % (i, n, n, flagify(i, l)))
        else:
            out.append('<div class="verse" id="b%d-v%d"><span class="vn">%d</span><span class="h h1">%s</span><span class="h h2">%s</span></div>' % (i, n, n, flagify(i, mm[0]), flagify(i, ' '.join(mm[1:]))))
    return out


def render_item_source(item, sub_ctx=None):
    """returns (html, info) for the source blocks of one item"""
    a, b = item['rng']
    out = []
    ul = []
    words_run = []
    placed = set()
    vcount = [0]
    pnum = [0]
    media_after = {}
    for m in MEDIA:
        if m['item'] == item['id']:
            media_after.setdefault(m['after'], []).append(m)

    def flush_ul():
        nonlocal ul
        if ul:
            out.append('<ul class="src">%s</ul>' % ''.join(ul))
            ul = []

    def flush_words():
        nonlocal words_run
        if words_run:
            out.append('<ul class="src words" dir="rtl">%s</ul>' % ''.join('<li id="b%d" lang="ar">%s</li>' % (i, flagify(i, t)) for i, t in words_run))
            words_run = []

    seen_wh = set()
    for i in range(a, b):
        bl = SRC.get(i)
        if bl is None:
            continue
        # media after previous block handled below
        if i in WITHHELD:
            flush_ul(); flush_words()
            wh = WITHHELD[i]
            if wh['key'] not in seen_wh:
                seen_wh.add(wh['key'])
                out.append(withheld_card(wh, item))
        elif bl['k'] == 't':
            flush_ul(); flush_words()
            out.append(render_table(i))
        else:
            t = clean(bl['text'])
            imgs = bl['imgs']
            if imgs and not t:
                flush_ul(); flush_words()
                out.append('<figure class="figs" id="b%d">%s</figure>' % (i, ''.join(img_tag(p) for p in imgs)))
            elif t:
                if i in PRACTICE_SET and not (bl['bold'] and bl['underline'] and HEAD_EX.match(t)) and len(t.split()) <= 3:
                    flush_ul()
                    words_run.append((i, t))
                else:
                    flush_words()
                    if i in YOUTUBE:
                        flush_ul()
                        out.append(yt_widget(i, YOUTUBE[i], t))
                    elif t.startswith('http'):
                        flush_ul()
                        out.append('<p class="src"><a href="%s" target="_blank" rel="noopener">%s</a></p>' % (esc(t), esc(t)))
                    elif i in SPEECH_BLOCKS:
                        flush_ul()
                        lines = [clean(x) for x in bl['text'].split('\n') if clean(x)]
                        out.append('<div class="speech" id="b%d" dir="rtl">%s</div>' % (i, ''.join(
                            '<p class="para" id="b%d-p%d"><span class="pn" aria-label="paragraph %d">%d</span><span class="pt">%s</span></p>' % (i, n, n, n, flagify(i, l)) for n, l in enumerate(lines, 1))))
                    elif i in VERSE_BLOCKS:
                        flush_ul()
                        out.append('<div class="verses" id="b%d" dir="rtl">%s</div>' % (i, ''.join(render_verse_block(i, VERSE_BLOCKS[i], vcount))))
                    else:
                        cls = ''
                        if i in TITLE_RED: cls = ' t-read'
                        elif i in TITLE_BLUE: cls = ' t-listen'
                        if bl['listed'] and not (bl['bold'] and bl['underline'] and (HEAD_EX.match(t) or HEAD_HOW.match(t))):
                            ul.append('<li id="b%d" class="%s">%s</li>' % (i, cls.strip(), flagify(i, t)))
                        else:
                            flush_ul()
                            hd = bl['bold'] and bl['underline']
                            if HEAD_EX.match(t) and (hd or len(t) < 90):
                                out.append('<h3 class="ex%s" id="b%d">%s</h3>' % (cls, i, flagify(i, t)))
                            elif hd and HEAD_HOW.match(t):
                                out.append('<h3 class="how" id="b%d">%s</h3>' % (i, flagify(i, t)))
                            elif hd or (bl['bold'] and cls):
                                out.append('<h4 class="sub%s" id="b%d">%s</h4>' % (cls, i, flagify(i, t)))
                            else:
                                out.append('<p class="src%s%s" id="b%d">%s</p>' % (' b' if bl['bold'] else '', cls, i, flagify(i, t)))
            if imgs and t:
                out.append('<figure class="figs">%s</figure>' % ''.join(img_tag(p) for p in imgs))
        # media after this block
        if i in media_after:
            flush_ul(); flush_words()
            for m in media_after[i]:
                out.append(media_widget(m))
                placed.add(m['id'])
    flush_ul(); flush_words()
    missing = [m['id'] for m in MEDIA if m['item'] == item['id'] and m['id'] not in placed]
    if missing:
        raise SystemExit('media not placed for %s: %s (anchor outside range?)' % (item['id'], missing))
    return ''.join(out)


def blocks_text_lines(i):
    """all display lines of a source block (for the fidelity check)"""
    b = SRC[i]
    if b['k'] == 'p':
        return [clean(x) for x in b['text'].split('\n') if clean(x)]
    res = []
    for r in b['rows']:
        for c in r:
            res += [clean(x) for x in c['text'].split('\n') if clean(x)]
    return res
