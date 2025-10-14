from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}


with DAG(
    dag_id="dbt_pipeline",
    default_args=default_args,
    description="Run dbt with Docker in Airflow",
    schedule_interval=None,  # Manual trigger only, could be adjusted according to needs
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["dbt", "transform"],
) as dag:
    
      #first task -> dbt run
    dbt_run = DockerOperator(
        task_id="dbt_run",
        image="project_dbt_image:latest",
        api_version="auto",
        auto_remove=True,
        command="run",
        docker_url="unix://var/run/docker.sock",  # path to Docker socket on WSL
        network_mode="airflow-docker_default",
    )

    #second task -> dbt test
    dbt_test = DockerOperator(
        task_id="dbt_test",
        image="project_dbt_image:latest",
        api_version="auto",
        auto_remove=True,
        command="test",
        docker_url="unix://var/run/docker.sock",
        network_mode="airflow-docker_default",
    )

    # Define dependencies
    dbt_run >> dbt_test