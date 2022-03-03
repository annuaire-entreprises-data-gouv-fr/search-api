#!/bin/bash
mkdir -p dags
mkdir -p logs
chmod -R 777 logs
mkdir -p pg-airflow
mkdir -p plugins
mkdir -p scripts
mkdir -p ssh
echo "AIRFLOW_UID=$(id -u)" >> .env
echo "AIRFLOW_GID=0" >> .env