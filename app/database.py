import sqlite3
from pathlib import Path

from flask import Flask, current_app, g
from werkzeug.security import generate_password_hash


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity BETWEEN 0 AND 9999),
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    database = g.pop("db", None)
    if database is not None:
        database.close()


def initialize_database(reset: bool = False) -> None:
    database = get_db()
    if reset:
        database.executescript("DROP TABLE IF EXISTS equipment; DROP TABLE IF EXISTS users;")

    database.executescript(SCHEMA)
    admin_password = current_app.config.get("ADMIN_PASSWORD")
    if admin_password:
        database.execute(
            "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
            (current_app.config["ADMIN_USERNAME"], generate_password_hash(admin_password)),
        )
    database.execute(
        """
        INSERT OR IGNORE INTO equipment (code, name, category, status, quantity, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("EQ-001", "Microscopio binocular", "Óptica", "Disponible", 4, "Laboratorio A"),
    )
    database.execute(
        """
        INSERT OR IGNORE INTO equipment (code, name, category, status, quantity, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("EQ-002", "Balanza analítica", "Medición", "En mantenimiento", 1, "Calibración anual"),
    )
    database.commit()


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
