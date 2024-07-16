import asyncio
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

logger = logging.getLogger(__name__)

class MetricCollector:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.driver = None

    async def setup_driver(self):
        loop = asyncio.get_event_loop()
        self.driver = await loop.run_in_executor(None, webdriver.Chrome)

    async def collect_metrics(self, url: str) -> Dict[str, float]:
        if not self.driver:
            await self.setup_driver()

        metrics = {}
        try:
            await asyncio.get_event_loop().run_in_executor(None, self.driver.get, url)
            
            # Wait for the page to load
            await asyncio.get_event_loop().run_in_executor(
                None, 
                WebDriverWait(self.driver, self.timeout).until,
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Collect timing metrics
            timing = await asyncio.get_event_loop().run_in_executor(
                None,
                self.driver.execute_script,
                "return performance.timing.toJSON()"
            )

            navigation_start = timing['navigationStart']
            load_event_end = timing['loadEventEnd']
            response_start = timing['responseStart']

            metrics['page_load_time'] = (load_event_end - navigation_start) / 1000
            metrics['time_to_first_byte'] = (response_start - navigation_start) / 1000

            # Collect First Contentful Paint
            first_contentful_paint = await asyncio.get_event_loop().run_in_executor(
                None,
                self.driver.execute_script,
                """
                return performance.getEntriesByType('paint')
                    .find(entry => entry.name === 'first-contentful-paint')?.startTime;
                """
            )

            if first_contentful_paint is not None:
                metrics['first_contentful_paint'] = first_contentful_paint / 1000

        except TimeoutException:
            logger.error(f"Timeout while loading {url}")
        except WebDriverException as e:
            logger.error(f"WebDriver error for {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error collecting metrics for {url}: {str(e)}")

        return metrics

    async def close(self):
        if self.driver:
            await asyncio.get_event_loop().run_in_executor(None, self.driver.quit)