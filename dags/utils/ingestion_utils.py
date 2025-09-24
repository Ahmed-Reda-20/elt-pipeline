import json
from psycopg2 import sql
from psycopg2.extras import execute_values, Json
from .db_utils import get_db_connection, get_last_processed_id
from .api_utlils import fetch_api_data

def ingest_api_data(batch_id, api_endpoint, table_name, api_id_column, source_system="fakestoreapi"):
    
    """
    Ingests incremental API data into a database table.

    This function:
      1. Fetches the latest data from the given API endpoint.
      2. Filters out rows already processed (using last stored ID).
      3. Inserts new rows into the target table with metadata (batch, size, status).
      4. Handles per-row errors gracefully by marking failed rows.

    Args:
        batch_id (str): Unique identifier for this ingestion run (UUID).
        api_endpoint (str): API endpoint URL to fetch data from example: 'products'.
        table_name (str): Target table in the bronze layer to insert rows into.
        api_id_column (str): Column name that uniquely identifies each record from the API.
        source_system (str, optional): Name of the source system. Defaults to "fakestoreapi".

    Returns:
        str: Summary message indicating success/failure and number of rows processed.
    """

    
    last_id = get_last_processed_id(table_name, api_id_column)

    try:
        data = fetch_api_data(api_endpoint)
    except Exception as e:
        return f"FAILED: API request failed - {type(e).__name__}: {e}"
    #Checking if the fetched records has any new id then appending new records in a list.
    last_id = int(last_id) if last_id is not None else 0
    incremental_data = [p for p in data if int(p['id']) > last_id]

    if not incremental_data:
        return f"SUCCESS: No new data from {api_endpoint}"

    success_rows = []
    failed_rows = []

    for item in incremental_data:
        try:
            # Possible failure points:
            # - item["id"] missing → KeyError
            # - item["id"] wrong type (string instead of int) → type mismatch
            # - Json(item) fails if item is not serializable
            # - len(json.dumps(item).encode("utf-8")) can fail if item has invalid characters
            row = (
                item.get("id"),              # PRIMARY KEY / NOT NULL check can fail
                Json(item),                  # convert Python dict → PostgreSQL JSONB
                source_system,
                batch_id,
                api_endpoint,
                len(json.dumps(item).encode("utf-8")),  # size calc
                "success",
                None,
            )
            success_rows.append(row)

        except Exception as e:
            # If *anything above* fails (id missing, JSON invalid, constraint issues)
            # → we capture the row in "failed" for lineage & debugging
            row = (
                item.get("id", None),  # fallback to None if missing
                Json(item),            # still try to store the raw JSON for debugging
                source_system,
                batch_id,
                api_endpoint,
                len(json.dumps(item).encode("utf-8")),
                "failed",
                f"{type(e).__name__}: {str(e)}",  # log exact error
            )
            failed_rows.append(row)


    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            insert_query = sql.SQL("""
                INSERT INTO bronze.{table} (
                    {id_col}, raw_json, source_system,
                    batch_id, api_endpoint, data_size_bytes,
                    processing_status, error_message
                ) VALUES %s
            """).format(
                table=sql.Identifier(table_name),
                id_col=sql.Identifier(api_id_column)
            )

            if success_rows:
                execute_values(cur, insert_query, success_rows)
            if failed_rows:
                execute_values(cur, insert_query, failed_rows)

    return f"SUCCESS: Processed {len(success_rows)} new rows, {len(failed_rows)} failed from {api_endpoint}"