const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const playwrightPath = process.argv[2] || 'playwright';
const baseUrl = (process.argv[3] || 'http://127.0.0.1:4194').replace(/\/$/, '');
const { chromium, request } = require(playwrightPath);

async function assertAsset(api, url) {
  const response = await api.get(url);
  assert.equal(response.ok(), true, `${url} returned ${response.status()}`);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const artifacts = path.join(process.cwd(), 'test-artifacts');
  fs.mkdirSync(artifacts, { recursive: true });

  for (const viewport of [
    { name: 'desktop', width: 1440, height: 1000 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'mobile', width: 390, height: 844 },
    { name: 'narrow', width: 320, height: 720 },
  ]) {
    const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
    const page = await context.newPage();
    const errors = [];
    page.on('console', (message) => {
      if (message.type() === 'error') errors.push(`console: ${message.text()}`);
    });
    page.on('pageerror', (error) => errors.push(`pageerror: ${error.message}`));

    const response = await page.goto(`${baseUrl}/`, { waitUntil: 'networkidle' });
    assert.equal(response.ok(), true, `home failed at ${viewport.name}`);
    assert.match(await page.title(), /让每个 claim 回到来源/);
    assert.match(await page.locator('h1').innerText(), /让每个\s*claim\s*回到来源/);
    assert.equal(await page.locator('.workflow-card').count(), 5);
    assert.equal(await page.locator('[data-lineage]').count(), 5);
    assert.equal(await page.locator('.tool-grid article').count(), 4);

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    assert.ok(overflow <= 1, `${viewport.name} horizontal overflow: ${overflow}px`);

    await page.locator('[data-lineage="verify"]').click();
    assert.match(await page.locator('[data-detail-title]').innerText(), /分别核验/);
    assert.equal(await page.locator('[data-detail-list] li').count(), 3);

    await page.locator('[data-language-toggle]').click();
    assert.equal(await page.locator('html').getAttribute('lang'), 'en');
    assert.match(await page.title(), /Make every claim trace back/);
    assert.match(await page.locator('h1').innerText(), /Make every\s*claim\s*trace back/);
    assert.match(await page.locator('[data-detail-title]').innerText(), /Verify claims/);

    await page.reload({ waitUntil: 'networkidle' });
    assert.equal(await page.locator('html').getAttribute('lang'), 'en', 'language preference did not persist');

    await page.locator('[data-language-toggle]').click();
    assert.equal(await page.locator('html').getAttribute('lang'), 'zh-CN');

    await page.screenshot({ path: path.join(artifacts, `${viewport.name}.png`), fullPage: true });
    assert.deepEqual(errors, [], `${viewport.name} browser errors: ${errors.join('; ')}`);
    await context.close();
  }

  const noJsContext = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  const noJsPage = await noJsContext.newPage();
  await noJsPage.goto(`${baseUrl}/`, { waitUntil: 'domcontentloaded' });
  assert.match(await noJsPage.locator('h1').innerText(), /让每个\s*claim\s*回到来源/);
  assert.equal(await noJsPage.locator('.workflow-card').count(), 5);
  await noJsContext.close();

  const reducedContext = await browser.newContext({ reducedMotion: 'reduce', viewport: { width: 390, height: 844 } });
  const reducedPage = await reducedContext.newPage();
  await reducedPage.goto(`${baseUrl}/`, { waitUntil: 'networkidle' });
  const reducedOpacity = await reducedPage.locator('.workflow-card').first().evaluate((element) => getComputedStyle(element).opacity);
  assert.equal(reducedOpacity, '1');
  await reducedContext.close();

  const notFound = await browser.newPage();
  const notFoundResponse = await notFound.goto(`${baseUrl}/404.html`, { waitUntil: 'domcontentloaded' });
  assert.equal(notFoundResponse.ok(), true);
  assert.match(await notFound.locator('h1').innerText(), /来源链/);
  await notFound.close();

  const api = await request.newContext();
  await Promise.all([
    assertAsset(api, `${baseUrl}/styles.css`),
    assertAsset(api, `${baseUrl}/app.js`),
    assertAsset(api, `${baseUrl}/assets/favicon.svg`),
    assertAsset(api, `${baseUrl}/site.webmanifest`),
    assertAsset(api, `${baseUrl}/robots.txt`),
    assertAsset(api, `${baseUrl}/sitemap.xml`),
  ]);
  await api.dispose();

  await browser.close();
  console.log('Site smoke test passed: bilingual UI, evidence interaction, responsive layouts, reduced motion, assets, and 404.');
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
