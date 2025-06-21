import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def init_driver():
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")

    print("[+] Initializing Chrome...")
    driver = uc.Chrome(options=options, use_subprocess=True)
    return driver

def scroll_to_bottom(driver):
    print("[+] Scrolling to load all props...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_prizepicks():
    url = "https://app.prizepicks.com/"
    driver = init_driver()
    driver.get(url)

    print("[+] Loading PrizePicks page...")
    time.sleep(5)

    scroll_to_bottom(driver)

    print("[+] Saving HTML for debugging...")
    with open("prizepicks_raw.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    driver.quit()
    print("[✓] Raw HTML saved to prizepicks_raw.html")

if __name__ == "__main__":
    scrape_prizepicks()
