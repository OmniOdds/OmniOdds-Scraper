const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
    ],
  });

  const page = await browser.newPage();

  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
  );

  console.log('➡️ Navigating to PrizePicks...');
  await page.goto('https://www.prizepicks.com', { waitUntil: 'networkidle2' });

  const apiUrl = 'https://api.prizepicks.com/projections';

  console.log('📡 Intercepting API...');
  const [response] = await Promise.all([
    page.waitForResponse(resp => resp.url().includes('/api/v2/players') && resp.status() === 200),
    page.goto('https://www.prizepicks.com', { waitUntil: 'networkidle2' }),
  ]);

  const json = await response.json();

  const props = {};
  for (const entry of json.included || []) {
    if (entry.type !== 'projection') continue;

    const sport = entry.attributes?.league || 'Unknown';
    if (!props[sport]) props[sport] = [];

    props[sport].push({
      name: entry.attributes?.athlete_name,
      stat: entry.attributes?.stat_type,
      line: entry.attributes?.line_score,
      team: entry.attributes?.team,
      game_time: entry.attributes?.start_time,
    });
  }

  console.log('✅ Scraped PrizePicks Props Grouped by Sport:\n');
  for (const [sport, entries] of Object.entries(props)) {
    console.log(`\n📂 ${sport} (${entries.length} props):`);
    for (const prop of entries) {
      console.log(`- ${prop.name} | ${prop.stat} | ${prop.line}`);
    }
  }

  await browser.close();
})();
