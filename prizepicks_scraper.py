import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def human_delay(a=0.5, b=1.5):
    time.sleep(random.uniform(a, b))

def init_driver():
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)
    return driver

def scroll_to_bottom(driver, scroll_pause=1.5, max_scrolls=20):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_delay(scroll_pause, scroll_pause + 1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_prizepicks():
    print("[+] Loading PrizePicks page...")
    url = "https://www.prizepicks.com"
    driver = init_driver()
    driver.get(url)

    # Wait for cards to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'card') and .//div[contains(text(), 'MORE')]]"))
        )
    except:
        print("[-] Timeout waiting for prop cards to load.")
        driver.quit()
        return

    print("[+] Scrolling to load all props...")
    scroll_to_bottom(driver)

    card_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'card') and .//div[contains(text(), 'MORE')]]")

    if not card_elements:
        print("[-] Player cards not found.")
        driver.quit()
        return

    print(f"[+] Found {len(card_elements)} player prop cards.")

    props = []
    for card in card_elements:
        try:
            name = card.find_element(By.CLASS_NAME, "name__text").text
            stat = card.find_element(By.CLASS_NAME, "stat__text").text
            line = card.find_element(By.CLASS_NAME, "line__text").text
            props.append({"name": name, "stat": stat, "line": line})
        except:
            continue

    print("[+] Sample Props:")
    for prop in props[:10]:
        print(prop)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_filename = f"prizepicks_raw_{timestamp}.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print(f"[+] Raw HTML saved to {html_filename}")
    driver.quit()

if __name__ == "__main__":
    scrape_prizepicks()
