const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const proxyUser = '2etWVpLRQJYyBQN2';
const proxyPass = 'wifi;;;;';
const proxyHost = 'proxy.soax.com';
const proxyPort = '9000';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      `--proxy-server=http://${proxyHost}:${proxyPort}`,
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });

  const page = await browser.newPage();

  // Authenticate with SOAX proxy
  await page.authenticate({
    username: proxyUser,
    password: proxyPass
  });

  // Intercept the raw API response
  let capturedData = null;
  await page.setRequestInterception(true);

  page.on('request', (req) => req.continue());

  page.on('response', async (res) => {
    const url = res.url();
    if (url.includes('/api/v2/players')) {
      try {
        capturedData = await res.json();
        console.log('[✅ API INTERCEPTED]');
        console.log(JSON.stringify(capturedData, null, 2));
      } catch (err) {
        console.error('Error parsing response:', err);
      }
    }
  });

  // Navigate to PrizePicks
  await page.goto('https://app.prizepicks.com/', {
    waitUntil: 'networkidle2',
    timeout: 60000
  });

  // Replaces page.waitForTimeout(10000)
  await new Promise(resolve => setTimeout(resolve, 10000));

  if (!capturedData) {
    console.error('❌ No data intercepted.');
  }

  await browser.close();
})();
