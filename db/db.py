import psycopg2 # type: ignore

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="jardin_anciens",
        user="user",
        password="password"
    )
    return conn
