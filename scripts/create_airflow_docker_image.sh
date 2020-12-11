docker build -t docker-airflow-custom -f docker/airflow.Dockerfile --build-arg AIRFLOW_DEPS=kubernetes $(pwd)/docker/.
