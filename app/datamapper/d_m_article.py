from typing import List, Optional
from db.db import get_db_connection
from models.m_article import Article, ArticleCreate, ArticleUpdate

class ArticleMapper:
    @staticmethod
    def get_all() -> List[Article]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM article")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Article(id=row[0], name=row[1], type_id=row[2], description=row[3], total_stock=row[4], remaining_quantity=row[5], season_id=row[6]) for row in rows]

    @staticmethod
    def create(article: ArticleCreate) -> Article:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO article (name, description, total_stock, remaining_quantity, type_id, season_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
                (article.name, article.description, article.total_stock, article.remaining_quantity, article.type_id, article.season_id)
            )
            row = cur.fetchone()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        return Article(id=row[0], name=row[1], type_id=row[2], description=row[3], total_stock=row[4], remaining_quantity=row[5], season_id=row[6])

    @staticmethod
    def update(article_id: int, article: ArticleUpdate) -> Optional[Article]:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE article SET name = %s, type_id = %s, description = %s, total_stock = %s, remaining_quantity = %s, season_id = %s WHERE id = %s RETURNING *",
                (article.name, article.type_id, article.description, article.total_stock, article.remaining_quantity, article.season_id, article_id)
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
        return Article(id=row[0], name=row[1], type_id=row[2], description=row[3], total_stock=row[4], remaining_quantity=row[5], season_id=row[6])

    @staticmethod
    def delete(article_id: int) -> bool:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM article WHERE id = %s", (article_id,))
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
            cur.execute("DELETE FROM article")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_id(article_id: int) -> Optional[Article]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM article WHERE id = %s", (article_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row is None:
            return None
        
        return Article(id=row[0], name=row[1], type_id=row[2], description=row[3], total_stock=row[4], remaining_quantity=row[5], season_id=row[6])