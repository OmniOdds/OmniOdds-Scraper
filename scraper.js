const fs = require("fs");
const axios = require("axios");
const HttpsProxyAgent = require("https-proxy-agent");

// Load proxy list
const proxies = fs.readFileSync("us-proxylist.txt", "utf-8")
  .split("\n")
  .filter(line => line.trim() !== "");

const maxRetries = proxies.length;

async function fetchData(proxy) {
  try {
    const agent = new HttpsProxyAgent(`http://${proxy}`);

    const response = await axios.get("https://api.prizepicks.com/projections", {
      httpsAgent: agent,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://prizepicks.com",
        "Referer": "https://prizepicks.com/",
      },
      timeout: 8000
    });

    console.log("✅ Success with proxy:", proxy);
    console.log("📊 Data sample:", response.data.included?.slice(0, 2)); // optional preview
  } catch (err) {
    console.log(`❌ Failed with proxy: ${proxy}`);
    throw err;
  }
}

async function startScraper() {
  for (let i = 0; i < maxRetries; i++) {
    const proxy = proxies[i];
    console.log(`🌐 Trying proxy ${i + 1}/${maxRetries}: ${proxy}`);
    try {
      await fetchData(proxy);
      return;
    } catch (e) {
      console.log("Retrying with next proxy...");
    }
  }

  console.error("❌ All proxies failed. PrizePicks may be blocking all listed IPs.");
}

startScraper();
