import pytest


@pytest.mark.historia("HU-05")
@pytest.mark.tipo("camino_feliz")
def test_eliminar_equipo_confirmado(driver, authenticated_list):
    authenticated_list.delete("EQ-002", confirm=True)

    authenticated_list.wait.until(lambda _driver: "EQ-002" not in authenticated_list.codes())
    assert "Equipo eliminado correctamente." in authenticated_list.body_text


@pytest.mark.historia("HU-05")
@pytest.mark.tipo("negativa")
def test_cancelar_eliminacion_conserva_el_equipo(driver, authenticated_list):
    authenticated_list.delete("EQ-001", confirm=False)

    assert "EQ-001" in authenticated_list.codes()
    assert "Equipo eliminado correctamente." not in authenticated_list.body_text


@pytest.mark.historia("HU-05")
@pytest.mark.tipo("limite")
def test_eliminar_ultimo_equipo_muestra_inventario_vacio(driver, authenticated_list):
    authenticated_list.delete("EQ-001", confirm=True)
    authenticated_list.wait.until(lambda _driver: "EQ-001" not in authenticated_list.codes())
    authenticated_list.delete("EQ-002", confirm=True)

    authenticated_list.wait.until(lambda _driver: len(authenticated_list.codes()) == 0)
    assert "Agrega el primer equipo del inventario." in authenticated_list.body_text

