import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException

# -------- SETTINGS --------
PRIZEPICKS_URL = "https://app.prizepicks.com/"
SAVE_HTML_PATH = "debug.html"
USE_PROXY = False  # Change to True if adding a proxy

# -------- OPTIONAL PROXY (Soax example) --------
PROXY_HOST = "proxy.soax.com"
PROXY_PORT = 9000
PROXY_USER = "2etWvpLRQJYyBQN2"
PROXY_PASS = "wifi;;;;"

def get_chrome_options():
    options = Options()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    if USE_PROXY:
        options.add_argument(f'--proxy-server=http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}')

    return options

def setup_driver():
    options = get_chrome_options()
    driver = uc.Chrome(options=options)
    return driver

def scrape_prizepicks():
    try:
        driver = setup_driver()
        driver.get(PRIZEPICKS_URL)
        time.sleep(5)  # Let it load fully

        # Save page for debug purposes
        with open(SAVE_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        props = driver.find_elements(By.CLASS_NAME, "projection-container")
        print(f"Found {len(props)} props.")

        for prop in props:
            try:
                name = prop.find_element(By.CLASS_NAME, "name").text
                stat = prop.find_element(By.CLASS_NAME, "stat").text
                value = prop.find_element(By.CLASS_NAME, "score").text
                print(f"{name} | {stat} | {value}")
            except Exception as e:
                print("Error extracting prop:", str(e))

        driver.quit()

    except TimeoutException:
        print("Timeout while loading PrizePicks page.")
    except Exception as e:
        print("General scraping error:", str(e))

if __name__ == "__main__":
    scrape_prizepicks()
