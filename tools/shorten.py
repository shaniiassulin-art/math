# -*- coding: utf-8 -*-
"""קיצור מצגת - עמוד נפרד (#shorten) באתר החומר התיאורטי (build_hub.py קורא ל-ensure_shorten).

מעלים PDF של מצגת, והדף מוצא שקפים שכל התוכן שלהם (טקסט, נוסחאות, צבעים והדגשות) מופיע בדיוק כך בשקף מאוחר יותר:
שלבי ביניים של אנימציה וכפילויות. שקף שיש בו משהו ייחודי - אפילו הדגשה בצבע אחר - נשאר.
אפשר לשנות כל החלטה ביד. הייצוא מעתיק את השקפים שנשארו מה-PDF המקורי כמו שהם (pdf-lib), בלי לערוך אותם.
המצגות המקוצרות נשמרות במכשיר (IndexedDB) ואפשר לפתוח ולייצא אותן שוב.
"""

SHORTEN_ASSETS = r"""<!-- shorten:start -->
<style>
  body:not(.shorten-mode) .shorten-section{ display:none; }
  body.shorten-mode .shorten-host > *:not(.shorten-section){ display:none !important; }
  .shorten-section h2{ margin-top:0; }
  .sh-back{ display:inline-flex; align-items:center; min-height:44px; margin:0 0 18px; padding:0 16px; border-radius:100px;
    border:1.5px solid var(--line, #E4DCCB); background:#fff; color:var(--indigo-2, #1F2A47); font-family:inherit; font-weight:800; font-size:.95rem; cursor:pointer; }
  .sh-card{ margin:14px 0; padding:16px; border-radius:16px; background:#fff; border:1.5px solid var(--line, #E4DCCB); }
  .sh-card h3{ margin:0 0 8px; font-size:1.05rem; }
  .sh-rules{ margin:0; padding-inline-start:20px; color:var(--ink-soft, #4A5578); font-size:.92rem; line-height:1.6; }
  .sh-btn{ min-height:44px; padding:6px 16px; border-radius:12px; border:1.5px solid #6B3FA0; background:#6B3FA0; color:#fff; font-family:inherit; font-weight:800; font-size:.95rem; cursor:pointer; }
  .sh-btn.alt{ background:#fff; color:#6B3FA0; }
  .sh-btn:disabled{ opacity:.55; cursor:wait; }
  .sh-row{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
  .sh-status{ font-weight:700; margin:10px 0; }
  .sh-prog{ width:100%; height:8px; accent-color:#6B3FA0; }
  .sh-grid{ display:grid; grid-template-columns:repeat(auto-fill, minmax(150px, 1fr)); gap:10px; margin-top:12px; }
  .sh-slide{ position:relative; border-radius:10px; border:2.5px solid #2E8B57; background:#fff; padding:4px; cursor:pointer; text-align:right; font-family:inherit; }
  .sh-slide img{ display:block; width:100%; height:auto; border-radius:6px; }
  .sh-slide.out{ border-color:#C9C2B5; opacity:.5; }
  .sh-slide .sh-n{ position:absolute; top:6px; right:6px; background:#1F2A47; color:#fff; border-radius:6px; padding:0 6px; font-size:.78rem; font-weight:800; }
  .sh-slide .sh-why{ display:block; font-size:.75rem; color:#4A5578; margin-top:4px; min-height:1.2em; }
  .sh-slide.out .sh-why{ color:#9B2C2C; }
  .sh-saved li{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; padding:8px 0; border-bottom:1px solid #EEE7D9; }
  .sh-saved li b{ margin-inline-end:auto; }
  .sh-note{ padding:10px 12px; border-radius:10px; background:#FFF6E0; border:1px solid #EBC877; font-size:.92rem; }
  .sh-note[hidden]{ display:none; }
  .sidebar .shorten-open-btn{ display:flex; align-items:center; justify-content:center; width:100%; min-height:46px; margin:0 0 10px !important; border-radius:12px; box-sizing:border-box;
    padding:8px 12px; border:1.5px solid rgba(255,255,255,.3); background:rgba(255,255,255,.1); color:#fff; font-weight:800; font-size:.95rem; text-decoration:none; }
</style>
<section class="shorten-section" id="shorten" aria-labelledby="shTitle">
  <h2 id="shTitle">✂️ קיצור מצגת</h2>
  <p>מעלים מצגת (PDF), והאתר מוחק רק שקפים מיותרים: שלבי ביניים וכפילויות שכל התוכן שלהם מופיע בשקף אחר שנשאר. השקפים שנשארים לא משתנים בכלל.</p>
  <div class="sh-card"><h3>הכללים</h3><ul class="sh-rules">
    <li>שקף נמחק רק אם <b>כל</b> מה שיש בו - טקסט, נוסחאות, מטריצות, צבעים, סימונים והדגשות - מופיע בדיוק כך בשקף מאוחר יותר שנשאר (למשל השקף המסכם של רצף שלבים).</li>
    <li>אם שני שקפים מראים אותו תרגיל עם הדגשה שונה - שניהם נשארים, אלא אם שקף אחר מראה את שתי ההדגשות יחד.</li>
    <li>אם יש בשקף ביניים משהו שלא מופיע בסיכום - הוא נשאר. בספק - השקף נשאר.</li>
    <li>כל מצגת נשמרת בנפרד. אפשר לבדוק כל החלטה ולשנות אותה בלחיצה על השקף.</li>
  </ul></div>
  <div class="sh-card">
    <div class="sh-row"><label class="sh-btn" for="shFile">📂 בחירת מצגת (PDF)</label><input type="file" id="shFile" accept="application/pdf" hidden></div>
    <div class="sh-status" id="shStatus" aria-live="polite"></div>
    <progress class="sh-prog" id="shProg" max="1" value="0" hidden></progress>
    <div class="sh-row" id="shActions" hidden>
      <button type="button" class="sh-btn" id="shExport">📤 ייצוא המצגת המקוצרת</button>
      <button type="button" class="sh-btn alt" id="shSave">💾 שמירה באתר</button>
      <button type="button" class="sh-btn alt" id="shAll">הצגת כל השקפים</button>
    </div>
    <p class="sh-note" id="shNote" hidden></p>
    <div class="sh-grid" id="shGrid"></div>
  </div>
  <div class="sh-card"><h3>המצגות המקוצרות שלי</h3><ul class="sh-saved" id="shSaved" style="list-style:none;margin:0;padding:0"></ul>
    <p class="sh-note" style="margin-top:10px">המצגות נשמרות באתר <b>במכשיר הזה</b>. כדי שמצגת תיכנס לקבצי הקורס ולתוכן של האתר לכולם - ייצאי אותה ושלחי לי אותה בצ'אט.</p></div>
</section>
<script>
(function(){
  try {
  var sec = document.getElementById('shorten'); if(!sec) return;
  var content = document.getElementById('files') || document.getElementById('review');
  if(content && content.parentElement){ content.parentElement.insertBefore(sec, content); }
  var host = sec.parentElement; host.classList.add('shorten-host');
  // ---------- עמוד נפרד ----------
  var back = document.createElement('button'); back.type = 'button'; back.className = 'sh-back'; back.textContent = '→ חזרה למדריך';
  sec.insertBefore(back, sec.firstChild);
  var anchor = document.querySelector('.sidebar .exam-open-btn') || document.querySelector('.sidebar .ai-open-btn');
  if(anchor){ var b = document.createElement('a'); b.className = 'shorten-open-btn'; b.href = '#shorten'; b.textContent = '✂️ קיצור מצגת';
    anchor.parentNode.insertBefore(b, anchor.nextSibling); }
  var mode = null, lastY = 0, cameIn = false;
  function isOn(){ return location.hash === '#shorten'; }
  function update(){
    var on = isOn(); if(on === mode) return;
    if(on){ if(mode === false){ lastY = window.scrollY; cameIn = true; } document.body.classList.add('shorten-mode');
      var mt = document.getElementById('menuToggle'); if(mt) mt.checked = false; setTimeout(function(){ window.scrollTo(0, 0); }, 0); listSaved(); }
    else { document.body.classList.remove('shorten-mode'); if(mode === true) setTimeout(function(){ window.scrollTo(0, lastY); }, 0); }
    mode = on;
  }
  back.addEventListener('click', function(){ try { history.replaceState(null, '', location.pathname + location.search); } catch(e){} update(); });
  window.addEventListener('hashchange', update); window.addEventListener('popstate', update);
  document.addEventListener('click', function(e){ var a = e.target.closest && e.target.closest('a[href="#shorten"]'); if(a) setTimeout(update, 0); });
  update();

  // ---------- ספריות (נטענות רק כשצריך) ----------
  function load(src){ return new Promise(function(ok, bad){ var s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = bad; document.head.appendChild(s); }); }
  var libs = null;
  function needLibs(){
    if(!libs) libs = load('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js').then(function(){
      window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
      return load('https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js'); });
    return libs;
  }
  var $ = function(id){ return document.getElementById(id); };
  function status(t){ $('shStatus').textContent = t; }
  function note(t){ $('shNote').textContent = t; $('shNote').hidden = !t; }

  // ---------- ניתוח ----------
  var W = 320, H = 240, TOL = 48, SLACK = 0.004;
  var cur = null;   // {name, bytes, n, thumbs[], keep[], why[]}
  function renderPage(pdf, i, w){
    return pdf.getPage(i).then(function(pg){
      var v0 = pg.getViewport({scale: 1}), sc = w / v0.width, v = pg.getViewport({scale: sc});
      var c = document.createElement('canvas'); c.width = Math.round(v.width); c.height = Math.round(v.height);
      return pg.render({canvasContext: c.getContext('2d'), viewport: v}).promise.then(function(){ return c; });
    });
  }
  function pixels(c){ var d = document.createElement('canvas'); d.width = W; d.height = H; var g = d.getContext('2d'); g.drawImage(c, 0, 0, W, H); return g.getImageData(0, 0, W, H).data; }
  function analyse(px){
    var n = px.length, N = W * H;
    // רקע: הצבע החציוני של כל פיקסל בכל השקפים (תבנית העיצוב של המצגת)
    var bg = new Uint8ClampedArray(N * 3), col = new Array(n);
    for(var p = 0; p < N; p++){
      for(var ch = 0; ch < 3; ch++){
        for(var k = 0; k < n; k++) col[k] = px[k][p * 4 + ch];
        col.sort(function(a, b){ return a - b; }); bg[p * 3 + ch] = col[n >> 1];
      }
    }
    function far(a, i, b, j){ return Math.abs(a[i] - b[j]) + Math.abs(a[i + 1] - b[j + 1]) + Math.abs(a[i + 2] - b[j + 2]) > TOL; }
    var ink = px.map(function(a){ var m = []; for(var p = 0; p < N; p++) if(far(a, p * 4, bg, p * 3)) m.push(p); return m; });
    var keep = [], why = [];
    for(var i = 0; i < n; i++){
      keep[i] = true; why[i] = '';
      if(ink[i].length < 40){ continue; }        // שקף כמעט ריק / שקף כותרת: נשאר
      for(var j = i + 1; j < n; j++){
        var bad = 0, lim = Math.max(3, ink[i].length * SLACK), a = px[i], b = px[j];
        for(var q = 0; q < ink[i].length && bad <= lim; q++){ var o = ink[i][q] * 4; if(far(a, o, b, o)) bad++; }
        if(bad <= lim){ keep[i] = false; why[i] = 'כל התוכן מופיע בשקף ' + (j + 1); break; }
      }
    }
    // שרשרת: אם השקף שמכסה נמחק - הוא מכוסה בעצמו בשקף מאוחר יותר, אז המידע עדיין נשאר
    return {keep: keep, why: why};
  }
  function show(){
    var g = $('shGrid'); g.innerHTML = '';
    var k = cur.keep.filter(Boolean).length;
    status(cur.name + ': ' + cur.n + ' שקפים ← ' + k + ' שקפים (נמחקו ' + (cur.n - k) + '). לחיצה על שקף מחליפה בין "נשאר" ל"נמחק".');
    cur.thumbs.forEach(function(src, i){
      if(!showAll && !cur.keep[i] && false) return;
      var bt = document.createElement('button'); bt.type = 'button'; bt.className = 'sh-slide' + (cur.keep[i] ? '' : ' out');
      bt.innerHTML = '<span class="sh-n">' + (i + 1) + '</span><img alt="שקף ' + (i + 1) + '" src="' + src + '"><span class="sh-why">' + (cur.keep[i] ? (cur.manual && cur.manual[i] ? 'נשאר (בחירה שלך)' : '') : (cur.why[i] || 'נמחק (בחירה שלך)')) + '</span>';
      bt.onclick = function(){ cur.keep[i] = !cur.keep[i]; cur.manual = cur.manual || {}; cur.manual[i] = true; if(!cur.keep[i]) cur.why[i] = cur.why[i] || ''; show(); };
      g.appendChild(bt);
    });
    $('shActions').hidden = false;
  }
  var showAll = true;
  $('shAll').onclick = function(){ showAll = !showAll; var g = $('shGrid'); [].forEach.call(g.children, function(c){ if(c.classList.contains('out')) c.hidden = !showAll; }); this.textContent = showAll ? 'רק השקפים שנשארים' : 'הצגת כל השקפים'; };
  $('shFile').addEventListener('change', function(){
    var f = this.files && this.files[0]; if(!f) return; this.value = '';
    note(''); $('shGrid').innerHTML = ''; $('shActions').hidden = true; status('טוענת...');
    var prog = $('shProg');
    needLibs().then(function(){ return f.arrayBuffer(); }).then(function(buf){
      var bytes = new Uint8Array(buf);
      return window.pdfjsLib.getDocument({data: bytes.slice()}).promise.then(function(pdf){
        var n = pdf.numPages, thumbs = [], px = [], i = 0;
        prog.hidden = false; prog.max = n; prog.value = 0;
        function next(){
          if(i >= n) return Promise.resolve();
          i++; status('קוראת שקף ' + i + ' מתוך ' + n + '...');
          return renderPage(pdf, i, 640).then(function(c){ thumbs.push(c.toDataURL('image/jpeg', 0.7)); px.push(pixels(c)); prog.value = i; return next(); });
        }
        return next().then(function(){
          status('משווה בין השקפים...');
          return new Promise(function(ok){ setTimeout(function(){ ok(analyse(px)); }, 30); });
        }).then(function(r){
          prog.hidden = true;
          cur = {name: f.name.replace(/\.pdf$/i, ''), bytes: bytes, n: n, thumbs: thumbs, keep: r.keep, why: r.why};
          show();
        });
      });
    }).catch(function(e){ prog.hidden = true; status(''); note('לא הצלחתי לקרוא את הקובץ. בדקי שזה PDF ושיש חיבור לאינטרנט.'); if(window.console) console.error(e); });
  });

  // ---------- ייצוא ----------
  function build(bytes, keep){
    return needLibs().then(function(){
      var L = window.PDFLib;
      return L.PDFDocument.load(bytes).then(function(src){
        return L.PDFDocument.create().then(function(out){
          var idx = []; keep.forEach(function(k, i){ if(k) idx.push(i); });
          return out.copyPages(src, idx).then(function(pages){ pages.forEach(function(p){ out.addPage(p); }); return out.save(); });
        });
      });
    });
  }
  function deliver(data, name){
    var file = null; try { file = new File([data], name, {type: 'application/pdf'}); } catch(e){}
    if(file && navigator.canShare && navigator.canShare({files: [file]})){
      return navigator.share({files: [file], title: name}).catch(function(e){ if(!e || e.name !== 'AbortError') note('הקובץ מוכן - לחצי שוב על "ייצוא" כדי לשמור או לשלוח אותו.'); });
    }
    var url = URL.createObjectURL(new Blob([data], {type: 'application/pdf'})), a = document.createElement('a');
    a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function(){ URL.revokeObjectURL(url); }, 60000);
    note('הקובץ ירד למכשיר (בתיקיית ההורדות).');
  }
  $('shExport').onclick = function(){
    var bt = this; if(!cur) return; bt.disabled = true;
    build(cur.bytes, cur.keep).then(function(out){ bt.disabled = false; deliver(out, cur.name + ' - מקוצר.pdf'); })
      .catch(function(e){ bt.disabled = false; note('הייצוא נכשל.'); if(window.console) console.error(e); });
  };

  // ---------- שמירה במכשיר (IndexedDB) ----------
  function db(){ return new Promise(function(ok, bad){ var r = indexedDB.open('mathShorten', 1);
    r.onupgradeneeded = function(){ r.result.createObjectStore('decks', {keyPath: 'id'}); }; r.onsuccess = function(){ ok(r.result); }; r.onerror = function(){ bad(r.error); }; }); }
  function tx(mode, fn){ return db().then(function(d){ return new Promise(function(ok, bad){ var t = d.transaction('decks', mode), s = t.objectStore('decks'), res = fn(s);
    t.oncomplete = function(){ ok(res && res.result); }; t.onerror = function(){ bad(t.error); }; }); }); }
  $('shSave').onclick = function(){
    var bt = this; if(!cur) return; bt.disabled = true;
    build(cur.bytes, cur.keep).then(function(out){
      var rec = {id: cur.name, name: cur.name, date: new Date().toISOString(), from: cur.n, to: cur.keep.filter(Boolean).length, pdf: new Blob([out], {type: 'application/pdf'}), keep: cur.keep.slice()};
      return tx('readwrite', function(s){ return s.put(rec); });
    }).then(function(){ bt.disabled = false; note('נשמר במכשיר. מופיע למטה ב"המצגות המקוצרות שלי".'); listSaved(); })
      .catch(function(e){ bt.disabled = false; note('השמירה נכשלה (אולי הדפדפן חוסם שמירה במצב פרטי).'); if(window.console) console.error(e); });
  };
  function listSaved(){
    var ul = $('shSaved'); if(!window.indexedDB){ ul.innerHTML = '<li>הדפדפן לא תומך בשמירה.</li>'; return; }
    tx('readonly', function(s){ return s.getAll(); }).then(function(all){
      all = all || []; ul.innerHTML = all.length ? '' : '<li>עוד אין מצגות שמורות.</li>';
      all.forEach(function(r){
        var li = document.createElement('li');
        li.innerHTML = '<b></b><span></span>';
        li.querySelector('b').textContent = r.name; li.querySelector('span').textContent = r.from + ' ← ' + r.to + ' שקפים';
        var o = document.createElement('button'); o.type = 'button'; o.className = 'sh-btn alt'; o.textContent = 'פתיחה';
        o.onclick = function(){ window.open(URL.createObjectURL(r.pdf), '_blank'); };
        var e = document.createElement('button'); e.type = 'button'; e.className = 'sh-btn'; e.textContent = '📤 ייצוא';
        e.onclick = function(){ r.pdf.arrayBuffer().then(function(b){ deliver(new Uint8Array(b), r.name + ' - מקוצר.pdf'); }); };
        var d = document.createElement('button'); d.type = 'button'; d.className = 'sh-btn alt'; d.textContent = 'מחיקה';
        d.onclick = function(){ tx('readwrite', function(s){ return s.delete(r.id); }).then(listSaved); };
        li.appendChild(o); li.appendChild(e); li.appendChild(d); ul.appendChild(li);
      });
    }).catch(function(){ ul.innerHTML = '<li>אי אפשר לקרוא את השמירות בדפדפן הזה.</li>'; });
  }
  } catch(err){ if(window.console) console.error('shorten', err); }
})();
</script>
<!-- shorten:end -->
"""


def ensure_shorten(page, put_between):
    def add(pg, block):
        i = pg.rindex('</body>')
        return pg[:i] + block + pg[i:]
    return put_between(page, '<!-- shorten:start -->', '<!-- shorten:end -->', SHORTEN_ASSETS, add)
