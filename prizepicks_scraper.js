// prizepicks_scraper.js

const axios = require('axios');
const fs = require('fs');

// Optional: you can rotate proxies or use headers here
const headers = {
  'Accept': 'application/json',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'Origin': 'https://app.prizepicks.com',
  'Referer': 'https://app.prizepicks.com/',
};

const url = 'https://api.prizepicks.com/projections?league_id=7&per_page=250';

async function fetchProps() {
  try {
    const response = await axios.get(url, { headers });
    const projections = response.data.included.filter(item => item.type === 'projection');
    
    const results = projections.map(p => ({
      player_id: p.id,
      player_name: p.attributes.name,
      stat_type: p.attributes.stat_type,
      line_score: p.attributes.line_score,
      game_id: p.attributes.game_id,
      is_live: p.attributes.is_live,
      is_promo: p.attributes.is_promo,
      group_key: p.attributes.group_key,
    }));

    fs.writeFileSync('prizepicks_live_data.json', JSON.stringify(results, null, 2));
    console.log('✅ Data saved to prizepicks_live_data.json');
  } catch (error) {
    console.error('❌ Failed to fetch PrizePicks data:', error.message);
  }
}

fetchProps();
