# Build the local Docker image for the Airflow server

cp $(pwd)/requirements-airflow.txt $(pwd)/docker/requirements-airflow.txt

docker build -t docker-airflow-custom -f docker/airflow.Dockerfile --build-arg AIRFLOW_DEPS=kubernetes,gcp $(pwd)/docker/.

rm $(pwd)/docker/requirements-airflow.txt