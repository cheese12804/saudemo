import allure
from selenium.webdriver.support import expected_conditions as EC

from base_page import BasePage
from configs.logging_config import logger
from ..locator.commont_locator import CommonLocator
from ..locator.home_locator import ListProductPageLocator

class HomePage(BasePage):
    @staticmethod
    @allure.step("Sorted products by: {option_value}")
    def sort_products(option_value):
        logger.info(f"ListProductPage: Sorting products by {option_value}")
        HomePage.wait_for_element_clickable(ListProductPageLocator.FILTER_DROPDOWN)
        HomePage.click(ListProductPageLocator.FILTER_DROPDOWN)
        HomePage.wait_for_element_clickable(CommonLocator.element_by_text(option_value))
        HomePage.click(CommonLocator.element_by_text(option_value))
    @staticmethod
    @allure.step(f"Add to cart product product_name")
    def add_to_cart(product_name):
        logger.info(f"ListProductPage: Adding product to cart {product_name}")
        HomePage.wait_for_element_clickable(ListProductPageLocator.add_to_cart_by_name(product_name))
        HomePage.click(ListProductPageLocator.add_to_cart_by_name(product_name))
    @staticmethod
    @allure.step("Open cart page")
    def open_cart():
        logger.info("ListProductPage: Opening cart page")
        HomePage.wait_for_element_clickable(ListProductPageLocator.CART_BADGE)
        HomePage.click(ListProductPageLocator.CART_BADGE)
    @staticmethod
    def get_product_names():
        elements = HomePage.find_elements(ListProductPageLocator.PRODUCT_NAME_ITEMS)
        return [e.text.strip() for e in elements]
    @staticmethod
    def get_product_prices():
        elements = HomePage.find_elements(ListProductPageLocator.PRODUCT_PRICE_ITEMS)
        return [float(e.text.replace("$", "").strip()) for e in elements]
    @staticmethod
    def is_sort_successful(option_value):
        if option_value in ["Name (A to Z)", "Name (Z to A)"]:
            names = HomePage.get_product_names()
            logger.info(f"Captured product names: {names}")
            expected = sorted(names, reverse=(option_value == "Name (Z to A)"))
            logger.info(f"Expected sorted names ({option_value}): {expected}")
            return names == expected
        if option_value in ["Price (low to high)", "Price (high to low)"]:
            prices = HomePage.get_product_prices()
            logger.info(f"Captured product prices: {prices}")
            expected = sorted(prices, reverse=(option_value == "Price (high to low)"))
            logger.info(f"Expected sorted prices ({option_value}): {expected}")
            return prices == expected
