echo docker exec -it "${PWD##*/}"_webserver_1 python -c "from airflow.models import DagBag; d = DagBag();"
docker exec -it "${PWD##*/}"_webserver_1 python -c "from airflow.models import DagBag; d = DagBag();"

