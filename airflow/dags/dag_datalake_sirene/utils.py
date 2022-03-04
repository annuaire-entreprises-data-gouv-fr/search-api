import json
import logging

import requests
from dag_datalake_sirene import secrets
from dag_datalake_sirene.variables import (
    AIO_URL,
    AIRFLOW_DAG_HOME,
    DAG_FOLDER,
    DAG_NAME,
    TMP_FOLDER,
    TODAY,
)
from operators.elastic_create_siren import ElasticCreateSirenOperator
from operators.elastic_fill_siren import ElasticFillSirenOperator
from operators.papermill_minio import PapermillMinioOperator


def get_next_color(**kwargs):
    try:
        response = requests.get(AIO_URL + "/colors")
        next_color = json.loads(response.content)["NEXT_COLOR"]
    except requests.exceptions.RequestException:
        next_color = "blue"
    logging.info(f"Next color: {next_color}")
    kwargs["ti"].xcom_push(key="next_color", value=next_color)


def format_sirene_notebook(**kwargs):
    next_color = kwargs["ti"].xcom_pull(key="next_color", task_ids="get_next_color")
    elastic_index = "siren-" + next_color

    format_notebook = PapermillMinioOperator(
        task_id="format_sirene_notebook",
        input_nb=AIRFLOW_DAG_HOME + DAG_FOLDER + "process-data-before-indexation.ipynb",
        output_nb=TODAY + ".ipynb",
        tmp_path=TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/",
        minio_url=secrets.MINIO_URL,
        minio_bucket=secrets.MINIO_BUCKET,
        minio_user=secrets.MINIO_USER,
        minio_password=secrets.MINIO_PASSWORD,
        minio_output_filepath=DAG_FOLDER
        + DAG_NAME
        + "/"
        + TODAY
        + "/format_sirene_notebook/",
        parameters={
            "msgs": "Ran from Airflow " + TODAY + "!",
            "DATA_DIR": TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/data/",
            "OUTPUT_DATA_FOLDER": TMP_FOLDER + DAG_FOLDER + DAG_NAME + "/output/",
            "ELASTIC_INDEX": elastic_index,
        },
    )
    format_notebook.execute(dict())


def create_elastic_siren(**kwargs):
    next_color = kwargs["ti"].xcom_pull(key="next_color", task_ids="get_next_color")
    elastic_index = "siren-" + next_color
    create_index = ElasticCreateSirenOperator(
        task_id="create_elastic_index",
        elastic_url=secrets.ELASTIC_URL,
        elastic_index=elastic_index,
        elastic_user=secrets.ELASTIC_USER,
        elastic_password=secrets.ELASTIC_PASSWORD,
    )
    create_index.execute(dict())


def fill_siren(**kwargs):
    next_color = kwargs["ti"].xcom_pull(key="next_color", task_ids="get_next_color")
    elastic_index = "siren-" + next_color

    all_deps = [
        *"-0".join(list(str(x) for x in range(0, 10))).split("-")[1:],
        *list(str(x) for x in range(10, 20)),
        *["2A", "2B"],
        *list(str(x) for x in range(21, 95)),
        *"-7510".join(list(str(x) for x in range(0, 10))).split("-")[1:],
        *"-751".join(list(str(x) for x in range(10, 21))).split("-")[1:],
        *[""],
    ]
    all_deps.remove("75")

    for dep in all_deps:
        print(
            DAG_FOLDER
            + DAG_NAME
            + "/"
            + TODAY
            + "/"
            + elastic_index
            + "_"
            + dep
            + ".csv"
        )
        fill_elastic = ElasticFillSirenOperator(
            task_id="fill_elastic_index",
            elastic_url=secrets.ELASTIC_URL,
            elastic_index=elastic_index,
            elastic_user=secrets.ELASTIC_USER,
            elastic_password=secrets.ELASTIC_PASSWORD,
            elastic_bulk_size=1500,
            minio_url=secrets.MINIO_URL,
            minio_bucket=secrets.MINIO_BUCKET,
            minio_user=secrets.MINIO_USER,
            minio_password=secrets.MINIO_PASSWORD,
            minio_filepath=DAG_FOLDER
            + DAG_NAME
            + "/"
            + TODAY
            + "/format_sirene_notebook/output/"
            + elastic_index
            + "_"
            + dep
            + ".csv",
        )
        fill_elastic.execute(dict())
