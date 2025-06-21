import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def setup_browser():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")  # Remove this if you want to see browser
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_prizepicks_props(sport='NBA'):
    url = "https://app.prizepicks.com/"
    driver = setup_browser()
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    try:
        # Click the sport filter tab
        sport_tab = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{sport}')]")))
        sport_tab.click()

        # Wait for player cards to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "player-card")))
        time.sleep(5)

        props = []
        cards = driver.find_elements(By.CLASS_NAME, "player-card")
        for card in cards:
            try:
                name = card.find_element(By.CLASS_NAME, "name").text
                stat_line = card.find_element(By.CLASS_NAME, "stat-line").text
                value = card.find_element(By.CLASS_NAME, "presale-score").text
                props.append({
                    "name": name,
                    "line": stat_line,
                    "value": value
                })
            except:
                continue

        with open("live_prizepicks_props.json", "w") as f:
            json.dump(props, f, indent=2)

        print(f"✅ Scraped {len(props)} props successfully.")
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_prizepicks_props("NBA")
