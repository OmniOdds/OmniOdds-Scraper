// scraper.js

const axios = require('axios');
const fs = require('fs');

(async () => {
  try {
    console.log('🔄 Fetching all PrizePicks props by sport...');

    const response = await axios.get('https://api.prizepicks.com/projections');
    const data = response.data;

    const included = data.included || [];

    // Group by sport
    const sportsGrouped = {};

    included.forEach(entry => {
      if (entry.type === 'projection') {
        const sport = entry.attributes.league || 'unknown';

        if (!sportsGrouped[sport]) {
          sportsGrouped[sport] = [];
        }

        const line = entry.attributes.line_score || entry.attributes.line || null;
        const statName = entry.attributes.stat_type || entry.attributes.stat_display_name || '';
        const description = entry.attributes.description || '';
        const gameTime = entry.attributes.start_time || '';

        sportsGrouped[sport].push({
          description,
          stat: statName,
          line,
          game_time: gameTime,
          type: entry.attributes.projection_type || ''
        });
      }
    });

    // Save to file or print nicely
    Object.keys(sportsGrouped).forEach(sport => {
      const filename = `${sport.toLowerCase()}.json`;
      fs.writeFileSync(filename, JSON.stringify(sportsGrouped[sport], null, 2));
      console.log(`✅ Saved ${sportsGrouped[sport].length} props for ${sport} → ${filename}`);
    });

    console.log('✅ All sports props scraped and saved.');
  } catch (err) {
    console.error('❌ Failed to fetch PrizePicks props:', err.message);
  }
})();
