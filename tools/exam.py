# -*- coding: utf-8 -*-
"""מחולל מבחנים - מתווסף לכל אתר למידה (build_hub.py קורא ל-ensure_exam).

השאלות: כל השאלות לדוגמה באתר (= כל השאלות מקבצי הקורס), נקראות מהדף עצמו בזמן ריצה:
  נושא   - ה"חלק" (h2 עם id בצורה exN-pM) שהשאלה נמצאת בו, מקובץ לפי יחידה
  קובץ   - מתוך שורת המקור "📍 <קובץ> · <מקום>" ("תרגול נוסף לתרגיל N" שייך לקובץ של תרגיל N)
  רמה    - לפי היקף הפתרון (מספר שלבים ושורות): השליש הקצר - קלה, האמצעי - בינונית, הארוך - קשה
שאלות שבוצעו נשמרות בדפדפן (localStorage), בנפרד לכל אתר.
"""

EXAM_BTN_SIDEBAR = '<button type="button" class="exam-open-btn" data-exam-open>📝 מחולל מבחנים</button>'
EXAM_BTN_TOPBAR = '<button type="button" class="hub-exam" data-exam-open aria-label="מחולל מבחנים">📝 מבחן</button>'

EXAM_ASSETS = r"""<!-- exam:start -->
<style>
  /* ===== מחולל מבחנים ===== */
  .exam-open-btn{ display:block; width:100%; min-height:44px; margin:8px 0 0; padding:8px 12px; border-radius:12px; border:2px solid #6B3FA0;
    background:#F3EDFA; color:#4B2A78; font-family:inherit; font-weight:800; font-size:.95rem; cursor:pointer; }
  .exam-open-btn:hover{ background:#E9DEF7; }
  .hub-topbar .hub-actions{ display:inline-flex; align-items:center; gap:8px; }
  .hub-exam{ position:relative; display:inline-flex; align-items:center; gap:4px; min-height:30px; padding:0 11px; border-radius:100px;
    border:1px solid #E3B95C; background:rgba(227,185,92,.16); color:#F5F0E1; font-family:inherit; font-weight:700; font-size:.82rem; line-height:1; cursor:pointer; }
  .hub-exam::after{ content:""; position:absolute; inset:-8px -4px; }
  .hub-exam:focus-visible{ outline:3px solid #E3B95C; outline-offset:2px; }

  .xm{ position:fixed; inset:0; z-index:80; background:#F7F3EA; overflow-y:auto; -webkit-overflow-scrolling:touch; direction:rtl;
    font-family:'Assistant', system-ui, 'Arial Hebrew', Arial, sans-serif; color:#1F2A47; }
  .xm[hidden]{ display:none; }
  body.xm-on{ overflow:hidden; }
  .xm-bar{ position:sticky; top:0; z-index:2; display:flex; align-items:center; justify-content:space-between; gap:10px; min-height:52px;
    padding:0 max(14px, env(safe-area-inset-right,0px)); background:#4B2A78; color:#fff; }
  .xm-bar h2{ margin:0; font-size:1.08rem; font-weight:800; color:#fff; }
  .xm-x{ min-width:44px; min-height:44px; border:0; background:transparent; color:#fff; font-size:1.3rem; cursor:pointer; border-radius:10px; }
  .xm-x:focus-visible, .xm-refresh:focus-visible{ outline:3px solid #E3B95C; }
  .xm-bar-btns{ display:flex; align-items:center; gap:6px; }
  .xm-refresh{ min-height:36px; padding:0 12px; border-radius:100px; border:1px solid rgba(255,255,255,.35); background:rgba(255,255,255,.1);
    color:#fff; font-family:inherit; font-weight:700; font-size:.9rem; cursor:pointer; }
  .xm-in{ max-width:760px; margin:0 auto; padding:16px 16px 90px; }
  .xm-card{ background:#fff; border:1px solid #E4DCCB; border-radius:16px; padding:16px; margin:0 0 14px; }
  .xm-card h3{ margin:0 0 10px; font-size:1.02rem; font-weight:800; color:#4B2A78; }
  .xm-sub{ margin:0 0 6px; color:#4A5578; line-height:1.6; font-size:.95rem; }
  .xm-row{ display:flex; flex-wrap:wrap; align-items:center; gap:8px; }
  .xm-seg{ display:inline-flex; flex-wrap:wrap; gap:6px; }
  .xm-seg button, .xm-chip{ min-height:40px; padding:0 14px; border-radius:100px; border:1.5px solid #CFC3E3; background:#fff; color:#4B2A78;
    font-family:inherit; font-weight:700; font-size:.92rem; cursor:pointer; }
  .xm-seg button[aria-pressed="true"]{ background:#6B3FA0; border-color:#6B3FA0; color:#fff; }
  .xm-num{ width:72px; min-height:40px; border:1.5px solid #CFC3E3; border-radius:10px; font:inherit; font-weight:700; text-align:center; font-size:1rem; }
  .xm-unit{ margin:12px 0 4px; font-weight:800; color:#1F2A47; font-size:.95rem; }
  .xm-topic{ display:flex; align-items:center; justify-content:space-between; gap:10px; padding:8px 0; border-top:1px solid #F0EADF; }
  .xm-topic span{ line-height:1.45; font-size:.93rem; }
  .xm-topic small{ color:#7A84A0; white-space:nowrap; }
  .xm-topic select{ min-height:38px; border:1.5px solid #CFC3E3; border-radius:10px; font:inherit; font-size:.9rem; background:#fff; color:#1F2A47; max-width:44%; }
  .xm-files label, .xm-check{ display:flex; align-items:center; gap:8px; min-height:38px; font-size:.95rem; }
  .xm-files input, .xm-check input{ width:20px; height:20px; accent-color:#6B3FA0; flex:none; }
  .xm-files label{ align-items:flex-start; padding:6px 0; line-height:1.45; }
  .xm-files label input{ margin-top:3px; }
  .xm-about{ display:block; color:#4A5578; font-size:.85rem; margin-top:2px; }
  .xm-go{ display:block; width:100%; min-height:52px; border:0; border-radius:14px; background:#6B3FA0; color:#fff; font-family:inherit;
    font-weight:800; font-size:1.08rem; cursor:pointer; margin-top:6px; }
  .xm-go:disabled{ opacity:.5; cursor:default; }
  .xm-go.alt{ background:#fff; color:#4B2A78; border:2px solid #6B3FA0; }
  .xm-note{ background:#FFF7E3; border:1px solid #EBCB7E; border-radius:12px; padding:10px 12px; margin:0 0 12px; line-height:1.6; font-size:.93rem; }
  .xm-note:empty{ display:none; }
  .xm-link{ border:0; background:none; color:#6B3FA0; font:inherit; font-weight:700; text-decoration:underline; cursor:pointer; padding:4px 2px; min-height:32px; }
  .xm-done-list{ margin:8px 0 0; padding:0; list-style:none; }
  .xm-done-list li{ display:flex; justify-content:space-between; align-items:center; gap:8px; padding:6px 0; border-top:1px solid #F0EADF; font-size:.9rem; }
  .xm-q{ background:#fff; border:2px solid #CFC3E3; border-radius:16px; padding:14px; margin:0 0 16px; }
  .xm-q-h{ display:flex; flex-wrap:wrap; align-items:center; gap:8px; margin:0 0 8px; }
  .xm-q-h b{ font-size:1.05rem; color:#4B2A78; }
  .xm-tag{ display:inline-block; padding:2px 10px; border-radius:100px; font-size:.8rem; font-weight:700; background:#F1F2F5; color:#4A5578; }
  .xm-lv-1{ background:#E3F2EE; color:#1E6B57; } .xm-lv-2{ background:#FBF0DC; color:#8A5A0B; } .xm-lv-3{ background:#F8E4E1; color:#A23F35; }
  .xm-q .box.sample{ margin:6px 0 0 !important; border:0 !important; box-shadow:none !important; padding:0 !important; background:transparent !important; }
  .xm-q .box.sample > .box-title{ display:none; }
  .xm-q .box.sample::before{ display:none !important; }
  .xm-src{ color:#7A84A0; font-size:.85rem; }
  .xm-mark{ display:flex; align-items:center; gap:8px; margin:12px 0 0; padding-top:10px; border-top:1px dashed #E4DCCB; font-weight:700; font-size:.93rem; }
  .xm-mark input{ width:22px; height:22px; accent-color:#2E7D5B; }
  .xm-toast{ position:fixed; bottom:20px; left:50%; transform:translateX(-50%); z-index:90; background:#1F2A47; color:#fff; padding:12px 18px;
    border-radius:12px; font-weight:700; max-width:90vw; text-align:center; }
  /* סימון באתר עצמו */
  .xm-badges{ display:inline-flex; flex-wrap:wrap; align-items:center; gap:6px; margin-inline-start:8px; vertical-align:middle; }
  .xm-done-badge{ display:inline-flex; align-items:center; gap:4px; padding:2px 10px; border-radius:100px; background:#E3F2EE; color:#1E6B57; font-size:.8rem; font-weight:800; }
  .xm-done-badge button{ border:0; background:none; color:#1E6B57; text-decoration:underline; font:inherit; font-weight:700; cursor:pointer; padding:0 2px; }
  /* ===== הדפסה / שמירה כ-PDF: רק השאלות, בלי פתרונות ===== */
  .xm-print{ display:none; }
  .xm-pdf-row{ display:flex; flex-wrap:wrap; gap:10px; margin:16px 0 22px; }
  .xm-pdf-row .xm-go{ flex:1 1 220px; margin:0; padding:8px 16px; line-height:1.35; }
  .xm-pdf-note{ margin:-10px 0 20px; }
  .xm-pdf-note[hidden]{ display:none; }
  @media print{
    @page{ size:A4; margin:16mm 14mm; }
    body.xm-printing{ overflow:visible !important; background:#fff !important; }
    body.xm-printing > *:not(#xmPrint){ display:none !important; }
    body.xm-printing #xmPrint{ display:block !important; direction:rtl; color:#000; font-size:12pt; line-height:1.65; }
    .xm-print h1{ font-size:17pt; margin:0 0 2px; }
    .xm-print .xp-meta{ color:#444; font-size:10pt; margin:0 0 10px; padding-bottom:8px; border-bottom:1.5px solid #000; }
    .xm-print .xp-q{ break-inside:avoid; page-break-inside:avoid; padding:10px 0 0; margin:0 0 6px; }
    .xm-print .xp-q h2{ font-size:13pt; margin:0 0 4px; }
    .xm-print .xp-space{ height:3.2cm; border-bottom:1px dashed #aaa; }
    .xm-print .box, .xm-print .box.sample{ border:0 !important; box-shadow:none !important; padding:0 !important; margin:0 !important; background:none !important; }
    .xm-print .box::before{ display:none !important; }
    .xm-print svg, .xm-print img{ max-width:100%; }
  }
</style>
<div class="xm-print" id="xmPrint" aria-hidden="true"></div>
<div class="xm" id="examApp" hidden role="dialog" aria-modal="true" aria-labelledby="xmTitle">
  <div class="xm-bar"><h2 id="xmTitle">📝 מחולל מבחנים</h2><div class="xm-bar-btns"><button type="button" class="xm-refresh" id="xmRefresh" aria-label="רענון: טעינת הגרסה העדכנית של האתר">↻ רענון</button><button type="button" class="xm-x" id="xmClose" aria-label="סגירה">✕</button></div></div>
  <div class="xm-in" id="xmBody"></div>
</div>
<script>
(function(){
  try {
  var PATH = location.pathname.replace(/index\.html$/, '');
  var K_DONE = 'mathExamDone_v1:' + PATH, K_CUR = 'mathExamCur_v1:' + PATH, K_SET = 'mathExamSet_v1:' + PATH;
  var LV = {1:'קלה', 2:'בינונית', 3:'קשה'};
  function load(k, d){ try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch(e){ return d; } }
  function save(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function txt(el){ if(!el) return ''; var c = el.cloneNode(true); c.querySelectorAll('annotation').forEach(function(a){ a.remove(); }); return c.textContent.replace(/\s+/g,' ').trim(); }

  // ---------- 1. כל השאלות מהדף ----------
  var Q = [], byId = {}, topics = [], tById = {}, unit = '', topic = null;
  document.querySelectorAll('section.exercise .ex-title, h2[id], .box.sample').forEach(function(el){
    if(el.classList.contains('ex-title')){ unit = txt(el); return; }
    if(el.tagName === 'H2'){
      if(!/^ex\d+-p\d+$/.test(el.id)) return;
      topic = {id: el.id, name: txt(el).replace(/^חלק\s*\d+\s*[-–]\s*/, ''), unit: unit, qs: []};
      topics.push(topic); tById[topic.id] = topic; return;
    }
    if(el.closest('.xm') || !el.closest('section.exercise') || !el.querySelector('.sample-sol')) return;
    if(!topic){ topic = {id:'all', name:'כללי', unit: unit, qs: []}; topics.push(topic); tById.all = topic; }
    var srcEl = el.querySelector('.sample-src'), src = '';
    if(srcEl){ var c = srcEl.cloneNode(true); var n = c.querySelector('.sample-num'); if(n) n.remove(); src = txt(c).replace(/^📍\s*/, ''); }
    var file = (src.split(' · ')[0] || 'קובץ').replace(/^תרגול נוסף ל/, '');
    var sol = el.querySelector('.sample-sol');
    var score = sol ? sol.querySelectorAll('.sol-step').length * 3 + sol.querySelectorAll('.sol-line, .formula, .mline, .kv-row, .fl-row').length * 0.6 + txt(el.querySelector('.sample-q')).length / 120 : 1;
    var q = {id: el.id, el: el, topic: topic.id, file: file, src: src, score: score};
    Q.push(q); byId[q.id] = q; topic.qs.push(q);
  });
  if(!Q.length) return;
  // רמה: שלישים לפי היקף הפתרון
  var sorted = Q.slice().sort(function(a,b){ return a.score - b.score; });
  sorted.forEach(function(q, i){ q.level = i < sorted.length / 3 ? 1 : (i < 2 * sorted.length / 3 ? 2 : 3); });
  topics = topics.filter(function(t){ return t.qs.length; });
  var files = []; Q.forEach(function(q){ if(files.indexOf(q.file) < 0) files.push(q.file); });

  var done = load(K_DONE, {});
  function isDone(id){ return !!done[id]; }

  // ---------- 2. סימון בתוך האתר ----------
  function paintSite(){
    Q.forEach(function(q){
      var t = q.el.querySelector('.box-title'); if(!t) return;
      var b = t.querySelector('.xm-badges');
      if(!b){ b = document.createElement('span'); b.className = 'xm-badges'; t.appendChild(b); }
      b.innerHTML = '<span class="xm-tag xm-lv-' + q.level + '">רמה ' + LV[q.level] + '</span>' +
        (isDone(q.id) ? '<span class="xm-done-badge">✓ בוצעה במבחן <button type="button" data-undone="' + q.id + '">ביטול</button></span>' : '');
    });
  }
  document.addEventListener('click', function(e){
    var u = e.target.closest('[data-undone]'); if(!u) return;
    delete done[u.getAttribute('data-undone')]; save(K_DONE, done); paintSite();
    if(!app.hidden) render();
  });

  // ---------- 3. החלון ----------
  var app = document.getElementById('examApp'), body = document.getElementById('xmBody');
  var set = load(K_SET, {n: 6, mode: 'all', level: 0, per: {}, files: {}, incl: false});
  set.mode = 'all';   // רמה אחת לכל המבחן (בלי רמה לפי נושא)
  function open(){ app.hidden = false; document.body.classList.add('xm-on'); render(); app.scrollTop = 0; document.getElementById('xmClose').focus(); }
  function close(){ app.hidden = true; document.body.classList.remove('xm-on'); }
  document.addEventListener('click', function(e){ if(e.target.closest('[data-exam-open]')){ e.preventDefault(); var mt = document.getElementById('menuToggle'); if(mt) mt.checked = false; open(); } });
  document.getElementById('xmClose').addEventListener('click', close);
  // רענון: טוען את הגרסה העדכנית של האתר, ופותח שוב את מחולל המבחנים (המבחן הפתוח שמור)
  document.getElementById('xmRefresh').addEventListener('click', function(){
    try { sessionStorage.setItem('mathExamReopen', '1'); } catch(e){}
    location.replace(location.pathname + '?r=' + Date.now());
  });
  try { if(sessionStorage.getItem('mathExamReopen')){ sessionStorage.removeItem('mathExamReopen'); setTimeout(open, 0); } } catch(e){}
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && !app.hidden) close(); });

  function render(){ var cur = load(K_CUR, null); if(cur && cur.ids && cur.ids.length) renderExam(cur); else renderSetup(''); }

  function levelOf(t){ return set.level || 0; }   // 0 = מעורבת
  function pool(){
    return Q.filter(function(q){
      if(set.files[q.file] === false) return false;
      if(!set.incl && isDone(q.id)) return false;
      var lv = levelOf(tById[q.topic]); if(lv === -1) return false;
      return lv === 0 || q.level === lv;
    });
  }

  // במה הקובץ עוסק, בגדול: שם היחידה שלו - או, כשהיחידה היא בעצם שם הקובץ (מצגת), החלקים שלה
  function fileTopics(f){
    var units = [], parts = [], base = f.replace(/^מצגת\s+/, '');
    Q.forEach(function(q){ if(q.file !== f) return; var t = tById[q.topic];
      if(t.unit && units.indexOf(t.unit) < 0) units.push(t.unit);
      if(t.name && !/^האם AI/.test(t.name) && parts.indexOf(t.name) < 0) parts.push(t.name); });
    var same = units.length && units.every(function(u){ return base.indexOf(u) >= 0 || u.indexOf(base) >= 0; });
    return (same || !units.length ? parts : units).join(', ');
  }

  function renderSetup(msg){
    var doneIds = Object.keys(done).filter(function(id){ return byId[id]; });
    var h = '';
    var cur = load(K_CUR, null);
    h += '<div class="xm-note" id="xmMsg">' + (msg || '') + '</div>';
    h += '<div class="xm-card"><p class="xm-sub">המבחן נבנה מ<b>כל השאלות שבקבצי הקורס</b> באתר: ' + Q.length + ' שאלות מ-' + files.length + ' קבצים. ' +
         'השאלות מתחלקות בין הנושאים ובין הקבצים, ושאלות שכבר ביצעת לא חוזרות.</p>' +
         '<p class="xm-sub">רמת הקושי נקבעת לפי היקף הפתרון: השליש הקצר - קלה, האמצעי - בינונית, הארוך - קשה. הרמה של כל שאלה מופיעה גם ליד השאלה באתר.</p></div>';
    h += '<div class="xm-card"><h3>כמה שאלות?</h3><div class="xm-row"><input class="xm-num" id="xmN" type="number" min="1" max="40" inputmode="numeric" value="' + set.n + '"> <span class="xm-sub" style="margin:0">שאלות</span></div></div>';
    h += '<div class="xm-card"><h3>רמת קושי</h3>';
    h += '<div class="xm-seg" role="group" aria-label="רמה">' + [[1,'קלה'],[2,'בינונית'],[3,'קשה'],[0,'מעורבת']].map(function(o){
      return '<button type="button" data-level="' + o[0] + '" aria-pressed="' + ((set.level || 0) === o[0]) + '">' + o[1] + '</button>'; }).join('') + '</div>';
    h += '</div>';
    h += '<div class="xm-card"><h3>מאילו קבצים?</h3><div class="xm-files">' + files.map(function(f){
      var n = Q.filter(function(q){ return q.file === f; }).length;
      var about = fileTopics(f);
      return '<label><input type="checkbox" data-file="' + esc(f) + '"' + (set.files[f] === false ? '' : ' checked') + '><span><b>' + esc(f) + '</b> <small class="xm-src">(' + n + ' שאלות)</small>' +
        (about ? '<span class="xm-about">(' + esc(about) + ')</span>' : '') + '</span></label>'; }).join('') + '</div></div>';
    h += '<div class="xm-card"><h3>שאלות שכבר ביצעת: ' + doneIds.length + '</h3>' +
         '<label class="xm-check"><input type="checkbox" id="xmIncl"' + (set.incl ? ' checked' : '') + '> לכלול גם שאלות שכבר ביצעתי</label>';
    if(doneIds.length){
      h += '<button type="button" class="xm-link" id="xmShowDone">הצגת הרשימה וביטול סימונים</button><ul class="xm-done-list" id="xmDoneList" hidden>' +
        doneIds.map(function(id){ var q = byId[id]; return '<li><span>' + esc(q.src) + ' · <span class="xm-src">' + esc(tById[q.topic].name) + '</span></span><button type="button" class="xm-link" data-undone="' + id + '">ביטול</button></li>'; }).join('') +
        '<li><span></span><button type="button" class="xm-link" id="xmUndoAll">ביטול כל הסימונים</button></li></ul>';
    }
    h += '</div>';
    var p = pool().length;
    h += '<p class="xm-sub" style="text-align:center">יש ' + p + ' שאלות שמתאימות לבחירה</p>';
    h += '<button type="button" class="xm-go" id="xmGo"' + (p ? '' : ' disabled') + '>✨ חוללי מבחן</button>';
    if(cur && cur.ids && cur.ids.length) h += '<button type="button" class="xm-go alt" id="xmResume">חזרה למבחן הפתוח</button>';
    body.innerHTML = h;

    body.querySelectorAll('[data-level]').forEach(function(b){ b.onclick = function(){ set.level = +b.getAttribute('data-level'); save(K_SET, set); renderSetup(''); }; });
    body.querySelectorAll('[data-file]').forEach(function(c){ c.onchange = function(){ set.files[c.getAttribute('data-file')] = c.checked; save(K_SET, set); renderSetup(''); }; });
    document.getElementById('xmIncl').onchange = function(){ set.incl = this.checked; save(K_SET, set); renderSetup(''); };
    document.getElementById('xmN').onchange = function(){ set.n = Math.max(1, Math.min(40, parseInt(this.value, 10) || 6)); save(K_SET, set); };
    var sd = document.getElementById('xmShowDone'); if(sd) sd.onclick = function(){ var l = document.getElementById('xmDoneList'); l.hidden = !l.hidden; };
    var ua = document.getElementById('xmUndoAll'); if(ua) ua.onclick = function(){ done = {}; save(K_DONE, done); paintSite(); renderSetup('כל הסימונים בוטלו - כל השאלות זמינות שוב.'); };
    var rs = document.getElementById('xmResume'); if(rs) rs.onclick = function(){ renderExam(load(K_CUR, null)); };
    document.getElementById('xmGo').onclick = generate;
  }

  function shuffle(a){ for(var i = a.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  // בחירה: סבב בין הנושאים (כל נושא בתורו), ובכל נושא - שאלה מהקובץ שהכי פחות מיוצג עד עכשיו במבחן
  function generate(){
    var n = set.n = Math.max(1, Math.min(40, parseInt(document.getElementById('xmN').value, 10) || 6)); save(K_SET, set);
    var P = pool(), groups = {}, order = [];
    P.forEach(function(q){ if(!groups[q.topic]){ groups[q.topic] = []; order.push(q.topic); } groups[q.topic].push(q); });
    order = shuffle(order); order.forEach(function(t){ shuffle(groups[t]); });
    var pick = [], perFile = {};
    while(pick.length < n){
      var added = false;
      for(var i = 0; i < order.length && pick.length < n; i++){
        var g = groups[order[i]]; if(!g.length) continue;
        g.sort(function(a,b){ return (perFile[a.file] || 0) - (perFile[b.file] || 0); });
        var q = g.shift(); pick.push(q); perFile[q.file] = (perFile[q.file] || 0) + 1; added = true;
      }
      if(!added) break;
    }
    if(!pick.length){ renderSetup('אין שאלות שמתאימות לבחירה. אפשר לשנות רמה, להוסיף קבצים, או לבטל סימונים של שאלות שבוצעו.'); return; }
    pick.sort(function(a,b){ return Q.indexOf(a) - Q.indexOf(b); });   // לפי סדר החומר
    var lvName = set.level ? 'רמה ' + LV[set.level] : 'רמה מעורבת';
    var cur = {ids: pick.map(function(q){ return q.id; }), title: lvName, short: pick.length < n ? n : 0};
    save(K_CUR, cur); renderExam(cur);
  }

  function cloneQ(q, k){
    var html = q.el.outerHTML, ids = [];
    html.replace(/\sid="([^"]+)"/g, function(m, id){ ids.push(id); return m; });
    ids.forEach(function(id){
      var e = id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      html = html.replace(new RegExp('(id|aria-controls|for)="' + e + '"', 'g'), '$1="xm' + k + '-' + id + '"').replace(new RegExp('#' + e + '([)"\'])', 'g'), '#xm' + k + '-' + id + '$1');
    });
    var d = document.createElement('div'); d.innerHTML = html;
    var box = d.firstElementChild;
    box.querySelectorAll('.xm-badges').forEach(function(b){ b.remove(); });
    box.querySelectorAll('.sample-sol').forEach(function(s){ s.hidden = true; });
    box.querySelectorAll('.sample-btn').forEach(function(b){
      b.setAttribute('aria-expanded', 'false');
      b.addEventListener('click', function(){ var s = document.getElementById(b.getAttribute('aria-controls')); if(!s) return;
        var open = b.getAttribute('aria-expanded') === 'true'; b.setAttribute('aria-expanded', String(!open)); s.hidden = open; });
    });
    return box;
  }

  function printExam(cur, qs){
    var pr = document.getElementById('xmPrint'); if(!pr) return;
    if(pr.parentNode !== document.body) document.body.appendChild(pr);
    var site = document.title.replace(/^מדריך למבחן\s*-?\s*/, '');
    var d = new Date(), date = d.getDate() + '.' + (d.getMonth() + 1) + '.' + d.getFullYear();
    pr.innerHTML = '<h1>מבחן · ' + esc(site.trim()) + '</h1><div class="xp-meta">' + qs.length + ' שאלות · ' + esc(cur.title) + ' · ' + date + '</div>';
    qs.forEach(function(q, k){
      var w = document.createElement('div'); w.className = 'xp-q';
      w.innerHTML = '<h2>שאלה ' + (k + 1) + '</h2>';
      var box = cloneQ(q, 'p' + k);
      box.querySelectorAll('.box-title, .sample-btn, .sample-hint, .sample-sol, .sample-src, .xm-badges').forEach(function(x){ x.remove(); });
      w.appendChild(box);
      var sp = document.createElement('div'); sp.className = 'xp-space'; w.appendChild(sp);
      pr.appendChild(w);
    });
    var oldTitle = document.title, opened = false;
    document.title = 'מבחן - ' + site.trim() + ' - ' + date;
    document.body.classList.add('xm-printing');
    function before(){ opened = true; }
    function after(){ document.body.classList.remove('xm-printing'); document.title = oldTitle; window.removeEventListener('afterprint', after); window.removeEventListener('beforeprint', before); }
    window.addEventListener('beforeprint', before);
    window.addEventListener('afterprint', after);
    var note = document.getElementById('xmPdfNote');
    var how = 'אם חלון ההדפסה לא נפתח: באייפון - לחצי על כפתור השיתוף של ספארי (הריבוע עם החץ) ← "הדפסה", ושם על כפתור השיתוף ← "שמירה בקבצים". במחשב - Ctrl+P (או ⌘+P) ובחרי "שמירה כ-PDF". יודפסו רק השאלות, בלי הפתרונות.';
    if(window.navigator.standalone){
      // באפליקציה ממסך הבית אין לאייפון הדפסה בכלל
      if(note){ note.textContent = 'בגרסה שנפתחת ממסך הבית אין לאייפון אפשרות הדפסה - השתמשי בכפתור "📤 קובץ PDF לשיתוף".'; note.hidden = false; }
      after(); return;
    }
    // חייב לקרות מיד בלחיצה - אחרת ספארי באייפון חוסם את חלון ההדפסה
    try { window.print(); } catch(e){}
    setTimeout(function(){ if(!opened){ document.title = oldTitle; if(note){ note.textContent = how; note.hidden = false; } } }, 1500);
  }

  // ---------- קובץ PDF אמיתי (גם באפליקציה ממסך הבית, שבה אין הדפסה) ----------
  // השאלות הן תמונות שהוכנו מראש (tools/exam_images.js); הכותרות מצוירות כאן; הקובץ נבנה בלי ספריות.
  var IMG_INFO = null;
  function getInfo(){
    if(IMG_INFO) return Promise.resolve(IMG_INFO);
    return fetch('exam-img/index.json', {cache: 'no-cache'}).then(function(r){ if(!r.ok) throw new Error('index'); return r.json(); }).then(function(j){ IMG_INFO = j; return j; });
  }
  function b64bytes(d){ var s = atob(d.split(',')[1]), a = new Uint8Array(s.length); for(var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
  function textImg(lines){   // lines: [[text, px, bold, color]] -> jpeg {bytes,w,h}; 1360px = רוחב התוכן
    var W = 1360, pad = 6, H = pad * 2;
    lines.forEach(function(l){ H += Math.round(l[1] * 1.45); });
    var c = document.createElement('canvas'); c.width = W; c.height = H;
    var g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
    g.direction = 'rtl'; g.textAlign = 'right'; g.textBaseline = 'top';
    var y = pad;
    lines.forEach(function(l){ g.font = (l[2] ? '700 ' : '400 ') + l[1] + "px Assistant, 'Arial Hebrew', Arial, sans-serif"; g.fillStyle = l[3] || '#1F2A47'; g.fillText(l[0], W - 2, y + l[1] * 0.12); y += Math.round(l[1] * 1.45); });
    return {bytes: b64bytes(c.toDataURL('image/jpeg', 0.9)), w: W, h: H};
  }
  function makePdf(pages){   // pages: [[{img, x, y, w, h} | {line:[x1,y1,x2,y2]}]] - נקודות, y מלמעלה
    var enc = new TextEncoder(), parts = [], off = 0, offs = [], imgs = [], n;
    function push(x){ var b = typeof x === 'string' ? enc.encode(x) : x; parts.push(b); off += b.length; }
    pages.forEach(function(pg){ pg.forEach(function(it){ if(it.img && imgs.indexOf(it.img) < 0) imgs.push(it.img); }); });
    var firstImg = 3, firstPage = firstImg + imgs.length, total = firstPage + pages.length * 2 - 1;
    push(new Uint8Array([37, 80, 68, 70, 45, 49, 46, 52, 10, 37, 226, 227, 207, 211, 10]));
    function obj(k, body){ offs[k] = off; push(k + ' 0 obj\n' + body + '\nendobj\n'); }
    obj(1, '<< /Type /Catalog /Pages 2 0 R >>');
    var kids = pages.map(function(_, i){ return (firstPage + i * 2) + ' 0 R'; }).join(' ');
    obj(2, '<< /Type /Pages /Kids [' + kids + '] /Count ' + pages.length + ' >>');
    imgs.forEach(function(im, i){
      n = firstImg + i; offs[n] = off;
      push(n + ' 0 obj\n<< /Type /XObject /Subtype /Image /Width ' + im.w + ' /Height ' + im.h + ' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ' + im.bytes.length + ' >>\nstream\n');
      push(im.bytes); push('\nendstream\nendobj\n');
    });
    pages.forEach(function(pg, i){
      var res = [], cs = '';
      pg.forEach(function(it){
        if(it.img){ var k = imgs.indexOf(it.img); if(res.indexOf(k) < 0) res.push(k);
          cs += 'q ' + it.w.toFixed(2) + ' 0 0 ' + it.h.toFixed(2) + ' ' + it.x.toFixed(2) + ' ' + (842 - it.y - it.h).toFixed(2) + ' cm /Im' + k + ' Do Q\n'; }
        else if(it.line){ var L = it.line; cs += 'q 0.62 0.62 0.62 RG 0.6 w ' + (it.dash ? '[3 3] 0 d ' : '') + L[0] + ' ' + (842 - L[1]) + ' m ' + L[2] + ' ' + (842 - L[3]) + ' l S Q\n'; }
      });
      var pn = firstPage + i * 2, cn = pn + 1;
      obj(pn, '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /XObject << ' +
        res.map(function(k){ return '/Im' + k + ' ' + (firstImg + k) + ' 0 R'; }).join(' ') + ' >> >> /Contents ' + cn + ' 0 R >>');
      var cb = enc.encode(cs); offs[cn] = off;
      push(cn + ' 0 obj\n<< /Length ' + cb.length + ' >>\nstream\n'); push(cb); push('\nendstream\nendobj\n');
    });
    var xo = off, x = 'xref\n0 ' + (total + 1) + '\n0000000000 65535 f \n';
    for(var k = 1; k <= total; k++) x += ('0000000000' + offs[k]).slice(-10) + ' 00000 n \n';
    push(x + 'trailer\n<< /Size ' + (total + 1) + ' /Root 1 0 R >>\nstartxref\n' + xo + '\n%%EOF\n');
    return new Blob(parts, {type: 'application/pdf'});
  }
  function buildPdf(cur, qs){
    return getInfo().then(function(info){
      return Promise.all(qs.map(function(q){
        return fetch('exam-img/' + q.id + '.jpg').then(function(r){ if(!r.ok) throw new Error(q.id); return r.arrayBuffer(); })
          .then(function(b){ var sz = info.q[q.id] || [1360, 200]; return {bytes: new Uint8Array(b), w: sz[0], h: sz[1]}; });
      }));
    }).then(function(imgs){
      var site = document.title.replace(/^מדריך למבחן\s*-?\s*/, '').trim();
      var d = new Date(), date = d.getDate() + '.' + (d.getMonth() + 1) + '.' + d.getFullYear();
      var X = 40, CW = 515, TOP = 40, BOT = 802, k = CW / 1360;
      var pages = [[]], pg = pages[0], y = TOP;
      var head = textImg([['מבחן · ' + site, 40, true], [qs.length + ' שאלות · ' + cur.title + ' · ' + date, 26, false, '#555']]);
      pg.push({img: head, x: X, y: y, w: CW, h: head.h * k}); y += head.h * k + 4;
      pg.push({line: [X, y, X + CW, y]}); y += 12;
      imgs.forEach(function(im, i){
        var lab = textImg([['שאלה ' + (i + 1), 32, true]]);
        var lh = lab.h * k, w = CW, h = im.h * k;
        if(h > BOT - TOP - lh){ var f = (BOT - TOP - lh) / h; w *= f; h *= f; }
        if(y + lh + h > BOT){ pg = []; pages.push(pg); y = TOP; }
        pg.push({img: lab, x: X, y: y, w: CW, h: lh}); y += lh + 2;
        pg.push({img: im, x: X + CW - w, y: y, w: w, h: h}); y += h;
        var space = Math.min(110, BOT - y);
        y += space;
        if(space > 20) pg.push({line: [X, y - 6, X + CW, y - 6], dash: true});
        y += 8;
      });
      var name = 'מבחן - ' + site + ' - ' + date + '.pdf';
      return {blob: makePdf(pages), name: name};
    });
  }
  function sharePdf(cur, qs, btn){
    var note = document.getElementById('xmPdfNote');
    function say(t){ if(note){ note.textContent = t; note.hidden = !t; } }
    if(btn._file){ return deliver(btn._file); }
    var label = btn.textContent; btn.disabled = true; btn.textContent = '⏳ מכינה את הקובץ...'; say('');
    buildPdf(cur, qs).then(function(r){
      var file = null;
      try { file = new File([r.blob], r.name, {type: 'application/pdf'}); } catch(e){}
      btn._file = file || r.blob; btn._name = r.name; btn.disabled = false; btn.textContent = '📤 שיתוף הקובץ';
      deliver(btn._file);
    }).catch(function(e){ btn.disabled = false; btn.textContent = label; say('לא הצלחתי להכין את הקובץ. בדקי שיש חיבור לאינטרנט ונסי שוב.'); if(window.console) console.error('exam pdf', e); });
    function deliver(f){
      if(f instanceof File && navigator.canShare && navigator.canShare({files: [f]})){
        navigator.share({files: [f], title: btn._name}).then(function(){ say(''); }).catch(function(e){
          if(e && e.name === 'AbortError') return;
          say('הקובץ מוכן - לחצי על "📤 שיתוף הקובץ" כדי לשמור או לשלוח אותו.');
        });
        return;
      }
      var url = URL.createObjectURL(f), a = document.createElement('a');
      a.href = url; a.download = btn._name || 'exam.pdf'; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function(){ URL.revokeObjectURL(url); }, 60000);
      say('הקובץ ירד למכשיר (בתיקיית ההורדות).');
    }
  }

  function renderExam(cur){
    var qs = cur.ids.map(function(id){ return byId[id]; }).filter(Boolean);
    var h = '<div class="xm-note">' + (cur.short ? 'ביקשת ' + cur.short + ' שאלות, אבל נמצאו רק ' + qs.length + ' שמתאימות לבחירה (בלי שאלות שכבר ביצעת).' : '') + '</div>';
    h += '<div class="xm-card"><h3>מבחן · ' + qs.length + ' שאלות · ' + esc(cur.title) + '</h3><p class="xm-sub">פתרי כל שאלה לבד, ורק אחר כך פתחי את הפתרון. בסוף לחצי "סיימתי" - השאלות המסומנות ב-✓ לא יופיעו במבחנים הבאים.</p></div>';
    var standalone = !!window.navigator.standalone || (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches);
    h += '<div class="xm-pdf-row"><button type="button" class="xm-go alt" id="xmShare">📤 קובץ PDF לשיתוף - בלי פתרונות</button>' +
         (standalone ? '' : '<button type="button" class="xm-go alt" id="xmPdf">🖨️ הדפסה - בלי פתרונות</button>') + '</div>' +
         '<p class="xm-note xm-pdf-note" id="xmPdfNote" hidden></p>';
    body.innerHTML = h;
    var pb = document.getElementById('xmPdf'); if(pb) pb.onclick = function(){ printExam(cur, qs); };
    document.getElementById('xmShare').onclick = function(){ sharePdf(cur, qs, this); };
    qs.forEach(function(q, k){
      var t = tById[q.topic];
      var card = document.createElement('div'); card.className = 'xm-q';
      card.innerHTML = '<div class="xm-q-h"><b>שאלה ' + (k + 1) + '</b><span class="xm-tag xm-lv-' + q.level + '">רמה ' + LV[q.level] + '</span><span class="xm-tag">' + esc(t.name) + '</span></div>' +
        '<div class="xm-src">📍 ' + esc(q.src) + '</div>';
      card.appendChild(cloneQ(q, k));
      var m = document.createElement('label'); m.className = 'xm-mark';
      m.innerHTML = '<input type="checkbox" data-q="' + q.id + '" checked> ביצעתי את השאלה הזו';
      card.appendChild(m);
      body.appendChild(card);
    });
    var f = document.createElement('div');
    f.innerHTML = '<button type="button" class="xm-go" id="xmFinish">✅ סיימתי - לסמן את השאלות שביצעתי</button>' +
                  '<button type="button" class="xm-go alt" id="xmBack">חזרה להגדרות (המבחן נשמר)</button>' +
                  '<button type="button" class="xm-go alt" id="xmDrop">ביטול המבחן בלי לסמן</button>';
    body.appendChild(f);
    document.getElementById('xmFinish').onclick = function(){
      var c = 0;
      body.querySelectorAll('input[data-q]').forEach(function(i){ if(i.checked){ done[i.getAttribute('data-q')] = Date.now(); c++; } });
      save(K_DONE, done); save(K_CUR, null); paintSite();
      renderSetup('✓ סימנתי ' + c + ' שאלות כבוצעו. הן מסומנות גם באתר עצמו, ולא יופיעו במבחנים הבאים (אלא אם תבטלי את הסימון).');
      app.scrollTop = 0;
    };
    document.getElementById('xmBack').onclick = function(){ renderSetup(''); app.scrollTop = 0; };
    document.getElementById('xmDrop').onclick = function(){ save(K_CUR, null); renderSetup('המבחן בוטל. אף שאלה לא סומנה.'); app.scrollTop = 0; };
  }

  paintSite();
  } catch(err){ if(window.console) console.error('exam', err); }
})();
</script>
<!-- exam:end -->
"""


def ensure_exam(page, put_between):
    """adds the exam generator (styles, window, script) + its two buttons; idempotent"""
    def add(pg, block):
        i = pg.rindex('</body>')
        return pg[:i] + block + pg[i:]
    page = put_between(page, '<!-- exam:start -->', '<!-- exam:end -->', EXAM_ASSETS, add)
    if 'data-exam-open>📝 מחולל מבחנים' not in page and 'data-ai-open>' in page:
        i = page.index('</button>', page.index('data-ai-open>')) + len('</button>')
        page = page[:i] + '\n    ' + EXAM_BTN_SIDEBAR + page[i:]
    return page
