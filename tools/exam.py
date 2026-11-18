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
  .xm-x:focus-visible{ outline:3px solid #E3B95C; }
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
  .xm-files input, .xm-check input{ width:20px; height:20px; accent-color:#6B3FA0; }
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
  .xm-go.xm-pdf{ margin:16px 0 22px; padding:8px 16px; line-height:1.35; }
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
  <div class="xm-bar"><h2 id="xmTitle">📝 מחולל מבחנים</h2><button type="button" class="xm-x" id="xmClose" aria-label="סגירה">✕</button></div>
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
  function open(){ app.hidden = false; document.body.classList.add('xm-on'); render(); app.scrollTop = 0; document.getElementById('xmClose').focus(); }
  function close(){ app.hidden = true; document.body.classList.remove('xm-on'); }
  document.addEventListener('click', function(e){ if(e.target.closest('[data-exam-open]')){ e.preventDefault(); var mt = document.getElementById('menuToggle'); if(mt) mt.checked = false; open(); } });
  document.getElementById('xmClose').addEventListener('click', close);
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && !app.hidden) close(); });

  function render(){ var cur = load(K_CUR, null); if(cur && cur.ids && cur.ids.length) renderExam(cur); else renderSetup(''); }

  function levelOf(t){ return set.mode === 'all' ? (set.level || 0) : (set.per[t.id] == null ? 0 : +set.per[t.id]); }   // -1 = לא לכלול, 0 = מעורבת
  function pool(){
    return Q.filter(function(q){
      if(set.files[q.file] === false) return false;
      if(!set.incl && isDone(q.id)) return false;
      var lv = levelOf(tById[q.topic]); if(lv === -1) return false;
      return lv === 0 || q.level === lv;
    });
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
    h += '<div class="xm-card"><h3>רמת קושי</h3><div class="xm-seg" role="group" aria-label="איך לקבוע רמה">' +
         '<button type="button" data-mode="all" aria-pressed="' + (set.mode === 'all') + '">רמה אחת לכל המבחן</button>' +
         '<button type="button" data-mode="per" aria-pressed="' + (set.mode === 'per') + '">רמה לכל נושא</button></div>';
    if(set.mode === 'all'){
      h += '<div class="xm-seg" style="margin-top:10px" role="group" aria-label="רמה">' + [[1,'קלה'],[2,'בינונית'],[3,'קשה'],[0,'מעורבת']].map(function(o){
        return '<button type="button" data-level="' + o[0] + '" aria-pressed="' + ((set.level || 0) === o[0]) + '">' + o[1] + '</button>'; }).join('') + '</div>';
    } else {
      var lastUnit = null;
      topics.forEach(function(t){
        if(t.unit !== lastUnit){ h += '<div class="xm-unit">' + esc(t.unit) + '</div>'; lastUnit = t.unit; }
        var v = levelOf(t), left = t.qs.filter(function(q){ return set.incl || !isDone(q.id); }).length;
        h += '<label class="xm-topic"><span>' + esc(t.name) + ' <small>(' + left + ' שאלות)</small></span><select data-topic="' + t.id + '">' +
             [[-1,'לא לכלול'],[0,'מעורבת'],[1,'קלה'],[2,'בינונית'],[3,'קשה']].map(function(o){ return '<option value="' + o[0] + '"' + (v === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') +
             '</select></label>';
      });
      h += '<div class="xm-row" style="margin-top:8px"><button type="button" class="xm-link" data-allper="0">הכול מעורבת</button><button type="button" class="xm-link" data-allper="-1">ניקוי - אף נושא</button></div>';
    }
    h += '</div>';
    h += '<div class="xm-card"><h3>מאילו קבצים?</h3><div class="xm-files">' + files.map(function(f){
      var n = Q.filter(function(q){ return q.file === f; }).length;
      return '<label><input type="checkbox" data-file="' + esc(f) + '"' + (set.files[f] === false ? '' : ' checked') + '> ' + esc(f) + ' <small class="xm-src">(' + n + ')</small></label>'; }).join('') + '</div></div>';
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

    body.querySelectorAll('[data-mode]').forEach(function(b){ b.onclick = function(){ set.mode = b.getAttribute('data-mode'); save(K_SET, set); renderSetup(''); }; });
    body.querySelectorAll('[data-level]').forEach(function(b){ b.onclick = function(){ set.level = +b.getAttribute('data-level'); save(K_SET, set); renderSetup(''); }; });
    body.querySelectorAll('select[data-topic]').forEach(function(s){ s.onchange = function(){ set.per[s.getAttribute('data-topic')] = +s.value; save(K_SET, set); renderSetup(''); }; });
    body.querySelectorAll('[data-allper]').forEach(function(b){ b.onclick = function(){ var v = +b.getAttribute('data-allper'); topics.forEach(function(t){ set.per[t.id] = v; }); save(K_SET, set); renderSetup(''); }; });
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
    var lvName = set.mode === 'all' ? (set.level ? 'רמה ' + LV[set.level] : 'רמה מעורבת') : 'רמה לפי נושא';
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
      if(note){ note.textContent = 'בגרסה שנפתחת ממסך הבית אין לאייפון אפשרות הדפסה. פתחי את האתר בספארי, צרי את המבחן ולחצי שוב על הכפתור.'; note.hidden = false; }
      after(); return;
    }
    // חייב לקרות מיד בלחיצה - אחרת ספארי באייפון חוסם את חלון ההדפסה
    try { window.print(); } catch(e){}
    setTimeout(function(){ if(!opened){ document.title = oldTitle; if(note){ note.textContent = how; note.hidden = false; } } }, 1500);
  }

  function renderExam(cur){
    var qs = cur.ids.map(function(id){ return byId[id]; }).filter(Boolean);
    var h = '<div class="xm-note">' + (cur.short ? 'ביקשת ' + cur.short + ' שאלות, אבל נמצאו רק ' + qs.length + ' שמתאימות לבחירה (בלי שאלות שכבר ביצעת).' : '') + '</div>';
    h += '<div class="xm-card"><h3>מבחן · ' + qs.length + ' שאלות · ' + esc(cur.title) + '</h3><p class="xm-sub">פתרי כל שאלה לבד, ורק אחר כך פתחי את הפתרון. בסוף לחצי "סיימתי" - השאלות המסומנות ב-✓ לא יופיעו במבחנים הבאים.</p></div>';
    h += '<button type="button" class="xm-go alt xm-pdf" id="xmPdf">📄 שמירה כ-PDF - בלי פתרונות</button>' +
         '<p class="xm-note xm-pdf-note" id="xmPdfNote" hidden></p>';
    body.innerHTML = h;
    document.getElementById('xmPdf').onclick = function(){ printExam(cur, qs); };
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
