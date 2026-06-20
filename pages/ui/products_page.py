from typing import Optional
from pages.ui.base_page import BasePage
from selenium.webdriver.common.by import By

class ProductsPage(BasePage):
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def add_product_by_name(self, product_name: str):
        visible_name = product_name
        if "-" in product_name:
            visible_name = product_name.replace("-", " ").title()

        xpath = (
            "//div[contains(@class,'inventory_item')]"
            f"//div[contains(@class,'inventory_item_name') and normalize-space(text())=\"{visible_name}\"]"
            "//ancestor::div[contains(@class,'inventory_item')]//button"
        )
        try:
            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
            return
        except Exception:
            add_button = (By.ID, f"add-to-cart-{product_name}")
            self.click(add_button)

    def remove_product_by_name(self, product_name: str):
        remove_button = (By.ID, f"remove-{product_name}")
        self.click(remove_button)

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def badge(self) -> Optional[str]:
        if self.is_element_present(self.CART_BADGE, timeout=2):
            return self.text_of_element(self.CART_BADGE)
        return "0"

    def product_name_by_index(self, index: int) -> Optional[str]:
        product_items = self.find_all(self.PRODUCT_NAME)
        if 0 <= index < len(product_items):
            return product_items[index].text
        return None

    def menu(self):
        self.click(self.MENU_BUTTON)

    def logout(self):
        self.click(self.LOGOUT_LINK)