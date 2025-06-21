import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load proxy credentials
load_dotenv()
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")

# Set up Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Add proxy settings
proxy_auth = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
options.add_argument(f"--proxy-server={proxy_auth}")

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("[*] Loading PrizePicks page...")
    driver.get("https://www.prizepicks.com")
    time.sleep(5)

    print("[*] Saving HTML for debugging...")
    with open("prizepicks_raw.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("[*] Raw HTML saved to prizepicks_raw.html")
except Exception as e:
    print(f"[!] Error: {e}")
finally:
    driver.quit()
