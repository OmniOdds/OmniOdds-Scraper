const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

(async () => {
  console.log('🟡 Launching browser...');
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-blink-features=AutomationControlled',
    ],
  });

  const page = await browser.newPage();

  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
  );

  console.log('🟡 Navigating to PrizePicks...');
  await page.goto('https://www.prizepicks.com/', {
    waitUntil: 'domcontentloaded',
    timeout: 120000,
  });

  // Use delay instead of waitForTimeout
  const delay = ms => new Promise(res => setTimeout(res, ms));
  await delay(10000);

  console.log('🟡 Intercepting network for props data...');
  let rawData;

  try {
    rawData = await page.waitForResponse(
      res =>
        res.url().includes('/api/v2/players') &&
        res.status() === 200 &&
        res.request().method() === 'GET',
      { timeout: 30000 }
    );
  } catch (err) {
    console.warn('🔁 API not detected, retrying full reload...');
    await page.reload({ waitUntil: 'domcontentloaded' });
    await delay(10000);

    try {
      rawData = await page.waitForResponse(
        res =>
          res.url().includes('/api/v2/players') &&
          res.status() === 200 &&
          res.request().method() === 'GET',
        { timeout: 30000 }
      );
    } catch (error) {
      console.error('❌ Still failed to capture API.');
      await browser.close();
      return;
    }
  }

  const json = await rawData.json();

  const grouped = {};

  json.included.forEach(entry => {
    if (!entry.attributes?.line_score || !entry.attributes?.stat_type) return;

    const sport = entry.attributes.league || 'Other';
    if (!grouped[sport]) grouped[sport] = [];

    grouped[sport].push({
      name: entry.attributes.name,
      stat: entry.attributes.stat_type,
      value: entry.attributes.line_score,
      team: entry.attributes.team,
      matchup: entry.attributes.matchup,
    });
  });

  fs.writeFileSync('prizepicks_all_sports.json', JSON.stringify(grouped, null, 2));
  console.log('✅ Saved props by sport to prizepicks_all_sports.json');

  await browser.close();
})();
