from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import Select

from tests.pages.base_page import BasePage


class EquipmentFormPage(BasePage):
    FORM = (By.CSS_SELECTOR, "[data-testid='equipment-form']")

    def wait_until_loaded(self) -> "EquipmentFormPage":
        self.wait.until(expected.visibility_of_element_located(self.FORM))
        return self

    def fill(
        self,
        *,
        code: str,
        name: str,
        category: str,
        status: str,
        quantity: str,
        notes: str = "",
    ) -> None:
        values = {
            "code": code,
            "name": name,
            "category": category,
            "quantity": quantity,
            "notes": notes,
        }
        for field_id, value in values.items():
            field = self.driver.find_element(By.ID, field_id)
            field.clear()
            field.send_keys(value)
        Select(self.driver.find_element(By.ID, "status")).select_by_visible_text(status)

    def submit(self) -> None:
        form = self.driver.find_element(*self.FORM)
        form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
