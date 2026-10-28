#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_hub.py - בונה את דף הבית (index.html) של אתר המתמטיקה מתוך sites.json
ומתוך האתרים שבתיקיות (<slug>/index.html): שם, יחידות, מספר נושאים ותאריך עדכון.

בנוסף, מוודא שכל האתרים משתמשים באותו מפתח Google לחיפוש החכם (שם אחד בדפדפן),
כך שמכניסים את המפתח פעם אחת - בדף הבית או באחד האתרים - והוא עובד בכולם.

האתרים בתיקיות הם עותקים עצמאיים - עורכים אותם ישירות כאן, במאגר math.
Netlify מריץ את הסקריפט הזה בכל פרסום, כך שדף הבית תמיד מעודכן.
שימוש:  python3 build_hub.py
"""
import html, json, os, re, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SHARED_KEY = 'mathGeminiKey_v1'

ICON_INNER = ('<rect width="64" height="64" rx="14" fill="#2C3A5E"/>'
              '<path d="M14 23.5C18 19 24 19.5 32 19.5S45 19 50.5 18" fill="none" stroke="#E3B95C" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M26 20.5C26.5 31 25 40 19 47" fill="none" stroke="#E3B95C" stroke-width="5" stroke-linecap="round"/>'
              '<path d="M39.5 20C38.5 31 38.5 41 47 46" fill="none" stroke="#E3B95C" stroke-width="5" stroke-linecap="round"/>')
FAVICON = ('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E'
           + ICON_INNER.replace('#2C3A5E', '#1F2A47').replace('"', '%22').replace('<', '%3C').replace('>', '%3E').replace('#', '%23')
           + '%3C/svg%3E')


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def last_change(folder):
    try:
        return run('git', 'log', '-1', '--format=%cI', '--', folder, cwd=ROOT)
    except Exception:
        return ''


def share_key(page):
    """Every site stores the Google key under one shared name. Returns (page, old names found)."""
    old = re.findall(r"KEY_STORE\s*=\s*'(\w+)'", page)
    page = re.sub(r"(KEY_STORE\s*=\s*)'\w+'", r"\1'" + SHARED_KEY + "'", page)
    return page, [o for o in old if o != SHARED_KEY]


SWIPE_BACK = r"""<!-- hub:swipe-back -->
<script>
// החלקה מימין לשמאל = חזרה אחורה (לדף הקודם, או לדף הבית של אתר המתמטיקה)
(function(){
  try {
    var sx = 0, sy = 0, st = 0, ok = false;
    function blocked(el){
      for(; el && el !== document.documentElement; el = el.parentElement){
        if(el.matches && el.matches('input, textarea, select, math, pre, .ai-overlay, .sidebar')) return true;
        var cs = window.getComputedStyle(el);
        if((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 2) return true;
      }
      return false;
    }
    document.addEventListener('touchstart', function(e){
      if(e.touches.length !== 1){ ok = false; return; }
      var t = e.touches[0]; sx = t.clientX; sy = t.clientY; st = Date.now();
      var mt = document.getElementById('menuToggle'), ov = document.getElementById('aiOverlay');
      ok = !blocked(e.target) && !(mt && mt.checked) && !(ov && !ov.hidden);
    }, {passive: true});
    document.addEventListener('touchmove', function(e){ if(e.touches.length !== 1) ok = false; }, {passive: true});
    document.addEventListener('touchend', function(e){
      if(!ok) return; ok = false;
      var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if(dx < -90 && Math.abs(dy) < Math.abs(dx) * 0.5 && Date.now() - st < 800){
        var fromHere = document.referrer && document.referrer.indexOf(location.origin) === 0;
        if(fromHere && history.length > 1) history.back(); else location.href = '../';
      }
    }, {passive: true});
  } catch(err){}
})();
</script>
"""


BAR_H = 52   # גובה הסרגל העליון (px)

REFRESH_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
               'stroke-linejoin="round" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.34-5.66"/><polyline points="20 4 20 9 15 9"/></svg>')


def topbar(home_html):
    return ('<!-- hub:topbar:start -->\n'
            '<div class="hub-topbar" role="navigation" aria-label="אתר המתמטיקה">'
            + home_html +
            '<button type="button" class="hub-refresh" id="hubRefresh" aria-label="רענון: טעינת הגרסה העדכנית של האתר" title="רענון">'
            + REFRESH_SVG + '<span>רענון</span></button></div>\n<!-- hub:topbar:end -->\n')


SUB_BAR = topbar('<a class="hub-home" href="../"><span aria-hidden="true">⌂</span> כל אתרי המתמטיקה</a>')
HUB_BAR = topbar('<span class="hub-home"><span aria-hidden="true">π</span> מתמטיקה</span>')

TOPBAR_ASSETS = ("""<!-- hub:topbar-assets:start -->
<style>
  /* סרגל עליון קבוע: חזרה לדף הבית + רענון, באותו מקום בכל האתרים */
  .hub-topbar{ position:sticky; top:0; z-index:35; display:flex; align-items:center; justify-content:space-between; gap:12px;
    min-height:%(h)dpx; padding:0 max(12px, env(safe-area-inset-right, 0px)) 0 max(12px, env(safe-area-inset-left, 0px));
    background:#1F2A47; font-family:'Assistant', system-ui, 'Arial Hebrew', Arial, sans-serif; box-shadow:0 1px 0 rgba(255,255,255,.08); }
  .hub-topbar .hub-home{ display:inline-flex; align-items:center; gap:8px; min-height:44px; color:#F5F0E1; text-decoration:none; font-weight:600; font-size:.95rem; }
  .hub-topbar .hub-home > span{ color:#E3B95C; font-weight:700; }
  .hub-refresh{ position:relative; display:inline-flex; align-items:center; gap:5px; min-height:30px; padding:0 11px; border-radius:100px;
    border:1px solid rgba(255,255,255,.28); background:rgba(255,255,255,.07); color:#F5F0E1;
    font-family:inherit; font-weight:600; font-size:.82rem; line-height:1; cursor:pointer; }
  .hub-refresh::after{ content:""; position:absolute; inset:-8px -4px; }   /* אזור לחיצה נוח (44px) גם כשהכפתור נראה קטן */
  .hub-refresh:hover{ background:rgba(255,255,255,.16); }
  .hub-refresh:focus-visible, .hub-topbar .hub-home:focus-visible{ outline:3px solid #E3B95C; outline-offset:2px; border-radius:100px; }
  .hub-refresh svg{ width:14px; height:14px; }
  .hub-refresh.spin svg{ animation:hubSpin .8s linear infinite; }
  @keyframes hubSpin{ to{ transform:rotate(360deg); } }
  @media (prefers-reduced-motion: reduce){ .hub-refresh.spin svg{ animation:none; } }
  /* כפתור הרענון הצף הישן לא נחוץ יותר; כפתור "למעלה" חוזר למקומו */
  #refreshBtn{ display:none !important; }
  a.top-btn#topBtn{ bottom:calc(26px + env(safe-area-inset-bottom, 0px)) !important; left:calc(20px + env(safe-area-inset-left, 0px)) !important; }
  /* במחשב: סרגל הצד מתחיל מתחת לסרגל העליון */
  @media (min-width: 881px){ .sidebar{ top:%(h)dpx !important; height:calc(100vh - %(h)dpx) !important; } }
  /* מפתח החיפוש החכם מנוהל בדף הבית בלבד */
  #aiSetup, #aiKeyOk{ display:none !important; }
  .hub-key-note{ margin:4px 0 14px; padding:12px 16px; border-radius:12px; background:#FFF6D6; border:2px solid #E3B95C; color:#3A2E10; font-size:.95rem; }
  .hub-key-note a{ color:#1F2A47; font-weight:700; }
  @media print{ .hub-topbar{ display:none !important; } }
</style>
<script>
(function(){
  try {
    var KEY = 'hubRefreshY', btn = document.getElementById('hubRefresh');
    if(btn) btn.addEventListener('click', function(){
      btn.classList.add('spin');
      try { sessionStorage.setItem(KEY, String(window.scrollY)); } catch(e){}
      location.replace(location.pathname + '?r=' + Date.now());
    });
    var y = null;
    try { y = sessionStorage.getItem(KEY); sessionStorage.removeItem(KEY); } catch(e){}
    if(/[?&]r=\\d+/.test(location.search)){ try { history.replaceState(null, '', location.pathname + location.hash); } catch(e){} }
    if(y !== null){
      var go = function(){ window.scrollTo({top: parseFloat(y) || 0, behavior: 'instant'}); };
      requestAnimationFrame(function(){ requestAnimationFrame(go); });
      window.addEventListener('load', function(){ setTimeout(go, 120); setTimeout(go, 500); });
    }
  } catch(err){}
  try {
    var note = document.getElementById('hubKeyNote');
    if(note){
      var has = function(){ try { return !!localStorage.getItem('%(key)s'); } catch(e){ return false; } };
      var upd = function(){ note.hidden = has(); };
      document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('[data-ai-open]')) upd(); }, true);
      upd();
    }
  } catch(err){}
})();
</script>
<!-- hub:topbar-assets:end -->
""" % {'h': BAR_H, 'key': SHARED_KEY})

KEY_NOTE = ('<!-- hub:keynote --><p class="hub-key-note" id="hubKeyNote" hidden>🔑 החיפוש החכם צריך מפתח של Google, '
            'שמדביקים <b>פעם אחת</b> ב<a href="../#key">דף הבית של אתר המתמטיקה</a>. אחרי זה הוא עובד בכל האתרים.</p>')


def put_between(page, start, end, block, fallback):
    """Replace the block between markers; if there are none, call fallback(page, block)."""
    if start in page:
        a = page.index(start); b = page.index(end) + len(end)
        if page[b:b + 1] == '\n':
            b += 1
        return page[:a] + block + page[b:]
    return fallback(page, block)


def ensure_topbar_and_key(page):
    # 1. the top bar (replaces the old non-sticky "back" bar)
    def add_bar(pg, block):
        old = re.search(r'<div class="hub-back-bar"[^>]*>.*?</div>\n?', pg, re.S)
        if old:
            return pg[:old.start()] + block + pg[old.end():]
        m = re.search(r'<body[^>]*>\n?', pg)
        return pg[:m.end()] + block + pg[m.end():]
    page = put_between(page, '<!-- hub:topbar:start -->', '<!-- hub:topbar:end -->', SUB_BAR, add_bar)
    # 2. its styles and script
    def add_assets(pg, block):
        i = pg.rindex('</body>')
        return pg[:i] + block + pg[i:]
    page = put_between(page, '<!-- hub:topbar-assets:start -->', '<!-- hub:topbar-assets:end -->', TOPBAR_ASSETS, add_assets)
    # 3. headings land below the sticky bar
    page = page.replace('const OFFSET = 45;', f'const OFFSET = {45 + BAR_H};')
    page = page.replace('getBoundingClientRect().top+window.scrollY-45', f'getBoundingClientRect().top+window.scrollY-{45 + BAR_H}')
    # 4. smart-search key: set once in the home page, not in every site
    if 'hub:keynote' not in page:
        m = re.search(r'<p class="ai-sub">.*?</p>', page, re.S)
        if m:
            page = page[:m.end()] + '\n    ' + KEY_NOTE + page[m.end():]
    page = page.replace('קודם צריך לשמור מפתח בתיבה הצהובה למעלה.', 'קודם צריך להדביק מפתח פעם אחת בדף הבית של אתר המתמטיקה.')
    page = re.sub(r"המפתח לא תקין\.[^']*", 'המפתח לא תקין. אפשר להחליף אותו בדף הבית של אתר המתמטיקה.', page)
    return page


AI_ASK_V2 = """async function askApi(prompt, signal){
    // hub-ai-v2: ניסיון חוזר כש-Google עמוס, מודל גיבוי, והודעת שגיאה מדויקת
    const key=getKey();
    if(!key){ refreshKeyBox(); throw {code:'no_key'}; }
    const parts=[];
    for(const f of images){
      let data;
      try { data=await toJpegBase64(f); } catch(e){ throw {code:'image_rejected'}; }
      parts.push({inline_data:{mime_type:'image/jpeg', data}});
    }
    parts.push({text:prompt});
    const body=JSON.stringify({contents:[{role:'user',parts}], generationConfig:{responseMimeType:'application/json', temperature:0.2}});
    const MODELS=['gemini-flash-latest','gemini-2.5-flash','gemini-flash-lite-latest'];
    const wait=ms=>new Promise((res,rej)=>{ const t=setTimeout(res,ms); if(signal) signal.addEventListener('abort',()=>{ clearTimeout(t); rej({code:'cancelled'}); },{once:true}); });
    let last={code:'upstream_error'}, sawLimit=false;
    for(const model of MODELS){
      for(let attempt=0; attempt<2; attempt++){
        let r;
        try {
          r=await fetch('https://generativelanguage.googleapis.com/v1beta/models/'+model+':generateContent',{method:'POST',signal,
            headers:{'content-type':'application/json','x-goog-api-key':key}, body});
        } catch(e){
          if(e && e.name==='AbortError') throw e;
          last={code:'network'}; await wait(1200); continue;
        }
        if(r.ok){
          const data=await r.json();
          const cand=(data.candidates||[])[0];
          if(!cand){ last={code:'refused'}; break; }
          const text=((cand.content&&cand.content.parts)||[]).map(p=>p.text||'').join('');
          try { return parseJsonLoose(text); } catch(e){ last={code:'invalid_json'}; continue; }
        }
        let msg='', gmsg='';
        try { const j=await r.json(); msg=JSON.stringify(j); gmsg=(j.error&&j.error.message)||''; } catch(e){}
        if(r.status===400 && /API_KEY|api key/i.test(msg)) throw {code:'bad_key'};
        if(r.status===401 || r.status===403) throw {code:'bad_key'};
        if(r.status===429){ sawLimit=true; last={code:'rate_limited'}; break; }          // מכסה נגמרה במודל הזה - מנסים את הבא
        if(r.status===404){ last={code:'upstream_error', detail:'404'}; break; }       // המודל לא זמין - מנסים את הבא
        if(r.status>=500){ last={code:'overloaded', detail:String(r.status)}; await wait(1500*(attempt+1)); continue; }
        last={code:'upstream_error', detail:(r.status+' '+gmsg).trim().slice(0,140)}; break;
      }
    }
    if(sawLimit && last.code!=='invalid_json') throw {code:'rate_limited'};
    throw last;
  }
  """

AI_MSG_EXTRA = ("overloaded:'השרת של Google עמוס כרגע. ניסיתי שוב כמה פעמים ולא הצליח - נסי שוב בעוד דקה.', "
                "network:'אין חיבור ל-Google (אינטרנט או חסימה בדפדפן). בדקי את החיבור ונסי שוב.', "
                "upstream_error:'Google החזיר שגיאה.', ")


def ensure_ai_v2(page):
    """Smart search: retries and a backup model when Google is busy, and an exact error message."""
    if 'async function askApi(' not in page or 'hub-ai-v2' in page:
        return page
    a = page.index('async function askApi(')
    b = page.index('const MSG=', a)
    page = page[:a] + AI_ASK_V2 + page[b:]
    page = page.replace('const MSG={', 'const MSG={' + AI_MSG_EXTRA, 1)
    old = "else setStatus((e && MSG[e.code]) || 'משהו השתבש בחיבור. נסי שוב.', true);"
    new_ = "else setStatus(((e && MSG[e.code]) || 'משהו השתבש בחיבור. נסי שוב.') + (e && e.detail ? ' (' + e.detail + ')' : ''), true);"
    page = page.replace(old, new_)
    return page


def ensure_sub_extras(page):
    """Bottom space (so a host badge never hides content) + swipe right-to-left to go back."""
    add = ''
    # the extra space at the end of the page (for the Netlify badge) is no longer needed - remove it if present
    page = re.sub(r'<!-- hub:bottom-space -->\n<div class="hub-bottom-space"[^>]*></div>\n', '', page)
    if 'hub:swipe-back' not in page:
        add += SWIPE_BACK
    if add:
        i = page.rindex('</body>')
        page = page[:i] + add + page[i:]
    return page


def info(page):
    title = re.search(r'<title>(.*?)</title>', page, re.S)
    units = [re.sub(r'<[^>]+>', '', u).strip() for u in re.findall(r'<h2 class="ex-title"[^>]*>(.*?)</h2>', page, re.S)]
    topics = len(re.findall(r'<h3 class="q"', page))
    return (html.unescape(title.group(1).strip()) if title else ''), units, topics


def write_if_changed(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and open(path, encoding='utf-8').read() == text:
        return False
    open(path, 'w', encoding='utf-8').write(text)
    return True


def hebrew_date(iso):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', iso or '')
    return f'{int(m.group(3))}.{int(m.group(2))}.{m.group(1)}' if m else ''


def card(s):
    e = html.escape
    sources = ''.join(f'<li>{e(x)}</li>' for x in s.get('sources', []))
    src_box = ''
    if s.get('sources_summary') or sources:
        src_box = (f'<span class="site-sources"><b>{e(s.get("sources_summary", "מבוסס על"))}:</b>'
                   + (f'<ul>{sources}</ul>' if sources else '') + '</span>')
    meta = []
    if s['date']:
        meta.append('עודכן ' + hebrew_date(s['date']))
    return f'''
      <a class="site-card {e(s.get('type', ''))}" href="{e(s['slug'])}/">
        <span class="site-kind">{e(s.get('kind', ''))}</span>
        <span class="site-name">{e(s['name'])}</span>
        <span class="site-desc">{e(s['description'])}</span>
        {src_box}
        <span class="site-meta">{' · '.join(meta)}</span>
        <span class="site-go">פתיחה <span aria-hidden="true">←</span></span>
      </a>'''


def hub(cfg, sites, old_keys):
    e = html.escape
    groups = ''
    for g in cfg['groups']:
        cards = ''.join(card(s) for s in sites if s.get('group') == g['id'])
        if not cards:
            continue
        groups += f'''
    <section class="group">
      <h2>{e(g['title'])}</h2>
      <div class="cards">{cards}
      </div>
    </section>
'''
    tpl = open(os.path.join(ROOT, 'hub_template.html'), encoding='utf-8').read()
    apple = open(os.path.join(ROOT, 'apple-touch-icon.png.b64'), encoding='utf-8').read().strip()
    return (tpl.replace('{{TITLE}}', e(cfg['hub_title']))
               .replace('{{SUBTITLE}}', e(cfg['hub_subtitle']))
               .replace('{{GROUPS}}', groups)
               .replace('{{ICON_INNER}}', ICON_INNER)
               .replace('{{FAVICON}}', FAVICON)
               .replace('{{APPLE_ICON}}', 'data:image/png;base64,' + apple)
               .replace('{{KEY_NAME}}', SHARED_KEY)
               .replace('{{OLD_KEYS}}', json.dumps(sorted(set(old_keys))))
               .replace('{{TOPBAR}}', HUB_BAR)
               .replace('{{TOPBAR_ASSETS}}', TOPBAR_ASSETS))


def main():
    cfg = json.load(open(os.path.join(ROOT, 'sites.json'), encoding='utf-8'))
    out, old_keys = [], list(cfg.get('old_key_names', []))
    for s in cfg['sites']:
        path = os.path.join(ROOT, s['slug'], 'index.html')
        page, old = share_key(open(path, encoding='utf-8').read())
        page = ensure_sub_extras(page)
        page = ensure_topbar_and_key(page)
        page = ensure_ai_v2(page)
        old_keys += old
        if write_if_changed(path, page):
            print(f"  עודכן: {s['slug']}/index.html")
        title, units, topics = info(page)
        out.append(dict(s, title=title, units=units, topics=topics, date=last_change(s['slug'])))
        print(f"✓ {s['slug']:20} {title}  ({len(units)} יחידות, {topics} נושאים)")
    changed = write_if_changed(os.path.join(ROOT, 'index.html'), hub(cfg, out, old_keys))
    print('דף הבית', 'עודכן' if changed else 'ללא שינוי')


if __name__ == '__main__':
    main()
