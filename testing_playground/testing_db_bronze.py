import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    dbname="elt_dwh",
    user="airflow",
    password="airflow"
)
cur = conn.cursor()
cur.execute("SELECT * FROM bronze.bronze_products LIMIT 10;")
print(cur.fetchall())
cur.close()
conn.close()
