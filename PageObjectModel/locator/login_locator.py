from selenium.webdriver.common.by import By
class LoginPageLocator:
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='Username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']")
    SIGNIN_BUTTON = (By.XPATH, "//input[@type='submit']")
    INVALID_CREDENTIALS_MESSAGE = (By.XPATH, "//h3[@data-test='error']")