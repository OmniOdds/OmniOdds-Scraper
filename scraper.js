const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const PROXY_HOST = 'your-proxy.soax.com';
const PROXY_PORT = 'your_port';
const PROXY_USER = 'your_username';
const PROXY_PASS = 'your_password';

(async () => {
  console.log('Launching browser...');

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      `--proxy-server=http://${PROXY_HOST}:${PROXY_PORT}`,
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
    ]
  });

  const page = await browser.newPage();

  // Set proxy authentication
  await page.authenticate({
    username: PROXY_USER,
    password: PROXY_PASS,
  });

  console.log('Navigating to PrizePicks...');
  await page.goto('https://prizepicks.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });

  let propsData = null;

  // Intercept the API response
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('/api/v2/players')) {
      try {
        const json = await response.json();
        propsData = json;
        console.log('✅ API response captured.');
      } catch (err) {
        console.error('❌ Error parsing JSON:', err);
      }
    }
  });

  // Retry logic
  for (let i = 0; i < 5; i++) {
    if (propsData) break;
    console.log(`Waiting for API response... (retry ${i + 1})`);
    await new Promise(res => setTimeout(res, 4000));
  }

  if (!propsData) {
    console.log('❌ Failed to fetch PrizePicks props after retries.');
    await browser.close();
    return;
  }

  // Group by sport
  const grouped = {};
  for (const prop of propsData.included) {
    const league = prop.attributes?.league ?? 'Unknown';
    if (!grouped[league]) grouped[league] = [];
    grouped[league].push({
      name: prop.attributes.name,
      stat_type: prop.attributes.stat_type,
      line_score: prop.attributes.line_score,
      team: prop.attributes.team,
    });
  }

  fs.writeFileSync('prizepicks_props_by_sport.json', JSON.stringify(grouped, null, 2));
  console.log('✅ Saved to prizepicks_props_by_sport.json');

  await browser.close();
})();
