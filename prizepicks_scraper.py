import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = uc.Chrome(options=options)
    return driver

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def wait_for_props(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="player-card"]'))
        )
        print("[+] Player cards loaded.")
    except:
        print("[-] Player cards not found.")
        driver.quit()
        exit()

def extract_props(driver):
    props = []
    cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="player-card"]')
    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, '[data-testid="player-name"]').text
            stat = card.find_element(By.CSS_SELECTOR, '[data-testid="stat-category"]').text
            line = card.find_element(By.CSS_SELECTOR, '[data-testid="line-score"]').text
            props.append({
                "name": name,
                "stat": stat,
                "line": line
            })
        except Exception as e:
            continue
    return props

def main():
    url = "https://app.prizepicks.com"
    driver = setup_driver()
    print("[+] Loading PrizePicks page...")
    driver.get(url)

    wait_for_props(driver)
    print("[+] Scrolling to load all props...")
    scroll_to_bottom(driver)
    
    props = extract_props(driver)
    with open("prizepicks_props.json", "w") as f:
        json.dump(props, f, indent=2)

    print(f"[✓] Extracted {len(props)} props and saved to prizepicks_props.json.")
    driver.quit()

if __name__ == "__main__":
    main()
