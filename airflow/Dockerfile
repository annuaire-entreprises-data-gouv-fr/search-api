FROM apache/airflow

USER root

RUN apt-get install curl

ARG AIRFLOW_HOME=/opt/airflow 

ADD dags /opt/airflow/dags 

ADD airflow.cfg /opt/airflow/airflow.cfg

RUN pip install --upgrade pip

RUN chown -R "airflow:root" /opt/airflow/

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org boto3

USER airflow

ADD requirements.txt /requirements.txt

EXPOSE 8080

RUN pip install -r /requirements.txt
