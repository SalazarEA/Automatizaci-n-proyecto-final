import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    def visit(self, url: str):
        self.logger.info("Visiting URL: %s", url)
        self.driver.get(url)

    def find(self, locator: tuple[By, str], timeout: int = 10):
        self.logger.debug("Find element: %s", locator)
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_visible(self, locator: tuple[By, str], timeout: int = 10):
        self.logger.debug("Find visible element: %s", locator)
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator: tuple[By, str], timeout: int = 10):
        self.logger.info("Click element: %s", locator)
        element = self.find_visible(locator, timeout)
        element.click()

    def type(self, locator: tuple[By, str], text: str, timeout: int = 10):
        self.logger.info("Type into %s: %r", locator, text)
        element = self.find_visible(locator, timeout)
        element.clear()
        element.send_keys(text)

    def text_of_element(self, locator: tuple[By, str], timeout: int = 10) -> str:
        text = self.find_visible(locator, timeout).text
        self.logger.debug("Text of %s: %r", locator, text)
        return text

    def element_is_visible(self, locator: tuple[By, str], timeout: int = 10) -> bool:
        try:
            visible = self.find_visible(locator, timeout).is_displayed()
            self.logger.debug("Element visible %s: %s", locator, visible)
            return visible
        except TimeoutException:
            self.logger.debug("Element not visible: %s", locator)
            return False

    def reload(self):
        self.logger.info("Reloading page")
        self.driver.refresh()

    def is_element_present(self, locator: tuple[By, str], timeout: int = 5) -> bool:
        try:
            self.find(locator, timeout)
            self.logger.debug("Element present: %s", locator)
            return True
        except TimeoutException:
            self.logger.debug("Element not present: %s", locator)
            return False

    def find_all(self, locator: tuple[By, str], timeout: int = 10):
        self.logger.debug("Find all elements: %s", locator)
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
