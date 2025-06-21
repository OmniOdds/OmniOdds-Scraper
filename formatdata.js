const fs = require('fs');

// Load the raw data
const rawData = JSON.parse(fs.readFileSync('latest.json'));

// Extract and clean the projection data
const cleanedProps = rawData.data
  .filter(item => item.type === "projection" && item.attributes?.line_score !== null)
  .map(item => ({
    player_name: item.attributes?.description || "Unknown",
    stat_type: item.attributes?.stat_type || "Unknown",
    line_score: item.attributes?.line_score || 0,
    start_time: item.attributes?.start_time || "Unknown",
    projection_type: item.attributes?.projection_type || "Unknown",
    is_live: item.attributes?.is_live || false
  }));

// Save to file
fs.writeFileSync('cleaned_props.json', JSON.stringify(cleanedProps, null, 2));
console.log("✅ Cleaned data saved to cleaned_props.json");
