"""
base_page.py

Common functionality shared by every Page Object:
- explicit waits (never time.sleep — avoids brittle, timing-dependent tests)
- small wrapper methods so tests never call driver / By directly
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def type_text(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def click(self, locator):
        self.find_clickable(locator).click()

    def get_text(self, locator):
        return self.find(locator).text.strip()

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False
