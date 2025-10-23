from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from configs.config import Config
from configs.logging_config import logger


class DriverManager:
    driver = None

    @staticmethod
    def init_driver():
        if DriverManager.driver is None:
            browser = Config.BROWSER
            logger.info(f"Initializing {browser} driver")
            options = Options()
            options.add_argument("--guest")
            if browser == 'chrome':
                DriverManager.driver = webdriver.Chrome(options=options)
            elif browser == 'firefox':
                DriverManager.driver = webdriver.Firefox()
            elif browser == 'edge':
                DriverManager.driver = webdriver.Edge()
            else:
                logger.warning(f"Browser '{browser}' không được hỗ trợ. Sử dụng Chrome mặc định.")
                DriverManager.driver = webdriver.Chrome()

            logger.info("Maximizing browser window and setting implicit wait")
            DriverManager.driver.maximize_window()
            DriverManager.driver.implicitly_wait(Config.IMPLICIT_WAIT)
            logger.info(f"Driver initialized successfully: {browser}")
        else:
            logger.debug("Driver already exists, reusing current instance")
        return DriverManager.driver

    @staticmethod
    def get_driver():
        return DriverManager.driver

    @staticmethod
    def open_base_url():
        logger.info(f"Opening URL: {Config.LOGIN_URL}")
        driver = DriverManager.init_driver()
        driver.get(Config.LOGIN_URL)
        logger.info("URL opened successfully")

    @staticmethod
    def quit_driver():
        if DriverManager.driver is not None:
            logger.info("Quitting driver")
            try:
                DriverManager.driver.quit()
                logger.info("Driver quit successfully")
            except Exception as e:
                logger.error(f"Error while quitting driver: {str(e)}")
            finally:
                DriverManager.driver = None
        else:
            logger.debug("Driver is already None")
