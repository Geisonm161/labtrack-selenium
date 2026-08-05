# LabTrack — pruebas automatizadas con Selenium

LabTrack es una aplicación web individual para administrar el inventario de equipos de un laboratorio. Incluye autenticación, búsqueda y operaciones CRUD completas. La suite usa Selenium WebDriver con Page Object Model y genera un reporte HTML autocontenido junto con una captura automática por cada escenario.

## Cobertura de la tarea

| Historia | Flujo | Camino feliz | Negativa | Límite |
|---|---|---:|---:|---:|
| HU-01 | Inicio de sesión | ✓ | ✓ | ✓ |
| HU-02 | Crear equipo | ✓ | ✓ | ✓ |
| HU-03 | Consultar/buscar equipo | ✓ | ✓ | ✓ |
| HU-04 | Actualizar equipo | ✓ | ✓ | ✓ |
| HU-05 | Eliminar equipo | ✓ | ✓ | ✓ |

Total: **15 escenarios automatizados**. No se utiliza Selenium IDE.

## Requisitos

- Python 3.11 o superior
- Google Chrome instalado
- Conexión a Internet durante la primera resolución de ChromeDriver por Selenium Manager

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows, la activación es `.venv\Scripts\activate`.

## Ejecutar la aplicación

Configura una cuenta local y una clave de sesión antes de iniciar. Elige valores propios y no los publiques:

```bash
export LABTRACK_ADMIN_USER="admin"
export LABTRACK_ADMIN_PASSWORD="TU_CLAVE_LOCAL"
export LABTRACK_SECRET_KEY="TU_CLAVE_ALEATORIA_DE_SESION"
python run.py
```

Abrir `http://127.0.0.1:5000` e iniciar sesión con los valores configurados.

La base SQLite se crea automáticamente en `instance/inventario.sqlite3` con dos equipos de ejemplo. Las variables solamente se necesitan al crear la base por primera vez.

## Ejecutar las pruebas

```bash
pytest
```

La ejecución crea:

- `reports/reporte.html`: reporte autocontenido con el resultado y la evidencia incrustada.
- `reports/screenshots/`: una imagen PNG por cada escenario.

También es posible ejecutar una historia específica:

```bash
pytest -m "historia('HU-01')"
```

## Organización

```text
app/
├── repositories/       acceso a SQLite
├── routes/             controladores HTTP
├── services/           autenticación, reglas y validaciones
├── static/             sistema visual responsive
└── templates/          vistas Jinja
tests/
├── pages/              Page Objects de Selenium
├── conftest.py         navegador, servidor, datos y capturas
└── test_*.py           escenarios agrupados por historia
docs/                   historias, guion y lista de entrega
reports/                reporte HTML y capturas generadas
```

## Documentación académica

- [Historias de usuario](docs/historias_usuario.md): contenido listo para registrar como cinco historias separadas en Jira o Azure DevOps.
- [Guion del video](docs/guion_video.md): recorrido sugerido para demostrar la ejecución.
- [Lista de entrega](docs/checklist_entrega.md): controles finales para evitar penalizaciones de acceso o formato.

> El documento de la asignación exige que las historias estén publicadas en Jira o Azure DevOps. El archivo local sirve como fuente para crearlas, pero no sustituye el enlace público al tablero.
