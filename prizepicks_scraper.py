import requests
import json
import time
import random

# Actual working proxy list - REPLACE with your real proxy IPs and credentials
PROXIES = [
    "http://user123:pass456@198.51.100.45:8000",
    "http://user123:pass456@203.0.113.12:8000",
    "http://user123:pass456@172.16.254.22:8000"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://app.prizepicks.com",
    "Referer": "https://app.prizepicks.com/"
}

API_URL = "https://api.prizepicks.com/projections?per_page=250&page={}"

def get_random_proxy():
    return { "http": random.choice(PROXIES), "https": random.choice(PROXIES) }

def fetch_props():
    all_props = []
    for page in range(1, 11):
        url = API_URL.format(page)
        print(f"[+] Fetching page {page}...")
        try:
            proxy = get_random_proxy()
            response = requests.get(url, headers=HEADERS, proxies=proxy, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if not data["data"]:
                    print("[*] No more data found.")
                    break
                all_props.extend(data["data"])
            elif response.status_code == 429:
                print(f"[!] Rate limited on page {page}. Retrying after delay...")
                time.sleep(random.randint(5, 10))
            else:
                print(f"[!] Unexpected status code {response.status_code} on page {page}")
        except Exception as e:
            print(f"[!] Error on page {page}: {e}")
            continue
        time.sleep(random.uniform(1, 2))

    with open("prizepicks_api_raw.json", "w") as f:
        json.dump(all_props, f, indent=2)
    print(f"[â] Saved {len(all_props)} props to prizepicks_api_raw.json")

if __name__ == "__main__":
    fetch_props()
