from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class PIMPage(BasePage):

    ADD_EMPLOYEE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Add']"
    )

    FIRST_NAME_INPUT = (
        By.NAME,
        "firstName"
    )

    LAST_NAME_INPUT = (
        By.NAME,
        "lastName"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//button[@type='submit']"
    )

    FORM_LOADER = (
        By.CSS_SELECTOR,
        ".oxd-form-loader"
    )

    EMPLOYEE_FULL_NAME_HEADER = (
        By.XPATH,
        "//h6[contains(@class,'oxd-text--h6')]"
    )

    def wait_for_employee_list(self):
        """Wait until Employee List page is ready."""
        self.wait.until(
            lambda driver:
            "/pim/viewEmployeeList" in driver.current_url
        )

        self.wait.until(
            EC.element_to_be_clickable(
                self.ADD_EMPLOYEE_BUTTON
            )
        )

        return self

    def click_add_employee(self):
        """Open the Add Employee page."""
        self.wait_for_employee_list()

        self.driver.find_element(
            *self.ADD_EMPLOYEE_BUTTON
        ).click()

        self.wait.until(
            lambda driver:
            "/pim/addEmployee" in driver.current_url
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.FIRST_NAME_INPUT
            )
        )

        return self

    def add_employee(self, first_name, last_name):

        self.type_text(
            self.FIRST_NAME_INPUT,
            first_name
        )

        self.type_text(
            self.LAST_NAME_INPUT,
            last_name
        )

        # Wait for any form loader to disappear
        try:
            self.wait.until(
                EC.invisibility_of_element_located(
                    self.FORM_LOADER
                )
            )
        except Exception:
            pass

        self.wait.until(
            EC.element_to_be_clickable(
                self.SAVE_BUTTON
            )
        ).click()

        self.wait_for_employee_saved()

        return self

    def wait_for_employee_saved(self):
        """Wait until employee creation completes."""
        self.wait.until(
            lambda driver:
            "/pim/viewPersonalDetails" in driver.current_url
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.EMPLOYEE_FULL_NAME_HEADER
            )
        )

        return self