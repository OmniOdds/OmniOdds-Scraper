const fs = require('fs');
const axios = require('axios');

// URL for PrizePicks raw player prop data
const url = 'https://api.prizepicks.com/api/v2/players';

// Optional headers to mimic a real browser
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
    
    // Save raw data to file
    fs.writeFileSync('latest.json', JSON.stringify(response.data, null, 2));
    
    console.log("✅ Successfully saved to latest.json");
  } catch (err) {
    console.error("❌ Failed to fetch PrizePicks data:", err.message);
  }
}

scrapePrizePicks();
