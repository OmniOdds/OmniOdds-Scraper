import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_browser():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")  # Remove this if you want to see it visually
    return webdriver.Chrome(options=options)

def scrape_prizepicks_props(sport='NBA'):
    url = "https://app.prizepicks.com/"
    driver = setup_browser()
    driver.get(url)
    wait = WebDriverWait(driver, 25)

    props = []

    try:
        print("📡 Waiting for PrizePicks to load...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sports-tabs")))

        # Click sport filter
        print(f"🎯 Selecting {sport}...")
        sport_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{sport}')]")))
        sport_button.click()
        time.sleep(3)

        print("📄 Waiting for player cards to load...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "player-card")))
        cards = driver.find_elements(By.CLASS_NAME, "player-card")

        print(f"🔍 Found {len(cards)} cards, scraping...")

        for card in cards:
            try:
                name = card.find_element(By.CLASS_NAME, "name").text
                stat = card.find_element(By.CLASS_NAME, "stat-line").text
                value = card.find_element(By.CLASS_NAME, "presale-score").text
                props.append({
                    "name": name,
                    "line": stat,
                    "value": value
                })
            except Exception as card_error:
                print("⚠️ Failed to parse a card:", card_error)
                continue

        # Save props
        with open("live_prizepicks_props.json", "w") as f:
            json.dump(props, f, indent=2)

        print(f"✅ Successfully scraped {len(props)} props!")
    except Exception as e:
        print("❌ Error during scraping:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_prizepicks_props("NBA")
