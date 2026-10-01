// Render the thumbnail and the standalone diagram card to PNG.
// Usage: node render.js [portrait-image-path]
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const page_url = 'file://' + path.join(dir, 'thumbnail.html');
  const portrait = process.argv[2] ? 'file://' + path.resolve(process.argv[2]) : '';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });

  await page.goto(page_url + (portrait ? '?portrait=' + encodeURIComponent(portrait) : ''), { waitUntil: 'networkidle' });
  await page.evaluate(async () => { await document.fonts.load('900 40px Montserrat'); await document.fonts.ready; return document.fonts.check('900 40px Montserrat'); }).then(ok => console.log('Montserrat loaded:', ok));
  await page.screenshot({ path: path.join(dir, 'thumbnail.png') });

  await page.goto(page_url + '?only=diagram', { waitUntil: 'networkidle' });
  await page.evaluate(async () => { await document.fonts.load('900 40px Montserrat'); await document.fonts.ready; return document.fonts.check('900 40px Montserrat'); }).then(ok => console.log('Montserrat loaded:', ok));
  await page.locator('#card').screenshot({ path: path.join(dir, 'diagramm.png'), omitBackground: true, scale: 'device' });

  await browser.close();
})();
