# Playwright Python Pytest Automation Framework

A modern, synchronous, hybrid automation framework for UI and API testing using Playwright and pytest. This framework is designed to be minimal, scalable, and follow best practices, with no redundant components. It supports UI testing on `https://rahulshettyacademy.com/seleniumPractise/#/` and API testing on `https://practice.expandtesting.com/notes/api/api-docs/`.

## Purpose

This framework provides a robust setup for end-to-end testing, suitable for projects requiring both UI and API automation, such as Socotra (insurance apps) or Tempus-LIMS (healthcare). It uses pytest for test execution, Playwright for UI, and `requests` for API, with HTML reporting and modular design.

## Prerequisites

- **Operating System**: Windows (tested on Windows 10/11)
- **Python**: 3.13.2 (or 3.10+)
- **IDE**: PyCharm (recommended)
- **Internet**: Accessible test sites (`rahulshettyacademy.com`, `practice.expandtesting.com`) from India
- **Terminal**: Command Prompt (preferred over PowerShell for simplicity)

## Folder Creation and Setup

### 1. Create Project Folder

```cmd
mkdir E:\Drive (D)\SoftwareEngineer\Python\playwright_python_pytest
cd E:\Drive (D)\SoftwareEngineer\Python\playwright_python_pytest
```

### 2. Create Virtual Environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

- Verify activation: See `(.venv)` in prompt
- Check Python: `python --version` (should show 3.13.2)

### 3. Install Dependencies

```cmd
pip install pytest playwright pytest-playwright requests pytest-html
pip freeze > requirements.txt
```

### 4. Install Playwright Browsers

```cmd
playwright install
```

### 5. Verify Dependencies

```cmd
pip list
```

Expected output (versions may vary):

```text
Package            Version
------------------ -------
pip                24.3.1
playwright         1.47.0
pytest             8.3.3
pytest-html        4.1.1
pytest-playwright  0.5.2
requests           2.32.3
...
```

## Framework Structure

Create the following structure in `playwright_python_pytest/`:

```
playwright_python_pytest/
├── tests/
│   ├── ui/
│   │   └── test_cart.py
│   ├── api/
│   │   └── test_notes.py
│   └── conftest.py
├── pages/
│   └── cart_page.py
├── api/
│   └── notes_api.py
├── utils/
│   └── config.py
├── reports/
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## File Contents

### .gitignore

```text
.venv/
__pycache__/
*.pyc
reports/*
*.zip
.pytest_cache/
```

### pytest.ini

```ini
[pytest]
addopts = -v --html=./reports/report.html --self-contained-html
markers =
    ui: Mark UI tests
    api: Mark API tests
```

### utils/config.py

```python
class Config:
    UI_BASE_URL = "https://rahulshettyacademy.com/seleniumPractise/#/"
    API_BASE_URL = "https://practice.expandtesting.com/notes/api"
```

### tests/conftest.py

```python
import pytest
from playwright.sync_api import sync_playwright
from apis.notes_api import NotesApi
from utils.config import Config


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def api_client():
    return NotesApi(Config.API_BASE_URL)
```

### pages/cart_page.py

```python
from playwright.sync_api import Page
from utils.config import Config

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = Config.UI_BASE_URL
        self.add_to_cart_btn = page.locator("text=ADD TO CART").first
        self.cart_icon = page.locator(".cart-icon")

    def navigate(self):
        self.page.goto(self.url)

    def add_item_to_cart(self):
        self.add_to_cart_btn.click()

    def go_to_cart(self):
        self.cart_icon.click()
```

### tests/ui/test_cart.py

```python
import pytest
from pages.cart_page import CartPage

@pytest.mark.ui
def test_add_item_to_cart(page):
    cart_page = CartPage(page)
    cart_page.navigate()
    cart_page.add_item_to_cart()
    cart_page.go_to_cart()
    assert "cart" in page.url, "Failed to navigate to cart page"
```

### api/notes_api.py

```python
import requests

class NotesApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def create_note(self, title: str, description: str, category: str):
        payload = {
            "title": title,
            "description": description,
            "category": category
        }
        response = requests.post(f"{self.base_url}/notes", json=payload, headers=self.headers)
        return response
```

### tests/api/test_notes.py

```python
import pytest

@pytest.mark.api
def test_create_note(api_client):
    response = api_client.create_note(
        title="Test Note",
        description="This is a test note",
        category="Work"
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()["data"]["title"] == "Test Note", "Title mismatch"
```

## Basic Commands

### Activate Virtual Environment

```cmd
cd E:\Drive (D)\SoftwareEngineer\Python\playwright_python_pytest
.venv\Scripts\activate
```

### Run UI Test

```cmd
pytest tests/ui/test_cart.py -s
```

Debug with Playwright Inspector:

```cmd
set PWDEBUG=1
pytest tests/ui/test_cart.py -s
```

### Run API Test

```cmd
pytest tests/api/test_notes.py -s
```

### Run All Tests

```cmd
pytest -s
```

### Generate HTML Report

Included automatically via `pytest.ini`.
View at: `reports/report.html`.

### Reinstall Dependencies

```cmd
pip install -r requirements.txt
```

### Install Playwright Browsers

```cmd
playwright install --with-deps
```

## PyCharm Configuration

### Set Python Interpreter

1. File > Settings > Project: playwright_python_pytest > Python Interpreter
2. Add Interpreter > Existing > Select `E:\Drive (D)\SoftwareEngineer\Python\playwright_python_pytest\.venv\Scripts\python.exe`

### Auto-Activate Virtual Environment in Terminal

1. File > Settings > Tools > Terminal
2. Set Shell path: `cmd.exe /k E:\Drive (D)\SoftwareEngineer\Python\playwright_python_pytest\.venv\Scripts\activate.bat`

### Run Tests

Right-click `tests/ui/test_cart.py` or `tests/api/test_notes.py` > Run.

## Troubleshooting

### ModuleNotFoundError: No module named 'playwright'

**Cause**: Packages not installed in active virtual environment.

**Fix**:
```cmd
.venv\Scripts\activate
pip install pytest playwright pytest-playwright requests pytest-html
```

### pip list Shows Only pip

**Cause**: Installed packages globally or in wrong environment.

**Fix**:
```cmd
.venv\Scripts\activate
pip install pytest playwright pytest-playwright requests pytest-html
pip list
```

### Installation Fails

**Cause**: Network issues or outdated pip.

**Fix**:
```cmd
pip install --upgrade pip
pip install pytest playwright pytest-playwright requests pytest-html --no-cache-dir
```

### Tests Fail with Browser Errors

**Cause**: Playwright browsers not installed.

**Fix**:
```cmd
playwright install --with-deps
```

### PyCharm Uses Wrong Interpreter

**Cause**: Global Python used instead of .venv.

**Fix**: Set interpreter to `.venv\Scripts\python.exe` (see PyCharm Configuration).

### Virtual Environment Not Activating

**Cause**: Wrong command or path.

**Fix**:
```cmd
cd E:\Drive (D)\SoftwareEngineer\Python\playwright_python_pytest
.venv\Scripts\activate
```

### Recreate Virtual Environment

**Cause**: Corrupted or misconfigured environment.

**Fix**:
```cmd
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```