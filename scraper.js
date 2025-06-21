const fs = require("fs");
const axios = require("axios");
const HttpsProxyAgent = require("https-proxy-agent");

// Load Soax proxy list (format: username:password@ip:port)
const proxies = fs.readFileSync("us-proxylist.txt", "utf-8")
  .split("\n")
  .filter(p => p.trim() !== "");

async function fetchData(proxy) {
  const proxyUrl = `http://${proxy}`;
  const agent = new HttpsProxyAgent(proxyUrl);

  try {
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
      timeout: 8000,
    });

    console.log("✅ Success with proxy:", proxy);
    console.log("📊 Data Sample:", response.data.included?.slice(0, 2));
    return true;
  } catch (error) {
    console.log("❌ Failed with proxy:", proxy);
    return false;
  }
}

async function runWithRotation() {
  for (let i = 0; i < proxies.length; i++) {
    const proxy = proxies[i];
    console.log(`🔁 Trying proxy ${i + 1}/${proxies.length}: ${proxy}`);
    const success = await fetchData(proxy);
    if (success) return;
  }

  console.error("❌ All proxies failed. PrizePicks may be blocking all listed IPs or headers.");
}

runWithRotation();
