# Pipeline MVP

MVP project for Airflow-based scheduling of data pipeline processing for MapAction. This repository is used for local development and for running in GCP.

## Structure

`/dags`

`/plugins`

`/scripts`

`/data`

`/requirements.txt`

`/requirements-airflow.txt`

## Local development

### Requirements

Docker is a dependency for running a local version of Airflow.

### Initial setup

To create a virtual environment for local development, run the following from the root folder:

`source ./scripts/setup_environment.sh`

When you add new dependencies, rerun this command to install the new dependencies in your virtual environment.

### Development

To start the Airflow server, run the following from the root folder:

`sh ./start_airflow.sh`

The Airflow server runs in a Docker container, which has the `/dags`, `/plugins` and `/data` folders mounted in there, together with the `requirements-airflow.txt` file. When starting the container, these requirements are installed. The `/data` folder is accessible from `/opt/data` folder inside the Airflow server/worker. The `/dags` folder contains all the dags and is automatically synchronized, while the `/plugins` folder contains the plugins including all the processing logic. This is also automatically synchronized but still a bit shaky, so if things are not working, restart the Docker container.