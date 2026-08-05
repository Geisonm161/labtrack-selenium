from sqlite3 import Row

from werkzeug.security import check_password_hash

from app.database import get_db


def authenticate(username: str, password: str) -> Row | None:
    user = get_db().execute(
        "SELECT * FROM users WHERE username = ?", (username.strip(),)
    ).fetchone()
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None

