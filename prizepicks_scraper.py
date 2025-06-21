#!/usr/bin/env python3

import requests
import time
import json
from datetime import datetime
import random

class DebugPrizePicksScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        })

    def get_props(self):
        print("🚀 OmniOdds Debug Scraper")
        url = "https://partner-api.prizepicks.com/projections"

        try:
            response = self.session.get(url, timeout=10)
            print(f"📡 Status Code: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    with open("raw_response.json", "w") as f:
                        json.dump(data, f, indent=2)
                    print("✅ Raw JSON saved to raw_response.json")

                    props = self.parse_props(data)
                    return props
                except Exception as e:
                    print(f"❌ JSON parse error: {e}")
                    print(response.text[:1000])  # Show preview
                    return []

            elif response.status_code in [403, 429]:
                print(f"🚫 BLOCKED - {response.status_code}: {response.reason}")
                return []

            else:
                print(f"❌ Unexpected status: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Request failed: {e}")
            return []

    def parse_props(self, data):
        props = []

        try:
            for item in data.get("included", []):
                attr = item.get("attributes", {})
                rel = item.get("relationships", {})
                player = attr.get("name") or attr.get("description")
                stat = attr.get("stat_type")
                line = attr.get("line_score")

                if player and line:
                    props.append({
                        "id": item.get("id"),
                        "player": player,
                        "line": line,
                        "stat_type": stat,
                        "odds_type": attr.get("odds_type"),
                        "league": rel.get("league", {}).get("data", {}).get("id"),
                        "timestamp": datetime.now().isoformat(),
                        "source": "PrizePicks"
                    })

        except Exception as e:
            print(f"❌ Parse Error: {e}")

        return props

    def save_props(self, props):
        try:
            with open("props.json", "w") as f:
                json.dump(props, f, indent=2)
            print(f"💾 Saved {len(props)} props to props.json")
        except Exception as e:
            print(f"❌ Save failed: {e}")

def main():
    scraper = DebugPrizePicksScraper()
    props = scraper.get_props()

    if props:
        scraper.save_props(props)
        print("✅ Scrape Complete!")
    else:
        print("⚠️ No props returned.")

if __name__ == "__main__":
    main()
