// Real headless Chrome rendering at mobile CSS viewport widths.
const { chromium } = require('playwright-core');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const base = process.env.CATALOG_URL || 'http://127.0.0.1:8000';
const output = path.resolve(__dirname, '../../results/mobile');
const executablePath = process.env.CHROME_PATH || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function main() {
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({headless: true, executablePath});
  const checks = [];
  try {
    for (const width of [320, 390, 430]) {
      const context = await browser.newContext({viewport: {width, height: 844}, isMobile: true, hasTouch: true, deviceScaleFactor: 1});
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const response = await page.goto(base);
      assert.equal(response.status(), 200);
      await page.locator('#workspace').waitFor({state: 'visible'});
      for (const [id, title] of [['task-01', 'Independent value-list snapshots'], ['task-02', 'Inventory summary over HTTP']]) {
        const card = page.locator(`nav[aria-label="Tasks"] a[href="#${id}"]`);
        await card.tap();
        await page.waitForFunction(expected => document.querySelector('#task-title').textContent === expected, title);
        assert.equal(await card.getAttribute('aria-current'), 'page');
        for (const selector of ['#task-title', '#statement', '#environment', '#difficulty-note']) {
          assert.ok((await page.locator(selector).textContent()).trim());
        }
        const layout = await page.evaluate(() => {
          const width = document.documentElement.clientWidth;
          const article = document.querySelector('article').getBoundingClientRect();
          const aside = document.querySelector('aside').getBoundingClientRect();
          const links = [...document.querySelectorAll('nav a')].map(link => {
            const rect = link.getBoundingClientRect();
            return {width: rect.width, height: rect.height};
          });
          const overflow = [...document.querySelectorAll('body *')].filter(element => {
            const rect = element.getBoundingClientRect();
            return rect.width > 0 && (rect.left < -1 || rect.right > width + 1);
          }).map(element => element.tagName + (element.id ? '#' + element.id : ''));
          return {viewport: width, scrollWidth: document.documentElement.scrollWidth,
                  detailBelowList: article.top >= aside.bottom - 1, links, overflow,
                  statementFontSize: getComputedStyle(document.querySelector('#statement p')).fontSize};
        });
        assert.equal(layout.viewport, width);
        assert.ok(layout.scrollWidth <= width, JSON.stringify(layout));
        assert.deepEqual(layout.overflow, []);
        assert.equal(layout.detailBelowList, true);
        assert.ok(layout.links.every(link => link.width >= 44 && link.height >= 44));
        assert.deepEqual(errors, []);
        const screenshot = `${width}-${id}.png`;
        await page.screenshot({path: path.join(output, screenshot), fullPage: true, animations: 'disabled'});
        checks.push({width, task: id, passed: true, ...layout, screenshot});
      }
      await context.close();
    }
    console.log(JSON.stringify({passed: true, method: 'Local headless Chrome; mobile viewport and touch emulation',
      browser: browser.version(), base, checks,
      limitations: ['Not physical-device testing', 'Not Safari or Firefox testing']}, null, 2));
  } finally { await browser.close(); }
}

main().catch(error => {console.error(error); process.exitCode = 1;});
