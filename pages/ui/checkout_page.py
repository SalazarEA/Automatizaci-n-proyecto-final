from pages.ui.base_page import BasePage
from selenium.webdriver.common.by import By

class CheckoutPage(BasePage):
    INPUT_FIRST_NAME = (By.ID, "first-name")
    INPUT_LAST_NAME = (By.ID, "last-name")
    INPUT_POSTAL_CODE = (By.ID, "postal-code")
    BUTTON_CONTINUE = (By.ID, "continue")
    BUTTON_FINISH = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")

    def fill_customer_information(self, first_name: str, last_name: str, postal_code: str):
        self.type(self.INPUT_FIRST_NAME, first_name)
        self.type(self.INPUT_LAST_NAME, last_name)
        self.type(self.INPUT_POSTAL_CODE, postal_code)

    def continue_checkout(self):
        self.click(self.BUTTON_CONTINUE)

    def finish_checkout(self):
        self.click(self.BUTTON_FINISH)

    def order_complete_message(self) -> str:
        return self.text_of_element(self.COMPLETE_HEADER)

    def has_error_message(self) -> bool:
        return self.element_is_visible(self.ERROR_MESSAGE)