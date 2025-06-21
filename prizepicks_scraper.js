const fs = require('fs');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

const PROXY_HOST = 'proxy.soax.com';
const PROXY_PORT = '9000';
const PROXY_USER = 'your_soax_user';
const PROXY_PASS = 'your_soax_pass';

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

  console.log('🔄 Navigating to PrizePicks...');
  await page.goto('https://app.prizepicks.com/', { waitUntil: 'networkidle2', timeout: 60000 });

  try {
    await page.waitForSelector('.projection-card', { timeout: 15000 });
  } catch (err) {
    console.error('❌ Props not found in time.');
    await browser.close();
    return;
  }

  const props = await page.evaluate(() => {
    const cards = document.querySelectorAll('.projection-card');
    const data = [];

    cards.forEach(card => {
      const name = card.querySelector('.name')?.innerText || 'N/A';
      const stat = card.querySelector('.stat')?.innerText || 'N/A';
      const line = card.querySelector('.score')?.innerText || 'N/A';
      data.push({ name, stat, line });
    });

    return data;
  });

  fs.writeFileSync('prizepicks_props.json', JSON.stringify(props, null, 2));
  console.log(`✅ Saved ${props.length} props to prizepicks_props.json`);

  await browser.close();
})();
