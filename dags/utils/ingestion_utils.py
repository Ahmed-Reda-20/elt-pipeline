import json
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
    incremental_data = [p for p in data if p['id'] > last_id]

    if not incremental_data:
        return f"SUCCESS: No new data from {api_endpoint}"

    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            for item in incremental_data:
                try:
                    cur.execute(f"""
                        INSERT INTO {table_name} (
                            {api_id_column}, raw_json, source_system,
                            batch_id, api_endpoint, data_size_bytes,
                            processing_status, error_message
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        item.get('id'),
                        json.dumps(item),
                        source_system,
                        batch_id,
                        api_endpoint,
                        len(json.dumps(item).encode('utf-8')),
                        "success",
                        None
                    ))
                except Exception as e:
                    cur.execute(f"""
                        INSERT INTO {table_name} (
                            {api_id_column}, raw_json, source_system,
                            batch_id, api_endpoint, data_size_bytes,
                            processing_status, error_message
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        item.get('id', None),
                        json.dumps(item),
                        source_system,
                        batch_id,
                        api_endpoint,
                        len(json.dumps(item).encode('utf-8')),
                        "failed",
                        f"{type(e).__name__}: {str(e)}"
                    ))

    return f"SUCCESS: Processed {len(incremental_data)} new data from {api_endpoint}"
