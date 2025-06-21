const fs = require('fs');
const axios = require('axios');

const url = 'https://api.prizepicks.com/projections?league_id=7&per_page=250&state=all'; // NBA league_id=7

const headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'Accept': 'application/json',
  'Origin': 'https://app.prizepicks.com',
  'Referer': 'https://app.prizepicks.com/',
};

async function scrapePrizePicks() {
  try {
    console.log("⏳ Fetching PrizePicks prop data...");
    const response = await axios.get(url, { headers });

    fs.writeFileSync('latest.json', JSON.stringify(response.data, null, 2));
    console.log("✅ Data saved to latest.json");
  } catch (err) {
    console.error("❌ Failed to fetch PrizePicks data:", err.message);
  }
}

scrapePrizePicks();
