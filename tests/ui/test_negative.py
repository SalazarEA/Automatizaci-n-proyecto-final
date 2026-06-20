import pytest

from pages.ui.cart_page import CartPage
from pages.ui.checkout_page import CheckoutPage
from pages.ui.login_page import LoginPage
from pages.ui.products_page import ProductsPage


@pytest.mark.negative
def test_locked_out_user_cannot_login(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("locked_out_user", "secret_sauce")
    assert login.has_error_message(), "Locked out user should see an error message"


@pytest.mark.negative
def test_checkout_requires_all_customer_information(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Bike Light")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_information("Jane", "", "12345")
    checkout_page.continue_checkout()

    assert checkout_page.has_error_message(), "Checkout should show an error when required fields are missing"


@pytest.mark.negative
def test_invalid_login_shows_error_message(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "invalid_password")
    assert login.has_error_message(), "Should show error for invalid password"


@pytest.mark.negative
def test_checkout_missing_postal_code(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_information("Test", "User", "")
    checkout_page.continue_checkout()

    assert checkout_page.has_error_message(), "Should show error for missing postal code"


@pytest.mark.negative
def test_checkout_missing_first_name(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Bike Light")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_information("", "Doe", "12345")
    checkout_page.continue_checkout()

    assert checkout_page.has_error_message(), "Should show error for missing first name"
