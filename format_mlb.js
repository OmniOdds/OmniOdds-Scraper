const fs = require('fs');

const rawData = fs.readFileSync('prizepicks_mlb.json');
const data = JSON.parse(rawData);

const formatted = data.included
  .filter(entry => entry.type === "new_player")
  .map(player => ({
    name: player.attributes.name,
    team: player.attributes.team,
    position: player.attributes.position,
    image: player.attributes.image_url,
    league: player.attributes.league,
    team_id: player.relationships?.team?.data?.id || 'N/A',
    league_id: player.attributes.league_id
  }));

console.log("✅ MLB Props (Formatted):\n");
formatted.slice(0, 10).forEach((p, i) => {
  console.log(`${i + 1}. ${p.name} (${p.position}) - ${p.team} [${p.league}]`);
  console.log(`   Image: ${p.image}`);
  console.log(`   Team ID: ${p.team_id} | League ID: ${p.league_id}`);
  console.log("------------------------------------------------");
});
