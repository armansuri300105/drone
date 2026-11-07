import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def capture():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)

    try:
        print("Navigating to http://localhost:5000...")
        driver.get("http://localhost:5000")
        time.sleep(3)  # wait for satellite tiles and connection

        docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "screenshots")
        os.makedirs(docs_dir, exist_ok=True)

        # 1. Idle screenshot
        idle_path = os.path.join(docs_dir, "01_dashboard_idle.png")
        driver.save_screenshot(idle_path)
        print(f"Captured: {idle_path}")

        # 2. Add waypoints via Leaflet map events
        print("Adding waypoints on map...")
        driver.execute_script("""
            map.fire('click', { latlng: L.latLng(42.3835, 20.4355) });
            map.fire('click', { latlng: L.latLng(42.3870, 20.4320) });
            map.fire('click', { latlng: L.latLng(42.3830, 20.4250) });
        """)
        time.sleep(1)

        # 3. Launch flight
        print("Launching flight mission...")
        driver.execute_script("document.getElementById('btn-start').click();")
        
        # Wait 4 seconds for takeoff and flying
        time.sleep(4)

        # 4. Flying screenshot
        flying_path = os.path.join(docs_dir, "02_dashboard_flying.png")
        driver.save_screenshot(flying_path)
        print(f"Captured: {flying_path}")

        # 5. Click Return to Home to show RTH in action
        print("Clicking Return to Home...")
        driver.execute_script("document.getElementById('btn-rth').click();")
        time.sleep(2)

        rth_path = os.path.join(docs_dir, "03_dashboard_rth.png")
        driver.save_screenshot(rth_path)
        print(f"Captured: {rth_path}")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture()
