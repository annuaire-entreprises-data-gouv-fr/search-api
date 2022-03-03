import logging
import time
from typing import Optional

import numpy as np
import pandas as pd
from airflow.models import BaseOperator
from elasticsearch import helpers
from elasticsearch_dsl import connections
from minio import Minio
from operators.elastic_mapping_siren import Siren


def doc_generator(df: pd.DataFrame):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield Siren(meta={"id": document["siret"]}, **document.to_dict()).to_dict(
            include_meta=True
        )
        # Serialize the instance into a dictionary so that it can be saved in elasticsearch.


class ElasticFillSirenOperator(BaseOperator):
    """
    Fill elasticsearch Index
    :param elastic_url: endpoint url of elasticsearch
    :type elastic_url: str
    :param elastic_index: index to create
    :type elastic_index: str
    :param elastic_user: user for elasticsearch
    :type elastic_user: str
    :param elastic_password: password for elasticsearch
    :type elastic_password: str
    :param elastic_bulk_size: size of bulk for indexation
    :type elastic_bulk_size: int
    :param minio_url: minio url where report should be store
    :type minio_url: str
    :param minio_bucket: minio bucket where report should be store
    :type minio_bucket: str
    :param minio_user: minio user which will store report
    :type minio_user: str
    :param minio_password: minio password of minio user
    :type minio_password: str
    :param minio_filepath: complete filepath where to store report
    :type minio_filepath: str
    :param column_id: column which will be used for id in elasticsearch
    :type column_id: str
    """

    supports_lineage = True

    template_fields = (
        "elastic_url",
        "elastic_index",
        "elastic_user",
        "elastic_password",
        "elastic_bulk_size",
        "minio_url",
        "minio_bucket",
        "minio_user",
        "minio_password",
        "minio_filepath",
        "column_id",
    )

    def __init__(
        self,
        *,
        elastic_url: Optional[str] = None,
        elastic_index: Optional[str] = None,
        elastic_user: Optional[str] = None,
        elastic_password: Optional[str] = None,
        elastic_bulk_size: Optional[int] = None,
        minio_url: Optional[str] = None,
        minio_bucket: Optional[str] = None,
        minio_user: Optional[str] = None,
        minio_password: Optional[str] = None,
        minio_filepath: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.elastic_url = elastic_url
        self.elastic_index = elastic_index
        self.elastic_user = elastic_user
        self.elastic_password = elastic_password
        self.elastic_bulk_size = elastic_bulk_size
        self.minio_url = minio_url
        self.minio_bucket = minio_bucket
        self.minio_user = minio_user
        self.minio_password = minio_password
        self.minio_filepath = minio_filepath

        # initiate the default connection to elasticsearch
        connections.create_connection(
            hosts=[self.elastic_url],
            http_auth=(self.elastic_user, self.elastic_password),
            retry_on_timeout=True,
        )

        self.elastic_connection = connections.get_connection()

    def execute(self, context):

        if not self.elastic_url:
            raise ValueError("Please provide elasticsearch url endpoint!")

        client = Minio(
            self.minio_url,
            access_key=self.minio_user,
            secret_key=self.minio_password,
            secure=True,
        )
        obj = client.get_object(
            self.minio_bucket,
            self.minio_filepath,
        )
        df_dep = pd.read_csv(obj, dtype=str)
        df_dep = df_dep.replace({np.nan: None})

        logging.info(
            "Successfully retrieved file - "
            + str(df_dep.shape[0])
            + " documents to process"
        )

        try:
            for success, details in helpers.parallel_bulk(
                self.elastic_connection,
                doc_generator(df=df_dep),
                chunk_size=self.elastic_bulk_size,
            ):
                # logging.info(f'{details} \n {success}')
                if not success:
                    raise Exception(f"A file_access document failed: {details}")
        except Exception as e:
            logging.error(f"Failed to send to Elasticsearch: {e}")

        time.sleep(1)

        doc_count = self.elastic_connection.cat.count(
            index=self.elastic_index, params={"format": "json"}
        )[0]["count"]
        logging.info(f"Number of documents indexed: {doc_count}")

        elastic_mapping = Siren._index.get_mapping()
        logging.info(f"The {self.elastic_index} index mapping: {elastic_mapping}")
