#!/usr/bin/env python3
"""
Military-Grade PrizePicks Scraper
Advanced anti-detection bypass with human simulation
"""

import requests
import json
import re
import time
import random
import ssl
import base64
import hashlib
from urllib.parse import urlencode
from datetime import datetime
import os
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
import fake_useragent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MilitaryGradeScraper:
    """Advanced anti-detection scraper with military-grade techniques"""
    
    def __init__(self):
        self.session_pool = []
        self.user_agents = []
        self.proxy_list = []
        self.success_count = 0
        self.failure_count = 0
        self.blocked_count = 0
        self.last_success_time = 0
        self.rotation_index = 0
        
        # Advanced headers pool
        self.header_sets = [
            # Chrome Windows
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'origin': 'https://app.prizepicks.com',
                'referer': 'https://app.prizepicks.com/',
            },
            # iPhone Safari
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'origin': 'https://app.prizepicks.com',
                'referer': 'https://app.prizepicks.com/',
            },
            # Edge Windows
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'origin': 'https://app.prizepicks.com',
                'referer': 'https://app.prizepicks.com/',
            }
        ]
        
        # Endpoint rotation
        self.endpoints = [
            'https://api.prizepicks.com/projections',
            'https://api.prizepicks.com/projections?league_id=7&per_page=250',
            'https://mobile-api.prizepicks.com/projections',
            'https://partner-api.prizepicks.com/projections',
            'https://client-api.prizepicks.com/projections',
            'https://web-api.prizepicks.com/projections',
            'https://app.prizepicks.com/api/projections',
            'https://backend.prizepicks.com/projections',
            'https://feed.prizepicks.com/projections',
            'https://live.prizepicks.com/projections',
            'https://api-v2.prizepicks.com/projections',
            'https://cdn.prizepicks.com/projections',
        ]
        
        self.init_sessions()
        
    def init_sessions(self):
        """Initialize multiple HTTP sessions with different configurations"""
        print("[INIT] Creating session pool...")
        
        for i in range(5):
            session = requests.Session()
            
            # Random retry strategy
            retry_strategy = Retry(
                total=3,
                backoff_factor=random.uniform(0.5, 2.0),
                status_forcelist=[429, 500, 502, 503, 504],
            )
            
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            
            # Random timeout
            session.timeout = random.uniform(10, 20)
            
            self.session_pool.append(session)
            
        print(f"[INIT] Created {len(self.session_pool)} sessions")
    
    def get_advanced_headers(self):
        """Get randomized headers with advanced fingerprinting"""
        headers = random.choice(self.header_sets).copy()
        
        # Add random headers for uniqueness
        headers.update({
            'cache-control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'pragma': random.choice(['no-cache', '']),
            'dnt': str(random.randint(0, 1)),
            'upgrade-insecure-requests': '1',
            'x-requested-with': random.choice(['XMLHttpRequest', '']),
        })
        
        # Random viewport size
        if 'sec-ch-viewport' not in headers:
            width = random.choice([1920, 1366, 1440, 1536, 1280])
            height = random.choice([1080, 768, 900, 864, 720])
            headers['sec-ch-viewport-width'] = str(width)
            headers['sec-ch-viewport-height'] = str(height)
        
        return headers
    
    def human_delay(self):
        """Simulate human-like delays"""
        base_delay = random.uniform(2.0, 5.0)
        jitter = random.uniform(0.1, 1.0)
        
        # Add extra delay if we've been blocked recently
        if self.blocked_count > 0:
            penalty = min(self.blocked_count * 2, 30)
            base_delay += penalty
            print(f"[DELAY] Adding {penalty}s penalty (blocked {self.blocked_count} times)")
        
        total_delay = base_delay + jitter
        print(f"[DELAY] Waiting {total_delay:.1f}s...")
        time.sleep(total_delay)
    
    def curl_fallback(self, url, headers):
        """Use curl as fallback with advanced options"""
        try:
            print("[CURL] Attempting curl fallback...")
            
            # Build curl command
            cmd = [
                'curl', '-s', '-L', '--max-time', '15',
                '--user-agent', headers.get('User-Agent', ''),
                '--header', 'Accept: application/json',
                '--header', f'Referer: {headers.get("referer", "")}',
                '--header', f'Origin: {headers.get("origin", "")}',
                '--compressed',
                '--http2',
                '--tlsv1.2',
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)
                    print("[CURL] Success!")
                    return data
                except json.JSONDecodeError:
                    print("[CURL] Invalid JSON response")
            else:
                print(f"[CURL] Failed: {result.stderr}")
                
        except Exception as e:
            print(f"[CURL] Error: {e}")
        
        return None
    
    def multi_method_request(self, url):
        """Try multiple methods to bypass detection"""
        methods_tried = []
        
        # Method 1: Session pool rotation
        for i, session in enumerate(self.session_pool):
            try:
                headers = self.get_advanced_headers()
                print(f"[SESSION-{i}] Trying {url}...")
                
                response = session.get(url, headers=headers, verify=False, timeout=15)
                methods_tried.append(f"session-{i}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"[SESSION-{i}] SUCCESS!")
                        self.success_count += 1
                        self.last_success_time = time.time()
                        return data, f"session-{i}"
                    except json.JSONDecodeError:
                        print(f"[SESSION-{i}] Invalid JSON")
                        continue
                        
                elif response.status_code == 403:
                    print(f"[SESSION-{i}] Blocked (403)")
                    self.blocked_count += 1
                    continue
                    
                elif response.status_code == 429:
                    print(f"[SESSION-{i}] Rate limited (429)")
                    self.blocked_count += 1
                    continue
                    
                else:
                    print(f"[SESSION-{i}] HTTP {response.status_code}")
                    self.failure_count += 1
                    
            except Exception as e:
                print(f"[SESSION-{i}] Error: {e}")
                methods_tried.append(f"session-{i}-error")
                continue
        
        # Method 2: Curl fallback
        headers = self.get_advanced_headers()
        curl_result = self.curl_fallback(url, headers)
        methods_tried.append("curl")
        
        if curl_result:
            self.success_count += 1
            return curl_result, "curl"
        
        # Method 3: Raw socket with custom TLS
        try:
            print("[SOCKET] Attempting raw socket...")
            methods_tried.append("socket")
            
            import socket
            import ssl as ssl_module
            from urllib.parse import urlparse
            
            parsed = urlparse(url)
            host = parsed.hostname
            port = 443
            path = parsed.path + ('?' + parsed.query if parsed.query else '')
            
            # Create socket with custom TLS
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            context = ssl_module.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl_module.CERT_NONE
            
            wrapped_sock = context.wrap_socket(sock, server_hostname=host)
            wrapped_sock.connect((host, port))
            
            # Send HTTP request
            headers = self.get_advanced_headers()
            http_request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n"
            for key, value in headers.items():
                http_request += f"{key}: {value}\r\n"
            http_request += "\r\n"
            
            wrapped_sock.send(http_request.encode())
            
            # Read response
            response = b""
            while True:
                try:
                    chunk = wrapped_sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                    if b'\r\n\r\n' in response and len(response) > 1000:
                        break
                except:
                    break
            
            wrapped_sock.close()
            
            # Parse response
            response_str = response.decode('utf-8', errors='ignore')
            if '200 OK' in response_str:
                json_start = response_str.find('{')
                if json_start != -1:
                    json_str = response_str[json_start:]
                    try:
                        data = json.loads(json_str)
                        print("[SOCKET] SUCCESS!")
                        self.success_count += 1
                        return data, "socket"
                    except json.JSONDecodeError:
                        pass
            
        except Exception as e:
            print(f"[SOCKET] Error: {e}")
        
        # Method 4: Browser automation with undetected-chromedriver
        try:
            print("[BROWSER] Attempting browser automation...")
            methods_tried.append("browser")
            
            browser_result = self.browser_fallback(url)
            if browser_result:
                self.success_count += 1
                return browser_result, "browser"
                
        except Exception as e:
            print(f"[BROWSER] Error: {e}")
        
        self.failure_count += 1
        return None, f"all-failed-{'-'.join(methods_tried)}"
    
    def browser_fallback(self, url):
        """Ultimate fallback: Real browser automation"""
        driver = None
        try:
            print("[BROWSER] Launching stealth browser...")
            
            # Try different browser configurations
            configs = [
                {'headless': True, 'args': ['--no-sandbox', '--disable-dev-shm-usage']},
                {'headless': False, 'args': ['--disable-blink-features=AutomationControlled']},
            ]
            
            for config in configs:
                try:
                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options
                    from selenium.webdriver.chrome.service import Service
                    import shutil
                    
                    options = Options()
                    if config['headless']:
                        options.add_argument('--headless')
                    
                    for arg in config['args']:
                        options.add_argument(arg)
                    
                    options.add_argument('--disable-gpu')
                    options.add_argument('--disable-features=VizDisplayCompositor')
                    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)
                    
                    # Set Chrome binary
                    chrome_path = shutil.which('chromium') or '/usr/bin/chromium'
                    options.binary_location = chrome_path
                    
                    service = Service()
                    driver = webdriver.Chrome(service=service, options=options)
                    
                    # Navigate and extract
                    driver.get(url)
                    time.sleep(5)
                    
                    # Try to extract JSON from page source
                    page_source = driver.page_source
                    
                    # Look for JSON patterns
                    json_patterns = [
                        r'<pre[^>]*>(.*?)</pre>',
                        r'{"data":\s*\[.*?\].*?}',
                        r'{.*?"data".*?}',
                    ]
                    
                    for pattern in json_patterns:
                        matches = re.findall(pattern, page_source, re.DOTALL)
                        for match in matches:
                            try:
                                clean_json = match.strip()
                                if clean_json.startswith('{') and clean_json.endswith('}'):
                                    data = json.loads(clean_json)
                                    if 'data' in data:
                                        print("[BROWSER] JSON extracted successfully!")
                                        return data
                            except json.JSONDecodeError:
                                continue
                    
                    driver.quit()
                    
                except Exception as e:
                    if driver:
                        driver.quit()
                    print(f"[BROWSER] Config failed: {e}")
                    continue
            
        except ImportError:
            print("[BROWSER] Selenium not available")
        except Exception as e:
            print(f"[BROWSER] Failed: {e}")
        
        return None
    
    def scrape_prizepicks(self):
        """Main scraping function with advanced bypass"""
        print("=" * 60)
        print("🎯 MILITARY-GRADE PRIZEPICKS SCRAPER INITIATED")
        print("=" * 60)
        
        # Try all endpoints with rotation
        for attempt in range(3):  # 3 full cycles
            print(f"\n[CYCLE {attempt + 1}] Starting endpoint rotation...")
            
            for i, endpoint in enumerate(self.endpoints):
                print(f"\n[ENDPOINT {i+1}/{len(self.endpoints)}] {endpoint}")
                
                # Human delay between requests
                if i > 0:
                    self.human_delay()
                
                # Try multiple methods
                data, method = self.multi_method_request(endpoint)
                
                if data and isinstance(data, dict) and 'data' in data:
                    props = self.parse_props(data)
                    if props:
                        print(f"\n🎯 SUCCESS! Method: {method}")
                        print(f"📊 Collected {len(props)} props")
                        self.print_stats()
                        return props
                
                # Rotate to next endpoint immediately if blocked
                if self.blocked_count > 5:
                    print(f"[ROTATE] Too many blocks ({self.blocked_count}), rotating faster...")
                    continue
            
            # Longer delay between cycles
            if attempt < 2:
                print(f"\n[CYCLE-BREAK] Cooling down before cycle {attempt + 2}...")
                time.sleep(random.uniform(10, 20))
        
        print("\n❌ ALL METHODS EXHAUSTED")
        self.print_failure_analysis()
        return []
    
    def parse_props(self, data):
        """Extract props from API response"""
        if not data or 'data' not in data:
            return []
        
        props = []
        for item in data['data']:
            try:
                attrs = item.get('attributes', {})
                
                prop = {
                    'name': attrs.get('name', 'Unknown'),
                    'stat': attrs.get('stat_type', 'Unknown'),
                    'line': float(attrs.get('line_score', 0)),
                    'team': attrs.get('team', attrs.get('league', 'Unknown'))
                }
                
                if prop['name'] != 'Unknown' and prop['stat'] != 'Unknown' and prop['line'] > 0:
                    props.append(prop)
                    
            except (KeyError, ValueError, TypeError):
                continue
        
        return props
    
    def print_stats(self):
        """Print scraping statistics"""
        total_attempts = self.success_count + self.failure_count + self.blocked_count
        success_rate = (self.success_count / max(total_attempts, 1)) * 100
        
        print("\n📈 SCRAPING STATISTICS:")
        print(f"✅ Successes: {self.success_count}")
        print(f"❌ Failures: {self.failure_count}")
        print(f"🚫 Blocked: {self.blocked_count}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if self.last_success_time > 0:
            time_since = time.time() - self.last_success_time
            print(f"⏰ Last Success: {time_since:.1f}s ago")
    
    def print_failure_analysis(self):
        """Analyze why scraping failed"""
        print("\n🔍 FAILURE ANALYSIS:")
        
        if self.blocked_count > self.failure_count:
            print("🚫 Primary Issue: ANTI-BOT DETECTION")
            print("   - PrizePicks has implemented aggressive rate limiting")
            print("   - All HTTP methods are being blocked (403/429)")
            print("   - Recommendation: Use browser automation or wait for cooldown")
            print("   - Alternative: Try from different IP/network")
        
        elif self.failure_count > 0:
            print("🌐 Primary Issue: NETWORK/CONNECTIVITY")
            print("   - Check internet connection")
            print("   - API endpoints may be down")
            print("   - Try different network or VPN")
        
        else:
            print("❓ Unknown Issue - All methods failed silently")
            print("   - Possible SSL/TLS issues")
            print("   - Server may be completely down")
        
        print(f"\n📊 Block/Failure Ratio: {self.blocked_count}/{self.failure_count}")
        print("💡 Next Steps:")
        print("   1. Wait 30+ minutes for rate limit reset")
        print("   2. Try from different IP address")
        print("   3. Use residential proxy service")
        print("   4. Browser automation with human-like delays")
        
        self.print_stats()

def main():
    """Main execution function"""
    scraper = MilitaryGradeScraper()
    props = scraper.scrape_prizepicks()
    
    if props:
        print(f"\n✅ Successfully scraped {len(props)} props:")
        print(json.dumps(props, indent=2))
        
        # Save to file
        with open('prizepicks_props.json', 'w') as f:
            json.dump({
                'props': props,
                'timestamp': datetime.now().isoformat(),
                'stats': {
                    'success_count': scraper.success_count,
                    'failure_count': scraper.failure_count,
                    'blocked_count': scraper.blocked_count
                }
            }, f, indent=2)
        print("\n💾 Data saved to prizepicks_props.json")
    else:
        print("\n❌ Scraping failed - no props collected")
        return False
    
    return True

if __name__ == "__main__":
    main()
