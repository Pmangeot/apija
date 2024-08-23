from typing import List, Optional
from db.db import get_db_connection
from models.m_type import Type, TypeCreate, TypeUpdate

class TypeMapper:
    @staticmethod
    def get_all() -> List[Type]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM type")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Type(id=row[0], name=row[1], description=row[2]) for row in rows]
    
    @staticmethod
    def get_by_id(type_id: int) -> Optional[Type]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM type WHERE id = %s", (type_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row is None:
            return None
        return Type(id=row[0], name=row[1], description=row[2])

    @staticmethod
    def create(type: TypeCreate) -> Type:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO type (name, description) VALUES (%s, %s) RETURNING *",
                (type.name, type.description)
            )
            row = cur.fetchone()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        return Type(id=row[0], name=row[1], description=row[2])

    @staticmethod
    def update(type_id: int, type: TypeUpdate) -> Optional[Type]:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE type SET name = %s, description = %s WHERE id = %s RETURNING *",
                (type.name, type.description, type_id)
            )
            row = cur.fetchone()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        if row is None:
            return None
        return Type(id=row[0], name=row[1], description=row[2])

    @staticmethod
    def delete(type_id: int) -> bool:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM type WHERE id = %s", (type_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        return cur.rowcount > 0

    @staticmethod
    def delete_all() -> None:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM type")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()