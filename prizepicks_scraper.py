import requests
import json
import time
import random

# === Load proxies from file ===
def load_proxies(file_path='allgeo-proxylist.txt'):
    with open(file_path, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

PROXIES = load_proxies()

def get_proxy():
    proxy = random.choice(PROXIES)
    return {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

# === Scraper logic ===
def fetch_props():
    all_props = []
    base_url = "https://api.prizepicks.com/projections"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    for page in range(1, 15):
        params = {
            "per_page": 250,
            "page": page
        }

        proxy = get_proxy()
        try:
            print(f"[+] Fetching page {page} with proxy: {proxy['http']}")
            response = requests.get(base_url, headers=headers, params=params, proxies=proxy, timeout=15)

            if response.status_code == 200:
                data = response.json()
                props = data.get("data", [])
                print(f"[✓] Page {page}: {len(props)} props")
                all_props.extend(props)
            elif response.status_code == 429:
                print("[!] Rate limited. Sleeping 10 seconds...")
                time.sleep(10)
                continue
            else:
                print(f"[!] Page {page} failed with status {response.status_code}")
        except Exception as e:
            print(f"[!] Error on page {page}: {str(e)}")

        time.sleep(random.uniform(1.5, 3.5))  # simulate human delay

    # === Save output ===
    with open("prizepicks_api_raw.json", "w") as f:
        json.dump(all_props, f, indent=2)
    print(f"[✓] Saved {len(all_props)} props to prizepicks_api_raw.json")

if __name__ == "__main__":
    fetch_props()
