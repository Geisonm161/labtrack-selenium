import pytest


@pytest.mark.historia("HU-03")
@pytest.mark.tipo("camino_feliz")
def test_consultar_detalle_de_equipo(driver, authenticated_list):
    authenticated_list.open_detail("EQ-001")

    assert "Microscopio binocular" in authenticated_list.body_text
    assert "Laboratorio A" in authenticated_list.body_text


@pytest.mark.historia("HU-03")
@pytest.mark.tipo("negativa")
def test_busqueda_sin_coincidencias_muestra_estado_vacio(driver, authenticated_list):
    authenticated_list.search("equipo-inexistente")

    assert "No encontramos equipos" in authenticated_list.body_text
    assert "Prueba con otro término de búsqueda." in authenticated_list.body_text


@pytest.mark.historia("HU-03")
@pytest.mark.tipo("limite")
def test_busqueda_acepta_termino_de_50_caracteres(driver, authenticated_list):
    boundary_query = "x" * 50
    authenticated_list.search(boundary_query)

    search_field = driver.find_element("id", "search")
    assert search_field.get_attribute("value") == boundary_query
    assert "No encontramos equipos" in authenticated_list.body_text

