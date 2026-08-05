import secrets
from functools import wraps
from typing import Any, Callable

from flask import abort, redirect, request, session, url_for


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(view)
    def wrapped_view(*args: Any, **kwargs: Any) -> Any:
        if "user_id" not in session:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(24)
    return session["csrf_token"]


def validate_csrf() -> None:
    submitted_token = request.form.get("csrf_token", "")
    if not submitted_token or not secrets.compare_digest(
        submitted_token, session.get("csrf_token", "")
    ):
        abort(400, "Solicitud inválida.")

