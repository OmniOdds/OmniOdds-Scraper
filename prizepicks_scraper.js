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
  await page.authenticate({ username: PROXY_USER, password: PROXY_PASS });

  console.log('🟢 Launching browser...');
  await page.goto('https://app.prizepicks.com/', {
    waitUntil: 'networkidle2',
    timeout: 60000
  });

  console.log('🟡 Scrolling to load props...');
  for (let i = 0; i < 20; i++) {
    await page.evaluate(() => window.scrollBy(0, 300));
    await new Promise(resolve => setTimeout(resolve, 300));
  }

  console.log('🕒 Waiting for props to appear...');
  await page.waitForSelector('div[data-testid="player-card"]', { timeout: 45000 });

  const props = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('div[data-testid="player-card"]'));

    return cards.map(card => {
      const name = card.querySelector('p[class*="PlayerName"]')?.innerText || 'Unknown';
      const stat = card.querySelector('p[class*="StatTitle"]')?.innerText || 'Unknown';
      const value = card.querySelector('p[class*="StatValue"]')?.innerText || 'Unknown';
      return { name, stat, value };
    });
  });

  console.log(`✅ Scraped ${props.length} player props:`);
  console.table(props);

  await browser.close();
})();
