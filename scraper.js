const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const delay = ms => new Promise(res => setTimeout(res, ms));

(async () => {
  console.log('🟡 Launching browser...');
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--window-size=1920,1080'
    ],
  });

  const page = await browser.newPage();

  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
  );

  await page.setViewport({ width: 1920, height: 1080 });

  console.log('🟡 Navigating to PrizePicks...');
  await page.goto('https://www.prizepicks.com/', {
    waitUntil: 'networkidle0',
    timeout: 60000,
  });

  await delay(10000);

  console.log('🟡 Intercepting API call...');
  let apiResponse;

  const interceptApi = async () => {
    try {
      apiResponse = await page.waitForResponse(
        res =>
          res.url().includes('/api/v2/players') &&
          res.request().method() === 'GET' &&
          res.status() === 200,
        { timeout: 25000 }
      );
      return true;
    } catch {
      return false;
    }
  };

  const maxRetries = 3;
  let attempts = 0;
  let success = await interceptApi();

  while (!success && attempts < maxRetries) {
    console.log(`🔁 Reload attempt ${attempts + 1}`);
    await page.reload({ waitUntil: 'networkidle0' });
    await delay(10000);
    success = await interceptApi();
    attempts++;
  }

  if (!success) {
    console.error('❌ Failed to capture PrizePicks API after retries.');
    await browser.close();
    return;
  }

  const data = await apiResponse.json();

  // Group props by sport
  const grouped = {};
  data.included.forEach(p => {
    const attr = p.attributes;
    if (!attr || !attr.stat_type || !attr.line_score) return;

    const sport = attr.league || 'Other';
    if (!grouped[sport]) grouped[sport] = [];

    grouped[sport].push({
      name: attr.name,
      stat: attr.stat_type,
      value: attr.line_score,
      team: attr.team,
      matchup: attr.matchup,
    });
  });

  fs.writeFileSync('prizepicks_all_sports.json', JSON.stringify(grouped, null, 2));
  console.log('✅ Saved prizepicks_all_sports.json with', Object.keys(grouped).length, 'sports');

  await browser.close();
})();

