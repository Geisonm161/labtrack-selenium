from sqlite3 import Row

from app.database import get_db


class EquipmentRepository:
    def list(self, query: str = "") -> list[Row]:
        database = get_db()
        if query:
            pattern = f"%{query}%"
            return database.execute(
                """
                SELECT * FROM equipment
                WHERE code LIKE ? OR name LIKE ? OR category LIKE ?
                ORDER BY id DESC
                """,
                (pattern, pattern, pattern),
            ).fetchall()
        return database.execute("SELECT * FROM equipment ORDER BY id DESC").fetchall()

    def get(self, equipment_id: int) -> Row | None:
        return get_db().execute(
            "SELECT * FROM equipment WHERE id = ?", (equipment_id,)
        ).fetchone()

    def code_exists(self, code: str, exclude_id: int | None = None) -> bool:
        if exclude_id is None:
            result = get_db().execute(
                "SELECT 1 FROM equipment WHERE code = ?", (code,)
            ).fetchone()
        else:
            result = get_db().execute(
                "SELECT 1 FROM equipment WHERE code = ? AND id != ?", (code, exclude_id)
            ).fetchone()
        return result is not None

    def create(self, data: dict[str, str | int]) -> int:
        database = get_db()
        cursor = database.execute(
            """
            INSERT INTO equipment (code, name, category, status, quantity, notes)
            VALUES (:code, :name, :category, :status, :quantity, :notes)
            """,
            data,
        )
        database.commit()
        return int(cursor.lastrowid)

    def update(self, equipment_id: int, data: dict[str, str | int]) -> None:
        database = get_db()
        database.execute(
            """
            UPDATE equipment
            SET code = :code, name = :name, category = :category,
                status = :status, quantity = :quantity, notes = :notes,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :id
            """,
            {**data, "id": equipment_id},
        )
        database.commit()

    def delete(self, equipment_id: int) -> None:
        database = get_db()
        database.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
        database.commit()

