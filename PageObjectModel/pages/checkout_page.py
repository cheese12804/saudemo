import allure
from selenium.webdriver.support import expected_conditions as EC

from base_page import BasePage
from configs.logging_config import logger
from ..locator.checkout_locator import CheckoutPageLocator
from ..locator.commont_locator import CommonLocator

class CheckoutPage(BasePage):
    @staticmethod
    @allure.step("Filling checkout form: {first_name}, {last_name}, {postal_code}")
    def fill_checkout_form(first_name, last_name, postal_code):
        logger.info(f"CheckoutPage: Filling checkout form: {first_name}, {last_name}, {postal_code}")
        CheckoutPage.wait_for_element_visible(CommonLocator.element_by_placeholder("First Name"))
        CheckoutPage.enter_text(CommonLocator.element_by_placeholder("First Name"), first_name)
        CheckoutPage.enter_text(CommonLocator.element_by_placeholder("Last Name"), last_name)
        CheckoutPage.enter_text(CommonLocator.element_by_placeholder("Zip/Postal Code"), postal_code)
    @staticmethod
    @allure.step("Clicking continue button")
    def click_continue():
        logger.info("CheckoutPage: Clicking continue button")
        CheckoutPage.wait_for_element_clickable(CheckoutPageLocator.CONTINUE_BUTTON)
        CheckoutPage.click(CheckoutPageLocator.CONTINUE_BUTTON)
    @staticmethod
    @allure.step("Clicking finish button")
    def click_finish():
        logger.info("CheckoutPage: Clicking finish button")
        CheckoutPage.wait_for_element_clickable(CheckoutPageLocator.FINISH_BUTTON)
        CheckoutPage.click(CheckoutPageLocator.FINISH_BUTTON)
    
    @staticmethod
    @allure.step("Verifying order completion")
    def wait_for_order_complete():
        logger.info("CheckoutPage: Verifying order completion")
        CheckoutPage.wait_for_element_visible(CommonLocator.element_by_text("Thank you for your order!"))
    