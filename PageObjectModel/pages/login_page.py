import allure

from base_page import BasePage
from configs.logging_config import logger
from ..locator.commont_locator import CommonLocator
from ..locator.login_locator import LoginPageLocator


class LoginPage(BasePage):
    @staticmethod
    @allure.step("Entering username: {username}")
    def enter_username(username):
        logger.info(f"LoginPage: Entering username: {username}")
        LoginPage.wait_for_element_visible(LoginPageLocator.USERNAME_INPUT)
        LoginPage.enter_text(LoginPageLocator.USERNAME_INPUT, username)

    @staticmethod
    @allure.step("Entering password: {password}")
    def enter_password(password):
        logger.info(f"LoginPage: Entering password: {password}")
        LoginPage.wait_for_element_visible(LoginPageLocator.PASSWORD_INPUT)
        LoginPage.enter_text(LoginPageLocator.PASSWORD_INPUT, password)

    @staticmethod
    @allure.step("Clicking login button")
    def click_login_button():
        logger.info("LoginPage: Clicking login button")
        LoginPage.wait_for_element_clickable(LoginPageLocator.SIGNIN_BUTTON)
        LoginPage.click(LoginPageLocator.SIGNIN_BUTTON)

    @staticmethod
    @allure.step("Login with credentials")
    def login_with_credentials(username, password):
        LoginPage.enter_username(username)
        LoginPage.enter_password(password)
        LoginPage.click_login_button()

    @staticmethod
    @allure.step("Checking if login is successful")
    def is_login_successful():
        CommonLocator.element_by_id("shopping_cart_container")

    @staticmethod
    @allure.step("Checking if login is unsuccessful")
    def verify_login_unsuccessful_msg():
        LoginPage.wait_for_element_visible(LoginPageLocator.INVALID_CREDENTIALS_MESSAGE)
        assert LoginPage.get_text(LoginPageLocator.INVALID_CREDENTIALS_MESSAGE) == 'Epic sadface: Username and password do not match any user in this service'
