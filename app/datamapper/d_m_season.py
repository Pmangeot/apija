from typing import List, Optional
from db.db import get_db_connection
from models.m_season import Season, SeasonUpdate, SeasonCreate
from models.m_reservation import Reservation, ReservationCreate, ReservationUpdate, ArticlesInResa
from models.m_article import Article
from collections import defaultdict
from fastapi import HTTPException

class SeasonMapper:
    @staticmethod
    def get_active_seasons() -> List[Season]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                season.id AS season_id,
                season.name,
                season.active,
                art.id AS article_id,
                art.name AS article_name,
                art.type_id,
                art.description,
                art.total_stock,
                art.remaining_quantity
            FROM 
                season
            LEFT JOIN 
                article art ON season.id = art.season_id
            WHERE 
                season.active = TRUE
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return []

        seasons_dict = defaultdict(lambda: {
            "name": None,
            "active": None,
            "articles": []
        })

        for row in rows:
            season_id = row[0]
            if seasons_dict[season_id]["name"] is None:
                seasons_dict[season_id]["name"] = row[1]
                seasons_dict[season_id]["active"] = row[2]

            if row[3] is not None:  
                article = Article(
                    id=row[3],
                    name=row[4],
                    type_id=row[5],
                    description=row[6],
                    total_stock=row[7],
                    remaining_quantity=row[8],
                    season_id=season_id
                )
                seasons_dict[season_id]["articles"].append(article)

        seasons = [
            Season(
                id=season_id,
                name=data["name"],
                active=data["active"],
                articles=data["articles"]
            ) for season_id, data in seasons_dict.items()
        ]

        return seasons

    @staticmethod
    def get_all_seasons() -> List[Season]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                season.id AS season_id,
                season.name,
                season.active,
                art.id AS article_id,
                art.name AS article_name,
                art.type_id,
                art.description,
                art.total_stock,
                art.remaining_quantity
            FROM 
                season
            LEFT JOIN 
                article art ON season.id = art.season_id
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return []

        # Grouper les articles par saison
        seasons_dict = defaultdict(lambda: {
            "name": None,
            "active": None,
            "articles": []
        })

        for row in rows:
            season_id = row[0]
            if seasons_dict[season_id]["name"] is None:
                seasons_dict[season_id]["name"] = row[1]
                seasons_dict[season_id]["active"] = row[2]

            if row[3] is not None:
                article = Article(
                    id=row[3],
                    name=row[4],
                    type_id=row[5],
                    description=row[6],
                    total_stock=row[7],
                    remaining_quantity=row[8],
                    season_id=season_id
                )
                seasons_dict[season_id]["articles"].append(article)

        seasons = [
            Season(
                id=season_id,
                name=data["name"],
                active=data["active"],
                articles=data["articles"]
            ) for season_id, data in seasons_dict.items()
        ]

        return seasons

    @staticmethod
    def create_season(new_season : SeasonCreate) -> Season:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertion de la saison
        cur.execute("""
            INSERT INTO season (name, active)
            VALUES (%s, %s) RETURNING id
        """, (new_season.name, new_season.active))

        season_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        season = Season(
            id=season_id,
            name=new_season.name,
            active=new_season.active,
            articles=[] 
        )

        return season
    
    @staticmethod
    def deactivate_season(season_id: int) -> Optional[Season]:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE season
                SET active = FALSE
                WHERE id = %s
                RETURNING id, name, active
            """, (season_id,))
            row = cur.fetchone()
            conn.commit()
            if row:
                return Season(
                    id=row[0],
                    name=row[1],
                    active=row[2],
                    articles=[]
                )
            return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_season(season_id: int) -> Optional[Season]:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, name, active 
                FROM season 
                WHERE id = %s
            """, (season_id,))
            row = cur.fetchone()

            if not row:
                return None

            cur.execute("""
                DELETE FROM season 
                WHERE id = %s
            """, (season_id,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()