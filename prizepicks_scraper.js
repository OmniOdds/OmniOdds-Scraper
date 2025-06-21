const axios = require('axios');
const { HttpsProxyAgent } = require('https-proxy-agent');

// Soax proxy setup
const proxy = 'http://2etWVpLRQJYyBQN2:wifi;;;@proxy.soax.com:9000';
const agent = new HttpsProxyAgent(proxy);

(async () => {
  try {
    const response = await axios.get('https://api.prizepicks.com/projections', {
      httpsAgent: agent,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                      '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.prizepicks.com/',
        'Origin': 'https://www.prizepicks.com',
        'Host': 'api.prizepicks.com'
      }
    });

    console.log(JSON.stringify(response.data, null, 2));

  } catch (error) {
    console.error('❌ Failed to fetch PrizePicks data:', error.response?.status || error.message);
  }
})();
