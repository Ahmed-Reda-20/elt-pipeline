from .db_utils import get_db_connection

def start_ingestion_log(batch_id: str, api_endpoint: str, source_system="fakestoreapi"):
    """Insert IN_PROGRESS row into ingestion_log."""
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ingestion_log (batch_id, source_system, api_endpoint, status)
                VALUES (%s, %s, %s, 'IN_PROGRESS')
            """, (batch_id, source_system, api_endpoint))

def end_ingestion_log(batch_id: str, status: str,error_message: str = None):
    """Update ingestion_log with final status for given batch_id."""
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE ingestion_log
                SET status = %s, end_time = NOW(), error_message = %s
                WHERE batch_id = %s
            """, (status, error_message, batch_id))
