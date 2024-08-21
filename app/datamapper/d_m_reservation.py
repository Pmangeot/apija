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
        cur.execute("SELECT * FROM reservation")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [Reservation(id=row[0], date=row[1], articles_total=row[2], user_id=row[3], state_id=row[4], season_id=row[5], ) for row in rows]

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
            INNER JOIN 
                reservation_article resa_art ON resa.id = resa_art.reservation_id
            INNER JOIN 
                article art ON resa_art.article_id = art.id
            WHERE 
                resa.id = %s
        """, (reservation_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return None

        # We only have one row as we request
        articles = [
            ArticlesInResa(
                article_id=row[6],
                quantity=row[7],
                article=Article(
                    id=row[6],
                    name=row[8],
                    type_id=row[9],
                    description=row[10],
                    total_stock=row[11],
                    remaining_quantity=row[12],
                    season_id=row[13]
                )
            ) for row in rows
        ]

        reservation = Reservation(
            id=rows[0][0],
            date=rows[0][1],
            articles_total=rows[0][2],
            user_id=rows[0][3],
            state_id=rows[0][4],
            season_id=rows[0][5],
            articles=articles
        )

        return reservation

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
            INNER JOIN 
                reservation_article resa_art ON resa.id = resa_art.reservation_id
            INNER JOIN 
                article art ON resa_art.article_id = art.id
            WHERE 
                resa.user_id = %s
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

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

            article = ArticlesInResa(
                article_id=row[6],
                quantity=row[7],
                article=Article(
                    id=row[6],
                    name=row[8],
                    type_id=row[9],
                    description=row[10],
                    total_stock=row[11],
                    remaining_quantity=row[12],
                    season_id=row[13]
                )
            )
            reservations_dict[res_id]["articles"].append(article)

        reservations = [
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

        return reservations

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