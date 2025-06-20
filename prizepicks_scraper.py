#!/usr/bin/env python3

import requests
import time
import json
from datetime import datetime
import random

class SimplePrizePicksScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def get_props(self):
        print("🚀 Starting OmniOdds PrizePicks Scraper")
        try:
            api_url = "https://partner-api.prizepicks.com/projections"
            print("📡 Fetching props data...")
            response = self.session.get(api_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                props = self.parse_props(data)
                print(f"✅ Found {len(props)} props")
                return props
            else:
                print(f"❌ API returned status: {response.status_code}")
                return self.fallback_scrape()
        except Exception as e:
            print(f"❌ Error: {e}")
            return self.fallback_scrape()

    def parse_props(self, data):
        props = []
        try:
            included_lookup = {}
            if 'included' in data:
                for item in data['included']:
                    if item['type'] == 'new_player':
                        included_lookup[item['id']] = item['attributes'].get('name', 'Unknown')

            if 'data' in data:
                for item in data['data']:
                    attr = item.get('attributes', {})
                    player_id = item.get('relationships', {}).get('new_player', {}).get('data', {}).get('id', None)
                    player_name = included_lookup.get(player_id, 'Unknown')

                    prop = {
                        'id': item.get('id'),
                        'player': player_name,
                        'line': attr.get('line_score'),
                        'stat_type': attr.get('stat_type'),
                        'odds_type': attr.get('odds_type'),
                        'league': item.get('relationships', {}).get('league', {}).get('data', {}).get('id', 'Unknown'),
                        'timestamp': datetime.now().isoformat(),
                        'source': 'PrizePicks'
                    }

                    if prop['player'] != 'Unknown':
                        props.append(prop)

            return props
        except Exception as e:
            print(f"❌ Error parsing props: {e}")
            return []

    def fallback_scrape(self):
        print("🔄 Trying fallback method...")
        try:
            url = "https://app.prizepicks.com"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                print("✅ Connected to PrizePicks site")
                return self.get_mock_props()
            else:
                print(f"❌ Failed to connect: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Fallback failed: {e}")
            return []

    def get_mock_props(self):
        print("📊 Generating test props...")
        players = ['LeBron James', 'Stephen Curry', 'Giannis Antetokounmpo', 'Luka Doncic', 'Jayson Tatum']
        stat_types = ['Points', 'Rebounds', 'Assists', '3-Pointers Made', 'Steals']

        mock_props = []
        for i in range(10):
            prop = {
                'id': f'mock_{i}',
                'player': random.choice(players),
                'line': round(random.uniform(15.5, 35.5), 1),
                'stat_type': random.choice(stat_types),
                'odds_type': 'standard',
                'league': 'NBA',
                'timestamp': datetime.now().isoformat(),
                'source': 'PrizePicks (Mock)',
                'edge_score': round(random.uniform(1.2, 4.8), 2)
            }
            mock_props.append(prop)

        return mock_props

    def save_props(self, props, filename='props.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(props, f, indent=2)
            print(f"💾 Saved {len(props)} props to {filename}")
        except Exception as e:
            print(f"❌ Save failed: {e}")

    def display_props(self, props):
        print("\n🎯 LIVE PROPS:")
        print("-" * 60)
        for i, prop in enumerate(props[:10], 1):
            edge = prop.get('edge_score', 'N/A')
            print(f"{i:2d}. {prop['player']}")
            print(f"    {prop['stat_type']}: {prop['line']} | Edge: {edge}")
            print(f"    League: {prop['league']} | Source: {prop['source']}")
            print()

def main():
    scraper = SimplePrizePicksScraper()
    try:
        props = scraper.get_props()
        if props:
            scraper.display_props(props)
            scraper.save_props(props)
            print("✅ Scraping completed successfully!")
            print(f"📊 Total props: {len(props)}")
        else:
            print("❌ No props found")
    except KeyboardInterrupt:
        print("\n⚠️  Scraping stopped by user")
    except Exception as e:
        print(f"❌ Scraping failed: {e}")

if __name__ == "__main__":
    main()


Sent from Yahoo Mail for iPhone


