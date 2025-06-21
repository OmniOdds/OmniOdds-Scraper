import time
import random
import json
import requests

class PrizePicksScraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://api.prizepicks.com/projections"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://app.prizepicks.com",
            "Referer": "https://app.prizepicks.com/",
        }

    def fetch_data(self):
        url = f"{self.base_url}?league_id=7&per_page=250"
        try:
            print(f"⚙️ Connecting to PrizePicks API: {url}")
            response = self.session.get(url, headers=self.headers, timeout=10)
            print(f"📡 Status Code: {response.status_code}")
            print("📄 Raw response preview:")
            print(response.text[:1000])

            if response.status_code == 200:
                data = response.json()
                self.save_data(data)
            else:
                print(f"❌ Error: Received status code {response.status_code}")
        except requests.RequestException as e:
            print(f"🚨 Exception occurred: {e}")

    def save_data(self, data):
        timestamp = int(time.time())
        filename = f"prizepicks_data_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Data saved to {filename}")

if __name__ == "__main__":
    scraper = PrizePicksScraper()
    scraper.fetch_data()
