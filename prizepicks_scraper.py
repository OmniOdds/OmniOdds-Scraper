import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

# SOAX Proxy Credentials (inserted as requested)
PROXY_HOST = "proxy.soax.com"
PROXY_PORT = 9000
PROXY_USER = "2etWvpLRQJYyBQN2"
PROXY_PASS = "wifi;;;;"

def create_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless=new")

    # Set proxy
    chrome_options.add_argument(f'--proxy-server=http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}')

    driver = uc.Chrome(options=chrome_options)
    return driver

def scrape_prizepicks():
    url = "https://app.prizepicks.com/"
    driver = create_driver()
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("[✓] Page loaded")

        time.sleep(5)  # Give time for JS to render the data

        script = """return window.__NUXT__ ? window.__NUXT__.state : null;"""
        data = driver.execute_script(script)

        if data:
            with open("prizepicks_data.json", "w") as f:
                json.dump(data, f, indent=2)
            print("[✓] Data saved to prizepicks_data.json")
        else:
            print("[✗] No data extracted.")
    except Exception as e:
        print("[!] Error fetching PrizePicks data:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_prizepicks()
