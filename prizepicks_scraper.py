import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

def scrape_prizepicks():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    
    try:
        print("[+] Loading PrizePicks page...")
        driver.get("https://www.prizepicks.com")
        time.sleep(5)  # Wait for JS to load the page

        print("[+] Scrolling to load all props...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        try:
            footer = driver.find_element(By.TAG_NAME, "footer")
            ActionChains(driver).move_to_element(footer).perform()
            time.sleep(2)
        except:
            print("[!] Footer not found, skipping...")

        html = driver.page_source
        with open("prizepicks_raw.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("[+] Raw HTML saved to prizepicks_raw.html")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_prizepicks()
