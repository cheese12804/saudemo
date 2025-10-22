import platform
import pytest
import allure
import os
from webdriver_manage.driver_manage import DriverManager
from configs.logging_config import logger
from utils.screenshot_util import ScreenshotUtil
from base_page import BasePage
from configs.config import Config


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            if DriverManager.driver:
                BasePage.attach_screenshot_to_allure(f"FAILED_{item.name}")
                BasePage.capture_screenshot(f"FAILED_{item.name}")
                logger.error(f"Screenshot captured for failed test: {item.name}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot on test failure: {str(e)}")



@pytest.fixture(scope="class", autouse=True)
def session_log():
    logger.info("=== BẮT ĐẦU TEST SESSION ===")
    yield
    logger.info("=== KẾT THÚC TEST SESSION ===")


@pytest.fixture(autouse=True)
def setup_teardown1():
    logger.info("Setting up test - Initializing driver")
    DriverManager.init_driver()
    logger.info("Test setup completed")
    yield
    logger.info("Tearing down test - Closing driver")
    DriverManager.quit_driver()
    logger.info("Test teardown completed")


@pytest.fixture(autouse=True)
def setup_teardown2():
    project_root = os.path.dirname(os.path.abspath(__file__))

    allure_results_dir = os.path.join(project_root, "allure-results")
    if not os.path.exists(allure_results_dir):
        os.makedirs(allure_results_dir)
    os_name = platform.system()
    os_version = platform.release()
    browser_name = os.getenv('BROWSER', 'chrome')
    env_file = os.path.join(allure_results_dir, "environment.properties")
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(f"os={os_name} {os_version}\n")
        f.write(f"browser={browser_name}\n")
        f.write(f"python_version={os.sys.version.split()[0]}\n")
        f.write(f"test_environment=Testing\n")

    DriverManager.open_base_url()

