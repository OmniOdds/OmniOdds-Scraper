const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const PROXY_HOST = 'proxy.soax.com';
const PROXY_PORT = '9000';
const PROXY_USER = '2etWvpLRQJYyBQN2';
const PROXY_PASS = 'wifi;;;';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      `--proxy-server=http://${PROXY_HOST}:${PROXY_PORT}`,
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });

  const page = await browser.newPage();

  await page.authenticate({
    username: PROXY_USER,
    password: PROXY_PASS
  });

  console.log('Launching Puppeteer...');
  await page.goto('https://app.prizepicks.com/', {
    waitUntil: 'networkidle2',
    timeout: 60000
  });

  console.log('Page loaded.');

  // OPTIONAL: Screenshot for debug
  await page.screenshot({ path: 'prizepicks_loaded.png' });

  await browser.close();
})();
