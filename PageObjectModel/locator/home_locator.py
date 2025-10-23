from selenium.webdriver.common.by import By
class HomeLocator:
    FILTER_DROPDOWN = (By.XPATH, "//select[@data-test='product-sort-container']")
    CART_BADGE = (By.XPATH, "//a[@data-test='shopping-cart-link']")
    PRODUCT_NAME_ITEMS = (By.XPATH, "//div[contains(@class,'inventory_item_name')]")
    PRODUCT_PRICE_ITEMS = (By.XPATH, "//div[@class='inventory_item_price']")
    LOGOUT_BUTTON = (By.ID, "logout_sidebar_link")
    MENU_BUTTON = (By.XPATH, "//button[text()='Open Menu']")
    @staticmethod
    def add_to_cart_by_name (name):
        xpath = f"//div[text()='{name}']/parent::a/parent::div/following-sibling::div//button"
        return (By.XPATH, xpath)
