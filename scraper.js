const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const proxyServer = 'http://proxy.soax.com:9000'; // USE HTTP only
const proxyUsername = '2etWpVLrQJvYBQN2';
const proxyPassword = 'wif...'; // use full correct pass

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      `--proxy-server=${proxyServer}`,
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });

  const page = await browser.newPage();

  try {
    // Soax proxy login
    await page.authenticate({
      username: proxyUsername,
      password: proxyPassword
    });

    console.log('➡️ Connecting through proxy...');
    await page.goto('https://prizepicks.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });

    console.log('✅ Page loaded, intercepting /api/v2/players...');
    const [response] = await Promise.all([
      page.waitForResponse(res => res.url().includes('/api/v2/players') && res.status() === 200, { timeout: 30000 }),
      page.reload({ waitUntil: 'networkidle0' }) // triggers API call again
    ]);

    const data = await response.json();

    const sports = {};
    for (const item of data.included || []) {
      const name = item.attributes?.name;
      const stat = item.attributes?.stat_type;
      const line = item.attributes?.line_score;
      const sport = item.attributes?.league;

      if (!sports[sport]) sports[sport] = [];
      sports[sport].push({ player: name, stat, line });
    }

    console.log(JSON.stringify(sports, null, 2));
    await browser.close();
  } catch (err) {
    console.error('❌ Scraper error:', err.message);
    await browser.close();
  }
})();
