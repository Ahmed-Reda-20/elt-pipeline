import psycopg2
from .config import DB_CONN

def get_db_connection():
    """Return a psycopg2 connection using project config."""
    return psycopg2.connect(**DB_CONN)

def get_last_processed_id(table_name: str, id_column_api: str) -> int:
    """Fetch MAX(id_column) from table for incremental ingestion."""
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT MAX({id_column_api}) FROM {table_name}")
            result = cur.fetchone()
            return result[0] if result and result[0] else 0
