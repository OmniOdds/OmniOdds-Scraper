# prizepicks_scraper.py
import requests
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://app.prizepicks.com/",
    "Origin": "https://app.prizepicks.com",
    "X-Requested-With": "XMLHttpRequest",
}

def fetch_prizepicks_props():
    url = "https://api.prizepicks.com/projections?league_id=7"  # NBA

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        with open("prizepicks_data.json", "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Data scraped and saved to prizepicks_data.json")
        return data

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return None

if __name__ == "__main__":
    print("📡 Scraping PrizePicks props...")
    fetch_prizepicks_props()
