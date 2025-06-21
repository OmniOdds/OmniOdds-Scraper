import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

def scroll_to_bottom(driver, delay=2):
    """ Scrolls to bottom to trigger lazy loading """
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

options = uc.ChromeOptions()
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = uc.Chrome(options=options)

try:
    print("[+] Opening PrizePicks...")
    driver.get("https://app.prizepicks.com/")
    time.sleep(5)

    # Wait for PlayerCard elements to render
    timeout = time.time() + 15
    while time.time() < timeout:
        if driver.find_elements(By.CLASS_NAME, "PlayerCard"):
            break
        time.sleep(1)

    print("[+] Scrolling to load all props...")
    scroll_to_bottom(driver)

    with open("prizepicks_raw.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("[✓] Page saved to prizepicks_raw.html")

finally:
    driver.quit()
