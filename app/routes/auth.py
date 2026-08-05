from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.security import validate_csrf
from app.services.auth_service import authenticate


auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/")
def index():
    destination = "equipment.list_equipment" if "user_id" in session else "auth.login"
    return redirect(url_for(destination))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        validate_csrf()
        user = authenticate(request.form.get("username", ""), request.form.get("password", ""))
        if user:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Sesión iniciada correctamente.", "success")
            return redirect(url_for("equipment.list_equipment"))
        flash("Credenciales inválidas.", "error")
    return render_template("login.html")


@auth_bp.post("/logout")
def logout():
    validate_csrf()
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))

