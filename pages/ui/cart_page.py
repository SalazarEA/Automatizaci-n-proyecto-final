from pages.ui.base_page import BasePage
from selenium.webdriver.common.by import By

class CartPage(BasePage):
    BUTTON_CHECKOUT = (By.ID, "checkout")
    BUTTON_CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def go_to_checkout(self):
        self.click(self.BUTTON_CHECKOUT)

    def continue_shopping(self):
        self.click(self.BUTTON_CONTINUE_SHOPPING)

    def get_cart_items(self) -> list[str]:
        elements = self.find_all(self.CART_ITEM_NAME)
        return [item.text for item in elements]

    def get_first_cart_item(self) -> str:
        items = self.get_cart_items()
        return items[0] if items else ""

    def remove_product_by_name(self, product_name: str):
        remove_button = (
            By.XPATH,
            f"//div[contains(@class,'cart_item')]//div[@class='inventory_item_name' and normalize-space(text())='{product_name}']"
            "//ancestor::div[contains(@class,'cart_item')]//button"
        )
        self.click(remove_button)

    def is_product_in_cart(self, product_name: str) -> bool:
        return product_name in self.get_cart_items()
