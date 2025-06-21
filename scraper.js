const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const proxyServer = 'proxy.soax.com:9000';
const proxyUsername = '2etWpVLrQJvYBQN2';
const proxyPassword = 'wif...'; // ← your real Soax password

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      `--proxy-server=http://${proxyServer}`,
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });

  const page = await browser.newPage();

  // Authenticate to Soax Proxy
  await page.authenticate({
    username: proxyUsername,
    password: proxyPassword
  });

  try {
    console.log('➡️ Navigating to PrizePicks...');
    await page.goto('https://prizepicks.com/', { waitUntil: 'networkidle2', timeout: 60000 });

    console.log('⏳ Intercepting props API...');
    const [response] = await Promise.all([
      page.waitForResponse(response =>
        response.url().includes('/api/v2/players') && response.status() === 200,
        { timeout: 60000 }
      ),
      page.reload({ waitUntil: 'networkidle0' }) // Trigger another request
    ]);

    const data = await response.json();

    // Group props by sport
    const sports = {};
    for (const item of data.included || []) {
      const { attributes, relationships } = item;
      const playerName = attributes?.name;
      const statType = attributes?.stat_type;
      const line = attributes?.line_score;
      const sport = attributes?.league;

      if (!sports[sport]) sports[sport] = [];

      sports[sport].push({
        player: playerName,
        stat: statType,
        line: line
      });
    }

    console.log('✅ Scraped props by sport:\n');
    console.log(JSON.stringify(sports, null, 2));

  } catch (error) {
    console.error('❌ Scraper error:', error.message);
  } finally {
    await browser.close();
  }
})();
