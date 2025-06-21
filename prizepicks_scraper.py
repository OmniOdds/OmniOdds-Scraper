import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class PrizePicksScraper:
    def __init__(self):
        self.driver = self.setup_browser()
        self.props = []

    def setup_browser(self):
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        # HEADLESS MUST BE SET LIKE THIS FOR uc
        options.headless = True
        return uc.Chrome(options=options)

    def scrape_prizepicks_props(self):
        try:
            print("Loading PrizePicks...")
            self.driver.get("https://app.prizepicks.com/")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "projection-picks"))
            )
            print("PrizePicks loaded. Scraping...")

            props_elements = self.driver.find_elements(By.CLASS_NAME, "projection-pick")
            for elem in props_elements:
                try:
                    player = elem.find_element(By.CLASS_NAME, "name").text
                    stat = elem.find_element(By.CLASS_NAME, "stat").text
                    line = elem.find_element(By.CLASS_NAME, "score").text
                    self.props.append({
                        "player": player,
                        "stat": stat,
                        "line": line
                    })
                except Exception as e:
                    print("Skipped one prop due to:", str(e))

            with open("prizepicks_props.json", "w") as f:
                json.dump(self.props, f, indent=2)

            print(f"✅ Scraped {len(self.props)} props.")
        except TimeoutException:
            print("❌ Timed out loading PrizePicks.")
        except Exception as e:
            print("❌ Fatal error during scrape:", str(e))
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = PrizePicksScraper()
    scraper.scrape_prizepicks_props()
