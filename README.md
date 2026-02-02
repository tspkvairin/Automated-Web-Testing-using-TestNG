# Assignment 5 — Automated UI Testing (pytest + Selenium)

This repository contains automated UI tests for **Assignment 5** using:
- **Python + pytest** for test lifecycle management (setup/teardown via fixtures)
- **Selenium WebDriver (Chrome)** for browser automation
- **Python logging** for file-based execution logs
- **pytest-html** for an HTML execution report
- **Automatic screenshots on test failure** (attached to the HTML report when possible)

## Test System
- Web application: **The Internet (Herokuapp)**
- Base URL: `https://the-internet.herokuapp.com`

## Implemented Test Cases
1. **Login with invalid credentials** — verifies error message
2. **Login with valid credentials + Logout** — verifies secure area and logout message
3. **Checkboxes** — toggles checkbox #1 and verifies state changes
4. **Dropdown** — selects Option 2 and verifies selected value

## Project Structure
Typical structure (names may vary slightly):

├─ conftest.py # fixtures: driver, logger, step; screenshot + report hook
├─ test_assignment5.py # UI tests (4 test cases)
├─ logs/ # generated logs (auto-created)
├─ screenshots/ # failure screenshots (auto-created)
├─ reports/ # HTML report output (auto-created)
├─ requirements.txt # optional but recommended
└─ README.md
