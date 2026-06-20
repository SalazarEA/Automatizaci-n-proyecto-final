import pytest

from pages.ui.cart_page import CartPage
from pages.ui.checkout_page import CheckoutPage
from pages.ui.login_page import LoginPage
from pages.ui.products_page import ProductsPage
from utils.data_loader import load_json_data


def test_complete_checkout_flow(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("sauce-labs-bike-light")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_information("John", "Doe", "12345")
    checkout_page.continue_checkout()
    checkout_page.finish_checkout()

    assert checkout_page.order_complete_message() == "Thank you for your order!"


@pytest.mark.parametrize("flow", load_json_data("data/checkout_flows.json"))
def test_complete_checkout_flow_from_data(driver, flow):
    login = LoginPage(driver)
    login.load()
    login.login_as_user(flow["username"], flow["password"])

    products_page = ProductsPage(driver)
    for product_name in flow["products"]:
        products_page.add_product_by_name(product_name)
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    for product_name in flow["products"]:
        assert cart_page.is_product_in_cart(product_name)
    cart_page.go_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_information(
        flow["first_name"], flow["last_name"], flow["postal_code"]
    )
    checkout_page.continue_checkout()
    checkout_page.finish_checkout()

    assert checkout_page.order_complete_message() == flow.get(
        "expected_message", "Thank you for your order!"
    )
