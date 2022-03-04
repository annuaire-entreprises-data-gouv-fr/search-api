from datetime import timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from dag_datalake_sirene.utils import (
    create_elastic_siren,
    fill_siren,
    format_sirene_notebook,
    get_next_color,
)
from dag_datalake_sirene.variables import DAG_FOLDER, DAG_NAME, TMP_FOLDER
from operators.clean_folder import CleanFolderOperator

with DAG(
    dag_id=DAG_NAME,
    schedule_interval="0 23 10 * *",
    start_date=days_ago(10),
    dagrun_timeout=timedelta(minutes=60 * 8),
    tags=["siren"],
) as dag:
    get_next_color = PythonOperator(
        task_id="get_next_color", provide_context=True, python_callable=get_next_color
    )

    clean_previous_folder = CleanFolderOperator(
        task_id="clean_previous_folder",
        folder_path=TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/",
    )

    format_sirene_notebook = PythonOperator(
        task_id="format_sirene_notebook",
        provide_context=True,
        python_callable=format_sirene_notebook,
    )

    clean_tmp_folder = CleanFolderOperator(
        task_id="clean_tmp_folder", folder_path=TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/"
    )

    create_elastic_siren = PythonOperator(
        task_id="create_elastic_siren",
        provide_context=True,
        python_callable=create_elastic_siren,
    )

    fill_elastic_siren = PythonOperator(
        task_id="fill_elastic_siren", provide_context=True, python_callable=fill_siren
    )

    clean_previous_folder.set_upstream(get_next_color)
    format_sirene_notebook.set_upstream(clean_previous_folder)
    clean_tmp_folder.set_upstream(format_sirene_notebook)
    create_elastic_siren.set_upstream(clean_tmp_folder)
    fill_elastic_siren.set_upstream(create_elastic_siren)
