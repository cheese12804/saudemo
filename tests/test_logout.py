import allure
from PageObjectModel.pages.home_page import HomePage
from PageObjectModel.pages.login_page import LoginPage


@allure.title("Logout")
@allure.description("Test logout functionality")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "logout", "positive")
def test_logout():
    username = "standard_user"
    password = "secret_sauce"
    LoginPage.login_with_credentials(username, password)
    HomePage.logout()