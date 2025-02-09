import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from utils.weather_integration.run import Run

logger = logging.getLogger(__name__)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 8),
    "email_on_failure": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="weather_integration",
    default_args=default_args,
    schedule=None,  # Updated to match Airflow 2.4+ syntax
    catchup=False,
    max_active_runs=1,
    tags=["weather"],
) as dag:

    @task(task_id="push_to_postgres", retries=1)
    def run_push():
        do = Run()
        do.run_integration()  # Make sure this method exists in Run class

    run_push()
