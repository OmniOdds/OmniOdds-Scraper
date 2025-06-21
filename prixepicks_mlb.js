const fs = require('fs');
const axios = require('axios');

const url = 'https://api.prizepicks.com/projections?league_id=3&per_page=250&state=all'; // MLB league_id=3

const headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'Accept': 'application/json',
  'Origin': 'https://app.prizepicks.com',
  'Referer': 'https://app.prizepicks.com/',
};

async function scrapePrizePicks() {
  try {
    console.log("⏳ Fetching PrizePicks MLB prop data...");
    const response = await axios.get(url, { headers });

    fs.writeFileSync('prizepicks_mlb.json', JSON.stringify(response.data, null, 2));
    console.log("✅ MLB data saved to prizepicks_mlb.json");
  } catch (err) {
    console.error("❌ Failed to fetch MLB PrizePicks data:", err.message);
  }
}

scrapePrizePicks();
