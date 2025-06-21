const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-blink-features=AutomationControlled'
    ]
  });

  const page = await browser.newPage();

  // Intercept the response from /api/v2/players to extract live props
  await page.setRequestInterception(true);
  page.on('request', req => {
    req.continue();
  });

  let liveData = null;

  page.on('response', async response => {
    const url = response.url();
    if (url.includes('/api/v2/players')) {
      try {
        const json = await response.json();
        liveData = json;
        fs.writeFileSync('live_prizepicks_data.json', JSON.stringify(json, null, 2));
        console.log('✅ Live data saved to live_prizepicks_data.json');
      } catch (e) {
        console.error('❌ Failed to parse PrizePicks response:', e);
      }
    }
  });

  try {
    await page.goto('https://prizepicks.com/', {
      waitUntil: 'networkidle2',
      timeout: 60000,
    });
  } catch (e) {
    console.error('❌ Page load failed:', e.message);
  }

  await new Promise(r => setTimeout(r, 10000)); // Wait for data to be captured
  await browser.close();

  if (!liveData) {
    console.log('❌ Live data was not captured. Try rerunning.');
  }
})();
