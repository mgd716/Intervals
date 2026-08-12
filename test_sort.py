from playwright.sync_api import sync_playwright
import time

def test_sorting():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:3000")

        # Wait for the map and sidebar to load
        page.wait_for_selector("#activity-list .activity-item", state="attached", timeout=30000)

        # Let the loadData and sorting complete
        time.sleep(3)

        print("Initial state (Sort by Date):")
        first_item = page.query_selector("#activity-list .activity-item:first-child")
        if first_item:
            print("First item date:", first_item.get_attribute("data-date"))

        # Change sort to Distance
        page.select_option("#sort-select", "distance")
        time.sleep(1) # wait for sorting
        print("\nChanged sort to Distance:")
        first_item = page.query_selector("#activity-list .activity-item:first-child")
        if first_item:
            print("First item distance:", first_item.get_attribute("data-distance"))

        # Change sort to Time
        page.select_option("#sort-select", "time")
        time.sleep(1) # wait for sorting
        print("\nChanged sort to Time:")
        first_item = page.query_selector("#activity-list .activity-item:first-child")
        if first_item:
            print("First item time:", first_item.get_attribute("data-time"))

        # Change sort to Pace
        page.select_option("#sort-select", "pace")
        time.sleep(1) # wait for sorting
        print("\nChanged sort to Pace:")
        first_item = page.query_selector("#activity-list .activity-item:first-child")
        if first_item:
            print("First item speed:", first_item.get_attribute("data-speed"))

        browser.close()

if __name__ == "__main__":
    test_sorting()
