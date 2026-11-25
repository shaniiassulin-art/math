# -*- coding: utf-8 -*-
"""מבחני חזרה באתר "אלגברה לינארית - הכנה למבחן" (algebra-solutions).

עמוד נפרד (#review): כל השאלות משלושת המבחנים (tools/samples/review_algebra.py), עם סינון לפי מבחן, נושא, רמה וסוג,
ושני קבצי PDF לשיתוף: התרגילים עם מקום לפתרון, והפתרונות המלאים של אותן שאלות.
התמונות לקבצים מוכנות מראש ב-tools/exam_images.js (algebra-solutions/review-img/).
samples.py קורא ל-section(...) ומוסיף את ASSETS לפני </body>.
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LV = {1: 'קלה', 2: 'בינונית', 3: 'קשה'}


def data(mod='review_algebra'):
    spec = importlib.util.spec_from_file_location(mod, os.path.join(HERE, 'samples', mod + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def section(render_one, mathify, mod='review_algebra'):
    m = data(mod)
    subject = getattr(m, 'SUBJECT', 'אלגברה לינארית')
    exams = dict(m.EXAMS)
    topics = dict(m.TOPICS)
    repl = {}
    used = [t for t, _ in m.TOPICS if any(t in q['topics'] for q in m.Q)]
    h = [f'\n    <!-- review:start --><section class="review-section" id="review" data-subject="{subject}" aria-labelledby="reviewTitle">',
         '<h2 id="reviewTitle">📝 מבחני חזרה</h2>',
         f'<p class="rv-intro">כל השאלות מ-{len(m.EXAMS)} מבחנים של הקורס ({len(m.Q)} שאלות), עם פתרון מלא לכל אחת. '
         'בחרי מבחנים, נושאים ורמה - ואפשר להוציא קובץ עם התרגילים ומקום לפתרון, וקובץ נפרד עם כל הפתרונות של אותן שאלות.</p>',
         '<div class="rv-filters">',
         '<div class="rv-f"><div class="rv-fh">מבחנים</div><div class="rv-chips">'
         + ''.join(f'<label class="rv-chip"><input type="checkbox" data-f="exam" value="{k}" checked><span>{v}</span></label>' for k, v in m.EXAMS)
         + '</div></div>',
         '<div class="rv-f"><div class="rv-fh">נושאים <button type="button" class="rv-all" data-all="topic">הכול</button> <button type="button" class="rv-all" data-none="topic">כלום</button></div><div class="rv-chips">'
         + ''.join(f'<label class="rv-chip"><input type="checkbox" data-f="topic" value="{t}" checked><span>{mathify(topics[t])}</span></label>' for t in used)
         + '</div></div>',
         '<div class="rv-f"><div class="rv-fh">רמת קושי</div><div class="rv-seg" role="group" aria-label="רמת קושי">'
         + ''.join(f'<button type="button" data-level="{k}" aria-pressed="{"true" if k == 0 else "false"}">{n}</button>' for k, n in [(0, 'הכול'), (1, 'קלה'), (2, 'בינונית'), (3, 'קשה')])
         + '</div></div>',
         '<div class="rv-f"><div class="rv-fh">סוג שאלה</div><div class="rv-seg" role="group" aria-label="סוג שאלה">'
         + ''.join(f'<button type="button" data-kind="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in [('all', 'הכול'), ('open', 'שאלות פתוחות'), ('mc', 'אמריקאיות')])
         + '</div></div>',
         '</div>',
         '<div class="rv-bar"><span class="rv-count" id="rvCount" aria-live="polite"></span>'
         '<button type="button" class="rv-pdf" id="rvPdfQ">📄 קובץ תרגילים - עם מקום לפתרון</button>'
         '<button type="button" class="rv-pdf" id="rvPdfS">✅ קובץ פתרונות מלאים</button></div>',
         '<p class="rv-note" id="rvNote" hidden></p>',
         '<div class="rv-list">']
    for q in m.Q:
        codes = [q['exam']] + list(q.get('also', []))
        names = ', '.join(exams[c] for c in codes)
        src = f'{names} - {q["num"]} ({q["pts"]} נק׳)'
        qt, _, op = q['q'].partition('§§OPTS§§')
        box = render_one('rv-' + q['id'], dict(src=src, q=qt.strip(), steps=q['steps'], ans=q['ans']))
        if op:      # the options go in after separate_regions, so the long formulas stay whole, one option per line
            ph = f'<!--rvopts:{q["id"]}-->'
            repl[ph] = '<div class="rv-opts">' + ''.join(
                f'<div class="rv-opt"><b>{l}.</b> <span class="rv-ox">{mathify(x)}</span></div>' for l, x in zip('אבגד', op.split('|||'))) + '</div>'
            box = box.replace('</p>', '</p>' + ph, 1)
        chips = (f'<span class="rv-tag rv-lv rv-lv-{q["level"]}">רמה {LV[q["level"]]}</span>'
                 + (f'<span class="rv-tag rv-mc">אמריקאית</span>' if q.get('mc') else '')
                 + ''.join(f'<span class="rv-tag">{mathify(topics[t])}</span>' for t in q['topics']))
        h.append(f'<div class="rv-item" data-id="{q["id"]}" data-exam="{" ".join(codes)}" data-topics="{" ".join(q["topics"])}" '
                 f'data-level="{q["level"]}" data-kind="{"mc" if q.get("mc") else "open"}" '
                 f'data-label="{exams[q["exam"]]}, {q["num"]} ({q["pts"]} נק׳)">'
                 f'<div class="rv-tags">{chips}</div>{box}</div>')
    h.append('</div><p class="rv-empty" id="rvEmpty" hidden>אין שאלות שמתאימות לבחירה. סמני עוד מבחנים או נושאים.</p></section><!-- review:end -->\n')
    return ''.join(h), repl


ASSETS = r"""<!-- review-assets:start -->
<style>
  /* ===== מבחני חזרה (#review) ===== */
  body:not(.review-mode) .review-section{ display:none; }
  body.review-mode .review-host > *:not(.review-section){ display:none !important; }
  .review-section h2{ margin-top:0; }
  .rv-back{ display:inline-flex; align-items:center; min-height:44px; margin:0 0 18px; padding:0 16px; border-radius:100px;
    border:1.5px solid var(--line, #E4DCCB); background:#fff; color:var(--indigo-2, #1F2A47); font-family:inherit; font-weight:800; font-size:.95rem; cursor:pointer; }
  .rv-intro{ color:var(--ink-soft, #4A5578); }
  .rv-filters{ display:grid; gap:14px; margin:16px 0; padding:16px; border-radius:16px; background:#fff; border:1.5px solid var(--line, #E4DCCB); }
  .rv-fh{ font-weight:800; margin-bottom:8px; display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
  .rv-all{ min-height:30px; padding:0 10px; border-radius:100px; border:1px solid #C9BEDC; background:#F6F1FC; color:#4A2C75; font-family:inherit; font-size:.8rem; font-weight:700; cursor:pointer; }
  .rv-chips{ display:flex; flex-wrap:wrap; gap:8px; }
  .rv-chip{ display:inline-flex; align-items:center; gap:6px; min-height:40px; padding:4px 12px; border-radius:100px; border:1.5px solid #D9CFEA; background:#fff; cursor:pointer; font-size:.92rem; }
  .rv-chip input{ width:18px; height:18px; accent-color:#6B3FA0; flex:none; margin:0; }
  .rv-chip:has(input:checked){ background:#F3EDFB; border-color:#6B3FA0; }
  .rv-seg{ display:flex; flex-wrap:wrap; gap:6px; }
  .rv-seg button{ min-height:40px; padding:0 14px; border-radius:100px; border:1.5px solid #D9CFEA; background:#fff; color:#2B2340; font-family:inherit; font-weight:700; cursor:pointer; }
  .rv-seg button[aria-pressed="true"]{ background:#6B3FA0; border-color:#6B3FA0; color:#fff; }
  .rv-bar{ display:flex; flex-wrap:wrap; align-items:center; gap:8px; padding:10px 0; background:var(--paper, #FBF8F2); }
  .rv-count{ font-weight:800; margin-inline-end:auto; }
  .rv-pdf{ min-height:44px; padding:6px 14px; border-radius:12px; border:1.5px solid #6B3FA0; background:#6B3FA0; color:#fff; font-family:inherit; font-weight:800; font-size:.92rem; cursor:pointer; line-height:1.3; }
  .rv-pdf#rvPdfS{ background:#fff; color:#6B3FA0; }
  .rv-pdf:disabled{ opacity:.6; cursor:wait; }
  .rv-note{ margin:0 0 10px; padding:10px 12px; border-radius:10px; background:#FFF6E0; border:1px solid #EBC877; }
  .rv-note[hidden], .rv-empty[hidden]{ display:none; }
  .rv-item{ margin:0 0 22px; }
  .review-section .box-q{ --lbl:"📝 שאלה ממבחן"; }
  .rv-item[hidden]{ display:none; }
  .rv-tags{ display:flex; flex-wrap:wrap; gap:6px; margin:0 0 6px; }
  .rv-tag{ display:inline-block; padding:2px 10px; border-radius:100px; background:#EEF1F8; color:#2B3A67; font-size:.8rem; font-weight:700; }
  .rv-lv-1{ background:#E3F4E8; color:#1E6B3A; } .rv-lv-2{ background:#FFF1D6; color:#8A5A00; } .rv-lv-3{ background:#FBE3E3; color:#9B2C2C; }
  .rv-mc{ background:#F3EDFB; color:#4A2C75; }
  .rv-opts{ display:flex; flex-direction:column; gap:6px; margin:4px 0 14px; }
  .rv-opt{ display:flex; align-items:baseline; gap:8px; }
  .rv-opt b{ flex:none; min-width:1.4em; }
  .rv-ox{ min-width:0; overflow-x:auto; -webkit-overflow-scrolling:touch; }
  .rv-empty{ padding:16px; text-align:center; color:var(--ink-soft, #4A5578); }
  .sidebar .review-open-btn{ display:flex; align-items:center; justify-content:center; width:100%; min-height:46px; margin:0 0 10px !important; border-radius:12px; box-sizing:border-box;
    padding:8px 12px; border:1.5px solid rgba(255,255,255,.3); background:rgba(255,255,255,.1); color:#fff; font-weight:800; font-size:.95rem; text-decoration:none; }
  .sidebar .review-open-btn:hover{ background:rgba(255,255,255,.18); }
</style>
<script>
(function(){
  try {
  var sec = document.getElementById('review'); if(!sec) return;
  var host = sec.parentElement; host.classList.add('review-host');
  var KEY = 'mathReview_v1:' + location.pathname;
  var LV = {1: 'קלה', 2: 'בינונית', 3: 'קשה'};
  var items = [].slice.call(sec.querySelectorAll('.rv-item'));
  var st = {exam: null, topic: null, level: 0, kind: 'all'};
  try { var sv = JSON.parse(localStorage.getItem(KEY) || 'null'); if(sv) st = sv; } catch(e){}
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(st)); } catch(e){} }

  // ---------- עמוד נפרד ----------
  var back = document.createElement('button'); back.type = 'button'; back.className = 'rv-back'; back.textContent = '→ חזרה למדריך';
  sec.insertBefore(back, sec.firstChild);
  var anchor = document.querySelector('.sidebar .exam-open-btn') || document.querySelector('.sidebar .ai-open-btn');
  if(anchor){ var b = document.createElement('a'); b.className = 'review-open-btn'; b.href = '#review'; b.textContent = '📝 מבחני חזרה';
    anchor.parentNode.insertBefore(b, anchor.nextSibling); }
  var mode = null, lastY = 0, cameIn = false;
  function isOn(){ var h = location.hash.slice(1); if(!h) return false; var t = document.getElementById(decodeURIComponent(h)); return !!t && (t === sec || sec.contains(t)); }
  function update(){
    var on = isOn(); if(on === mode) return;
    if(on){ if(mode === false){ lastY = window.scrollY; cameIn = true; }
      document.body.classList.add('review-mode');
      var mt = document.getElementById('menuToggle'); if(mt) mt.checked = false;
      var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      setTimeout(function(){ if(t && t !== sec) t.scrollIntoView(); else window.scrollTo(0, 0); }, 0);
    } else { document.body.classList.remove('review-mode'); if(mode === true) setTimeout(function(){ window.scrollTo(0, lastY); }, 0); }
    mode = on;
  }
  back.addEventListener('click', function(){
    var was = cameIn;
    try { history.replaceState(null, '', location.pathname + location.search); } catch(e){}
    update(); if(!was) window.scrollTo(0, 0);
  });
  window.addEventListener('hashchange', update);
  window.addEventListener('popstate', update);
  document.addEventListener('click', function(e){ var a = e.target.closest && e.target.closest('a[href="#review"]'); if(a) setTimeout(update, 0); });
  update();

  // ---------- סינון ----------
  var boxes = function(f){ return [].slice.call(sec.querySelectorAll('input[data-f="' + f + '"]')); };
  ['exam', 'topic'].forEach(function(f){
    if(st[f]) boxes(f).forEach(function(c){ c.checked = st[f].indexOf(c.value) >= 0; });
    boxes(f).forEach(function(c){ c.addEventListener('change', apply); });
  });
  sec.querySelectorAll('[data-all],[data-none]').forEach(function(bt){
    bt.addEventListener('click', function(){ var f = bt.getAttribute('data-all') || bt.getAttribute('data-none'), on = bt.hasAttribute('data-all');
      boxes(f).forEach(function(c){ c.checked = on; }); apply(); });
  });
  sec.querySelectorAll('[data-level]').forEach(function(bt){ bt.addEventListener('click', function(){ st.level = +bt.getAttribute('data-level'); apply(); }); });
  sec.querySelectorAll('[data-kind]').forEach(function(bt){ bt.addEventListener('click', function(){ st.kind = bt.getAttribute('data-kind'); apply(); }); });
  function visible(){ return items.filter(function(it){ return !it.hidden; }); }
  function apply(){
    st.exam = boxes('exam').filter(function(c){ return c.checked; }).map(function(c){ return c.value; });
    st.topic = boxes('topic').filter(function(c){ return c.checked; }).map(function(c){ return c.value; });
    sec.querySelectorAll('[data-level]').forEach(function(bt){ bt.setAttribute('aria-pressed', String(+bt.getAttribute('data-level') === st.level)); });
    sec.querySelectorAll('[data-kind]').forEach(function(bt){ bt.setAttribute('aria-pressed', String(bt.getAttribute('data-kind') === st.kind)); });
    items.forEach(function(it){
      var ok = it.dataset.exam.split(' ').some(function(e){ return st.exam.indexOf(e) >= 0; }) &&
        it.dataset.topics.split(' ').some(function(t){ return st.topic.indexOf(t) >= 0; }) &&
        (!st.level || +it.dataset.level === st.level) && (st.kind === 'all' || it.dataset.kind === st.kind);
      it.hidden = !ok;
    });
    var n = visible().length;
    document.getElementById('rvCount').textContent = n + ' שאלות';
    document.getElementById('rvEmpty').hidden = n > 0;
    document.getElementById('rvPdfQ').disabled = document.getElementById('rvPdfS').disabled = n === 0;
    ['rvPdfQ', 'rvPdfS'].forEach(function(id){ var b = document.getElementById(id); b._file = null; b.textContent = b._label || b.textContent; });
    say(''); save();
  }
  ['rvPdfQ', 'rvPdfS'].forEach(function(id){ var b = document.getElementById(id); b._label = b.textContent; });
  var note = document.getElementById('rvNote');
  function say(t){ note.textContent = t; note.hidden = !t; }
  apply();

  // ---------- קבצי PDF ----------
  var INFO = null;
  function info(){ return INFO ? Promise.resolve(INFO) : fetch('review-img/index.json', {cache: 'no-cache'}).then(function(r){ if(!r.ok) throw new Error('index'); return r.json(); }).then(function(j){ INFO = j; return j; }); }
  function img(name, sz){ return fetch('review-img/' + name + '.jpg').then(function(r){ if(!r.ok) throw new Error(name); return r.arrayBuffer(); }).then(function(b){ return {bytes: new Uint8Array(b), w: sz[0], h: sz[1]}; }); }
  function describe(){
    var all = function(f){ return boxes(f).every(function(c){ return c.checked; }); };
    var p = [];
    p.push(all('exam') ? 'כל המבחנים' : boxes('exam').filter(function(c){ return c.checked; }).map(function(c){ return c.nextElementSibling.textContent; }).join(', '));
    if(!all('topic')) p.push(st.topic.length + ' נושאים');
    p.push(st.level ? 'רמה ' + LV[st.level] : 'כל הרמות');
    if(st.kind !== 'all') p.push(st.kind === 'mc' ? 'שאלות אמריקאיות' : 'שאלות פתוחות');
    return p.join(' · ');
  }
  function build(withSol){
    var P = window.MathPdf; if(!P) return Promise.reject(new Error('MathPdf'));
    var its = visible();
    return info().then(function(inf){
      return Promise.all(its.map(function(it){
        var id = it.dataset.id, parts = [img(id + '-q', inf.q[id])];
        if(withSol) (inf.s[id] || []).forEach(function(sz, k){ parts.push(img(id + '-s' + (k + 1), sz)); });
        return Promise.all(parts);
      }));
    }).then(function(imgs){
      var d = new Date(), date = d.getDate() + '.' + (d.getMonth() + 1) + '.' + d.getFullYear();
      var X = 40, CW = 515, TOP = 40, BOT = 802, k = CW / 1360;
      var pages = [[]], pg = pages[0], y = TOP;
      function newPage(){ pg = []; pages.push(pg); y = TOP; }
      function put(im, gap){
        var w = CW, h = im.h * k; if(h > BOT - TOP){ var f = (BOT - TOP) / h; w *= f; h *= f; }
        if(y + h > BOT) newPage();
        pg.push({img: im, x: X + CW - w, y: y, w: w, h: h}); y += h + (gap || 0);
      }
      var head = P.textImg([['מבחני חזרה · ' + sec.dataset.subject + ' · ' + (withSol ? 'פתרונות' : 'תרגילים'), 40, true], [its.length + ' שאלות · ' + describe() + ' · ' + date, 26, false, '#555']]);
      put(head, 4); pg.push({line: [X, y, X + CW, y]}); y += 14;
      imgs.forEach(function(arr, i){
        var it = its[i], mc = it.dataset.kind === 'mc';
        var lab = P.textImg([['שאלה ' + (i + 1) + '  ·  ' + it.dataset.label, 30, true]]);
        var lh = lab.h * k, qh = arr[0].h * k;
        var need = lh + qh + (withSol ? 0 : (mc ? 40 : 230));
        if(y + Math.min(need, BOT - TOP) > BOT) newPage();
        put(lab, 2); put(arr[0], 6);
        if(!withSol){
          var space = mc ? 40 : 230, end = Math.min(BOT, y + space);
          for(var ly = y + 22; ly < end - 4; ly += 24) pg.push({line: [X, ly, X + CW, ly], dash: true});
          y = end + 10;
        } else {
          var sl = P.textImg([['פתרון', 28, true, '#1E6B3A']]); put(sl, 2);
          arr.slice(1).forEach(function(im){ put(im, 4); });
          y += 10; if(y < BOT){ pg.push({line: [X, y, X + CW, y]}); } y += 14;
        }
      });
      var name = 'מבחני חזרה - ' + sec.dataset.subject + ' - ' + (withSol ? 'פתרונות' : 'תרגילים') + ' - ' + date + '.pdf';
      return {blob: P.makePdf(pages), name: name};
    });
  }
  function deliver(btn){
    var f = btn._file;
    if(f instanceof File && navigator.canShare && navigator.canShare({files: [f]})){
      navigator.share({files: [f], title: btn._name}).then(function(){ say(''); }).catch(function(e){
        if(e && e.name === 'AbortError') return;
        say('הקובץ מוכן - לחצי שוב על הכפתור כדי לשמור או לשלוח אותו.');
      });
      return;
    }
    var url = URL.createObjectURL(f), a = document.createElement('a');
    a.href = url; a.download = btn._name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(url); }, 60000);
    say('הקובץ ירד למכשיר (בתיקיית ההורדות).');
  }
  function onPdf(withSol){ return function(){
    var btn = this; if(btn._file){ deliver(btn); return; }
    btn.disabled = true; btn.textContent = '⏳ מכינה את הקובץ...'; say('');
    build(withSol).then(function(r){
      var file = null; try { file = new File([r.blob], r.name, {type: 'application/pdf'}); } catch(e){}
      btn._file = file || r.blob; btn._name = r.name; btn.disabled = false; btn.textContent = '📤 שיתוף הקובץ' + (withSol ? ' (פתרונות)' : ' (תרגילים)');
      deliver(btn);
    }).catch(function(e){ btn.disabled = false; btn.textContent = btn._label; say('לא הצלחתי להכין את הקובץ. בדקי שיש חיבור לאינטרנט ונסי שוב.'); if(window.console) console.error('review pdf', e); });
  }; }
  document.getElementById('rvPdfQ').addEventListener('click', onPdf(false));
  document.getElementById('rvPdfS').addEventListener('click', onPdf(true));
  } catch(err){ if(window.console) console.error('review', err); }
})();
</script>
<!-- review-assets:end -->
"""
