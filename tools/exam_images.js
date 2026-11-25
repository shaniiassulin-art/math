// תמונות של השאלות (בלי הפתרונות) לקובץ ה-PDF של מחולל המבחנים.
// באפליקציה ממסך הבית אין לאייפון הדפסה, ולכן הדף בונה קובץ PDF בעצמו מהתמונות האלה - ומשתף אותו.
// לכל אתר: <אתר>/exam-img/<id>.jpg ו-<אתר>/exam-img/index.json (גודל כל תמונה בפיקסלים).
// שימוש (מתוך תיקיית הריפו, אחרי tools/samples.py):  node tools/exam_images.js
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITES = ['calculus-1', 'algebra-solutions', 'algebra-theory'];
const WIDTH = 680;          // רוחב השאלה בפיקסלים של CSS (בקובץ: 515 נקודות - רוחב עמוד A4 פחות שוליים)

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.woff2': 'font/woff2',
                '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.json': 'application/json', '.svg': 'image/svg+xml' };
const HEB = 'U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F';
const LAT = 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD';
const FONT_CSS = [['Assistant', 400, 'assistant', 400], ['Assistant', 600, 'assistant', 700], ['Assistant', 700, 'assistant', 700],
                  ['Frank Ruhl Libre', 700, 'frank-ruhl-libre', 700], ['Frank Ruhl Libre', 900, 'frank-ruhl-libre', 700]]
  .map(([fam, w, file, fw]) => [['hebrew', HEB], ['latin', LAT]].map(([sub, rng]) =>
    `@font-face{font-family:'${fam}';font-style:normal;font-weight:${w};font-display:block;src:url(/tools/fonts/${file}-${sub}-${fw}-normal.woff2) format('woff2');unicode-range:${rng};}`).join('\n')).join('\n');

function serve() {
  const srv = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    const f = fs.existsSync(p) && fs.statSync(p).isDirectory() ? path.join(p, 'index.html') : p;
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r(srv)));
}

(async () => {
  const srv = await serve();
  const port = srv.address().port;
  const browser = await chromium.launch();
  for (const site of SITES) {
    const out = path.join(ROOT, site, 'exam-img');
    fs.rmSync(out, { recursive: true, force: true });
    fs.mkdirSync(out, { recursive: true });
    const page = await browser.newPage({ viewport: { width: WIDTH + 80, height: 1200 }, deviceScaleFactor: 2 });
    await page.route(/fonts\.googleapis\.com/, r => r.fulfill({ contentType: 'text/css', body: FONT_CSS }));
    await page.route(/fonts\.gstatic\.com/, r => r.abort());
    await page.goto(`http://127.0.0.1:${port}/${site}/`, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const ids = await page.evaluate((W) => {
      const st = document.createElement('style');
      st.textContent = `#xr{position:absolute;top:0;left:0;width:${W}px;background:#fff;direction:rtl;padding:2px 0;z-index:99999;color:#1F2A47;}
        #xr .box,#xr .box.sample{border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;background:none!important;max-width:none!important;}
        #xr .box::before,#xr .box::after{display:none!important;}
        #xr .sample-q{margin:0;}
        body.xr-on .hub-topbar,body.xr-on .menu-fab,body.xr-on .top-btn,body.xr-on .refresh-btn{display:none!important;}`;
      document.head.appendChild(st);
      document.body.classList.add('xr-on');
      const box = document.createElement('div'); box.id = 'xr'; document.body.appendChild(box);
      return [...document.querySelectorAll('section.exercise .box.sample')].filter(e => e.querySelector('.sample-sol')).map(e => e.id);
    }, WIDTH);
    const sizes = {};
    for (const id of ids) {
      await page.evaluate((id) => {
        const xr = document.getElementById('xr');
        const c = document.getElementById(id).cloneNode(true);
        c.removeAttribute('id');
        c.querySelectorAll('[id]').forEach(e => e.removeAttribute('id'));
        c.querySelectorAll('.box-title, .sample-btn, .sample-hint, .sample-sol, .sample-src, .xm-badges').forEach(x => x.remove());
        xr.innerHTML = ''; xr.appendChild(c);
        window.scrollTo(0, 0);
      }, id);
      const el = await page.$('#xr');
      const bb = await el.boundingBox();
      await el.screenshot({ path: path.join(out, id + '.jpg'), type: 'jpeg', quality: 82 });
      sizes[id] = [Math.round(bb.width * 2), Math.round(bb.height * 2)];
    }
    fs.writeFileSync(path.join(out, 'index.json'), JSON.stringify({ w: WIDTH, q: sizes }));
    console.log(`${site}: ${ids.length} question images`);
    // מבחני חזרה: תמונה לשאלה, ותמונה לכל שלב בפתרון (כדי שהפתרון יתחלק יפה בין עמודים)
    const rv = await page.evaluate(() => [...document.querySelectorAll('.review-section .rv-item')].map(e => e.dataset.id));
    if (rv.length) {
      const rout = path.join(ROOT, site, 'review-img');
      fs.rmSync(rout, { recursive: true, force: true });
      fs.mkdirSync(rout, { recursive: true });
      const R = { w: WIDTH, q: {}, s: {} };
      const shot = async (file) => {
        const el = await page.$('#xr'); const bb = await el.boundingBox();
        await el.screenshot({ path: path.join(rout, file + '.jpg'), type: 'jpeg', quality: 82 });
        return [Math.round(bb.width * 2), Math.round(bb.height * 2)];
      };
      for (const id of rv) {
        const n = await page.evaluate((id) => {
          const src = document.querySelector('.rv-item[data-id="' + id + '"] .box.sample');
          const c = src.cloneNode(true);
          c.removeAttribute('id'); c.querySelectorAll('[id]').forEach(e => e.removeAttribute('id'));
          c.querySelectorAll('.box-title, .sample-btn, .sample-hint, .sample-sol, .sample-src, .xm-badges').forEach(x => x.remove());
          const xr = document.getElementById('xr'); xr.innerHTML = ''; xr.appendChild(c); window.scrollTo(0, 0);
          return src.querySelectorAll('.sample-sol > .sol-step, .sample-sol > .sol-ans').length;
        }, id);
        R.q[id] = await shot(id + '-q');
        R.s[id] = [];
        for (let k = 0; k < n; k++) {
          await page.evaluate(([id, k]) => {
            const src = document.querySelector('.rv-item[data-id="' + id + '"] .sample-sol');
            const sol = src.cloneNode(false); sol.removeAttribute('id'); sol.hidden = false; sol.style.display = 'flex';
            const part = src.querySelectorAll(':scope > .sol-step, :scope > .sol-ans')[k].cloneNode(true);
            part.querySelectorAll('[id]').forEach(e => e.removeAttribute('id'));
            part.querySelectorAll('.tip-row, .tip-panel').forEach(x => x.remove());
            sol.appendChild(part);
            const xr = document.getElementById('xr'); xr.innerHTML = ''; xr.appendChild(sol); window.scrollTo(0, 0);
          }, [id, k]);
          R.s[id].push(await shot(id + '-s' + (k + 1)));
        }
      }
      fs.writeFileSync(path.join(rout, 'index.json'), JSON.stringify(R));
      console.log(`${site}: ${rv.length} review questions, ${Object.values(R.s).reduce((a, x) => a + x.length, 0)} solution images`);
    }
    await page.close();
  }
  await browser.close();
  srv.close();
})();
