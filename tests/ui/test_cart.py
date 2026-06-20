import pytest
from pages.ui.cart_page import CartPage
from pages.ui.login_page import LoginPage
from pages.ui.products_page import ProductsPage


@pytest.mark.parametrize("index", [0, 4, 6])
def test_add_product_by_index_to_cart(driver, index):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    product_name = products_page.product_name_by_index(index)
    assert product_name is not None, f"Product does not exist at position {index}"

    products_page.add_product_by_name(product_name)
    assert products_page.badge() == "1", f"Cart badge should be '1' but got '{products_page.badge()}'"


def test_add_product_to_cart(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")
    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Bike Light")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_item = cart_page.get_first_cart_item()
    assert cart_item == "Sauce Labs Bike Light", f"Expected 'Sauce Labs Bike Light' but got '{cart_item}'"


def test_add_and_remove_product_from_cart(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")

    products_page = ProductsPage(driver)
    products_page.add_product_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.is_product_in_cart("Sauce Labs Backpack")
    cart_page.remove_product_by_name("Sauce Labs Backpack")
    assert not cart_page.is_product_in_cart("Sauce Labs Backpack")
