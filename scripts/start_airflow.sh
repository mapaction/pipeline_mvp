# Run from root of repository

docker run --name local-airflow-server -e ENVIRONMENT=local -d -p 8080:8080 -v $(pwd)/data/:/usr/local/airflow/data -v $(pwd)/dags/:/usr/local/airflow/dags puckel/docker-airflow webserver
