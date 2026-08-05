from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.security import login_required, validate_csrf
from app.services.equipment_service import EquipmentService


equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipos")


@equipment_bp.get("")
@login_required
def list_equipment():
    query = request.args.get("q", "").strip()[:50]
    equipment = EquipmentService().list(query)
    return render_template("equipment/list.html", equipment=equipment, query=query)


@equipment_bp.get("/<int:equipment_id>")
@login_required
def detail(equipment_id: int):
    equipment = EquipmentService().get(equipment_id)
    if equipment is None:
        abort(404)
    return render_template("equipment/detail.html", equipment=equipment)


@equipment_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def create():
    errors: dict[str, str] = {}
    if request.method == "POST":
        validate_csrf()
        equipment_id, errors = EquipmentService().create(request.form)
        if equipment_id is not None:
            flash("Equipo creado correctamente.", "success")
            return redirect(url_for("equipment.detail", equipment_id=equipment_id))
    values = request.form if request.method == "POST" else {}
    return render_template("equipment/form.html", title="Nuevo equipo", values=values, errors=errors)


@equipment_bp.route("/<int:equipment_id>/editar", methods=["GET", "POST"])
@login_required
def edit(equipment_id: int):
    service = EquipmentService()
    equipment = service.get(equipment_id)
    if equipment is None:
        abort(404)

    errors: dict[str, str] = {}
    if request.method == "POST":
        validate_csrf()
        errors = service.update(equipment_id, request.form)
        if not errors:
            flash("Equipo actualizado correctamente.", "success")
            return redirect(url_for("equipment.detail", equipment_id=equipment_id))
    values = request.form if request.method == "POST" else dict(equipment)
    return render_template(
        "equipment/form.html", title="Editar equipo", values=values, errors=errors, equipment=equipment
    )


@equipment_bp.post("/<int:equipment_id>/eliminar")
@login_required
def delete(equipment_id: int):
    validate_csrf()
    service = EquipmentService()
    if service.get(equipment_id) is None:
        abort(404)
    service.delete(equipment_id)
    flash("Equipo eliminado correctamente.", "success")
    return redirect(url_for("equipment.list_equipment"))
