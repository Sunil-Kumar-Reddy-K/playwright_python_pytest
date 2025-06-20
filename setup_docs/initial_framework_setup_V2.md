# 🎭 Playwright Python Pytest Framework - Complete Project Structure

A comprehensive hybrid automation framework for UI and API testing using Playwright and pytest.

## 📁 Project Structure

```
playwright_python_pytest/
├── .github/
│   └── workflows/                  # GitHub Actions workflows
│       └── playwright_runner.yml
├── apis/                           # API test modules
│   ├── authtoken_generator.py
│   ├── __init__.py
│   └── notes_api.py
├── pages/                          # Page Object Models
│   ├── base_page.py
│   └── cart_page.py
├── tests/
│   ├── api_tests/                  # API test cases
│   ├── ui_tests/                   # UI test cases
│   └── conftest.py                 # Pytest fixtures
├── utils/                          # Helper utilities
│   ├── config.py                   # Configuration settings
│   ├── page_manager.py             # Page object management
│   ├── report_generator.py         # Reporting utilities
│   └── soft_assert.py              # Soft assertion implementation
├── .gitignore
├── pytest.ini                     # Pytest configuration
├── README.md
└── requirements.txt                # Dependencies
```

## 🛠️ Dependencies

Key packages from `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| `playwright` | 1.52.0 | Browser automation |
| `pytest` | 8.4.0 | Testing framework |
| `pytest-html` | 4.1.1 | HTML test reports |
| `pytest-playwright` | 0.7.0 | Playwright-pytest integration |
| `allure-pytest` | 2.14.3 | Allure reporting |
| `requests` | 2.32.4 | HTTP library for API tests |

## 🏗️ Implementation Patterns

### 1. Page Object Model (POM)

#### Base Page (`pages/base_page.py`)
- Contains common page interactions and utilities
- Inherited by all page objects

#### Example Page Object (`pages/cart_page.py`)

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
```

### 2. Test Fixtures (`tests/conftest.py`)

Key fixtures available:
- **`browser`**: Manages browser instance
- **`page`**: New browser page per test
- **`page_manager`**: Centralized page object management
- **`api_client`**: Configured API client

### 3. API Testing

#### API Client (`apis/notes_api.py`)

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
        return requests.post(f"{self.base_url}/notes", 
                           json=payload, 
                           headers=self.headers)
```

### 4. Test Organization

#### UI Tests
- **Location**: `tests/ui_tests/`
- **Marker**: `@pytest.mark.ui`

**Example UI test case:**
```python
@pytest.mark.ui
def test_add_to_cart(page_manager):
    cart_page = page_manager.cart_page
    cart_page.navigate()
    cart_page.add_item_to_cart()
    cart_page.go_to_cart()
    # Assertions
```

#### API Tests
- **Location**: `tests/api_tests/`
- **Marker**: `@pytest.mark.api`

**Example API test case:**
```python
@pytest.mark.api
def test_create_note(api_client):
    response = api_client.create_note(
        title="Test Note",
        description="Test Description",
        category="Home"
    )
    assert response.status_code == 200
```

## ⚙️ Configuration

### pytest.ini

```ini
[pytest]
addopts = -v --html=./reports/report.html --self-contained-html
markers =
    ui: Mark UI tests
    api: Mark API tests
```

### GitHub Actions Workflow

The workflow includes:
- Runs on push to main branch
- Installs dependencies
- Runs tests
- Uploads test results

## 🚀 Running Tests

### Run All Tests
```bash
pytest
```

### Run UI Tests Only
```bash
pytest -m ui
```

### Run API Tests Only
```bash
pytest -m api
```

### Run with Allure Reporting
```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## 🔧 Utilities

### Page Manager (`utils/page_manager.py`)
Manages page object lifecycle with caching:

```python
class PageManager:
    def __init__(self, page: Page):
        self.page = page

    @cached_property
    def cart_page(self) -> CartPage:
        return CartPage(self.page)
```

### Soft Assertions (`utils/soft_assert.py`)
Collects multiple assertion failures:

```python
soft_assert = SoftAssert()
soft_assert.assert_equal(actual, expected, "Values should match")
soft_assert.assert_all()  # Raises collected failures
```

## 📊 Reporting

### HTML Reports
- Generated in `reports/` directory
- Self-contained HTML files

### Allure Reporting

#### Generate results:
```bash
pytest --alluredir=./allure-results
```

#### View report:
```bash
allure serve ./allure-results
```

## 🌐 Test Environments

### UI Testing
- **Base URL**: https://rahulshettyacademy.com/seleniumPractise/

### API Testing
- **Base URL**: https://practice.expandtesting.com/notes/api

## 🔄 CI/CD

GitHub Actions workflow includes:
- ✅ Test execution
- 📤 Results upload
- 📊 Reporting

## 📝 Additional Features

### Configuration Management
- Centralized configuration in `utils/config.py`
- Environment-specific settings
- Sensitive data handling

### Error Handling
- Custom exception classes
- Comprehensive logging
- Graceful failure handling

### Test Data Management
- Separate test data files
- Data-driven testing support
- Dynamic test data generation

### Cross-Browser Testing
- Support for Chromium, Firefox, and WebKit
- Parallel test execution
- Browser-specific configurations

This framework provides a robust foundation for both UI and API testing with modern Python testing practices and comprehensive reporting capabilities.