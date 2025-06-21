import time
import json
import random
import requests

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://app.prizepicks.com",
    "referer": "https://app.prizepicks.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

# 🔁 Proxy rotation list (replace with your own proxies)
PROXIES = [
    "http://username:password@proxy1.example.com:8000",
    "http://username:password@proxy2.example.com:8000",
    "http://username:password@proxy3.example.com:8000"
]

def get_proxy():
    return {
        "http": random.choice(PROXIES),
        "https": random.choice(PROXIES),
    }

def fetch_props(pages=10):
    all_props = []
    for page in range(1, pages + 1):
        print(f"[+] Fetching page {page}...")
        url = f"https://api.prizepicks.com/projections?per_page=250&page={page}"
        try:
            response = requests.get(url, headers=HEADERS, proxies=get_proxy(), timeout=10)

            if response.status_code == 429:
                print(f"[!] Rate limited on page {page}, skipping...")
                continue
            elif response.status_code != 200:
                print(f"[!] Failed to fetch page {page}: HTTP {response.status_code}")
                continue

            data = response.json()
            projections = data.get("data", [])
            all_props.extend(projections)

            time.sleep(random.uniform(2, 4))  # Random delay to reduce bot detection

        except Exception as e:
            print(f"[!] Error fetching page {page}: {e}")
            continue

    return all_props

def save_to_file(data, filename="prizepicks_api_raw.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[✓] Saved {len(data)} props to {filename}")

if __name__ == "__main__":
    print("[+] Fetching props from PrizePicks API using rotating proxies...")
    props = fetch_props()
    save_to_file(props)
