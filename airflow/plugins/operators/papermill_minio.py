from typing import Dict, Optional

import attr
import papermill as pm

from airflow.lineage.entities import File
from airflow.models import BaseOperator

from nbconvert import HTMLExporter
import codecs
import nbformat

import glob, os

from minio import Minio

@attr.s(auto_attribs=True)
class NoteBook(File):
    """Jupyter notebook"""

    type_hint: Optional[str] = "jupyter_notebook"
    parameters: Optional[Dict] = {}

    meta_schema: str = __name__ + '.NoteBook'


class PapermillMinioOperator(BaseOperator):
    """
    Executes a jupyter notebook through papermill that is annotated with parameters
    :param input_nb: input notebook (can also be a NoteBook or a File inlet)
    :type input_nb: str
    :param output_nb: output notebook (can also be a NoteBook or File outlet)
    :type output_nb: str
    :param tmp_path: tmp path to store report during processing
    :type tmp_path: str
    :param minio_url: minio url where report should be store
    :type minio_url: str
    :param minio_bucket: minio bucket where report should be store
    :type minio_bucket: str
    :param minio_user: minio user which will store report
    :type minio_user: str
    :param minio_password: minio password of minio user
    :type minio_password: str
    :param minio_output_filepath: complete filepath where to store report
    :type minio_output_filepath: str
    :param parameters: the notebook parameters to set
    :type parameters: dict
    """

    supports_lineage = True

    template_fields = ('input_nb', 'output_nb', 'tmp_path', 'minio_url', 'minio_bucket', 'minio_user', 'minio_password', 'minio_output_filepath', 'parameters')

    def __init__(
        self,
        *,
        input_nb: Optional[str] = None,
        output_nb: Optional[str] = None,
        tmp_path: Optional[str] = None,
        minio_url: Optional[str] = None,
        minio_bucket: Optional[str] = None,
        minio_user: Optional[str] = None,
        minio_password: Optional[str] = None,
        minio_output_filepath: Optional[str] = None,
        parameters: Optional[Dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.input_nb = input_nb
        self.output_nb = output_nb
        self.tmp_path = tmp_path
        self.minio_url = minio_url
        self.minio_bucket = minio_bucket
        self.minio_user = minio_user
        self.minio_password = minio_password
        self.minio_output_filepath = minio_output_filepath
        self.parameters = parameters

    def execute(self, context):
        if not self.input_nb or not self.output_nb:
            raise ValueError("Input notebook or output notebook is not specified")

        os.makedirs(os.path.dirname(self.tmp_path+"output/"), exist_ok=True)

        pm.execute_notebook(
            self.input_nb,
            self.tmp_path+self.output_nb,
            parameters=self.parameters,
            progress_bar=False,
            report_mode=True,
        )

        exporter = HTMLExporter()
        # read_file is '.ipynb', output_report is '.html'
        output_report = os.path.splitext(self.tmp_path+self.output_nb)[0]+'.html'
        output_notebook = nbformat.read(self.tmp_path+self.output_nb, as_version=4)
        output, resources = exporter.from_notebook_node(output_notebook)
        codecs.open(output_report, 'w', encoding='utf-8').write(output)

        client = Minio(
            self.minio_url,
            access_key=self.minio_user,
            secret_key=self.minio_password,
            secure=True
        )

        # check if bucket exists.
        found = client.bucket_exists(self.minio_bucket)
        if found:            
            client.fput_object(
                self.minio_bucket, 
                self.minio_output_filepath+output_report.split('/')[-1], 
                output_report,
                content_type="text/html; charset=utf-8",
                metadata={'Content-Disposition': 'inline'}
            )

            for path, subdirs, files in os.walk(self.tmp_path+"output/"):
                for name in files:
                    print(os.path.join(path, name))
                    isFile = os.path.isfile(os.path.join(path, name))
                    if(isFile):
                        client.fput_object(
                            self.minio_bucket, 
                            self.minio_output_filepath+os.path.join(path, name).replace(self.tmp_path,''),
                            os.path.join(path, name)
                        )
        
        report_url = 'https://{}/{}/{}'.format(
                self.minio_url,
                self.minio_bucket,
                self.minio_output_filepath+output_report.split('/')[-1]
            )
        context['ti'].xcom_push(key='report_url', value=report_url)
