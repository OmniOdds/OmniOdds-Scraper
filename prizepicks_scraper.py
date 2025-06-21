import requests
import random
import time
import json

PROXIES = [
    "http://2etWvpLRQJYyBQN2:wifi5@proxy.soax.com:9000"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://prizepicks.com",
    "Referer": "https://prizepicks.com/",
}

def get_proxy():
    return {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}

def fetch_prizepicks_props(max_retries=5):
    all_props = []
    page = 1

    while True:
        url = f"https://api.prizepicks.com/projections?per_page=250&page={page}"
        for attempt in range(max_retries):
            try:
                proxy = get_proxy()
                print(f"[{page}] Fetching with proxy {proxy['http']} (Attempt {attempt + 1})")
                response = requests.get(url, headers=HEADERS, proxies=proxy, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    props = data.get("data", [])
                    if not props:
                        print(f"[{page}] No more props found.")
                        return all_props
                    all_props.extend(props)
                    print(f"[{page}] Fetched {len(props)} props.")
                    break
                elif response.status_code == 429:
                    print(f"[{page}] Rate limited (429). Sleeping 10s...")
                    time.sleep(10)
                else:
                    print(f"[{page}] Unexpected status code: {response.status_code}")
            except Exception as e:
                print(f"[{page}] Error: {e}")
                time.sleep(3)
        else:
            print(f"[{page}] Failed after {max_retries} attempts. Moving on...")
            break
        page += 1
        time.sleep(2)  # delay between pages

    return all_props

if __name__ == "__main__":
    print("[+] Fetching PrizePicks props with rotating proxies...")
    props = fetch_prizepicks_props()
    with open("prizepicks_api_raw.json", "w") as f:
        json.dump(props, f, indent=2)
    print(f"[✓] Saved {len(props)} props to prizepicks_api_raw.json")
