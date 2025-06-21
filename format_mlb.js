const fs = require('fs');

// Read MLB JSON data from correct file
const rawData = fs.readFileSync('prizepicks_mlb.json');
const jsonData = JSON.parse(rawData);

// Access 'included' or fallback to 'data' array
const players = jsonData.included || jsonData.data;

if (!players || !Array.isArray(players)) {
  console.error("❌ No player data found in 'included' or 'data' fields.");
  process.exit(1);
}

// Filter and map player props
const formatted = players
  .filter(entry => entry.type === "new_player" && entry.attributes)
  .map(entry => {
    const attr = entry.attributes;
    return {
      name: attr.name,
      team: attr.team || attr.team_name || 'N/A',
      position: attr.position,
      projection: attr.line_score,
      stat_type: attr.stat_type,
    };
  });

console.log("🧾 MLB Props (Formatted Preview):");
console.log(formatted.slice(0, 10)); // Show first 10
