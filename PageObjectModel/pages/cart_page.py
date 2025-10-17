import allure
from selenium.webdriver.support import expected_conditions as EC

from base_page import BasePage
from configs.logging_config import logger
from ..locator.commont_locator import CommonLocator
from ..locator.cart_locator import CartPageLocator
class CartPage(BasePage):
    @staticmethod
    @allure.step("Getting checkout")
    def click_checkout():
        logger.info("CartPage: Clicking checkout button")
        CartPage.wait_for_element_clickable(CommonLocator.button_by_text("Checkout"))
        CartPage.click(CommonLocator.button_by_text("Checkout"))

    @staticmethod
    def get_cart_item_names():
        elements = CartPage.find_elements(CartPageLocator.CART_ITEM)
        return [e.text.strip() for e in elements]

    @staticmethod
    @allure.step("Verify cart contains expected products")
    def is_cart_containing(expected_names):
        actual_names = CartPage.get_cart_item_names()
        logger.info(f"CartPage: Actual items: {actual_names}")
        logger.info(f"CartPage: Expected items: {expected_names}")
        return sorted(actual_names) == sorted(expected_names)