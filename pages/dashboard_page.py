from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class DashboardPage(BasePage):

    PIM_MENU_ITEM = (
        By.XPATH,
        "//span[text()='PIM']"
    )

    USER_DROPDOWN = (
        By.CSS_SELECTOR,
        ".oxd-userdropdown-tab"
    )

    LOGOUT_LINK = (
        By.XPATH,
        "//a[text()='Logout']"
    )

    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[text()='Dashboard']"
    )

    def is_loaded(self):
        return self.is_visible(
            self.DASHBOARD_HEADER,
            timeout=10
        )

    def go_to_pim(self):
        pim_menu = self.find_clickable(
            self.PIM_MENU_ITEM
        )

        # Assignment specifically asks for hover + click.
        ActionChains(self.driver) \
            .move_to_element(pim_menu) \
            .click() \
            .perform()

        # Wait for PIM URL
        self.wait.until(
            lambda driver: "/pim/" in driver.current_url
        )

        return self

    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
        return self