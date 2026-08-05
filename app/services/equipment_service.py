from dataclasses import dataclass
from sqlite3 import Row

from app.repositories.equipment_repository import EquipmentRepository


ALLOWED_STATUSES = {"Disponible", "Prestado", "En mantenimiento"}


@dataclass(frozen=True)
class ValidationResult:
    data: dict[str, str | int]
    errors: dict[str, str]


class EquipmentService:
    def __init__(self, repository: EquipmentRepository | None = None) -> None:
        self.repository = repository or EquipmentRepository()

    def list(self, query: str = "") -> list[Row]:
        return self.repository.list(query.strip()[:50])

    def get(self, equipment_id: int) -> Row | None:
        return self.repository.get(equipment_id)

    def validate(self, form: dict[str, str], equipment_id: int | None = None) -> ValidationResult:
        code = form.get("code", "").strip().upper()
        name = form.get("name", "").strip()
        category = form.get("category", "").strip()
        status = form.get("status", "").strip()
        quantity_text = form.get("quantity", "").strip()
        notes = form.get("notes", "").strip()
        errors: dict[str, str] = {}

        if not 3 <= len(code) <= 12:
            errors["code"] = "El código debe tener entre 3 y 12 caracteres."
        elif self.repository.code_exists(code, equipment_id):
            errors["code"] = "Ya existe un equipo con este código."
        if not 3 <= len(name) <= 80:
            errors["name"] = "El nombre debe tener entre 3 y 80 caracteres."
        if not 3 <= len(category) <= 40:
            errors["category"] = "La categoría debe tener entre 3 y 40 caracteres."
        if status not in ALLOWED_STATUSES:
            errors["status"] = "Seleccione un estado válido."
        try:
            quantity = int(quantity_text)
            if not 0 <= quantity <= 9999:
                raise ValueError
        except ValueError:
            quantity = 0
            errors["quantity"] = "La cantidad debe estar entre 0 y 9999."
        if len(notes) > 200:
            errors["notes"] = "Las notas no pueden exceder 200 caracteres."

        return ValidationResult(
            data={
                "code": code,
                "name": name,
                "category": category,
                "status": status,
                "quantity": quantity,
                "notes": notes,
            },
            errors=errors,
        )

    def create(self, form: dict[str, str]) -> tuple[int | None, dict[str, str]]:
        result = self.validate(form)
        if result.errors:
            return None, result.errors
        return self.repository.create(result.data), {}

    def update(self, equipment_id: int, form: dict[str, str]) -> dict[str, str]:
        result = self.validate(form, equipment_id)
        if not result.errors:
            self.repository.update(equipment_id, result.data)
        return result.errors

    def delete(self, equipment_id: int) -> None:
        self.repository.delete(equipment_id)

