import allure
import faker

from PageObjectModel.pages.cart_page import CartPage
from PageObjectModel.pages.checkout_page import CheckoutPage
from PageObjectModel.pages.home_page import HomePage
from PageObjectModel.pages.login_page import LoginPage

fake = faker.Faker()


@allure.title("Buy product")
@allure.description("Test buy product")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "buy", "positive")
def test_buy_product():
    username = "standard_user"
    password = "secret_sauce"
    sort_option_by_name = "Name (Z to A)"
    sort_option_by_price = "Price (low to high)"
    product_name1 = "Sauce Labs Backpack"
    product_name2 = "Sauce Labs Bike Light"
    first_name = fake.first_name()
    last_name = fake.last_name()
    postal_code = fake.postcode()

    LoginPage.login_with_credentials(username, password)
    HomePage.sort_products(sort_option_by_name)
    assert HomePage.is_sort_successful(sort_option_by_name), "Products should be sorted by name in descending order"
    HomePage.sort_products(sort_option_by_price)
    assert HomePage.is_sort_successful(sort_option_by_price), "Products should be sorted by price in ascending order"
    HomePage.add_to_cart(product_name1)
    HomePage.add_to_cart(product_name2)
    HomePage.open_cart()
    assert CartPage.is_cart_containing([product_name1, product_name2]), "Cart should contain the two selected products"
    CartPage.click_checkout()
    CheckoutPage.fill_checkout_form(first_name, last_name, postal_code)
    CheckoutPage.click_continue()
    CheckoutPage.click_finish()
    CheckoutPage.wait_for_order_complete()
