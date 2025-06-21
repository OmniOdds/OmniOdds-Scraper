const fs = require('fs');

// Load raw data
const raw = JSON.parse(fs.readFileSync('prizepicks_mlb.json', 'utf8'));

// Check for props in 'data' if 'included' is missing
const source = raw.included && Array.isArray(raw.included)
  ? raw.included
  : raw.data || [];

if (!Array.isArray(source) || source.length === 0) {
  console.error("❌ No player data found in 'included' or 'data' fields.");
  process.exit(1);
}

// Filter out valid props
const players = source.filter(entry =>
  entry.type === 'new_player' || (entry.attributes && entry.attributes.name)
);

// Format props
const formatted = players.map(player => {
  const attr = player.attributes || {};
  return {
    player: attr.name,
    team: attr.team || 'N/A',
    stat_type: attr.stat_type || 'N/A',
    projection: attr.line_score || attr.line || 'N/A',
    position: attr.position || 'N/A'
  };
});

// Save output
fs.writeFileSync('mlb_formatted.json', JSON.stringify(formatted, null, 2));
console.log(`✅ Saved ${formatted.length} MLB props to mlb_formatted.json`);
