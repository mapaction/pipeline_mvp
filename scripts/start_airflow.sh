# Run from root of repository

docker run --name local-airflow-server \
           -e AIRFLOW__WEBSERVER__RELOAD_ON_PLUGIN_CHANGE=True \
           -e AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=False \
           -e ENVIRONMENT=local \
           -d \
           -p 8080:8080 \
           -v $(pwd)/plugins/:/usr/local/airflow/plugins \
           -v $(pwd)/requirements-airflow.txt:/requirements.txt \
           -v $(pwd)/data/:/opt/data \
           -v $(pwd)/dags/:/usr/local/airflow/dags \
           puckel/docker-airflow webserver
x-www-browser http://localhost:8080
