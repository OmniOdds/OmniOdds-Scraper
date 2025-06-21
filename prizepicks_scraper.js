const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

// Enable stealth mode
puppeteer.use(StealthPlugin());

// === CONFIG ===
const PRIZEPICKS_URL = 'https://app.prizepicks.com/';
const PROXY = 'your_proxy_ip:port'; // Example: 'proxy.soax.com:9000'
const PROXY_USER = 'your_proxy_username';
const PROXY_PASS = 'your_proxy_password';

// === MAIN FUNCTION ===
(async () => {
  console.log('Launching Puppeteer...');

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      `--proxy-server=http://${PROXY}`,
      '--no-sandbox',
      '--disable-setuid-sandbox',
    ],
  });

  const page = await browser.newPage();

  // Proxy authentication
  await page.authenticate({
    username: PROXY_USER,
    password: PROXY_PASS,
  });

  try {
    console.log('Navigating to PrizePicks...');
    await page.goto(PRIZEPICKS_URL, {
      waitUntil: 'networkidle2',
      timeout: 60000,
    });

    console.log('Waiting for props to load...');
    await page.waitForSelector('[data-testid="stat-line"]', { timeout: 20000 });

    const props = await page.evaluate(() => {
      const cards = document.querySelectorAll('[data-testid="stat-line"]');
      const data = [];
      cards.forEach(card => {
        const name = card.querySelector('[data-testid="player-name"]')?.innerText || 'Unknown';
        const line = card.querySelector('[data-testid="projection-score"]')?.innerText || 'N/A';
        const statType = card.querySelector('[data-testid="stat-type"]')?.innerText || 'Unknown';
        data.push({ name, line, statType });
      });
      return data;
    });

    // Save or display
    fs.writeFileSync('prizepicks_props.json', JSON.stringify(props, null, 2));
    console.log(`✅ Saved ${props.length} props to prizepicks_props.json`);
  } catch (err) {
    console.error('❌ Error scraping:', err.message);
  } finally {
    await browser.close();
  }
})();
