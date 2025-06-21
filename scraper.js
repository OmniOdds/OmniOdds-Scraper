const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs-extra');

puppeteer.use(StealthPlugin());

const scrapePrizePicks = async () => {
    console.log("🟡 Launching browser...");
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try {
        console.log("🔁 Navigating to PrizePicks...");
        await page.goto('https://www.prizepicks.com/', {
            waitUntil: 'networkidle2',
            timeout: 60000
        });

        console.log("🔍 Intercepting network for props data...");
        let dataFound = false;
        let retries = 0;

        while (!dataFound && retries < 5) {
            const [response] = await Promise.all([
                page.waitForResponse(resp => 
                    resp.url().includes('/api/v2/players') && resp.status() === 200, { timeout: 15000 }
                ).catch(() => null),
                page.reload({ waitUntil: 'networkidle2' }),
            ]);

            if (response) {
                const json = await response.json();
                const bySport = {};

                json.included?.forEach(playerProp => {
                    const sport = playerProp.attributes?.league || 'Unknown';
                    const entry = {
                        name: playerProp.attributes?.name,
                        stat_type: playerProp.attributes?.stat_type,
                        line: playerProp.attributes?.line_score,
                        game_time: playerProp.attributes?.start_time
                    };

                    if (!bySport[sport]) bySport[sport] = [];
                    bySport[sport].push(entry);
                });

                await fs.writeJson('prizepicks_all_sports.json', bySport, { spaces: 2 });
                console.log("✅ Props data saved to prizepicks_all_sports.json");
                dataFound = true;
            } else {
                console.log(`⏳ Retry #${++retries}...`);
                await new Promise(res => setTimeout(res, 3000));
            }
        }

        if (!dataFound) console.log("❌ Failed to fetch PrizePicks props after retries.");

    } catch (error) {
        console.error("🔥 Scraper failed:", error);
    } finally {
        await browser.close();
    }
};

scrapePrizePicks();
