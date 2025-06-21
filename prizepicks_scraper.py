import os
import time
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Load credentials from .env
load_dotenv()
PROXY = os.getenv("SOAX_PROXY")  # format: user:pass@host:port

# Proxy config
proxy_parts = PROXY.split('@')
proxy_auth = proxy_parts[0]
proxy_host = proxy_parts[1]
options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--proxy-server=http://{proxy_host}')

# Launch browser
driver = uc.Chrome(options=options)
driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
    "headers": {
        "Proxy-Authorization": f"Basic {proxy_auth.encode('utf-8').hex()}"
    }
})

try:
    driver.get("https://www.prizepicks.com")
    time.sleep(8)  # wait for JS to load
    
    # Optional scroll to trigger lazy load
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(4)

    # Save full page
    with open("prizepicks_raw.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    print("[✅] Page scraped successfully.")

except Exception as e:
    print(f"[❌] Error: {e}")
finally:
    driver.quit()
