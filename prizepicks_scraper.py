import json
import time
import random
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PrizePicksScraper:
    def __init__(self, headless=True, proxy=None):
        self.options = uc.ChromeOptions()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--window-size=1920,1080")
        if proxy:
            self.options.add_argument(f'--proxy-server={proxy}')
        self.driver = uc.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 15)
        self.data = []

    def load_proxies(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Proxy list not found: {filepath}")
        with open(filepath) as f:
            return [line.strip() for line in f if line.strip()]

    def human_delay(self, base=1.0):
        time.sleep(base + random.uniform(0.5, 1.5))

    def scrape(self):
        try:
            self.driver.get("https://app.prizepicks.com/")
            self.human_delay(2)

            # Wait for network request injection and data preload
            self.driver.execute_script("window.scrollTo(0, 500);")
            self.human_delay(2)

            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*=player-card]")))
            json_data = self.driver.execute_script("return window.__NUXT__")

            if not json_data:
                raise ValueError("No PrizePicks data was returned")

            projections = json_data['state']['projections']['all']
            players = json_data['state']['players']

            results = []
            for p in projections:
                player_info = players.get(str(p['player_id']), {})
                results.append({
                    "name": player_info.get("name"),
                    "team": player_info.get("team"),
                    "line": p.get("line_score"),
                    "stat_type": p.get("stat_type"),
                    "market_type": p.get("market_type"),
                    "game_time": p.get("game_time")
                })

            with open("prizepicks_props.json", "w") as f:
                json.dump(results, f, indent=2)
            print(f"✅ Scraped {len(results)} props successfully.")
        except Exception as e:
            print(f"Scraping error: {e}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    proxy_list_path = "allgeo-proxylist.txt"

    scraper = None
    try:
        proxy_list = PrizePicksScraper().load_proxies(proxy_list_path)
        for proxy in proxy_list:
            print(f"Using proxy: {proxy}")
            try:
                scraper = PrizePicksScraper(headless=True, proxy=proxy)
                scraper.scrape()
                break  # Exit loop if successful
            except Exception as e:
                print(f"Proxy failed: {proxy} -> {e}")
                continue
    except Exception as e:
        print(f"Setup error: {e}")
