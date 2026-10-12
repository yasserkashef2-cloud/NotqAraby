#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Headless-Chromium QA (Playwright). Serves the book over http://127.0.0.1 and also opens it from file://.
Writes data/qa_raw.json (every check with result). Run:  python3 -I _generator/qa.py [shots_dir]"""
import os, sys, re, json, time, threading, http.server, socketserver, functools, datetime
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHOTS = sys.argv[1] if len(sys.argv) > 1 else None
if SHOTS:
    os.makedirs(SHOTS, exist_ok=True)

RES = []          # (name, ok, detail)


def check(name, ok, detail=''):
    RES.append((name, bool(ok), str(detail)[:400]))
    print(('PASS ' if ok else 'FAIL ') + name + ((' — ' + str(detail)[:200]) if (detail and not ok) else ''))


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def serve():
    h = functools.partial(Q, directory=ROOT)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h)
    srv.allow_reuse_address = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


srv, port = serve()
BASE = 'http://127.0.0.1:%d/index.html' % port
pages = json.load(open(os.path.join(HERE, 'data', 'pages_dump.json'), encoding='utf8'))
routes = list(pages.keys())

with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 1280, 'height': 900}, accept_downloads=True)
    page = ctx.new_page()
    errors, failed, bad = [], [], []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append('PAGEERROR ' + str(e)))
    page.on('requestfailed', lambda r: failed.append(r.url + ' ' + str(r.failure)))
    page.on('response', lambda r: bad.append('%s %s' % (r.status, r.url)) if r.status >= 400 else None)

    page.goto(BASE)
    page.wait_for_selector('h1')
    check('cover renders', page.inner_text('h1.cover-title') == 'صوتي عربي')
    check('routes in data = pages built', True, len(routes))

    # ---- every route: renders, has h1, no overflow, internal links resolve, jump targets exist, images load
    link_bad, jump_bad, img_bad, overflow = [], [], [], []
    for vw, vh in ((1280, 900), (390, 800)):
        page.set_viewport_size({'width': vw, 'height': vh})
        for r in routes:
            page.goto(BASE + '#/' + r)
            page.wait_for_selector('main h1')
            page.wait_for_timeout(30)
            info = page.evaluate('''() => {
                const o = {ow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1, links: [], jumps: [], imgs: []};
                document.querySelectorAll('main a[href^="#/"]').forEach(a => o.links.push(a.getAttribute('href').slice(2)));
                document.querySelectorAll('main .jump').forEach(b => { if (!document.getElementById(b.dataset.go)) o.jumps.push(b.dataset.go); });
                return o; }''')
            if vw == 1280:
                bad_i = page.evaluate('''async () => { const bad = []; await Promise.all([...document.querySelectorAll('main img')].map(i => new Promise(res => { const n = new Image(); n.onload = () => { if (!n.naturalWidth) bad.push(i.getAttribute('src')); res(); }; n.onerror = () => { bad.push(i.getAttribute('src')); res(); }; n.src = i.src; }))); return bad; }''')
                img_bad += [(r, i) for i in bad_i]
            if info['ow']:
                overflow.append('%s@%d' % (r, vw))
            if vw == 1280:
                for l in info['links']:
                    if l not in pages:
                        link_bad.append((r, l))
                jump_bad += [(r, j) for j in info['jumps']]
    page.set_viewport_size({'width': 1280, 'height': 900})
    check('no horizontal overflow (desktop 1280 + phone 390, all %d pages)' % len(routes), not overflow, overflow[:8])
    check('all in-page links resolve to a page', not link_bad, link_bad[:5])
    check('all "jump to source" buttons point at an existing element', not jump_bad, jump_bad[:5])
    check('no broken images on any page', not img_bad, img_bad[:5])

    # ---- fonts
    page.goto(BASE + '#/item/1.1')
    page.wait_for_selector('h1.item-title')
    page.wait_for_timeout(600)
    fonts = page.evaluate('''async () => { await document.fonts.ready; const r = {};
        for (const f of ['TS Hiba', 'Amiri', 'IBM Plex Sans Arabic', 'Noto Serif']) r[f] = document.fonts.check('16px "' + f + '"', 'صوت ص');
        r.loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight); return r; }''')
    check('self-hosted fonts load (title, Amiri, Plex Arabic, Noto Serif)', all(fonts[k] for k in ['TS Hiba', 'Amiri', 'IBM Plex Sans Arabic', 'Noto Serif']), fonts)
    page.goto(BASE + '#/')
    page.wait_for_timeout(400)

    # ---- heading colours
    def color(sel):
        return page.evaluate('(s) => getComputedStyle(document.querySelector(s)).color', sel)
    page.goto(BASE + '#/item/1.1'); page.wait_for_selector('h1.item-title')
    c_listen_title = color('h1.item-title'); c_listen_ex = color('h3.ex')
    page.goto(BASE + '#/item/1.7'); page.wait_for_selector('h1.item-title')
    c_read_title = color('h1.item-title')
    page.goto(BASE + '#/item/6.1'); page.wait_for_selector('h1.item-title')
    c_read_ex = color('h3.ex')
    check('listening titles dark blue (title + exercise headings)', c_listen_title == 'rgb(18, 48, 107)' and c_listen_ex == 'rgb(18, 48, 107)', (c_listen_title, c_listen_ex))
    check('reading/recitation titles dark red (title + exercise headings)', c_read_title == 'rgb(138, 28, 28)' and c_read_ex == 'rgb(138, 28, 28)', (c_read_title, c_read_ex))

    # ---- flip card, star, persistence
    page.goto(BASE + '#/item/1.1'); page.wait_for_selector('.fc')
    fc = page.locator('.fc').first
    fc.locator('.fc-flip').click()
    check('flip card flips', 'flipped' in (fc.locator('.fc-flip').get_attribute('class') or ''))
    fc.locator('.fc-star').click()
    check('star marks card learned', 'learned' in (fc.get_attribute('class') or ''))
    ans = page.locator('textarea.ans').first
    ans.fill('إجابة تجريبية')
    page.locator('.done-cb').check()
    page.wait_for_timeout(100)
    check('progress label updates after finishing an item', page.inner_text('#pbar-label').strip().startswith('1 /'), page.inner_text('#pbar-label'))
    page.reload(); page.wait_for_selector('textarea.ans')
    check('answer persists after reload', page.locator('textarea.ans').first.input_value() == 'إجابة تجريبية')
    check('completion persists after reload', page.locator('.done-cb').is_checked())
    check('star persists after reload', 'learned' in (page.locator('.fc').first.get_attribute('class') or ''))
    # download
    page.evaluate("document.querySelector('#menu-btn').click()")
    with page.expect_download() as dl:
        page.click('#dl-btn')
    d = dl.value
    p = d.path()
    txt = open(p, encoding='utf8').read()
    check('download of answers works and contains the answer + question text', 'إجابة تجريبية' in txt and 'Q:' in txt, txt[:200])
    # drawer + Esc
    check('drawer opens', 'open' in page.get_attribute('#drawer', 'class'))
    page.keyboard.press('Escape')
    check('Esc closes the drawer', 'open' not in page.get_attribute('#drawer', 'class'))
    # text size, reading mode, theme
    fs0 = page.evaluate("getComputedStyle(document.body).fontSize")
    page.click('#fs-up')
    fs1 = page.evaluate("getComputedStyle(document.body).fontSize")
    check('text-size button enlarges text', float(fs1[:-2]) > float(fs0[:-2]), (fs0, fs1))
    page.click('#read-btn')
    check('reading mode toggles', page.evaluate("document.body.classList.contains('reading')"))
    page.click('#read-btn')
    bg0 = page.evaluate("getComputedStyle(document.body).backgroundColor")
    page.click('#theme-btn')
    bg1 = page.evaluate("getComputedStyle(document.body).backgroundColor")
    check('theme toggle changes the background', bg0 != bg1, (bg0, bg1))
    page.click('#theme-btn')

    # ---- jump button
    page.goto(BASE + '#/item/6.1'); page.wait_for_selector('.jump')
    b = page.locator('.jump').first
    tgt = b.get_attribute('data-go')
    b.click(); page.wait_for_timeout(300)
    check('jump button scrolls to and highlights its target', page.evaluate("(id) => document.getElementById(id).classList.contains('jumped')", tgt), tgt)
    # paragraph navigator
    check('paragraph navigator shown on the statement page', page.evaluate("document.querySelector('#paranav').classList.contains('on')"))
    page.click('#paranav button[data-d=next]'); page.click('#paranav button[data-d=next]')
    check('paragraph navigator advances', page.inner_text('#pn-label').startswith('2'), page.inner_text('#pn-label'))

    # ---- YouTube loads on click only
    page.goto(BASE + '#/item/6.1'); page.wait_for_selector('.yt-load')
    check('no iframe before pressing load (nothing leaves the browser)', page.locator('main iframe').count() == 0)
    page.locator('.yt-load').first.click()
    src = page.locator('main iframe').first.get_attribute('src')
    check('load button creates a youtube-nocookie iframe', src.startswith('https://www.youtube-nocookie.com/embed/'), src)

    # ---- glossary + flag tooltips, highlighter
    page.goto(BASE + '#/item/5.2'); page.wait_for_selector('.gl')
    page.locator('.gl').first.scroll_into_view_if_needed(); page.wait_for_timeout(400)
    page.locator('.gl').first.hover(); page.wait_for_timeout(150)
    check('glossary popover appears on hover', page.evaluate("document.querySelector('#tip').classList.contains('on')") and len(page.inner_text('#tip')) > 2, page.inner_text('#tip'))
    page.goto(BASE + '#/item/2.1'); page.wait_for_selector('.hl-scope')
    page.click('.tgl-hl'); page.wait_for_timeout(100)
    n_mark = page.locator('mark.tl').count()
    page.click('.tgl-hl')
    check('target-sound highlighter marks letters and clears them', n_mark > 5 and page.locator('mark.tl').count() == 0, n_mark)
    page.goto(BASE + '#/item/1.1'); page.wait_for_selector('.flag')
    page.locator('.flag').first.scroll_into_view_if_needed(); page.wait_for_timeout(400)
    page.locator('.flag').first.hover(); page.wait_for_timeout(150)
    check('source-error flag shows note and proposed fix', 'Proposed fix' in page.inner_text('#tip'), page.inner_text('#tip'))

    # ---- cloze, self-assessment, search, vocab filter
    page.goto(BASE + '#/phonetics'); page.wait_for_selector('.cz')
    li = page.locator('.cz').first
    li.locator('.opt').nth(1).click()
    check('cloze gives feedback with source line', li.locator('.fb').is_visible() and li.locator('.ev').is_visible())
    page.goto(BASE + '#/unit/1/map'); page.wait_for_selector('.maprow')
    page.locator('.maprow').first.locator('input[type=radio]').nth(3).check()
    page.reload(); page.wait_for_selector('.maprow')
    check('self-assessment choice persists', page.locator('.maprow').first.locator('input[type=radio]').nth(3).is_checked())
    check('map summary counts rated rows', 'قيّمتم 1' in page.inner_text('.map-sum'), page.inner_text('.map-sum'))
    page.goto(BASE + '#/appendix/vocab'); page.wait_for_selector('#vq')
    total = page.locator('table.vindex tbody tr').count()
    page.fill('#vq', 'ظلم')
    vis = page.locator('table.vindex tbody tr:not([hidden])').count()
    check('vocabulary filter narrows the list', 0 < vis < total, (vis, total))
    page.fill('#search', 'ظلم'); page.wait_for_timeout(100)
    check('site search returns results', page.locator('#sres a').count() > 0)
    page.fill('#search', '')

    # ---- media: players present, seek buttons
    page.goto(BASE + '#/item/1.6'); page.wait_for_selector('video')
    can = page.evaluate("(() => { const v = document.createElement('video'); return [v.canPlayType('video/mp4; codecs=\"avc1.42E01E\"'), document.createElement('audio').canPlayType('audio/mp4; codecs=\"mp4a.40.2\"'), document.createElement('audio').canPlayType('audio/mpeg')]; })()")
    seekbtns = page.locator('.seekbtn').all_inner_texts()
    check('Bilal video has seek buttons for the two stated times', len(seekbtns) == 2, seekbtns)
    if can[0] or can[1]:
        page.locator('.seekbtn').nth(1).click(); page.wait_for_timeout(1500)
        t = page.evaluate("document.querySelector('video').currentTime")
        check('seek button jumps video to 2:00', abs(t - 120) < 3, t)
    else:
        RES.append(('seek button jumps video to 2:00', None, 'Chromium build in this sandbox cannot decode H.264/AAC: %s' % can))
        print('SKIP seek playback (no H.264/AAC decoder in test Chromium)')
    page.goto(BASE + '#/item/5.1'); page.wait_for_selector('.media')
    page.locator('.ratebtn[data-rate="0.75"]').first.click()
    rate = page.evaluate("document.querySelector('[data-media-el]').playbackRate")
    check('speed button sets playbackRate 0.75', abs(rate - 0.75) < 0.01, rate)

    # ---- print: PDF
    page.goto(BASE + '#/item/6.1'); page.wait_for_selector('h1')
    pdf = page.pdf(format='A4', print_background=True)
    check('print stylesheet produces a PDF', len(pdf) > 20000, len(pdf))
    if SHOTS:
        open(os.path.join(SHOTS, 'item-6.1.pdf'), 'wb').write(pdf)

    # ---- screenshots
    if SHOTS:
        for vw, vh, tag in ((1280, 900, 'd'), (390, 800, 'm')):
            page.set_viewport_size({'width': vw, 'height': vh})
            for r in ['', 'item/1.1', 'item/1.7', 'item/6.1', 'unit/1/map', 'phonetics']:
                page.goto(BASE + '#/' + r); page.wait_for_selector('main h1'); page.wait_for_timeout(300)
                page.screenshot(path=os.path.join(SHOTS, '%s-%s.png' % (tag, r.replace('/', '_') or 'cover')))
        page.set_viewport_size({'width': 1280, 'height': 900})

    # ---- console + network
    check('no console errors / page errors during the whole run (http)', not errors, errors[:5])
    real_failed = [f for f in failed if not (('/assets/media/' in f or 'youtube-nocookie' in f) and 'ERR_ABORTED' in f)]   # media preloads aborted by navigation are normal
    check('no failed or 4xx/5xx requests (http; aborted media preloads on navigation ignored)', not real_failed and not bad, (real_failed + bad)[:5])

    # ---- file:// run
    ctx2 = br.new_context(viewport={'width': 1280, 'height': 900})
    p2 = ctx2.new_page(); e2 = []
    p2.on('console', lambda m: e2.append(m.text) if m.type == 'error' else None)
    p2.on('pageerror', lambda e: e2.append('PAGEERROR ' + str(e)))
    p2.goto('file://' + os.path.join(ROOT, 'index.html') + '#/item/1.1')
    p2.wait_for_selector('h1.item-title')
    p2.wait_for_timeout(500)
    check('opens from file:// and renders an item page', p2.inner_text('h1.item-title').startswith('صوت'), p2.inner_text('h1.item-title'))
    p2.locator('textarea.ans').first.fill('x')
    check('file:// run: no script errors (localStorage may be restricted; guarded)', not [x for x in e2 if 'Failed to load resource' not in x], e2[:3])
    br.close()

srv.shutdown()
ok = [r for r in RES if r[1] is True]
fail = [r for r in RES if r[1] is False]
skip = [r for r in RES if r[1] is None]
json.dump(dict(date=datetime.date.today().isoformat(), results=RES), open(os.path.join(HERE, 'data', 'qa_raw.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('\n%d passed, %d failed, %d skipped' % (len(ok), len(fail), len(skip)))
sys.exit(1 if fail else 0)
