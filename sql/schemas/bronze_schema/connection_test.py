import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        database="etl_bronze_db", 
        user="airflow",
        password="airflow"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cursor.fetchall()
    print(f"Bronze tables created: {tables}")
    conn.close()
    print("Bronze database connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")