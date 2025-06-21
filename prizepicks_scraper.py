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
    options.add_argument("--headless")  # Optional: Remove if you want visual mode
    return webdriver.Chrome(options=options)

def scrape_prizepicks_props(sport='NBA'):
    url = "https://app.prizepicks.com/"
    driver = setup_browser()
    driver.get(url)
    wait = WebDriverWait(driver, 40)

    props = []

    try:
        print("📡 Waiting for PrizePicks base container...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Home__HomeContainer")))

        print(f"🎯 Trying to select sport: {sport}...")
        time.sleep(2)  # Let the page settle

        # Try selecting the sport button
        try:
            sport_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{sport}')]")))
            sport_button.click()
            print("✅ Sport selected.")
        except:
            print("⚠️ Could not click sport button — may already be selected or not loaded.")

        print("📄 Waiting for player cards...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "player-card")))
        cards = driver.find_elements(By.CLASS_NAME, "player-card")

        print(f"🔍 Found {len(cards)} cards...")

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
            except Exception as err:
                print(f"⚠️ Failed to parse card: {err}")

        with open("live_prizepicks_props.json", "w") as f:
            json.dump(props, f, indent=2)

        print(f"✅ Scraped {len(props)} live props.")

    except Exception as e:
        print("❌ Fatal error during scrape:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_prizepicks_props("NBA")
