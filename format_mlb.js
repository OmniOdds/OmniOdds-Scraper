const fs = require('fs');

// Read the raw MLB JSON file
const rawData = fs.readFileSync('prizepicks_mlb.json');
const json = JSON.parse(rawData);

// Confirm the structure
if (!json || !Array.isArray(json.data)) {
  console.error("❌ 'data' field missing or not an array in prizepicks_mlb.json");
  process.exit(1);
}

// Extract and format the props
const formatted = json.data.map((entry) => {
  const attr = entry.attributes || {};
  return {
    name: attr.name || "Unknown",
    stat_type: attr.stat_type || "Unknown",
    line_score: attr.line_score || "N/A",
    team: attr.team || "Unknown",
    projection_type: attr.projection_type || "Unknown",
  };
});

// Output
console.log("✅ MLB Props (Formatted Preview):\n");
formatted.slice(0, 10).forEach((p, i) => {
  console.log(`${i + 1}. ${p.name} – ${p.stat_type}: ${p.line_score} [${p.team}]`);
});
