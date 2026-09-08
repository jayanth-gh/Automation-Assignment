# OrangeHRM Login & Employee Management Automation (Selenium + POM)

Automates the login flow and the "add employee → verify in Employee List →
logout" workflow against the public OrangeHRM demo, using the Page Object
Model.

## Project structure

```
orangehrm_automation/
├── pages/
│   ├── base_page.py            # shared explicit-wait helpers
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── pim_page.py             # includes Add Employee form
│   └── employee_list_page.py
├── tests/
│   ├── test_login.py           # automated subset of the manual login test cases
│   └── test_employee_management.py   # end-to-end assignment workflow
├── utils/
│   └── test_data.py            # generates unique, clearly-tagged test employee names
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Requires Google Chrome and a matching chromedriver on PATH (or switch
`webdriver.Chrome()` in the test fixtures to use `webdriver-manager` /
Selenium Manager, which Selenium 4.15+ handles automatically).

## Run

```bash
pytest -s tests/test_login.py               # login test cases
pytest -s tests/test_employee_management.py # add + verify + logout workflow
```

`-s` keeps stdout visible so the required `Name Verified` lines print to
the console for each employee found in the Employee List.

## Design notes

- **Waits:** every Page Object method waits via `WebDriverWait` /
  `expected_conditions` in `base_page.py` — no `time.sleep()`, to avoid
  flaky, timing-dependent tests.
- **Locators:** prefer `name`, stable CSS classes, and visible text over
  auto-generated ids/indexes, so the tests are less brittle against
  markup changes.
- **Test data:** `utils/test_data.py` tags every employee it creates with
  a `QA-<timestamp>-n` first name, so test data is obviously
  distinguishable from real records and never collides across runs.
- **Assertions:** functional assertions (dashboard loaded, error text,
  employee present in search results) rather than screenshot/visual
  diffs, matching the assignment's functional-verification scope.
- **Logout validation:** re-navigates to the dashboard URL and confirms
  the logout link/dropdown before clicking, then a follow-up assertion
  (not included above, but recommended) can confirm redirect back to
  the login page's username field being present.
