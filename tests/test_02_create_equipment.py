import pytest

from tests.pages.equipment_form_page import EquipmentFormPage


@pytest.mark.historia("HU-02")
@pytest.mark.tipo("camino_feliz")
def test_crear_equipo_con_datos_validos(driver, base_url, authenticated_list):
    authenticated_list.open_new()
    form = EquipmentFormPage(driver, base_url).wait_until_loaded()
    form.fill(code="EQ-100", name="Centrífuga digital", category="Procesamiento", status="Disponible", quantity="3", notes="Sala B")
    form.submit()

    assert "Equipo creado correctamente." in form.body_text
    assert "Centrífuga digital" in form.body_text


@pytest.mark.historia("HU-02")
@pytest.mark.tipo("negativa")
def test_crear_equipo_rechaza_codigo_duplicado(driver, base_url, authenticated_list):
    authenticated_list.open_new()
    form = EquipmentFormPage(driver, base_url).wait_until_loaded()
    form.fill(code="EQ-001", name="Equipo repetido", category="Óptica", status="Disponible", quantity="2")
    form.submit()

    assert "Ya existe un equipo con este código." in form.body_text
    assert "/nuevo" in driver.current_url


@pytest.mark.historia("HU-02")
@pytest.mark.tipo("limite")
def test_crear_equipo_acepta_nombre_de_80_caracteres(driver, base_url, authenticated_list):
    authenticated_list.open_new()
    form = EquipmentFormPage(driver, base_url).wait_until_loaded()
    boundary_name = "E" * 80
    form.fill(code="LIM-12345678", name=boundary_name, category="Instrumentación", status="Prestado", quantity="0")
    form.submit()

    assert "Equipo creado correctamente." in form.body_text
    assert boundary_name in form.body_text

