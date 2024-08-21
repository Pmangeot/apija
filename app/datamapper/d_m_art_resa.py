from typing import List, Optional
from db.db import get_db_connection
from models.m_reservation import Reservation, ReservationCreate, ReservationUpdate, ArticlesInResa
from models.m_article import Article
from models.m_reservation_articles import ReservationArticles, ReservationArticlesCreate, ReservationArticlesUpdate
from collections import defaultdict

class ArtResaMapper:
    @staticmethod
    def add(art_resa: ReservationArticlesCreate) -> ReservationArticles:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO reservation_article (reservation_id, article_id, quantity) VALUES (%s, %s, %s) RETURNING *",
                (art_resa.reservation_id, art_resa.article_id, art_resa.quantity)
            )
            row = cur.fetchone()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        return ReservationArticles(id=row[0], reservation_id=row[1], article_id=row[2], quantity=row[3])