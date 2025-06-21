const fs = require('fs');

const rawData = fs.readFileSync('latest.json');
const jsonData = JSON.parse(rawData);

// Look inside either `included` or `data` array
const players = jsonData.included || jsonData.data;

if (!players || !Array.isArray(players)) {
  console.log("❌ No player data found in 'included' or 'data' fields.");
  process.exit(1);
}

const formatted = players
  .filter(entry => entry.type === "new_player")
  .map(entry => {
    const attr = entry.attributes;
    return {
      name: attr.name,
      team: attr.team,
      position: attr.position,
      projection: attr.line_score,
      stat_type: attr.stat_type,
    };
  });

console.log("🧾 MLB Props (Formatted Preview):");
console.log(formatted.slice(0, 10)); // just show first 10
