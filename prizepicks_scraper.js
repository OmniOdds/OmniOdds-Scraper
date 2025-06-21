const axios = require('axios');
const fs = require('fs');

async function fetchPrizePicksProps() {
  try {
    const response = await axios.get('https://api.prizepicks.com/projections');
    const data = response.data;

    if (data && data.included && data.data) {
      // You can format this however you'd like
      const result = data.data.map(player => {
        const attributes = player.attributes;
        return {
          name: attributes.name,
          stat_type: attributes.stat_type,
          line_score: attributes.line_score,
          team: attributes.team,
          position: attributes.position,
          projection_type: attributes.projection_type
        };
      });

      console.log('\n✅ Fetched live PrizePicks data:\n');
      console.log(result.slice(0, 5)); // just show top 5 for now

      // Optionally save to JSON file or send to your FastAPI
      fs.writeFileSync('prizepicks_data.json', JSON.stringify(result, null, 2));
    } else {
      console.log('❌ PrizePicks returned empty or invalid response.');
    }
  } catch (error) {
    console.error('❌ Failed to fetch PrizePicks data:', error.message);
  }
}

fetchPrizePicksProps();
