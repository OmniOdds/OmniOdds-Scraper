const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const proxy = 'http://YOUR_SOAX_PROXY:PORT'; // e.g. http://us1234.proxy.soax.com:9000
const proxyUsername = 'YOUR_SOAX_USERNAME';
const proxyPassword = 'YOUR_SOAX_PASSWORD';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      `--proxy-server=${proxy}`
    ]
  });

  const page = await browser.newPage();

  // Proxy authentication
  await page.authenticate({
    username: proxyUsername,
    password: proxyPassword
  });

  try {
    console.log('Connecting to PrizePicks...');
    await page.goto('https://app.prizepicks.com/', { waitUntil: 'networkidle2', timeout: 60000 });

    console.log('Waiting for props to load...');
    await page.waitForSelector('.projection-table', { timeout: 60000 });

    const props = await page.evaluate(() => {
      const data = [];
      const cards = document.querySelectorAll('.projection-table .projection-card');
      cards.forEach(card => {
        const player = card.querySelector('.name')?.innerText.trim();
        const statLine = card.querySelector('.stat')?.innerText.trim();
        const line = card.querySelector('.score')?.innerText.trim();

        if (player && statLine && line) {
          data.push({
            player,
            statLine,
            line
          });
        }
      });
      return data;
    });

    fs.writeFileSync('prizepicks_props.json', JSON.stringify(props, null, 2));
    console.log(`✅ Scraped ${props.length} props and saved to prizepicks_props.json`);

  } catch (err) {
    console.error('❌ Scrape failed:', err.message);
  } finally {
    await browser.close();
  }
})();
