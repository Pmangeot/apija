from typing import List, Optional
from db.db import get_db_connection
from models.m_reservation import Reservation, ReservationCreate, ReservationUpdate, ArticlesInResa
from models.m_article import Article
from collections import defaultdict
from datetime import datetime


class ReservationMapper:
    @staticmethod
    def get_all() -> List[Reservation]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                resa.id AS reservation_id, 
                resa.date, 
                resa.articles_total, 
                resa.user_id, 
                resa.state_id, 
                resa.season_id, 
                resa_art.article_id, 
                resa_art.quantity, 
                art.name AS article_name, 
                art.type_id, 
                art.description, 
                art.total_stock,
                art.remaining_quantity,
                art.season_id AS article_season_id
            FROM 
                reservation resa
            LEFT JOIN 
                reservation_article resa_art ON resa.id = resa_art.reservation_id
            LEFT JOIN 
                article art ON resa_art.article_id = art.id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return ReservationMapper.format_reservation(rows)
    
    @staticmethod
    def get_by_id(reservation_id: int) -> Reservation:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                resa.id AS reservation_id, 
                resa.date, 
                resa.articles_total, 
                resa.user_id, 
                resa.state_id, 
                resa.season_id, 
                resa_art.article_id, 
                resa_art.quantity, 
                art.name AS article_name, 
                art.type_id, 
                art.description, 
                art.total_stock,
                art.remaining_quantity,
                art.season_id AS article_season_id
            FROM 
                reservation resa
            LEFT JOIN 
                reservation_article resa_art ON resa.id = resa_art.reservation_id
            LEFT JOIN 
                article art ON resa_art.article_id = art.id
            WHERE 
                resa.id = %s
        """, (reservation_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return ReservationMapper.format_reservation(rows)

    @staticmethod
    def get_multi_by_userid(user_id: int) -> List[Reservation]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                resa.id AS reservation_id, 
                resa.date, 
                resa.articles_total, 
                resa.user_id, 
                resa.state_id, 
                resa.season_id, 
                resa_art.article_id, 
                resa_art.quantity, 
                art.name AS article_name, 
                art.type_id, 
                art.description, 
                art.total_stock,
                art.remaining_quantity,
                art.season_id AS article_season_id
            FROM 
                reservation resa
            LEFT JOIN 
                reservation_article resa_art ON resa.id = resa_art.reservation_id
            LEFT JOIN 
                article art ON resa_art.article_id = art.id
            WHERE 
                resa.user_id = %s
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return ReservationMapper.format_reservation(rows)

    @staticmethod
    def create_reservation(reservation_data: ReservationCreate) -> Reservation:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            current_date = datetime.now().date()
            cur.execute(
                "INSERT INTO reservation (date, articles_total, user_id, state_id, season_id) VALUES (%s, %s, %s, %s, %s) RETURNING id, date, articles_total, user_id, state_id, season_id",
                (current_date, reservation_data.articles_total, reservation_data.user_id, reservation_data.state_id, reservation_data.season_id)
            )
            row = cur.fetchone()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        
        return Reservation(
            id=row[0], 
            date=row[1], 
            articles_total=row[2], 
            user_id=row[3], 
            state_id=row[4], 
            season_id=row[5], 
            articles=[]
        )
    
    @staticmethod
    def delete(reservation_id: int) -> bool:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM reservation WHERE id = %s", (reservation_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
        return cur.rowcount > 0
    
    @staticmethod
    def format_reservation(rows):
        if not rows:
            return None

        reservations_dict = defaultdict(lambda: {
            "date": None,
            "articles_total": None,
            "user_id": None,
            "state_id": None,
            "season_id": None,
            "articles": []
        })

        for row in rows:
            res_id = row[0]
            if not reservations_dict[res_id]["date"]:
                reservations_dict[res_id]["date"] = row[1]
                reservations_dict[res_id]["articles_total"] = row[2]
                reservations_dict[res_id]["user_id"] = row[3]
                reservations_dict[res_id]["state_id"] = row[4]
                reservations_dict[res_id]["season_id"] = row[5]

            if row[6] is not None and row[7] is not None:
                article = ArticlesInResa(
                    article_id=row[6],
                    quantity=row[7],
                    article=Article(
                        id=row[6],
                        name=row[8] if row[8] is not None else "",
                        type_id=row[9] if row[9] is not None else 0,
                        description=row[10] if row[10] is not None else "",
                        total_stock=row[11] if row[11] is not None else 0,
                        remaining_quantity=row[12] if row[12] is not None else 0,
                        season_id=row[13] if row[13] is not None else 0
                    )
                )
                reservations_dict[res_id]["articles"].append(article)

        return [
            Reservation(
                id=res_id,
                date=data["date"],
                articles_total=data["articles_total"],
                user_id=data["user_id"],
                state_id=data["state_id"],
                season_id=data["season_id"],
                articles=data["articles"]
            ) for res_id, data in reservations_dict.items()
        ]
