import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")  # Optional: remove to see browser
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    return uc.Chrome(options=options)

def fetch_prizepicks_data(driver):
    url = "https://api.prizepicks.com/projections?league_id=7"  # NBA = 7, NFL = 2, etc.
    driver.get(url)
    time.sleep(3)

    try:
        pre = driver.find_element(By.TAG_NAME, "pre")
        json_data = json.loads(pre.text)

        print("✅ Data Fetched:")
        print(json.dumps(json_data, indent=2))
        return json_data
    except Exception as e:
        print("❌ Failed to fetch data:", str(e))
        return None

if __name__ == "__main__":
    print("⏳ Launching browser...")
    driver = create_driver()

    try:
        data = fetch_prizepicks_data(driver)
        if not data:
            print("⚠️ No data returned.")
    finally:
        driver.quit()
