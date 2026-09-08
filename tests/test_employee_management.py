import sys
import os

import pytest
from selenium import webdriver

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.employee_list_page import EmployeeListPage
from utils.test_data import generate_employee_names


VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


@pytest.fixture
def driver():
    drv = webdriver.Chrome()
    drv.maximize_window()

    yield drv

    drv.quit()


def test_add_and_verify_employees(driver):

    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    pim_page = PIMPage(driver)
    employee_list_page = EmployeeListPage(driver)

    # 1. Login
    login_page.open().login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    assert dashboard_page.is_loaded(), (
        "Login did not reach the Dashboard"
    )

    # 2. Navigate to PIM using hover + click
    dashboard_page.go_to_pim()

    # 3. Generate 4 unique employee names
    employees = generate_employee_names(
        count=4
    )

    # 4. Add employees
    for first_name, last_name in employees:

        employee_list_page.open()

        pim_page.click_add_employee()

        pim_page.add_employee(
            first_name,
            last_name
        )

        assert "/pim/viewPersonalDetails" in driver.current_url, (
            f"Employee {first_name} {last_name} "
            "was not created successfully"
        )

    # 5. Verify all 4 employees
    employee_list_page.open()

    for first_name, last_name in employees:

        full_name = f"{first_name} {last_name}"

        print(
            f"\nSearching for: {full_name}"
        )

        employee_list_page.search_by_name(
            full_name
        )

        found = employee_list_page.is_employee_listed(
            full_name
        )

        assert found, (
            f"{full_name} was not found "
            "in the Employee List"
        )

        print("Name Verified")

    # 6. Logout
    driver.get(
        "https://opensource-demo.orangehrmlive.com/"
        "web/index.php/dashboard/index"
    )

    assert dashboard_page.is_loaded(), (
        "Dashboard did not load before logout"
    )

    dashboard_page.logout()

    assert "/auth/login" in driver.current_url, (
        "Logout did not return to the login page"
    )

    print("Logout Verified")