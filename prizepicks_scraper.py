import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_browser():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    return uc.Chrome(options=options, headless=False)

def scrape_prizepicks_props():
    url = "https://app.prizepicks.com/"
    driver = setup_browser()
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    props = []

    try:
        print("⌛ Waiting for PrizePicks main container...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Home__HomeContainer")))

        print("✅ Page loaded. Waiting for props...")
        time.sleep(4)
        cards = driver.find_elements(By.CLASS_NAME, "player-card")

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
                print("⚠️ Error parsing a card:", err)

        with open("prizepicks_props.json", "w") as f:
            json.dump(props, f, indent=2)

        print(f"✅ Scraped {len(props)} props.")

    except Exception as e:
        print("❌ Fatal error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_prizepicks_props()
