import os

import allure
import pytest
from playwright.sync_api import sync_playwright

from apis.authtoken_generator import get_auth_token
from apis.notes_api import NotesApi
from utils.config import Config
from utils.page_manager import PageManager
from utils.soft_assert import SoftAssert


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright_instance, request):
    # Get browser from command line or environment
    browser_name = request.config.getoption("--browser", default="chromium")
    if not browser_name:
        browser_name = os.getenv("PLAYWRIGHT_BROWSER", "chromium")

    headless = request.config.getoption("--headed", default=True)
    if headless == False:
        headless = False
    else:
        headless = os.getenv("HEADLESS", "true").lower() == "true"

    # Launch browser
    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(headless=headless)
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=headless)
    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(headless=headless)
    else:
        browser = playwright_instance.chromium.launch(headless=headless)

    yield browser
    browser.close()


# Add command line options
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium, firefox, webkit"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode"
    )


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def pages(page):
    """Fixture that provides access to all page objects through PageManager"""
    return PageManager(page)


@pytest.fixture(scope="function")
def api_client():
    return NotesApi(Config.API_BASE_URL)


@pytest.fixture(scope="session", name="get_token")
def auth_token_fixture() -> str:
    """Pytest fixture wrapping token utility."""
    return get_auth_token()


@pytest.fixture(scope="function")
def soft_assert():
    """
    Fixture to provide soft assertion capability to tests
    Returns a fresh SoftAssert instance for each test
    """
    return SoftAssert()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Attach screenshot on test failure for UI tests"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if this is a UI test and has page fixture
        if "page" in item.fixturenames:
            page = item.funcargs.get("page")
            if page:
                try:
                    screenshot = page.screenshot()
                    allure.attach(
                        screenshot,
                        name="Screenshot on Failure",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    print(f"Could not take screenshot: {e}")


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "smoke: Smoke test cases")
    config.addinivalue_line("markers", "regression: Regression test cases")
    config.addinivalue_line("markers", "critical: Critical functionality tests")


@pytest.fixture(scope="session", autouse=True)
def allure_environment_setup():
    """Set up environment information for Allure report"""
    import platform
    import os
    from datetime import datetime

    # Create environment.properties file for Allure
    env_props = f"""
Browser=Chromium
Platform={platform.system()} {platform.release()}
Python.Version={platform.python_version()}
Execution.Start={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test.Environment=QA
Application.URL={Config.UI_BASE_URL}
API.Base.URL={Config.API_BASE_URL}
""".strip()

    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as f:
        f.write(env_props)
