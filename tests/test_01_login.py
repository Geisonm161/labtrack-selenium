import pytest

from tests.pages.login_page import LoginPage


@pytest.mark.historia("HU-01")
@pytest.mark.tipo("camino_feliz")
def test_login_con_credenciales_validas(driver, base_url, admin_credentials):
    page = LoginPage(driver, base_url).load()
    page.login(*admin_credentials)

    page.wait.until(lambda current_driver: "/equipos" in current_driver.current_url)
    assert "Inventario de equipos" in page.body_text


@pytest.mark.historia("HU-01")
@pytest.mark.tipo("negativa")
def test_login_rechaza_credenciales_invalidas(driver, base_url, admin_credentials):
    page = LoginPage(driver, base_url).load()
    username, _password = admin_credentials
    page.login(username, "credencial-invalida")

    assert "Credenciales inválidas." in page.body_text
    assert "/login" in driver.current_url


@pytest.mark.historia("HU-01")
@pytest.mark.tipo("limite")
def test_login_no_permite_usuario_vacio(driver, base_url, admin_credentials):
    page = LoginPage(driver, base_url).load()
    _username, password = admin_credentials
    page.login("", password)

    assert page.username_validation_message()
    assert "/login" in driver.current_url
