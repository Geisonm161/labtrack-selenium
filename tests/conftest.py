import base64
import re
import secrets
import threading
from pathlib import Path

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from werkzeug.serving import make_server

from app import create_app
from app.database import initialize_database
from tests.pages.equipment_list_page import EquipmentListPage
from tests.pages.login_page import LoginPage


class TestServer(threading.Thread):
    def __init__(self, app) -> None:
        super().__init__(daemon=True)
        self.server = make_server("127.0.0.1", 0, app)
        self.port = self.server.server_port

    def run(self) -> None:
        self.server.serve_forever()

    def stop(self) -> None:
        self.server.shutdown()


def pytest_html_report_title(report) -> None:
    report.title = "LabTrack · Reporte de pruebas Selenium"


@pytest.fixture(scope="session")
def app(tmp_path_factory):
    database_path = tmp_path_factory.mktemp("database") / "test.sqlite3"
    admin_password = secrets.token_urlsafe(18)
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": secrets.token_hex(32),
            "DATABASE": str(database_path),
            "ADMIN_USERNAME": "selenium-admin",
            "ADMIN_PASSWORD": admin_password,
        }
    )


@pytest.fixture(scope="session")
def base_url(app):
    server = TestServer(app)
    server.start()
    yield f"http://127.0.0.1:{server.port}"
    server.stop()


@pytest.fixture(autouse=True)
def reset_database(app):
    with app.app_context():
        initialize_database(reset=True)


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1000")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(15)
    yield browser
    browser.quit()


@pytest.fixture(scope="session")
def admin_credentials(app):
    return app.config["ADMIN_USERNAME"], app.config["ADMIN_PASSWORD"]


@pytest.fixture
def authenticated_list(driver, base_url, admin_credentials):
    login_page = LoginPage(driver, base_url).load()
    login_page.login(*admin_credentials)
    equipment_page = EquipmentListPage(driver, base_url)
    equipment_page.wait.until(lambda current_driver: "/equipos" in current_driver.current_url)
    return equipment_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or "driver" not in item.funcargs:
        return

    browser = item.funcargs["driver"]
    screenshot_dir = Path("reports/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", item.name)
    screenshot_path = screenshot_dir / f"{safe_name}.png"
    screenshot = browser.get_screenshot_as_png()
    screenshot_path.write_bytes(screenshot)
    encoded_image = base64.b64encode(screenshot).decode("ascii")
    report.extras = getattr(report, "extras", [])
    report.extras.append(pytest_html.extras.png(encoded_image, name="Captura del escenario"))
