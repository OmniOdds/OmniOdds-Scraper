import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    return driver

def scroll_full_page(driver, pause=2, scroll_count=20):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_prizepicks():
    url = "https://www.prizepicks.com"
    driver = init_driver()
    print("[+] Initializing Chrome...")
    driver.get(url)

    print("[+] Waiting for props to load...")
    time.sleep(8)

    print("[+] Scrolling to load all props...")
    scroll_full_page(driver, pause=2, scroll_count=25)

    print("[+] Saving HTML for debugging...")
    with open("prizepicks_raw.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    driver.quit()
    print("[+] Raw HTML saved to prizepicks_raw.html")

if __name__ == "__main__":
    scrape_prizepicks()
