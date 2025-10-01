from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import uuid

from utils.ingestion_utils import ingest_api_data
from utils.logging_utils import start_ingestion_log, end_ingestion_log

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

with DAG(
    dag_id="bronze_dag",
    default_args=default_args,
    description="Bronze layer ingestion DAG",
    schedule_interval=None,  # Manual trigger only, could be adjusted according to needs
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["bronze", "ingestion"],
) as dag:

    def run_products_ingestion():
        """Extract products from API and insert into bronze_products table."""
        batch_id = str(uuid.uuid4())
        try:
            start_ingestion_log(batch_id, "products")
            ingest_api_data(batch_id, "products", "bronze_products", "api_product_id")
            end_ingestion_log(batch_id, status="SUCCESS")
        except Exception as e:
            end_ingestion_log(batch_id, status="FAILED", error_message=str(e))
            raise

    def run_users_ingestion():
        """Extract users from API and insert into bronze_users table."""
        batch_id = str(uuid.uuid4())
        try:
            start_ingestion_log(batch_id, "users")
            ingest_api_data(batch_id, "users", "bronze_users", "api_user_id")
            end_ingestion_log(batch_id, status="SUCCESS")
        except Exception as e:
            end_ingestion_log(batch_id, status="FAILED", error_message=str(e))
            raise

    def run_carts_ingestion():
        """Extract carts from API and insert into bronze_carts table."""
        batch_id = str(uuid.uuid4())
        try:
            start_ingestion_log(batch_id, "carts")
            ingest_api_data(batch_id, "carts", "bronze_carts", "api_cart_id")
            end_ingestion_log(batch_id, status="SUCCESS")
        except Exception as e:
            end_ingestion_log(batch_id, status="FAILED", error_message=str(e))
            raise

    products_task = PythonOperator(
        task_id="ingest_products",
        python_callable=run_products_ingestion,
    )

    users_task = PythonOperator(
        task_id="ingest_users",
        python_callable=run_users_ingestion,
    )

    carts_task = PythonOperator(
        task_id="ingest_carts",
        python_callable=run_carts_ingestion,
    )

    # Run in parallel (default)
    [products_task, users_task, carts_task]
