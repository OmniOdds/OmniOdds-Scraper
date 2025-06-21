import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def get_stealth_driver():
    options = uc.ChromeOptions()
    options.headless = False  # Set to True only when sure it's stable
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    return driver

def scrape_prizepicks():
    url = "https://api.prizepicks.com/projections?league_id=7&per_page=250"
    driver = get_stealth_driver()

    try:
        driver.get(url)
        time.sleep(random.uniform(5, 8))

        body_text = driver.find_element(By.TAG_NAME, 'pre').text
        data = json.loads(body_text)

        filename = f"prizepicks_data_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Data saved to {filename}")

    except Exception as e:
        print(f"🚨 Scraper failed: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_prizepicks()
