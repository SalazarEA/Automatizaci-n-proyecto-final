from selenium.webdriver.common.by import By
from pages.ui.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    INPUT_USERNAME = (By.ID, "user-name")
    INPUT_PASSWORD = (By.ID, "password")
    BUTTON_LOGIN = (By.ID, "login-button")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")

    def load(self):
        self.visit(self.URL)

    def login_as_user(self, username: str, password: str):
        self.type(self.INPUT_USERNAME, username)
        self.type(self.INPUT_PASSWORD, password)
        self.click(self.BUTTON_LOGIN)

    def has_error_message(self) -> bool:
        return self.element_is_visible(self.ERROR_MESSAGE)
    