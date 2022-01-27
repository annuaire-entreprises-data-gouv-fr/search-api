from datetime import datetime
import requests
import json

from operators.papermill_minio import PapermillMinioOperator
from operators.elastic_create_index import ElasticCreateIndexOperator
from operators.elastic_fill_index import ElasticFillIndexOperator

from dag_datalake_sirene.variables import AIO_URL
from dag_datalake_sirene import secrets
from variables import DAG_FOLDER, DAG_NAME, TODAY


def get_current_color(ti):
    try:
        response = requests.get(AIO_URL + '/colors')
        current_color = json.loads(response.content)['CURRENT_COLOR']
    except requests.exceptions.RequestException as e:
        current_color = 'blue'
    ti.xcom_push(key='current_color', value=current_color)


def format_sirene_notebook(ti):

    current_color = ti.xcom_pull(key='current_color', task_ids='get_current_color')
    elastic_index = 'siren-' + current_color

    format_notebook = PapermillMinioOperator(
        task_id="format_sirene_notebook",
        input_nb=AIRFLOW_DAG_HOME + DAG_FOLDER + "process-data-before-indexation.ipynb",
        output_nb=TODAY + ".ipynb",
        tmp_path=TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/",
        minio_url=secrets.MINIO_URL,
        minio_bucket=secrets.MINIO_BUCKET,
        minio_user=secrets.MINIO_USER,
        minio_password=secrets.MINIO_PASSWORD,
        minio_output_filepath=DAG_FOLDER + DAG_NAME + "/" + TODAY + "/format_sirene_notebook/",
        parameters={
            "msgs": "Ran from Airflow " + TODAY + "!",
            "DATA_DIR": TMP_FOLDER + DAG_FOLDER + DAG_NAME + '/data/',
            "OUTPUT_DATA_FOLDER": TMP_FOLDER + DAG_FOLDER + DAG_NAME + '/output/',
            "ELASTIC_INDEX": elastic_index
        }
    )
    format_notebook.execute(dict())


def create_elastic_index(ti):
    current_color = ti.xcom_pull(key='current_color', task_ids='get_current_color')
    elastic_index = 'siren-' + current_color
    create_index = ElasticCreateIndexOperator(
        task_id='create_elastic_index',
        elastic_url=secrets.ELASTIC_URL,
        elastic_index=elastic_index,
        elastic_user=secrets.ELASTIC_USER,
        elastic_password=secrets.ELASTIC_PASSWORD,
    )
    create_index.execute(dict())


def generate_kpi_notebook(ti):
    generate_kpi = PapermillMinioOperator(
      task_id="generate_kpi_notebook",
      input_nb=AIRFLOW_DAG_HOME+DAG_FOLDER+"generate-kpi-sirene.ipynb",
      output_nb=TODAY+".ipynb",
      tmp_path=TMP_FOLDER+DAG_FOLDER+DAG_NAME+"/",
      minio_url=secrets.MINIO_URL,
      minio_bucket=secrets.MINIO_BUCKET,
      minio_user=secrets.MINIO_USER,
      minio_password=secrets.MINIO_PASSWORD,
      minio_output_filepath=DAG_FOLDER+DAG_NAME+"/latest/generate_kpi_notebook/",
      parameters={
          "msgs": "Ran from Airflow "+TODAY+"!",
          "OUTPUT_DATA_FOLDER": TMP_FOLDER+DAG_FOLDER+DAG_NAME+'/output/',
      }
    )
    generate_kpi.execute(dict())


def fill_index():
    current_color = ti.xcom_pull(key='current_color', task_ids='get_current_color')
    elastic_index = 'siren-' + current_color

    all_deps = [*'-0'.join(list(str(x) for x in range(0, 10))).split('-')[1:],
                *list(str(x) for x in range(10, 20)),
                *['2A', '2B'],
                *list(str(x) for x in range(21, 95)),
                *'-7510'.join(list(str(x) for x in range(0, 10))).split('-')[1:],
                *'-751'.join(list(str(x) for x in range(10, 21))).split('-')[1:],
                *['']
                ]
    all_deps.remove('75')

    for dep in all_deps:
        print(DAG_FOLDER + DAG_NAME + '/' + TODAY + '/' + elastic_index + '_' + dep + '.csv')
        fill_elastic = ElasticFillIndexOperator(
            task_id='fill_elastic_index',
            elastic_url=secrets.ELASTIC_URL,
            elastic_index=ELASTIC_INDEX,
            elastic_user=secrets.ELASTIC_USER,
            elastic_password=secrets.ELASTIC_PASSWORD,
            elastic_bulk_size=1500,
            minio_url=secrets.MINIO_URL,
            minio_bucket=secrets.MINIO_BUCKET,
            minio_user=secrets.MINIO_USER,
            minio_password=secrets.MINIO_PASSWORD,
            minio_filepath=DAG_FOLDER + DAG_NAME + '/' + TODAY + '/format_sirene_notebook/output/' + elastic_index + '_' + dep + '.csv',
        )
        fill_elastic.execute(dict())
