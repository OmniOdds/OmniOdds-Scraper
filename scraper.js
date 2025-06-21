const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const useProxy = require('puppeteer-page-proxy');

puppeteer.use(StealthPlugin());

const PROXY_HOST = 'proxy.soax.com';
const PROXY_PORT = '9000';
const PROXY_USERNAME = '2etWpVLRQJvYBQN2';
const PROXY_PASSWORD = 'your_full_password_here'; // Replace this

(async () => {
  try {
    console.log('🔁 Launching browser...');
    const browser = await puppeteer.launch({
      headless: true,
      args: [`--proxy-server=http=${PROXY_HOST}:${PROXY_PORT}`]
    });

    const page = await browser.newPage();

    await page.authenticate({
      username: PROXY_USERNAME,
      password: PROXY_PASSWORD
    });

    console.log('🌐 Navigating to PrizePicks...');
    await page.goto('https://app.prizepicks.com/', { waitUntil: 'networkidle2' });

    console.log('📡 Intercepting /api/v2/players...');
    let propsData = await new Promise((resolve, reject) => {
      let timeout;

      page.on('response', async (res) => {
        const url = res.url();
        if (url.includes('/api/v2/players')) {
          clearTimeout(timeout);
          const json = await res.json();

          const grouped = {};
          for (const item of json.included || []) {
            if (item.type === 'new_player') {
              const league = item.attributes.league;
              if (!grouped[league]) grouped[league] = [];
              grouped[league].push({
                name: item.attributes.name,
                team: item.attributes.team,
                position: item.attributes.position,
              });
            }
          }
          resolve(grouped);
        }
      });

      timeout = setTimeout(() => reject('❌ Timed out — no API data received'), 20000);
    });

    console.log('✅ Scraped PrizePicks props grouped by sport:');
    console.log(JSON.stringify(propsData, null, 2));

    await browser.close();
  } catch (err) {
    console.error('❌ ERROR:', err);
  }
})();
