import pytest
from pages.ui.login_page import LoginPage
from pages.ui.products_page import ProductsPage
from utils.data_loader import load_users_from_csv, load_users_from_json


@pytest.mark.parametrize("user", load_users_from_csv("data/users.csv"))
def test_title_with_csv_users(driver, user):
    login = LoginPage(driver)
    login.load()
    assert login.driver.title == "Swag Labs"
    login.login_as_user(user["username"], user["password"])
    assert "/inventory.html" in login.driver.current_url


@pytest.mark.parametrize("user", load_users_from_json("data/users.json"))
def test_login_with_json_users(driver, user):
    login = LoginPage(driver)
    login.load()
    login.login_as_user(user["username"], user["password"])
    assert login.driver.title == "Swag Labs"
    assert "/inventory.html" in login.driver.current_url


def test_login_no_valid_user(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "wrong_password")
    assert login.has_error_message(), "No se muestra el mensaje de error"


def test_logout(driver):
    login = LoginPage(driver)
    login.load()
    login.login_as_user("standard_user", "secret_sauce")
    products_page = ProductsPage(driver)
    products_page.menu()
    products_page.logout()
    assert "https://www.saucedemo.com/" in login.driver.current_url, "No se redirige a la página de login después de cerrar sesión"
