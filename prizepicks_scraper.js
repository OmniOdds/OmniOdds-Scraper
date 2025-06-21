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

  console.log('Launching Puppeteer...');
  await page.goto('https://app.prizepicks.com/', {
    waitUntil: 'networkidle2',
    timeout: 60000
  });

  console.log('Page loaded.');

  // Wait for props to show up
  await page.waitForSelector('[data-testid="entry-card"]', { timeout: 20000 });

  const props = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('[data-testid="entry-card"]'));
    return cards.map(card => {
      const name = card.querySelector('[data-testid="player-name"]')?.innerText || 'Unknown';
      const stat = card.querySelector('[data-testid="stat-text"]')?.innerText || 'Unknown';
      const projection = card.querySelector('[data-testid="projection-score"]')?.innerText || 'Unknown';
      return { name, stat, projection };
    });
  });

  console.log(`✅ Scraped ${props.length} props:`);
  console.table(props);

  await browser.close();
})();
