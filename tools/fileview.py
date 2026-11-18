# -*- coding: utf-8 -*-
"""תצוגת קבצי הקורס בטלפון (build_hub.py קורא ל-ensure_fileview).

בטלפון: כל עמוד ברוחב המסך (בלי גלילה הצידה), ולחיצה על עמוד פותחת אותו במסך מלא:
הגדלה והקטנה בכפתורים או בצביטה, גלילה בין העמודים, מעבר לעמוד הבא/הקודם, וסגירה בכפתור או ב"חזרה".
"""

FILEVIEW_ASSETS = r"""<!-- fileview:start -->
<style>
  /* ===== קבצי הקורס בטלפון: עמוד ברוחב המסך + מסך מלא בלחיצה ===== */
  @media (max-width:700px){
    .files-section .file-pages:not(.slides){ width:100% !important; }
    .files-section .file-scroll{ overflow-x:visible; }
    .files-section .file-hint{ display:block; }
  }
  .files-section .file-slice img, .files-section .slide img{ cursor:zoom-in; }
  .fv{ position:fixed; inset:0; z-index:85; background:#20242E; display:flex; flex-direction:column; direction:rtl;
    font-family:'Assistant', system-ui, 'Arial Hebrew', Arial, sans-serif; }
  .fv[hidden]{ display:none; }
  body.fv-on{ overflow:hidden; }
  .fv-bar{ display:flex; align-items:center; justify-content:space-between; gap:8px; min-height:52px;
    padding:max(4px, env(safe-area-inset-top,0px)) max(10px, env(safe-area-inset-right,0px)) 4px max(10px, env(safe-area-inset-left,0px)); background:#1F2A47; color:#fff; }
  .fv-title{ flex:1; min-width:0; font-weight:700; font-size:.92rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .fv-btns{ display:flex; gap:6px; }
  .fv button{ min-width:44px; min-height:44px; border-radius:12px; border:1px solid rgba(255,255,255,.25); background:rgba(255,255,255,.08);
    color:#fff; font-family:inherit; font-size:1.05rem; font-weight:800; cursor:pointer; }
  .fv button:focus-visible{ outline:3px solid #E3B95C; }
  .fv-scroll{ flex:1; overflow:auto; -webkit-overflow-scrolling:touch; touch-action:pan-x pan-y pinch-zoom; }
  .fv-pages{ margin:0 auto; padding:10px 0 40px; }
  .fv-pages img{ display:block; width:100%; height:auto; margin:0 auto 10px; background:#fff; box-shadow:0 2px 10px rgba(0,0,0,.35); }
  .fv-foot{ display:flex; align-items:center; justify-content:center; gap:10px; padding:6px 10px max(8px, env(safe-area-inset-bottom,0px)); background:#1F2A47; color:#fff; font-weight:700; font-size:.9rem; }
  .fv-foot span{ min-width:90px; text-align:center; }
</style>
<div class="fv" id="fileViewer" hidden role="dialog" aria-modal="true" aria-label="תצוגת קובץ">
  <div class="fv-bar">
    <div class="fv-title" id="fvTitle"></div>
    <div class="fv-btns">
      <button type="button" id="fvOut" aria-label="הקטנה">−</button>
      <button type="button" id="fvIn" aria-label="הגדלה">+</button>
      <button type="button" id="fvClose" aria-label="סגירה">✕</button>
    </div>
  </div>
  <div class="fv-scroll" id="fvScroll"><div class="fv-pages" id="fvPages"></div></div>
  <div class="fv-foot"><button type="button" id="fvNext" aria-label="העמוד הבא">→</button><span id="fvNum"></span><button type="button" id="fvPrev" aria-label="העמוד הקודם">←</button></div>
</div>
<script>
(function(){
  try {
  var fv = document.getElementById('fileViewer'); if(!fv) return;
  var pagesEl = document.getElementById('fvPages'), scroll = document.getElementById('fvScroll');
  var title = document.getElementById('fvTitle'), num = document.getElementById('fvNum');
  var ZOOMS = [100, 140, 180, 240, 320], z = 1, imgs = [], pushed = false;
  // ההינט בטלפון
  document.querySelectorAll('.files-section .file-hint').forEach(function(h){ h.textContent = '👆 לחיצה על עמוד פותחת אותו בגדול - עם הגדלה ומעבר בין העמודים.'; });
  function pagesOf(doc){
    var seen = {}, out = [];
    doc.querySelectorAll('.file-slice img, .slide img').forEach(function(im){
      var src = im.getAttribute('src'); if(seen[src]) return; seen[src] = 1; out.push(src);
    });
    return out;
  }
  function setZoom(i){
    var y = scroll.scrollTop / Math.max(1, scroll.scrollHeight);
    z = Math.max(0, Math.min(ZOOMS.length - 1, i));
    pagesEl.style.width = ZOOMS[z] + '%';
    scroll.scrollTop = y * scroll.scrollHeight;
    scroll.scrollLeft = 0;   // RTL: מתחילים מצד ימין של העמוד, איפה שהשורה מתחילה
    document.getElementById('fvOut').disabled = z === 0; document.getElementById('fvIn').disabled = z === ZOOMS.length - 1;
  }
  function current(){
    var top = scroll.getBoundingClientRect().top, best = 0;
    imgs.forEach(function(im, i){ if(im.getBoundingClientRect().top - top < scroll.clientHeight / 2) best = i; });
    return best;
  }
  function showNum(){ num.textContent = 'עמוד ' + (current() + 1) + ' מתוך ' + imgs.length; }
  function go(i){ i = Math.max(0, Math.min(imgs.length - 1, i)); scroll.scrollTop += imgs[i].getBoundingClientRect().top - scroll.getBoundingClientRect().top - 8; showNum(); }
  function open(doc, src){
    var list = pagesOf(doc); if(!list.length) return;
    title.textContent = (doc.querySelector('.file-title') || {}).textContent || '';
    pagesEl.innerHTML = list.map(function(s, i){ return '<img src="' + s + '" alt="עמוד ' + (i + 1) + '" decoding="async"' + (Math.abs(i - list.indexOf(src)) > 2 ? ' loading="lazy"' : '') + '>'; }).join('');
    imgs = [].slice.call(pagesEl.querySelectorAll('img'));
    fv.hidden = false; document.body.classList.add('fv-on');
    setZoom(window.innerWidth < 700 ? 1 : 0);
    var k = Math.max(0, list.indexOf(src));
    setTimeout(function(){ go(k); }, 30); setTimeout(function(){ go(k); }, 350);
    if(!pushed){ try { history.pushState({fv: 1}, ''); pushed = true; } catch(e){} }
  }
  function close(fromPop){
    if(fv.hidden) return;
    fv.hidden = true; document.body.classList.remove('fv-on'); pagesEl.innerHTML = ''; imgs = [];
    if(pushed && !fromPop){ pushed = false; try { history.back(); } catch(e){} } else pushed = false;
  }
  document.addEventListener('click', function(e){
    var im = e.target.closest('.files-section .file-slice img, .files-section .slide img'); if(!im) return;
    var doc = im.closest('.file-doc'); if(!doc) return;
    e.preventDefault(); open(doc, im.getAttribute('src'));
  });
  window.addEventListener('popstate', function(){ if(!fv.hidden) close(true); });
  document.getElementById('fvClose').onclick = function(){ close(false); };
  document.getElementById('fvIn').onclick = function(){ setZoom(z + 1); };
  document.getElementById('fvOut').onclick = function(){ setZoom(z - 1); };
  document.getElementById('fvNext').onclick = function(){ go(current() + 1); };
  document.getElementById('fvPrev').onclick = function(){ go(current() - 1); };
  scroll.addEventListener('scroll', function(){ if(imgs.length) showNum(); }, {passive: true});
  document.addEventListener('keydown', function(e){
    if(fv.hidden) return;
    if(e.key === 'Escape') close(false);
    if(e.key === 'ArrowLeft') go(current() + 1);
    if(e.key === 'ArrowRight') go(current() - 1);
  });
  } catch(err){ if(window.console) console.error('fileview', err); }
})();
</script>
<!-- fileview:end -->
"""


def ensure_fileview(page, put_between):
    if 'files-section' not in page:
        return page
    def add(pg, block):
        i = pg.rindex('</body>')
        return pg[:i] + block + pg[i:]
    return put_between(page, '<!-- fileview:start -->', '<!-- fileview:end -->', FILEVIEW_ASSETS, add)
