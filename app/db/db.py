import psycopg2 # type: ignore
from core.config import settings 

def get_db_connection():
    conn = psycopg2.connect(
        host=settings.HOST,
        database=settings.DATABASE,
        user=settings.USER,
        password=settings.PASSWORD
    )
    return conn
