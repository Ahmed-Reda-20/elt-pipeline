import psycopg2

conn = psycopg2.connect(
    host="1016F610577F391",
    port=5433,
    dbname="etl_bronze_db",
    user="airflow",
    password="airflow"
)
cur = conn.cursor()
cur.execute("SELECT * FROM bronze_products LIMIT 10;")
print(cur.fetchall())
cur.close()
conn.close()
