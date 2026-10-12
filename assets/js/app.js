/* صوتي عربي — interactive book (vanilla JS, no network calls). Pages and data are inline in data.js so it works from file://. */
(function () {
  'use strict';
  var B = window.BOOK, P = window.PAGES;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var mem = {};
  var store = {
    get: function (k) { try { var v = window.localStorage.getItem(k); return v === null && mem[k] !== undefined ? mem[k] : v; } catch (e) { return mem[k] === undefined ? null : mem[k]; } },
    set: function (k, v) { mem[k] = v; try { window.localStorage.setItem(k, v); } catch (e) { /* private mode: kept in memory only */ } },
    del: function (k) { delete mem[k]; try { window.localStorage.removeItem(k); } catch (e) { } },
    keys: function () { var r = Object.keys(mem); try { for (var i = 0; i < window.localStorage.length; i++) { var k = window.localStorage.key(i); if (k && k.indexOf('sa.') === 0 && r.indexOf(k) < 0) r.push(k); } } catch (e) { } return r.filter(function (k) { return k.indexOf('sa.') === 0; }); }
  };
  var main = $('#main'), drawer = $('#drawer'), scrim = $('#scrim'), tip = $('#tip');
  var cur = '';

  /* ---------- helpers ---------- */
  var DIAC = /[ً-ٰٟـ۪-ۭ]/g;
  function norm(s) { return String(s).replace(DIAC, '').replace(/[إأآٱ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه').replace(/ؤ/g, 'و').replace(/ئ/g, 'ي').toLowerCase().replace(/\s+/g, ' ').trim(); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function routeNow() { var h = decodeURIComponent((location.hash || '').replace(/^#\/?/, '')); return Object.prototype.hasOwnProperty.call(P, h) ? h : ''; }
  function href(r) { return '#/' + r; }

  /* ---------- progress ---------- */
  function doneCount() { var n = 0; B.items.forEach(function (id) { if (store.get('sa.done.' + id) === '1') n++; }); return n; }
  function updateProgress() {
    var n = doneCount(), t = B.items.length, pct = Math.round(100 * n / t);
    $('#progress > i').style.width = pct + '%';
    $('#progress').setAttribute('aria-valuenow', pct);
    $('#pbar-label').textContent = n + ' / ' + t;
    $$('.mark[data-done]').forEach(function (m) { m.setAttribute('data-on', store.get('sa.done.' + m.getAttribute('data-done')) === '1' ? '1' : '0'); });
    $$('#drawer a[data-item]').forEach(function (a) { a.classList.toggle('dr-done', store.get('sa.done.' + a.getAttribute('data-item')) === '1'); });
  }

  /* ---------- drawer ---------- */
  function buildDrawer() {
    var h = '<h2 style="margin-top:0">الفهرس · Contents</h2><ul><li><a href="#/">الغلاف · Cover</a></li><li><a href="#/intro">مقدمة المقرر · Introduction</a></li><li><a href="#/contents">الفهرس الكامل · Full contents</a></li></ul>';
    B.toc.forEach(function (u) {
      h += '<h2><a href="' + href(u.r) + '">' + esc(u.ar) + '</a></h2><ul>';
      u.lessons.forEach(function (l) {
        h += '<li><a href="' + href(l.r) + '">' + esc(l.ar) + '</a><ul>';
        l.items.forEach(function (i) { h += '<li><a data-item="' + i.id + '" href="' + href(i.r) + '"><span class="num">' + i.id + '</span> ' + esc(i.ar) + '</a></li>'; });
        h += '</ul></li>';
      });
      u.extra.forEach(function (x) { h += '<li><a href="' + href(x.r) + '">' + esc(x.ar) + ' · ' + esc(x.en) + '</a></li>'; });
      h += '</ul>';
    });
    h += '<h2>مراجع وملاحق · Reference</h2><ul>';
    [['phonetics', 'مرجع النطق · Articulation'], ['expressions', 'عبارات للمناقشة · Expressions'], ['appendix/framework', 'الإطار المرجعي · Framework'], ['appendix/vocab', 'فهرس المفردات · Vocabulary index'], ['appendix/glossary', 'المعجم · Glossary'], ['appendix/report', 'تقرير المصادر · Sources report'], ['appendix/tech', 'ملاحظات تقنية · Technical notes']].forEach(function (x) { h += '<li><a href="' + href(x[0]) + '">' + x[1] + '</a></li>'; });
    h += '</ul><h2>أدواتي · My data</h2><p><button type="button" class="tb" id="dl-btn">تنزيل إجاباتي · Download my answers</button></p><p><button type="button" class="tb" id="clr-btn">مسح بياناتي · Clear my saved data</button></p>';
    drawer.innerHTML = h;
  }
  var lastFocus = null;
  function openDrawer() { lastFocus = document.activeElement; drawer.classList.add('open'); scrim.classList.add('on'); $('#menu-btn').setAttribute('aria-expanded', 'true'); var a = $('a', drawer); if (a) a.focus(); }
  function closeDrawer() { if (!drawer.classList.contains('open')) return; drawer.classList.remove('open'); scrim.classList.remove('on'); $('#menu-btn').setAttribute('aria-expanded', 'false'); (lastFocus && lastFocus.focus) ? lastFocus.focus() : $('#menu-btn').focus(); }

  /* ---------- page render ---------- */
  function hydrate() {
    $$('textarea[data-key]', main).forEach(function (t) { t.value = store.get(t.getAttribute('data-key')) || ''; });
    $$('input[type=checkbox][data-key]', main).forEach(function (c) { c.checked = store.get(c.getAttribute('data-key')) === '1'; });
    $$('input[type=radio][data-key]', main).forEach(function (r) { r.checked = store.get(r.getAttribute('data-key')) === r.value; });
    $$('.fc[data-star]', main).forEach(function (f) { var on = store.get(f.getAttribute('data-star')) === '1'; f.classList.toggle('learned', on); var s = $('.fc-star', f); s.textContent = on ? '★' : '☆'; s.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    $$('.cz', main).forEach(function (li) { var v = store.get(li.getAttribute('data-key')); if (v !== null) answerCloze(li, +v, true); });
    mapSummary();
    var fs = parseFloat(store.get('sa.rate') || '1');
    $$('.ratebtn', main).forEach(function (b) { b.setAttribute('aria-pressed', +b.getAttribute('data-rate') === 1 ? 'true' : 'false'); });
  }
  function mapSummary() {
    $$('.map-sum', main).forEach(function (el) {
      var u = el.getAttribute('data-unit'), rows = $$('.maprow', main).length, n = 0;
      for (var k = 0; k < rows; k++) { if (store.get('sa.self.' + u + '.' + k) !== null) n++; }
      el.innerHTML = '<span lang="ar">قيّمتم ' + n + ' من ' + rows + '</span> <span class="en" lang="en" dir="ltr">You have rated ' + n + ' of ' + rows + '</span>';
    });
  }
  function pager(route) {
    var i = B.order.indexOf(route), h = '<nav class="pager" aria-label="التنقل · page navigation">';
    if (i > 0) { var p = B.order[i - 1]; h += '<a class="btn" rel="prev" href="' + href(p) + '">→ ' + esc(B.titles[p][0]) + '</a>'; } else h += '<span></span>';
    if (i < B.order.length - 1) { var n = B.order[i + 1]; h += '<a class="btn" rel="next" href="' + href(n) + '">' + esc(B.titles[n][0]) + ' ←</a>'; }
    return h + '</nav>';
  }
  function setupParaNav() {
    var pn = $('#paranav'), paras = $$('.para', main);
    if (!paras.length) { pn.classList.remove('on'); return; }
    pn.classList.add('on');
    pn.setAttribute('data-i', '-1');
  }
  function render(route, noScroll) {
    cur = route;
    closeDrawer();
    main.innerHTML = P[route] + pager(route);
    document.title = (route ? B.titles[route][0] + ' — ' : '') + B.meta.title_ar + ' · ' + B.meta.title_en.replace(/^[^"]*"|"$/g, '');
    $$('#drawer a').forEach(function (a) { a.removeAttribute('aria-current'); if (a.getAttribute('href') === href(route)) a.setAttribute('aria-current', 'page'); });
    hydrate(); updateProgress(); setupParaNav();
    if (route) store.set('sa.last', route);
    var rb = $('#resume-btn');
    if (rb) { var l = store.get('sa.last'); if (l && P[l] && l) { rb.hidden = false; rb.setAttribute('href', href(l)); } }
    var hd = $('h1', main);
    if (hd) { hd.setAttribute('tabindex', '-1'); if (!noScroll) hd.focus({ preventScroll: true }); }
    if (!noScroll) window.scrollTo(0, 0);
    $('#live').textContent = (route ? B.titles[route][0] : B.titles[''][0]);
    hideTip();
    applyLetters(false);
  }
  function onHash() { render(routeNow()); }

  /* ---------- jump / media ---------- */
  function openAncestors(el) { var d = el.closest('details'); while (d) { d.open = true; d = d.parentElement && d.parentElement.closest('details'); } }
  function jumpTo(id, mediaId, secs) {
    var el = document.getElementById(id);
    if (!el) return;
    openAncestors(el);
    el.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' });
    el.classList.remove('jumped'); void el.offsetWidth; el.classList.add('jumped');
    el.setAttribute('tabindex', '-1'); try { el.focus({ preventScroll: true }); } catch (e) { }
    if (mediaId) seek(mediaId, secs);
  }
  function seek(mid, secs) {
    var m = $('[data-media-el="' + mid + '"]');
    if (!m) return;
    try { m.currentTime = secs; var p = m.play(); if (p && p.catch) p.catch(function () { }); } catch (e) { }
  }
  function loadYT(box, vid, start) {
    var stage = $('.yt-stage', box);
    var q = 'autoplay=1&rel=0&modestbranding=1' + (start ? '&start=' + start : '');
    if (location.protocol.indexOf('http') === 0) q += '&origin=' + encodeURIComponent(location.origin);
    stage.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(vid) + '?' + q + '" title="YouTube video" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>';
    if (location.protocol === 'file:' && !$('.fnote', box)) { var n = document.createElement('p'); n.className = 'mnote fnote'; n.textContent = 'Opened from a file: YouTube may refuse to play (error 153). Use the direct link below, or host the folder on a web server.'; box.appendChild(n); }
  }

  /* ---------- tooltips ---------- */
  function showTip(el) {
    var h;
    if (el.classList.contains('flag')) h = '<b>⚑ Source issue:</b> ' + esc(el.getAttribute('data-note')) + '<br><b>Proposed fix:</b> <span lang="ar" dir="rtl" style="font-family:Amiri,serif;font-size:1.15em">' + esc(el.getAttribute('data-fix')) + '</span>';
    else if (el.classList.contains('gl') && !el.closest('.gl-off')) h = esc(el.getAttribute('data-gl'));
    else return;
    tip.innerHTML = h; tip.classList.add('on');
    var r = el.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight;
    var x = Math.min(Math.max(8, r.left + r.width / 2 - tw / 2), window.innerWidth - tw - 8), y = r.top - th - 8;
    if (y < 8) y = r.bottom + 8;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
    tip.setAttribute('data-for', 'x');
  }
  function hideTip() { tip.classList.remove('on'); }

  /* ---------- target-letter highlighter ---------- */
  function applyLetters(on, btn) {
    var scope = $('.hl-scope .src-body', main);
    if (!scope) return;
    var it = $('.item', main);
    var letters = it ? it.getAttribute('data-target') : '';
    $$('mark.tl', scope).forEach(function (m) { m.replaceWith(document.createTextNode(m.textContent)); });
    scope.normalize();
    if (!on || !letters) return;
    var re = new RegExp('[' + letters + ']', 'g');
    var w = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, null), nodes = [], n;
    while ((n = w.nextNode())) { if (!n.parentNode.closest('mark,script,style') && re.test(n.nodeValue)) nodes.push(n); re.lastIndex = 0; }
    nodes.forEach(function (t) {
      var frag = document.createDocumentFragment(), s = t.nodeValue, last = 0, m;
      re.lastIndex = 0;
      while ((m = re.exec(s))) {
        // take following diacritics along
        var e = m.index + 1; while (e < s.length && /[ً-ٰٟ]/.test(s[e])) e++;
        if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
        var mk = document.createElement('mark'); mk.className = 'tl'; mk.textContent = s.slice(m.index, e); frag.appendChild(mk);
        last = e; re.lastIndex = e;
      }
      if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
      t.parentNode.replaceChild(frag, t);
    });
  }

  /* ---------- cloze ---------- */
  function answerCloze(li, i, silent) {
    var ok = +li.getAttribute('data-ok'), fb = $('.fb', li), ev = $('.ev', li);
    $$('.opt', li).forEach(function (b, k) { b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
    fb.hidden = false; ev.hidden = false;
    fb.className = 'fb ' + (i === ok ? 'ok' : 'bad');
    fb.textContent = i === ok ? '✓ صحيح · Correct' : '✗ ليس بعد — راجعوا السطر أدناه · Not yet — check the line below';
    if (!silent) store.set(li.getAttribute('data-key'), String(i));
  }

  /* ---------- download / clear ---------- */
  function download() {
    var keys = store.keys().filter(function (k) { return /^sa\.(ans|cult|refl|note|self|chk|done|cloze)\./.test(k); }).sort();
    var out = ['صوتي عربي — إجاباتي · My answers', 'Saved ' + new Date().toISOString(), ''];
    keys.forEach(function (k) {
      var v = store.get(k); if (v === null || v === '') return;
      out.push('[' + k + ']'); if (B.qtext[k]) out.push('Q: ' + B.qtext[k]); out.push('A: ' + v); out.push('');
    });
    var blob = new Blob(['﻿' + out.join('\n')], { type: 'text/plain;charset=utf-8' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'sawti-arabi-my-answers.txt';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  /* ---------- settings ---------- */
  function applyFs() { var f = parseFloat(store.get('sa.fs') || '1.125'); document.documentElement.style.setProperty('--fs', f + 'rem'); }
  function applyTheme() { var t = store.get('sa.theme'); if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t); else document.documentElement.removeAttribute('data-theme'); var b = $('#theme-btn'); b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false'); }
  function applyMode() { var on = store.get('sa.mode') === 'reading'; document.body.classList.toggle('reading', on); $('#read-btn').setAttribute('aria-pressed', on ? 'true' : 'false'); }

  /* ---------- search ---------- */
  function doSearch(q) {
    var box = $('#sres'); q = norm(q);
    if (q.length < 2) { box.hidden = true; return; }
    var res = [];
    for (var i = 0; i < B.search.length && res.length < 14; i++) { if (B.search[i][2].indexOf(q) >= 0) res.push(B.search[i]); }
    box.innerHTML = res.length ? res.map(function (r) { return '<a href="' + href(r[1]) + '">' + esc(r[0]) + '</a>'; }).join('') : '<a href="#" onclick="return false">لا نتائج · No results</a>';
    box.hidden = false;
  }

  /* ---------- events ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var el;
    if ((el = t.closest('.fc-flip'))) { var on = el.classList.toggle('flipped'); el.setAttribute('aria-pressed', on ? 'true' : 'false'); return; }
    if ((el = t.closest('.fc-star'))) { var f = el.closest('.fc'), v = !f.classList.contains('learned'); f.classList.toggle('learned', v); el.textContent = v ? '★' : '☆'; el.setAttribute('aria-pressed', v ? 'true' : 'false'); store.set(f.getAttribute('data-star'), v ? '1' : '0'); return; }
    if ((el = t.closest('.jump'))) { jumpTo(el.getAttribute('data-go'), el.getAttribute('data-media'), +el.getAttribute('data-seek')); return; }
    if ((el = t.closest('.seekbtn'))) { seek(el.getAttribute('data-target'), +el.getAttribute('data-seek')); return; }
    if ((el = t.closest('.ratebtn'))) { var m = $('[data-media-el="' + el.getAttribute('data-target') + '"]'); if (m) m.playbackRate = +el.getAttribute('data-rate'); $$('.ratebtn', el.parentNode).forEach(function (b) { b.setAttribute('aria-pressed', b === el ? 'true' : 'false'); }); return; }
    if ((el = t.closest('.yt-load'))) { loadYT(el.closest('.yt'), el.getAttribute('data-yt'), 0); return; }
    if ((el = t.closest('.ytseek'))) { loadYT(el.closest('.yt'), el.getAttribute('data-yt'), +el.getAttribute('data-seek')); return; }
    if ((el = t.closest('.tgl-hl'))) { var o = el.getAttribute('aria-pressed') !== 'true'; el.setAttribute('aria-pressed', o ? 'true' : 'false'); applyLetters(o); return; }
    if ((el = t.closest('.tgl-gl'))) { var g = el.getAttribute('aria-pressed') !== 'true'; el.setAttribute('aria-pressed', g ? 'true' : 'false'); $('.hl-scope .src-body', main).classList.toggle('gl-off', !g); hideTip(); return; }
    if ((el = t.closest('.opt'))) { answerCloze(el.closest('.cz'), +el.getAttribute('data-i'), false); return; }
    if (t.closest('#menu-btn')) { drawer.classList.contains('open') ? closeDrawer() : openDrawer(); return; }
    if (t.closest('#scrim')) { closeDrawer(); return; }
    if (t.closest('#fs-up')) { store.set('sa.fs', String(Math.min(1.6, parseFloat(store.get('sa.fs') || '1.125') + 0.1).toFixed(3))); applyFs(); return; }
    if (t.closest('#fs-dn')) { store.set('sa.fs', String(Math.max(0.85, parseFloat(store.get('sa.fs') || '1.125') - 0.1).toFixed(3))); applyFs(); return; }
    if (t.closest('#theme-btn')) { var c = store.get('sa.theme'); store.set('sa.theme', c === 'dark' ? 'light' : 'dark'); applyTheme(); return; }
    if (t.closest('#read-btn')) { store.set('sa.mode', store.get('sa.mode') === 'reading' ? 'normal' : 'reading'); applyMode(); return; }
    if (t.closest('#print-btn')) { window.print(); return; }
    if (t.closest('#dl-btn')) { download(); return; }
    if (t.closest('#clr-btn')) { if (confirm('مسح كل الإجابات والتقدم المحفوظة في هذا المتصفح؟ · Clear all saved answers and progress in this browser?')) { store.keys().forEach(function (k) { if (k !== 'sa.fs' && k !== 'sa.theme') store.del(k); }); render(cur, true); } return; }
    if ((el = t.closest('#paranav button'))) { var ps = $$('.para', main), pn = $('#paranav'), i = +pn.getAttribute('data-i'); i = el.getAttribute('data-d') === 'next' ? Math.min(ps.length - 1, i + 1) : Math.max(0, i - 1); pn.setAttribute('data-i', i); jumpTo(ps[i].id); $('#pn-label').textContent = (i + 1) + ' / ' + ps.length; return; }
    if (!t.closest('.flag,.gl')) hideTip();
    if (!t.closest('#sbox')) { $('#sres').hidden = true; }
    var a = t.closest('#sres a'); if (a) { $('#sres').hidden = true; $('#search').value = ''; }
    if (t.closest('#drawer a')) closeDrawer();
  });
  document.addEventListener('input', function (e) {
    var t = e.target;
    if (t.matches('textarea[data-key]')) store.set(t.getAttribute('data-key'), t.value);
    else if (t.id === 'search') doSearch(t.value);
    else if (t.id === 'vq') {
      var q = norm(t.value), rows = $$('table.vindex tbody tr', main), n = 0;
      rows.forEach(function (r) { var on = !q || r.getAttribute('data-q').indexOf(q) >= 0; r.hidden = !on; if (on) n++; });
      $('#vcount').textContent = n + ' / ' + rows.length;
    }
  });
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (t.matches('input[type=checkbox][data-key]')) { store.set(t.getAttribute('data-key'), t.checked ? '1' : '0'); updateProgress(); }
    else if (t.matches('input[type=radio][data-key]')) { store.set(t.getAttribute('data-key'), t.value); mapSummary(); }
  });
  ['mouseover', 'focusin'].forEach(function (ev) { document.addEventListener(ev, function (e) { var f = e.target.closest && e.target.closest('.flag,.gl'); if (f) showTip(f); }); });
  ['mouseout', 'focusout'].forEach(function (ev) { document.addEventListener(ev, function (e) { if (e.target.closest && e.target.closest('.flag,.gl')) hideTip(); }); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { hideTip(); $('#sres').hidden = true; closeDrawer(); }
    if (e.key === 'Tab' && drawer.classList.contains('open')) {
      var f = $$('a,button', drawer); if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });
  window.addEventListener('hashchange', onHash);
  window.addEventListener('scroll', hideTip, { passive: true });

  /* ---------- start ---------- */
  buildDrawer(); applyFs(); applyTheme(); applyMode();
  try { history.scrollRestoration = 'manual'; } catch (e) { }
  onHash();
})();
