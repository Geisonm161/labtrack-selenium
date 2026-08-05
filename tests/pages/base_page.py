from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 8)

    def open(self, path: str) -> None:
        self.driver.get(f"{self.base_url}{path}")

    @property
    def body_text(self) -> str:
        def read_body(driver: WebDriver) -> str | bool:
            try:
                return driver.find_element("tag name", "body").text or False
            except StaleElementReferenceException:
                return False

        return self.wait.until(read_body)
