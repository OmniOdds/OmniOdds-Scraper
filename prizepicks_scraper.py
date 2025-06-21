import requests
import json
import time

def fetch_prizepicks_props():
    url = "https://api.prizepicks.com/projections"
    params = {
        "league_id": "",      # All leagues
        "per_page": "250",    # Max per page
        "page": 1
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    all_data = []
    while True:
        print(f"[+] Fetching page {params['page']}...")
        res = requests.get(url, params=params, headers=headers)
        if res.status_code != 200:
            print(f"[!] Failed to fetch page {params['page']} (Status code: {res.status_code})")
            break
        
        page_data = res.json()
        if not page_data["data"]:
            break

        all_data.append(page_data)
        params["page"] += 1
        time.sleep(1.2)  # gentle delay to avoid detection

    return all_data[-1]  # Return last valid batch (you can merge all if you want full history)

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[✓] Saved {len(data['data'])} props to {filename}")

if __name__ == "__main__":
    print("[+] Fetching props from PrizePicks API...")
    props_data = fetch_prizepicks_props()
    save_json(props_data, "prizepicks_api_raw.json")
