from fastapi import HTTPException
from typing import Optional
import bcrypt # type: ignore
from db.db import get_db_connection
from models.m_user import User, UserCreate, UserUpdate, UserPasswordUpdate

class UserMapper:
    @staticmethod
    def create(user: UserCreate) -> User:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cur.execute(
                "INSERT INTO app_user (firstname, lastname, email, password, admin) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (user.firstname, user.lastname, user.email, hashed_password, False)
            )
            row = cur.fetchone()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        return User(id=row[0], firstname=row[1], lastname=row[2], email=row[3], admin=row[5])

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM app_user WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row is None:
            return None
        return User(id=row[0], firstname=row[1], lastname=row[2], email=row[3], admin=row[5])

    @staticmethod
    def get_by_id(id: int) -> Optional[User]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM app_user WHERE id = %s", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row is None:
            return None
        return User(id=row[0], firstname=row[1], lastname=row[2], email=row[3], admin=row[5])

    @staticmethod
    def update(user_id: int, user_update: UserUpdate) -> Optional[User]:
        update_data = user_update.dict(exclude_unset=True)

        set_clause = ", ".join(f"{key} = %s" for key in update_data.keys())
        values = list(update_data.values()) + [user_id]

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(f"UPDATE app_user SET {set_clause} WHERE id = %s RETURNING *", values)
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
        return User(id=row[0], firstname=row[1], lastname=row[2], email=row[3], admin=row[5])

    @staticmethod
    def password_update(user_id: int, user_update: UserPasswordUpdate) -> None:

        user = UserMapper.get_by_id(user_id)
        if not bcrypt.checkpw(user_update.old_password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            hashed_password = bcrypt.hashpw(user_update.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cur.execute(
                "UPDATE app_user SET password = %s WHERE id = %s RETURNING *",
                (hashed_password, user_id)
            )
            row = cur.fetchone()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        return user

    @staticmethod
    def delete_one(user_id: int) -> None:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM app_user WHERE id = %s", (user_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_all() -> None:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM app_user")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
