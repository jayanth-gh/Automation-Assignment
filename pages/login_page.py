"""
login_page.py

Responsibility: everything on the OrangeHRM login screen —
entering credentials, submitting, reading validation / error text.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    # Locators (verified against the demo app's stable name/class attributes,
    # not auto-generated ids, to keep the tests less brittle)
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    FIELD_ERROR = (By.CSS_SELECTOR, ".oxd-input-group__message")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".orangehrm-login-forgot-header")

    def open(self):
        self.driver.get(self.URL)
        return self

    def enter_username(self, username):
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username, password):
        """Convenience method combining the three steps above."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self):
        """Generic 'Invalid credentials' banner shown after a failed submit."""
        if self.is_visible(self.ERROR_ALERT):
            return self.get_text(self.ERROR_ALERT)
        return None

    def get_field_errors(self):
        """'Username is required' / 'Password is required' style messages."""
        return [el.text.strip() for el in self.find_all(self.FIELD_ERROR)]

    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD_LINK)
        return self
