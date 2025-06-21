import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# Setup Proxy
proxy_user = "2etWvpLRQJYyBQN2"
proxy_pass = "wifi;;;,"
proxy_host = "proxy.soax.com"
proxy_port = "9000"
proxy_string = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

def get_stealth_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--proxy-server={proxy_string}")
    return uc.Chrome(options=options)

def scrape_prizepicks():
    url = "https://app.prizepicks.com/"
    driver = get_stealth_driver()

    try:
        driver.get(url)
        time.sleep(random.uniform(5, 8))  # human-like delay

        print("[✔] Page loaded")
        # Wait and find prop elements — update selector as needed
        elements = driver.find_elements(By.CLASS_NAME, "name")  # example class

        if not elements:
            print("[!] No prop elements found.")
        else:
            for el in elements:
                print("Prop Name:", el.text)

    except Exception as e:
        print("[❌] Error scraping:", str(e))

    finally:
        driver.quit()

if __name__ == "__main__":
    print("[🚀] Scraping PrizePicks...")
    scrape_prizepicks()
