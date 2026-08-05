from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from tests.pages.base_page import BasePage


class EquipmentListPage(BasePage):
    SEARCH = (By.ID, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-form button[type='submit']")
    NEW_BUTTON = (By.LINK_TEXT, "+ Nuevo equipo")
    EMPTY_STATE = (By.CSS_SELECTOR, "[data-testid='empty-state']")

    def load(self) -> "EquipmentListPage":
        self.open("/equipos")
        self.wait.until(expected.visibility_of_element_located(self.SEARCH))
        return self

    def search(self, term: str) -> None:
        field = self.driver.find_element(*self.SEARCH)
        field.clear()
        field.send_keys(term)
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def codes(self) -> list[str]:
        return [row.get_attribute("data-code") for row in self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='equipment-row']")]

    def open_new(self) -> None:
        self.driver.find_element(*self.NEW_BUTTON).click()

    def open_detail(self, code: str) -> None:
        row = self._row(code)
        row.find_element(By.CSS_SELECTOR, ".table-link").click()

    def open_edit(self, code: str) -> None:
        self._row(code).find_element(By.LINK_TEXT, "Editar").click()

    def delete(self, code: str, confirm: bool = True) -> None:
        row = self._row(code)
        row.find_element(By.CSS_SELECTOR, "[data-open-dialog]").click()
        dialog = row.find_element(By.CSS_SELECTOR, "dialog")
        self.wait.until(lambda _driver: dialog.get_attribute("open") is not None)
        label = "Sí, eliminar" if confirm else "Cancelar"
        dialog.find_element(By.XPATH, f".//button[normalize-space()='{label}']").click()

    def _row(self, code: str):
        return self.wait.until(
            expected.presence_of_element_located(
                (By.CSS_SELECTOR, f"[data-testid='equipment-row'][data-code='{code}']")
            )
        )

