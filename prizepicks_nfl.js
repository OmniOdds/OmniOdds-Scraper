const fs = require('fs');
const axios = require('axios');

const url = 'https://api.prizepicks.com/projections?league_id=9&per_page=250&state=all'; // NFL league_id=9

const headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'Accept': 'application/json',
  'Origin': 'https://app.prizepicks.com',
  'Referer': 'https://app.prizepicks.com/',
};

async function scrapePrizePicks() {
  try {
    console.log("⏳ Fetching PrizePicks NFL prop data...");
    const response = await axios.get(url, { headers });

    fs.writeFileSync('prizepicks_nfl.json', JSON.stringify(response.data, null, 2));
    console.log("✅ NFL data saved to prizepicks_nfl.json");
  } catch (err) {
    console.error("❌ Failed to fetch NFL PrizePicks data:", err.message);
  }
}

scrapePrizePicks();
