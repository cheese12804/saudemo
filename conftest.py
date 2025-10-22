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
from utils.email_notification import send_email_with_attachment, send_simple_notification


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
    """Hook chạy sau khi kết thúc toàn bộ test session"""
    try:
        # Kiểm tra xem có bật email notification không
        from utils.email_notification import ENABLE_EMAIL_NOTIFICATION, SEND_ATTACHMENT, SEND_SIMPLE_NOTIFICATION
        
        if not ENABLE_EMAIL_NOTIFICATION:
            print("[Email Notification] Email notification is disabled in config")
            return
        
        # Lấy thông tin về test results
        test_summary = {
            "Total Tests": session.testscollected if hasattr(session, 'testscollected') else "Unknown",
            "Exit Status": exitstatus,
            "Exit Status Meaning": "PASSED" if exitstatus == 0 else "FAILED"
        }
        
        # Tìm thư mục allure-results
        project_root = os.path.dirname(os.path.abspath(__file__))
        allure_results_dir = os.path.join(project_root, "allure-results")
        
        # Kiểm tra xem có thư mục allure-results không
        if os.path.exists(allure_results_dir) and os.listdir(allure_results_dir):
            print(f"\n[Email Notification] Sending test results via email...")
            print(f"[Email Notification] Allure results directory: {allure_results_dir}")
            
            success = False
            
            # Thử gửi email với file đính kèm trước
            if SEND_ATTACHMENT:
                success = send_email_with_attachment(allure_results_dir, test_summary)
                if success:
                    print("[Email Notification] Email with attachment sent successfully!")
                else:
                    print("[Email Notification] Failed to send email with attachment")
            
            # Nếu không gửi được attachment hoặc không bật SEND_ATTACHMENT, thử gửi thông báo đơn giản
            if not success and SEND_SIMPLE_NOTIFICATION:
                success = send_simple_notification(allure_results_dir)
                if success:
                    print("[Email Notification] Simple notification sent successfully!")
                else:
                    print("[Email Notification] Failed to send simple notification")
            
            if not success:
                print("[Email Notification] All email sending methods failed")
        else:
            print(f"[Email Notification] No allure results found at {allure_results_dir}")
            print("[Email Notification] Skipping email notification")
            
    except Exception as e:
        print(f"[Email Notification] Error in email notification: {e}")
        logger.error(f"Email notification failed: {e}")


def pytest_configure(config):
    """Hook chạy khi pytest được cấu hình"""
    import os, platform, sys
    
    # 1) Lấy alluredir đúng chuẩn
    try:
        allure_results_dir = config.getoption("--alluredir")
    except Exception:
        allure_results_dir = None
    
    if not allure_results_dir:
        # Dùng rootpath của pytest để tránh lệch thư mục làm việc
        root = str(getattr(config, "rootpath", os.getcwd()))
        allure_results_dir = os.path.join(root, "allure-results")

    print(f"[Allure] results dir: {os.path.abspath(allure_results_dir)}")
    os.makedirs(allure_results_dir, exist_ok=True)

    # 2) Lấy thông tin browser có fallback
    browser = "Chrome"
    try:
        from configs.config import Config
        if hasattr(Config, "BROWSER"):
            browser = str(Config.BROWSER)
    except Exception as e:
        print(f"[Allure] Config import fallback because: {e}")

    # 3) Ghi environment.properties (idempotent)
    env_file = os.path.join(allure_results_dir, "environment.properties")
    try:
        if not os.path.exists(env_file):
            with open(env_file, "w", encoding="utf-8") as f:
                f.write(f"os={platform.system()} {platform.release()}\n")
                f.write(f"browser={browser}\n")
                f.write(f"python_version={sys.version.split()[0]}\n")
                f.write("test_environment=Testing\n")
            print(f"[Allure] env written: {env_file}")
        else:
            print(f"[Allure] env already exists: {env_file}")
    except Exception as e:
        print(f"[Allure] write env failed: {e}")

