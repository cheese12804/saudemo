import os
import allure
from datetime import datetime
from selenium import webdriver
from configs.logging_config import logger


class ScreenshotUtil:
    @staticmethod
    def capture_screenshot(driver, name=None):
        try:
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            if name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = f"screenshot_{timestamp}"
            
            filename = f"{name}.png"
            filepath = os.path.join(screenshot_dir, filename)

            driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            return None
    
    @staticmethod
    def attach_screenshot_to_allure(driver, name="Screenshot"):
        try:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"Screenshot attached to Allure report: {name}")
            
        except Exception as e:
            logger.error(f"Failed to attach screenshot to Allure: {str(e)}")
    
    @staticmethod
    def capture_and_attach_on_error(driver, name="Error Screenshot"):
        try:
            ScreenshotUtil.attach_screenshot_to_allure(driver, name)
            ScreenshotUtil.capture_screenshot(driver, name)
        except Exception as e:
            logger.error(f"Failed to capture error screenshot: {str(e)}")
    
