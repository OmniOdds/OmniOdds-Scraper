const fs = require('fs');

// Read scraped data
const rawData = JSON.parse(fs.readFileSync('latest.json', 'utf8'));
const projections = rawData.data;
const included = rawData.included;

// Helper: link playerId to playerName and team
const playerInfoMap = {};
included.forEach(item => {
  if (item.type === 'new_player') {
    playerInfoMap[item.id] = {
      name: item.attributes.name,
      team: item.attributes.team,
      position: item.attributes.position
    };
  }
});

console.log("🧠 Formatted Props:\n");

projections.forEach((item) => {
  const attr = item.attributes;
  const playerId = item.relationships.new_player.data.id;
  const player = playerInfoMap[playerId] || {};

  const name = player.name || "Unknown";
  const team = player.team || "N/A";
  const pos = player.position || "";

  const stat = attr.stat_type || "Unknown";
  const displayStat = attr.stat_display_name || stat;
  const line = attr.line_score;
  const projectionType = attr.projection_type;
  const gameTime = attr.start_time;

  console.log(`📌 ${name} (${team} ${pos})`);
  console.log(`   🏀 Stat: ${displayStat} (${projectionType})`);
  console.log(`   📈 Line: ${line}`);
  console.log(`   ⏰ Game Time: ${gameTime}`);
  console.log('------------------------------------');
});
