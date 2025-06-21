import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def human_delay(a=1.5, b=3.5):
    time.sleep(random.uniform(a, b))

def setup_driver():
    options = uc.ChromeOptions()
    options.headless = False  # Show browser for debugging
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    return driver

def fetch_prizepicks_props():
    url = "https://www.prizepicks.com/"
    driver = setup_driver()
    driver.get(url)

    try:
        print("[INFO] Page loaded. Waiting for prop elements...")

        # Wait for elements that might indicate props loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "projection-card"))
        )

        elements = driver.find_elements(By.CLASS_NAME, "projection-card")
        print(f"[INFO] Found {len(elements)} prop cards.")

        props = []
        for el in elements:
            try:
                name = el.find_element(By.CLASS_NAME, "name").text
                stat = el.find_element(By.CLASS_NAME, "stat").text
                line = el.find_element(By.CLASS_NAME, "presale-score").text
                props.append({
                    "player": name,
                    "stat": stat,
                    "line": line
                })
                human_delay(0.5, 1.2)
            except Exception as e:
                print("[WARN] Error parsing element:", e)

        print(f"\n✅ Scraped {len(props)} props:")
        for prop in props:
            print(prop)

        # DEBUG: Save HTML for inspection
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            print("[DEBUG] Saved page as debug.html for manual inspection.")

    except Exception as e:
        print("❌ Error fetching data:", e)

    driver.quit()

if __name__ == "__main__":
    fetch_prizepicks_props()
