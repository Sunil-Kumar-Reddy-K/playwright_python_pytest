import os
import subprocess
import sys
import platform
from datetime import datetime

import allure
import pytest
from playwright.sync_api import sync_playwright

from apis.authtoken_generator import get_auth_token
from apis.notes_api import NotesApi
from utils.config import config
from utils.page_manager import PageManager
from utils.soft_assert import SoftAssert


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium, firefox, webkit, chrome"
    )

    parser.addoption(
        "--env",
        action="store",
        default="qa",
        choices=["qa", "stage", "prod"],
        help="Environment to run tests against: qa, stage, prod"
    )

    parser.addoption(
        "--test-type",
        action="store",
        default="ui",
        choices=["ui", "api", "both"],
        help="Type of tests to run: ui, api, both"
    )


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment(request):
    """Configure the test environment based on command line arguments"""
    env = request.config.getoption("--env")
    test_type = request.config.getoption("--test-type")

    # Set the global configuration
    config.set_environment(env)
    config.set_test_type(test_type)

    print(f"\n🔧 Test Configuration:")
    print(f"   Environment: {config.current_env.upper()}")
    print(f"   Test Type: {config.current_test_type.upper()}")
    print(f"   UI Base URL: {config.ui_base_url}")
    print(f"   API Base URL: {config.api_base_url}")
    print(f"   Timeout: {config.timeout}ms")


@pytest.fixture
def browser(playwright, request):
    """Custom browser fixture that supports Chrome"""
    browser_name = request.config.getoption("--browser-name")
    headless = not request.config.getoption("--headed", default=True)

    # Browser launch configuration with environment-specific settings
    browser_args = {
        'headless': headless,
        'slow_mo': 100 if config.current_env == 'prod' else 0,  # Slower in prod
    }

    if browser_name.lower() == "chrome":
        return playwright.chromium.launch(channel="chrome", **browser_args)
    elif browser_name.lower() == "chromium":
        return playwright.chromium.launch(**browser_args)
    elif browser_name.lower() == "firefox":
        return playwright.firefox.launch(**browser_args)
    elif browser_name.lower() == "webkit":
        return playwright.webkit.launch(**browser_args)
    else:
        return playwright.chromium.launch(**browser_args)


@pytest.fixture(scope="function")
def page(browser):
    """Create a new page with environment-specific configurations"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=config.current_env != 'prod',  # Strict HTTPS in prod
    )

    page = context.new_page()

    # Set environment-specific timeout
    page.set_default_timeout(config.timeout)
    page.set_default_navigation_timeout(config.timeout)

    yield page

    context.close()


@pytest.fixture(scope="function")
def api_client():
    """API client configured for current environment"""
    return NotesApi(config.api_base_url)


@pytest.fixture(scope="session", name="get_token")
def auth_token_fixture() -> str:
    """Pytest fixture wrapping token utility."""
    return get_auth_token()


@pytest.fixture(scope="function")
def pages(page):
    """Fixture that provides access to all page objects through PageManager"""
    return PageManager(page)


@pytest.fixture(scope="function")
def soft_assert():
    """Fixture to provide soft assertion capability to tests"""
    return SoftAssert()


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on test-type argument"""
    test_type = config.getoption("--test-type")

    if test_type == "ui":
        # Skip API tests when running UI only
        skip_api = pytest.mark.skip(reason="Skipping API tests (--test-type=ui)")
        for item in items:
            if "api" in item.keywords:
                item.add_marker(skip_api)

    elif test_type == "api":
        # Skip UI tests when running API only
        skip_ui = pytest.mark.skip(reason="Skipping UI tests (--test-type=api)")
        for item in items:
            if "ui" in item.keywords:
                item.add_marker(skip_ui)

    # For "both", no filtering is applied


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
                        name=f"Screenshot on Failure - {config.current_env.upper()}",
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
    # Create environment.properties file for Allure
    env_props = f"""
Browser=Chromium
Platform={platform.system()} {platform.release()}
Python.Version={platform.python_version()}
Execution.Start={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test.Environment={config.current_env.upper()}
Test.Type={config.current_test_type.upper()}
Application.URL={config.ui_base_url}
API.Base.URL={config.api_base_url}
Timeout={config.timeout}ms
""".strip()

    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as f:
        f.write(env_props)


def pytest_sessionstart(session):
    """Print configuration summary at session start"""
    print(f"\n{'=' * 60}")
    print(f"🚀 STARTING TEST SESSION")
    print(f"{'=' * 60}")
    print(config)
    print(f"{'=' * 60}")


def pytest_sessionfinish(session, exitstatus):
    """Print session summary"""
    print(f"\n{'=' * 60}")
    print(f"✅ TEST SESSION COMPLETED")
    print(f"Exit Status: {exitstatus}")
    print(f"Environment: {config.current_env.upper()}")
    print(f"Test Type: {config.current_test_type.upper()}")
    print(f"{'=' * 60}")
