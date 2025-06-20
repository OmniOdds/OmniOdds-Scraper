import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json

def human_delay(min_sec=2, max_sec=4):
    """Randomized sleep to simulate human behavior"""
    time.sleep(random.uniform(min_sec, max_sec))

def init_driver():
    """Initialize a stealth Chrome driver"""
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = uc.Chrome(options=options)
    return driver

def extract_data_from_network(driver):
    """Navigate to PrizePicks and extract data"""
    driver.get("https://app.prizepicks.com/")
    human_delay(5, 7)
    
    # PrizePicks uses a public JSON endpoint
    api_url = "https://api.prizepicks.com/projections"
    driver.get(api_url)
    human_delay(3, 5)

    try:
        pre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        data = json.loads(pre.text)
        return data
    except Exception as e:
        print("Error fetching data:", e)
        return None
    finally:
        driver.quit()

def scrape_prizepicks():
    driver = init_driver()
    data = extract_data_from_network(driver)

    if not data:
        print("No data scraped.")
        return []

    props = []
    for entry in data.get('included', []):
        if entry['type'] == 'new_player':
            name = entry['attributes'].get('name')
            team = entry['attributes'].get('team')
            props.append({'player': name, 'team': team})
    
    return props

# Run the scraper
scraped_props = scrape_prizepicks()
for prop in scraped_props:
    print(prop)
