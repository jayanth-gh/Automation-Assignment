from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class EmployeeListPage(BasePage):

    URL = (
        "https://opensource-demo.orangehrmlive.com/"
        "web/index.php/pim/viewEmployeeList"
    )

    # OrangeHRM Employee Name is a dynamic autocomplete field.
    EMPLOYEE_NAME_SEARCH_INPUT = (
        By.XPATH,
        "(//input[@placeholder='Type for hints...'])[1]"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Search']"
    )

    # Autocomplete suggestions.
    AUTOCOMPLETE_OPTIONS = (
        By.XPATH,
        "//div[@role='option']"
    )

    # Employee result rows.
    RESULT_ROWS = (
        By.CSS_SELECTOR,
        ".oxd-table-card"
    )

    NO_RECORDS_MESSAGE = (
        By.XPATH,
        "//span[normalize-space()='No Records Found']"
    )

    def open(self):
        """
        Open the Employee List page and wait until the
        Employee Name field is ready.
        """
        self.driver.get(self.URL)

        self.wait.until(
            lambda driver:
            "/pim/viewEmployeeList" in driver.current_url
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.EMPLOYEE_NAME_SEARCH_INPUT
            )
        )

        return self

    def clear_search_field(self):
        """
        Reliably clear OrangeHRM's dynamic autocomplete field.

        Using Ctrl+A + Backspace is more reliable than clear()
        for this SPA autocomplete component.
        """
        search_box = self.wait.until(
            EC.element_to_be_clickable(
                self.EMPLOYEE_NAME_SEARCH_INPUT
            )
        )

        search_box.click()

        search_box.send_keys(
            Keys.CONTROL,
            "a"
        )

        search_box.send_keys(
            Keys.BACKSPACE
        )

        # Confirm the field is actually empty.
        self.wait.until(
            lambda driver:
            driver.find_element(
                *self.EMPLOYEE_NAME_SEARCH_INPUT
            ).get_attribute("value") == ""
        )

        return search_box

    def search_by_name(self, full_name):
        """
        Search for an employee using OrangeHRM's autocomplete.

        Example generated name:
            QA-793645-1 AutoTest

        We enter only the unique first portion:
            QA-793645-1
        """

        # Always start with a clean autocomplete field.
        search_box = self.clear_search_field()

        search_term = full_name.split(" ")[0]

        print(
            f"Entering search term: {search_term}"
        )

        search_box.send_keys(
            search_term
        )

        def find_matching_option(driver):
            """
            Find a fresh matching autocomplete option.

            The autocomplete can temporarily show:
                Searching....

            We ignore that temporary state.
            """
            options = driver.find_elements(
                *self.AUTOCOMPLETE_OPTIONS
            )

            for option in options:
                try:
                    if not option.is_displayed():
                        continue

                    text = option.text.strip()

                    if not text:
                        continue

                    if text.lower() == "searching....":
                        continue

                    if search_term.lower() in text.lower():
                        return True

                except Exception:
                    # The SPA may replace the element while the
                    # autocomplete request is still running.
                    continue

            return False

        # Wait until a real matching employee suggestion appears.
        self.wait.until(
            find_matching_option
        )

        def click_matching_option(driver):
            """
            Locate the matching suggestion again and click it.
            Elements are fetched fresh to avoid stale references.
            """
            options = driver.find_elements(
                *self.AUTOCOMPLETE_OPTIONS
            )

            for option in options:
                try:
                    if not option.is_displayed():
                        continue

                    text = option.text.strip()

                    if (
                        text
                        and text.lower() != "searching...."
                        and search_term.lower() in text.lower()
                    ):
                        print(
                            f"Selecting employee: {text}"
                        )

                        option.click()

                        return True

                except Exception:
                    # DOM can refresh between locating and clicking.
                    continue

            return False

        # Click the actual employee suggestion.
        self.wait.until(
            click_matching_option
        )

        # Search using the selected employee.
        self.wait.until(
            EC.element_to_be_clickable(
                self.SEARCH_BUTTON
            )
        ).click()

        return self

    def is_employee_listed(self, full_name):
        """
        Verify that the requested employee appears in the
        filtered Employee List result.
        """

        # Normalize whitespace and case for comparison.
        target = " ".join(
            full_name.strip().lower().split()
        )

        def results_ready(driver):
            # "No Records Found" is also a valid completed state.
            no_records = driver.find_elements(
                *self.NO_RECORDS_MESSAGE
            )

            if any(
                element.is_displayed()
                for element in no_records
            ):
                return True

            rows = driver.find_elements(
                *self.RESULT_ROWS
            )

            return len(rows) > 0

        # Wait until the AJAX search has completed.
        self.wait.until(
            results_ready
        )

        # Explicitly handle no results.
        no_records = self.driver.find_elements(
            *self.NO_RECORDS_MESSAGE
        )

        if any(
            element.is_displayed()
            for element in no_records
        ):
            return False

        # Fetch fresh result rows after the table refresh.
        rows = self.driver.find_elements(
            *self.RESULT_ROWS
        )

        for row in rows:
            try:
                row_text = " ".join(
                    row.text.strip().lower().split()
                )

                print(
                    f"Checking result row: {row_text}"
                )

                if target in row_text:
                    return True

            except Exception:
                # Ignore a row that was replaced during an SPA refresh.
                continue

        return False