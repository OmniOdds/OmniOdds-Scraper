const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const HttpsProxyAgent = require('https-proxy-agent');

puppeteer.use(StealthPlugin());

const proxies = [
  'wifijus:PLRQJYyBQN2@proxy.soax.com:9000'
];

const launchWithProxy = async (proxy) => {
  const proxyUrl = `http://${proxy}`;
  const agent = HttpsProxyAgent(proxyUrl);

  const browser = await puppeteer.launch({
    headless: true,
    args: [`--proxy-server=${proxyUrl}`, '--no-sandbox'],
  });

  const page = await browser.newPage();

  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
  );

  return { browser, page };
};

const scrapeWithRotation = async () => {
  for (let i = 0; i < proxies.length; i++) {
    const proxy = proxies[i];
    console.log(`🟡 Trying proxy ${i + 1}/${proxies.length}: ${proxy}`);

    try {
      const { browser, page } = await launchWithProxy(proxy);

      let data = null;

      page.on('response', async (response) => {
        const url = response.url();
        if (url.includes('/api/v2/players')) {
          try {
            const json = await response.json();
            data = json;
            console.log('✅ Successfully intercepted /api/v2/players');
            console.log(JSON.stringify(json, null, 2));
          } catch (err) {
            console.error('❌ Failed to parse JSON:', err.message);
          }
        }
      });

      await page.goto('https://prizepicks.com/', {
        waitUntil: 'networkidle2',
        timeout: 60000,
      });

      await page.waitForTimeout(7000); // Let all requests complete

      await browser.close();

      if (data) return data;
    } catch (error) {
      console.error(`❌ Proxy failed: ${proxy}`);
      console.error(error.message);
    }
  }

  throw new Error('All proxies failed. PrizePicks may be blocking all listed IPs.');
};

scrapeWithRotation().catch((err) => {
  console.error('❌ Scraping failed:', err.message);
});
