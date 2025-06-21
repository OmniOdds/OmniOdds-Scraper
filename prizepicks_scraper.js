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

  // Scroll slowly to force load
  for (let i = 0; i < 10; i++) {
    await page.evaluate(() => window.scrollBy(0, 500));
    await new Promise(resolve => setTimeout(resolve, 500));
  }

  // Wait for main content to show up
  await page.waitForSelector('.name', { timeout: 30000 });

  const props = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('.name'));
    return cards.map(card => {
      const name = card?.innerText || 'Unknown';
      const category = card?.closest('.stat-line')?.querySelector('.category')?.innerText || 'Unknown';
      const value = card?.closest('.stat-line')?.querySelector('.presale-score')?.innerText || 'Unknown';
      return { name, category, value };
    });
  });

  console.log(`✅ Scraped ${props.length} props:`);
  console.table(props);

  await browser.close();
})();
