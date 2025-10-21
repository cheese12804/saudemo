import allure

from PageObjectModel.pages.login_page import LoginPage


@allure.title("Login with valid credentials")
@allure.description("Test login functionality with correct username and password")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "login", "positive")
def test_login_valid_credentials():
    username = "standard_user"
    password = "secret_sauce"
    LoginPage.enter_username(username)
    LoginPage.enter_password(password)
    LoginPage.click_login_button()
    LoginPage.is_login_successful()


@allure.title("Login with invalid password")
@allure.description("Test login functionality with correct username but wrong password")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("login", "negative")
def test_login_invalid_password():
    username = "standard_user"
    password = "wrong_password"
    LoginPage.enter_username(username)
    LoginPage.enter_password(password)
    LoginPage.click_login_button()

    LoginPage.verify_login_unsuccessful_msg()
