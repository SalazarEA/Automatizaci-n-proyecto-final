import pytest

from pages.ui.cart_page import CartPage
from pages.ui.checkout_page import CheckoutPage
from pages.ui.login_page import LoginPage
from pages.ui.products_page import ProductsPage


def test_end_to_end_purchase_flow(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Backpack")
    products_page.add_product_by_name("Sauce Labs Bike Light")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.is_product_in_cart("Sauce Labs Backpack")
    assert cart_page.is_product_in_cart("Sauce Labs Bike Light")
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_information("Jane", "Doe", "12345")
    checkout_page.continue_checkout()
    checkout_page.finish_checkout()

    assert checkout_page.order_complete_message() == "Thank you for your order!"


def test_multiple_items_complete_purchase_flow(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Backpack")
    products_page.add_product_by_name("Sauce Labs Bike Light")
    products_page.add_product_by_name("Test.allTheThings() T-Shirt (Red)")

    assert products_page.badge() == "3"
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    assert len(cart_page.get_cart_items()) == 3
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_information("Test", "User", "55555")
    checkout_page.continue_checkout()
    checkout_page.finish_checkout()

    assert checkout_page.order_complete_message() == "Thank you for your order!"


def test_remove_from_cart_flow(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Backpack")
    products_page.add_product_by_name("Sauce Labs Bike Light")
    assert products_page.badge() == "2"

    products_page.go_to_cart()
    cart_page = CartPage(driver)
    assert len(cart_page.get_cart_items()) == 2

    cart_page.remove_product_by_name("Sauce Labs Bike Light")
    assert len(cart_page.get_cart_items()) == 1
    assert cart_page.is_product_in_cart("Sauce Labs Backpack")
    assert not cart_page.is_product_in_cart("Sauce Labs Bike Light")