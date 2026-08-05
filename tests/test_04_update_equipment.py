import pytest

from tests.pages.equipment_form_page import EquipmentFormPage


@pytest.mark.historia("HU-04")
@pytest.mark.tipo("camino_feliz")
def test_actualizar_equipo_con_datos_validos(driver, base_url, authenticated_list):
    authenticated_list.open_edit("EQ-001")
    form = EquipmentFormPage(driver, base_url).wait_until_loaded()
    form.fill(code="EQ-001", name="Microscopio binocular Pro", category="Óptica", status="Prestado", quantity="2", notes="Asignado a prácticas")
    form.submit()

    assert "Equipo actualizado correctamente." in form.body_text
    assert "Microscopio binocular Pro" in form.body_text
    assert "Prestado" in form.body_text


@pytest.mark.historia("HU-04")
@pytest.mark.tipo("negativa")
def test_actualizar_equipo_rechaza_codigo_de_otro_registro(driver, base_url, authenticated_list):
    authenticated_list.open_edit("EQ-001")
    form = EquipmentFormPage(driver, base_url).wait_until_loaded()
    form.fill(code="EQ-002", name="Microscopio binocular", category="Óptica", status="Disponible", quantity="4")
    form.submit()

    assert "Ya existe un equipo con este código." in form.body_text


@pytest.mark.historia("HU-04")
@pytest.mark.tipo("limite")
def test_actualizar_equipo_acepta_cantidad_maxima(driver, base_url, authenticated_list):
    authenticated_list.open_edit("EQ-002")
    form = EquipmentFormPage(driver, base_url).wait_until_loaded()
    form.fill(code="EQ-002", name="Balanza analítica", category="Medición", status="Disponible", quantity="9999", notes="Inventario máximo")
    form.submit()

    assert "Equipo actualizado correctamente." in form.body_text
    assert "9999" in form.body_text

