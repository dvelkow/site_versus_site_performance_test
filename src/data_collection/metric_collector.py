from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict

class MetricCollector:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Ensure chromedriver is in PATH

    def collect_metrics(self, url: str) -> Dict[str, float]:
        self.driver.get(url)

        # Wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Collect timing metrics
        timing = self.driver.execute_script("return performance.timing.toJSON()")

        navigation_start = timing['navigationStart']
        load_event_end = timing['loadEventEnd']
        response_start = timing['responseStart']

        page_load_time = (load_event_end - navigation_start) / 1000
        time_to_first_byte = (response_start - navigation_start) / 1000

        # Attempt to get First Contentful Paint
        try:
            first_contentful_paint = self.driver.execute_script("""
                var performance = window.performance || {};
                var entries = performance.getEntriesByType && performance.getEntriesByType('paint') || [];
                for (var i = 0; i < entries.length; i++) {
                    if (entries[i].name === 'first-contentful-paint') {
                        return entries[i].startTime;
                    }
                }
                return null;
            """)
        except Exception as e:
            print(f"Error getting First Contentful Paint: {e}")
            first_contentful_paint = None

        metrics = {
            'page_load_time': page_load_time,
            'time_to_first_byte': time_to_first_byte,
        }

        if first_contentful_paint is not None:
            metrics['first_contentful_paint'] = first_contentful_paint / 1000

        return metrics

    def close(self):
        self.driver.quit()