import requests
import json

def fetch_prizepicks_props():
    url = "https://api.prizepicks.com/projections"
    params = {
        "league_id": "",  # Leave blank for all
        "per_page": 250,
        "page": 1
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    print("[+] Fetching props from PrizePicks API...")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"[!] Error: {response.status_code}")
        return

    data = response.json()
    with open("prizepicks_api_raw.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"[+] Saved {len(data['included'])} props to prizepicks_api_raw.json")

if __name__ == "__main__":
    fetch_prizepicks_props()
