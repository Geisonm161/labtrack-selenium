from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "[data-testid='login-form'] button[type='submit']")

    def load(self) -> "LoginPage":
        self.open("/login")
        self.wait.until(expected.visibility_of_element_located(self.USERNAME))
        return self

    def login(self, username: str, password: str) -> None:
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()

    def username_validation_message(self) -> str:
        field = self.driver.find_element(*self.USERNAME)
        return self.driver.execute_script("return arguments[0].validationMessage", field)

