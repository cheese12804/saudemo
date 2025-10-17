from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from configs.logging_config import logger
from configs.config import Config
from webdriver_manage.driver_manage import DriverManager
from selenium.webdriver.support import expected_conditions as EC
from utils.screenshot_util import ScreenshotUtil


class BasePage:
    @staticmethod
    def wait_until():
        wait = WebDriverWait(DriverManager.get_driver(), Config.EXPLICIT_WAIT)
        return wait
    @staticmethod
    def find_element(locator) -> WebElement:
        element = DriverManager.get_driver().find_element(*locator)
        BasePage.highlight_element(element)
        return element

    @staticmethod
    def find_elements(locator) -> list[WebElement]:
        return DriverManager.driver.find_elements(*locator)

    @staticmethod
    def click(locator):
        logger.info(f"Clicking element: {locator}")
        BasePage.find_element(locator).click()

    @staticmethod
    def enter_text(locator, text):
        logger.info(f"Entering text into {locator}: {text}")
        element = BasePage.find_element(locator)
        element.clear()
        element.send_keys(text)

    @staticmethod
    def wait_for_element(locator):
        BasePage.wait_until().until(EC.presence_of_element_located(locator))

    @staticmethod
    def select_value(locator, option_value):
        logger.info(f"Selecting value '{option_value}' from {locator}")
        element = BasePage.find_element(locator)
        Select(element).select_by_value(option_value)

    @staticmethod
    def select_text(locator, visible_text):
        logger.info(f"Selecting text '{visible_text}' from {locator}")
        element = BasePage.find_element(locator)
        Select(element).select_by_visible_text(visible_text)
    @staticmethod
    def wait_for_element_visibility(locator):
        logger.info(f"Waiting for element visibility: {locator}")
        BasePage.wait_until().until(EC.visibility_of_element_located(locator))
    @staticmethod
    def wait_for_element_clickable(locator):
        logger.info(f"Waiting for element clickable: {locator}")
        BasePage.wait_until().until(EC.element_to_be_clickable(locator))
    @staticmethod
    def wait_for_element_visible(locator):
        logger.info(f"Waiting for element visible: {locator}")
        BasePage.wait_until().until(EC.visibility_of_element_located(locator))
    @staticmethod
    def wait_for_element_invisible(locator):
        logger.info(f"Waiting for element invisible: {locator}")
        BasePage.wait_until().until(EC.invisibility_of_element_located(locator))
    @staticmethod
    def capture_screenshot(name):
        ScreenshotUtil.capture_screenshot(DriverManager.driver, name)
    @staticmethod
    def attach_screenshot_to_allure(name):
        ScreenshotUtil.attach_screenshot_to_allure(DriverManager.driver, name)
    @staticmethod
    def capture_and_attach_on_error(name):
        ScreenshotUtil.capture_and_attach_on_error(DriverManager.driver, name)
    @staticmethod
    def get_parent_window():
        return DriverManager.driver.current_window_handle
    @staticmethod
    def get_all_windows():
        return DriverManager.driver.window_handles
    @staticmethod
    def switch_to_window_by_id(window_id):
        all_windows = BasePage.get_all_windows()
        for window in all_windows:
            if window == window_id:
                DriverManager.driver.switch_to.window(window)
                break

    @staticmethod
    def switch_to_window_by_title(title):
        all_windows = BasePage.get_all_windows()
        logger.info(f"Available windows: {len(all_windows)}")
        for window in all_windows:
            DriverManager.driver.switch_to.window(window)  # Switch to the window
            current_title = DriverManager.driver.title
            current_url = DriverManager.driver.current_url
            logger.info(f"Window title: '{current_title}', URL: '{current_url}'")
            if title.lower() in current_title.lower():  # Check if title contains the search term
                logger.info(f"Found matching window with title: '{current_title}'")
                break

    @staticmethod
    def switch_to_window_by_url(url_fragment):
        all_windows = BasePage.get_all_windows()
        logger.info(f"Available windows: {len(all_windows)}")
        for window in all_windows:
            DriverManager.driver.switch_to.window(window)
            current_url = DriverManager.driver.current_url
            current_title = DriverManager.driver.title
            logger.info(f"Window URL: '{current_url}', Title: '{current_title}'")
            if url_fragment in current_url:
                logger.info(f"Found matching window with URL containing '{url_fragment}': {current_url}")
                break

    @staticmethod
    def switch_to_frame(locator):
        frame = BasePage.find_element(locator)
        DriverManager.driver.switch_to.frame(frame)
    @staticmethod
    def close_all_windows_except_parent():
        parent_window = BasePage.get_parent_window()
        all_windows = BasePage.get_all_windows()
        for window in all_windows:
            if window != parent_window:
                DriverManager.driver.switch_to.window(window)
                DriverManager.driver.close()
        DriverManager.driver.switch_to.window(parent_window)
        if (len(BasePage.get_all_windows()) == 1):
            logger.info("All child windows closed, back to parent window")
        else:
            logger.error("Some child windows are still open")
    @staticmethod
    def scroll_to_element(locator):
        element = BasePage.find_element(locator)
        DriverManager.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.info(f"Scrolled to element: {locator}")
    @staticmethod
    def open_new_tab(url):
        DriverManager.driver.execute_script(f"window.open('{url}','_blank');")
        logger.info(f"Opened new tab with URL: {url}")
    @staticmethod
    def execute_script(script, *args):
        return DriverManager.driver.execute_script(script, *args)
    
    @staticmethod
    def highlight_element(element):
        DriverManager.driver.execute_script("""
            arguments[0].style.border='2px solid red';
        """, element)

    @staticmethod
    def open_new_tab_and_switch(url="https://www.saucedemo.com/inventory.html"):
        logger.info(f"Opening new tab with URL: {url}")
        DriverManager.driver.execute_script(f"window.open('{url}', '_blank');")
        DriverManager.driver.switch_to.window(DriverManager.driver.window_handles[1])
        logger.info("Switched to new tab to avoid password popup")

    @staticmethod
    def is_element_display(locator):
        BasePage.find_element(locator).is_displayed()

    @staticmethod
    def is_element_enable(locator):
        BasePage.find_element(locator).is_enabled()

    @staticmethod
    def get_text(locator) -> str:
        return BasePage.find_element(locator).text