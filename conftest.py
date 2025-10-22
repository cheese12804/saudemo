import platform
import pytest
import allure
import os
import sys
from webdriver_manage.driver_manage import DriverManager
from configs.logging_config import logger
from utils.screenshot_util import ScreenshotUtil
from base_page import BasePage
from configs.config import Config
from utils.email_notification import send_allure_report_email, send_simple_notification


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


def pytest_sessionfinish(session, exitstatus):
    """Hook chạy sau khi kết thúc toàn bộ test session - gửi email với Allure report"""
    try:
        print("\n" + "="*60)
        print("📧 EMAIL NOTIFICATION - Sending Allure Report")
        print("="*60)
        
        # Lấy thông tin về test results
        test_summary = {
            "Total Tests": session.testscollected if hasattr(session, 'testscollected') else "Unknown",
            "Exit Status": exitstatus,
            "Status": "✅ PASSED" if exitstatus == 0 else "❌ FAILED"
        }
        
        # Tìm thư mục allure-results
        project_root = os.path.dirname(os.path.abspath(__file__))
        allure_results_dir = os.path.join(project_root, "allure-results")
        
        # Kiểm tra xem có thư mục allure-results không
        if os.path.exists(allure_results_dir) and os.listdir(allure_results_dir):
            print(f"📁 Found Allure results at: {allure_results_dir}")
            print(f"📊 Test Summary: {test_summary}")
            
            # Thử gửi email với file đính kèm trước
            print("📧 Attempting to send email with Allure report attachment...")
            success = send_allure_report_email(allure_results_dir, test_summary)
            
            if success:
                print("✅ Email with Allure report sent successfully!")
            else:
                print("⚠️  Failed to send email with attachment, trying simple notification...")
                success = send_simple_notification(allure_results_dir)
                if success:
                    print("✅ Simple notification sent successfully!")
                else:
                    print("❌ All email sending methods failed")
        else:
            print(f"⚠️  No Allure results found at {allure_results_dir}")
            print("📧 Sending simple notification without attachment...")
            send_simple_notification(allure_results_dir)
            
    except Exception as e:
        print(f"❌ Error in email notification: {e}")
        logger.error(f"Email notification failed: {e}")

