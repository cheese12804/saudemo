from selenium.webdriver.common.by import By
class CartPageLocator:
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_ITEM = (By.CLASS_NAME, "inventory_item_name")
