from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from operators.clean_folder import CleanFolderOperator
from airflow.operators.python import PythonOperator

from dag_datalake_sirene import secrets
from dag_datalake_sirene.variables import AIRFLOW_DAG_HOME, TMP_FOLDER, DAG_FOLDER, DAG_NAME, TODAY
from dag_datalake_sirene.utils import get_next_color, format_sirene_notebook, create_elastic_index, \
    generate_kpi_notebook, fill_index

from datetime import timedelta
from datetime import datetime


with DAG(
        dag_id=DAG_NAME,
        schedule_interval='0 23 10 * *',
        start_date=days_ago(10),
        dagrun_timeout=timedelta(minutes=60 * 8),
        tags=['siren'],
) as dag:
    get_next_color = PythonOperator(
        task_id="get_next_color",
        provide_context=True,
        python_callable=get_next_color
    )

    clean_previous_folder = CleanFolderOperator(
        task_id='clean_previous_folder',
        folder_path=TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/"
    )

    format_sirene_notebook = PythonOperator(
        task_id="format_sirene_notebook",
        provide_context=True,
        python_callable=format_sirene_notebook
    )

    clean_tmp_folder = CleanFolderOperator(
        task_id='clean_tmp_folder',
        folder_path=TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/"
    )

    create_elastic_index = PythonOperator(
        task_id='create_elastic_index',
        provide_context=True,
        python_callable=create_elastic_index
    )
    '''
    generate_kpi_notebook = PythonOperator(
        task_id="generate_kpi_notebook",
        python_callable=generate_kpi_notebook
    )
    '''
    fill_elastic_index = PythonOperator(
        task_id="fill_elastic_index",
        provide_context=True,
        python_callable=fill_index
    )

    clean_previous_folder.set_upstream(get_next_color)
    format_sirene_notebook.set_upstream(clean_previous_folder)
    clean_tmp_folder.set_upstream(format_sirene_notebook)
    create_elastic_index.set_upstream(clean_tmp_folder)
    # generate_kpi_notebook.set_upstream(clean_tmp_folder)
    fill_elastic_index.set_upstream(create_elastic_index)
