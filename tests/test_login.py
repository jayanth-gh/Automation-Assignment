"""
test_login.py

Automates a representative subset of the manual login test cases
(see the QA report, section B/C, for the full manual set).
Run with: pytest -s tests/test_login.py
"""

import sys
import os
import pytest
from selenium import webdriver

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()
    yield drv
    drv.quit()


def test_tc01_valid_login(driver):
    login_page = LoginPage(driver).open().login(VALID_USERNAME, VALID_PASSWORD)
    assert DashboardPage(driver).is_loaded()


def test_tc02_invalid_username_valid_password(driver):
    login_page = LoginPage(driver).open().login("NotARealUser", VALID_PASSWORD)
    assert login_page.get_error_message() == "Invalid credentials"


def test_tc03_valid_username_invalid_password(driver):
    login_page = LoginPage(driver).open().login(VALID_USERNAME, "wrongPassword123")
    assert login_page.get_error_message() == "Invalid credentials"


def test_tc04_invalid_username_invalid_password(driver):
    login_page = LoginPage(driver).open().login("NotARealUser", "wrongPassword123")
    assert login_page.get_error_message() == "Invalid credentials"


def test_tc05_empty_username_and_password(driver):
    login_page = LoginPage(driver).open().click_login()
    errors = login_page.get_field_errors()
    assert any("Required" in e for e in errors)


def test_tc06_username_only(driver):
    login_page = LoginPage(driver).open().enter_username(VALID_USERNAME).click_login()
    errors = login_page.get_field_errors()
    assert any("Required" in e for e in errors)


def test_tc07_password_only(driver):
    login_page = LoginPage(driver).open().enter_password(VALID_PASSWORD).click_login()
    errors = login_page.get_field_errors()
    assert any("Required" in e for e in errors)


def test_tc08_password_is_masked(driver):
    login_page = LoginPage(driver).open()
    login_page.enter_password("secretValue")
    field = driver.find_element(*LoginPage.PASSWORD_INPUT)
    assert field.get_attribute("type") == "password"


def test_tc09_leading_trailing_whitespace_in_username(driver):
    login_page = LoginPage(driver).open().login(f"  {VALID_USERNAME}  ", VALID_PASSWORD)
    # Document whichever the app actually does: either it logs in
    # (whitespace trimmed) or shows "Invalid credentials" (not trimmed).
    dashboard = DashboardPage(driver)
    logged_in = dashboard.is_loaded()
    error = login_page.get_error_message()
    assert logged_in or error == "Invalid credentials"
