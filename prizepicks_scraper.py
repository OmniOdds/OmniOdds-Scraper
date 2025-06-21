import time
import random
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc

def load_proxies(file_path="allgeo-proxylist.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def get_random_proxy(proxies):
    return random.choice(proxies)

class PrizePicksScraper:
    def __init__(self, headless=True, proxy_list_path="allgeo-proxylist.txt"):
        self.headless = headless
        self.driver = None
        self.proxies = load_proxies(proxy_list_path)
        self.props_data = []
        self.setup_driver()

    def setup_driver(self):
        proxy = get_random_proxy(self.proxies)
        print(f"Using proxy: {proxy}")

        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument(f'--proxy-server={proxy}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")

        self.driver = uc.Chrome(options=options)

    def human_delay(self, min_time=1, max_time=3):
        time.sleep(random.uniform(min_time, max_time))

    def scrape_prizepicks(self):
        try:
            url = "https://app.prizepicks.com/"
            self.driver.get(url)
            self.human_delay(3, 5)

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='card']"))
            )
            self.human_delay()

            cards = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='card']")
            for card in cards:
                try:
                    player = card.find_element(By.CSS_SELECTOR, "div[class*='name']").text
                    stat = card.find_element(By.CSS_SELECTOR, "div[class*='stat']").text
                    line = card.find_element(By.CSS_SELECTOR, "div[class*='line']").text
                    team = card.find_element(By.CSS_SELECTOR, "div[class*='team']").text
                    self.props_data.append({
                        "player": player,
                        "stat": stat,
                        "line": line,
                        "team": team
                    })
                except Exception as e:
                    print(f"Failed to parse card: {e}")
                    continue

        except Exception as e:
            print(f"Scraping error: {e}")
        finally:
            self.driver.quit()

    def save_to_json(self, file_name="prizepicks_props.json"):
        with open(file_name, "w") as f:
            json.dump(self.props_data, f, indent=2)
        print(f"Saved {len(self.props_data)} props to {file_name}")

if __name__ == "__main__":
    scraper = PrizePicksScraper(headless=True)
    scraper.scrape_prizepicks()
    scraper.save_to_json()
