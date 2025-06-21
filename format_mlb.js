const fs = require('fs');

// Load the raw MLB JSON file
const raw = JSON.parse(fs.readFileSync('prizepicks_mlb.json', 'utf8'));

// Confirm valid structure
if (!raw || !raw.included || !Array.isArray(raw.included)) {
  console.error("❌ Invalid or missing 'included' field in prizepicks_mlb.json");
  process.exit(1);
}

// Extract new_player entries
const players = raw.included.filter(entry => entry.type === 'new_player');

// Format the props
const formatted = players.map(player => {
  const attr = player.attributes || {};
  return {
    player: attr.name,
    team: attr.team,
    stat_type: attr.stat_type || 'N/A',
    projection: attr.line_score || 'N/A',
    position: attr.position || 'N/A'
  };
});

// Save to file
fs.writeFileSync('mlb_formatted.json', JSON.stringify(formatted, null, 2));
console.log(`✅ Saved ${formatted.length} formatted props to mlb_formatted.json`);
