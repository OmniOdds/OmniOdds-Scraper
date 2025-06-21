const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const proxyUser = '2etWvpLRQJYyBQN2';
const proxyPass = 'wifi;;;;';
const proxyHost = 'proxy.soax.com';
const proxyPort = '9000';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      `--proxy-server=http://${proxyHost}:${proxyPort}`,
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=1920,1080'
    ],
    ignoreHTTPSErrors: true,
  });

  const page = await browser.newPage();

  // Authenticate with Soax proxy
  await page.authenticate({
    username: proxyUser,
    password: proxyPass
  });

  let capturedData = null;

  // Intercept the PrizePicks API response
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('/api/v2/players')) {
      try {
        const json = await response.json();
        capturedData = json;
        console.log('\n✅ [SUCCESS] PrizePicks API Data:\n');
        console.log(JSON.stringify(json, null, 2));
      } catch (err) {
        console.error('❌ Failed to parse JSON:', err.message);
      }
    }
  });

  // Go to PrizePicks
  await page.goto('https://app.prizepicks.com/', {
    waitUntil: 'domcontentloaded',
    timeout: 60000
  });

  // Wait and scroll to trigger API
  await page.evaluate(() => window.scrollBy(0, 1500));
  await new Promise(resolve => setTimeout(resolve, 10000));

  if (!capturedData) {
    console.log('❌ No data intercepted from /api/v2/players');
  }

  await browser.close();
})();
