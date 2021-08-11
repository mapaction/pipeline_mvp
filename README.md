# Pipeline MVP

MVP project for Airflow-based scheduling of data pipeline processing for MapAction. This repository is used for local
development and for running in GCP.

## Background and History

This project is one is a series of projects outlines in our
["Moonshoot" initative](https://mapaction.org/mapactions-moonshot-origins-and-ambitions). This seeks to automate many
of the tasks in pre-emergency data preparedness and the initial tasks in map production.

In 2020 we ran two projects exploring how we could automate the acquisition of data.

First was the "Slow Data Scramble". For this we focused on just one country - Yemen. We identified 22 commonly required
data artefacts. For each artefact and data source combination, we defined the acquisition and transformation necessary.

* There is a [blog post describing this project](https://mapaction.org/moonshot-part-2-the-slow-data-scramble)
* The code is here https://github.com/mapaction/datasources-etl

The second was our "Pipeline MVP" project. This took many of the concepts from the Slow Data Scramble. This generalised
to multiple countries 13 countries. Additionally, it migrated the code so that it could be hosted in Google Cloud
Platform using Airflow.

* This code is here https://github.com/mapaction/pipeline_mvp

## Structure

`/.github`

GitLab Actions configuration files (see [Continuous Deployment](#continuous-deployment)).

`/airflow_logic`

Folder with high-level scripts related to airflow (DAGs, Operators, etc).


`/map_action_logic`

Folder with the core MapAction logic.

`/auxiliary modules`

Folder with low-level supportive functions

`/configs`

Folder with configs and chemas

`/data`

Empty folder that is mounted in the local Docker container so that any data generated by the dags is also available in
the local environment.

`/requirements.txt`

Required Python packages.

`/requirements-dev.txt`

Required Python packages for development, only installed within local container.

`/docker-compose.yml`

Configuration file for running Airflow locally using Docker containers

`/Dockerfile`

Definition for the Docker image used to run Airflow locally.

`/kubernetes-pod-operator.Dockerfile`

Definition for the Docker image used to execute Airflow tasks in Google Cloud Composer (I think).

## Local development

The instructions below have been tested for setting up a local development environment on Ubuntu 20.04.
There are seperate instructions on developing on Windows Subsystem for Linux (WSL).

https://github.com/mapaction/pipeline_mvp/wiki/Docker-on-Windows

### Local requirements

1. [Git](https://git-scm.com/)
1. [Docker](https://www.docker.com) and [Docker compose](https://docs.docker.com/compose/)
    - Docker for Windows/macOS is recommended on these platforms
1. [Python](https://python.org) and the [pre-commit](https://pre-commit.com/#install) package

To install for macOS using brew:

```
$ brew install git pre-commit
$ brew install --cask docker
```

### Local setup

Clone the project repository and build a local Docker image using Docker Compose:

```shell
$ git clone https://github.com/mapaction/pipeline_mvp.git
$ cd pipeline_mvp/
$ docker compose build airflow
```

**Note:** This image is approx ~2GB in size.

### Local usage

To start the Airflow server:

```shell
$ cd pipeline_mvp/
$ docker compose up
```

The Airflow server runs in a Docker container, which as a number of directories (such as `/dags` and `/data`) mounted
as volumes (see `docker-compose.yml` for details). Files updated in these directories should update in real time (i.e.
without needing to update or recreate the container).

**Note:** If you change Python dependencies by changing `requirements.txt`, you will need to rebuild the Docker image
(see [Initial setup](#initial-setup)).

To stop the Airflow server:

```shell
$ docker compose down
```

## Code standards

This project has adopted a number of code standards to ensure there is consistency across different contributors, and
best practices are followed. To that end, some of these code standards are intentionally opinionated.

These code standards are enforced by:

* a [pre-commit hook](#pre-commit-hook) (locally)
* [Continuous Integration](#continuous-deployment) (remotely)

### EditorConfig

An [`.editorconfig`](https://editorconfig.org/) file is included to configure compatible editors to automatically
comply with code standards adopted for this project.

### Pre-commit hook

The [pre-commit](https://pre-commit.com) package (and its config file `.pre-commit-config.yaml`) is used to define,
and enforce, code standards adopted for this project. `pre-commit` will run automatically on each Git commit.

To run manually:

```
$ pre-commit run --all-files
```

To install so that `pre-commit` will run automatically on each Git commit enter this command:

```
pre-commit install
```

### Flake8

The [Flake8](https://flake8.pycqa.org/) package (and its config file `.flake8`) is used to define, and enforce, Python
specific code standards for this project. Flake8 checks will be automatically run as part of the
[Pre-commit hook](#pre-commit-hooks).

To run manually:

```
$ docker compose run airflow flake8 dags/ plugins/ tests/ airflow_logic/ map_action_logic/ gcp_settings/ storage_access/ config_access/ api_access/
```

### Black

The [Black](https://black.readthedocs.io/en/stable/) package is used to define, and enforce, Python code style rules for
this project. Black formatting will automatically be checked as part of the [Flake8](#flake8) checks.

To run manually:

```
$ docker compose run airflow black dags/ plugins/ tests/ airflow_logic/ map_action_logic/ gcp_settings/ storage_access/ config_access/ api_access/
```

## Package security

The [Safety](https://github.com/pyupio/safety-db) package is used to check for vulnerable Python packages used in this
project.

To run manually:

```
$ docker compose run airflow safety check --file=/usr/local/airflow/requirements.txt --full-report
$ docker compose run airflow safety check --file=/usr/local/airflow/requirements-dev.txt --full-report
```

## Contribution workflow

1. create a task in the [Data Pipeline Development](https://mapaction.atlassian.net/browse/DATAPIPE) Jira project (Internal, MapAction)
1. create a local Git branch.
1. make changes until you are satisfied.
1. update the CHANGELOG.md as appropriate.
1. commit and push branch to GitHub
1. create a pull request from your branch targetting the `master` branch
1. move the Jira task to 'in review' and add a link to the GitHub PR
1. notify other project members of your branch in the [#topic-automation](https://mapaction.slack.com/archives/CKF3LQGGL) Slack channel (Internal, MapAction) with a link to the GitHub PR for review
1. all reviews and comments should be captured in the PR
1. once review is complete, merge PR and remove merged branch
7. move the Jira task to 'done'

## Continuous Integration

GitHub Actions is used for Continuous Integration.

When triggered (by editing relevant files) these actions will:

* install development dependencies needed for linting tools
* run linting tools against relevant files

See the GitHub Actions configuration files in `/.github/workflows/` for details on the exact steps taken.

## Continuous Deployment

GitHub Actions is used for Continuous Deployment.

When triggered (by editing relevant files) these actions will:

* rebuild the container used for Airflow tasks (i.e. the execution environment)
* copy Airflow DAGs and plugins to a storage bucket

See the GitHub Actions configuration files in `/.github/workflows/` for details on the exact steps taken.

### Initial setup

1. in Google Cloud, create a Service Account (`pipeline-gh-actions-bot`) with these permissions:
  * *Storage Admin* role for the Google Cloud Registry bucket (`eu.artifacts.datapipeline-xxx.appspot.com`)
  * *Storage Admin* role for the DAGs/plugins Google Cloud bucket (`europe-west2-mapaction-xxx-bucket`)
  * `composer.environments.update` for the Google Cloud Composer environment (`mapaction-xxx`)
2. in Google Cloud, create a key (encoded as a JSON file), if needed, remove whitespace from this file (one line)
3. in the GitHub project, create new secrets (Settings -> Secrets) with these names:
  * `GCLOUD_BUCKET_PATH`: name of the DAGs/plugins Google Cloud bucket (`europe-west2-mapaction-xxx-bucket`)
  * `GCLOUD_IMAGE_NAME`: namme of the Google Cloud Registry image (`eu.gcr.io/datapipeline-xxx/mapaction-cloudcomposer-kubernetes-image`)
  * `GCLOUD_COMPOSER_ENVIRONMENT`: name of the Google Cloud Composer environment (`mapaction-xxx`)
  * `GCLOUD_PROJECT`: ID of the Google Cloud Platform project (`datapipeline-xxx`)
  * `GCLOUD_SERVICE_KEY`: JSON service account key as a string (do not remove whitespace)

**Note:** As currently deployed, the Service Account used for this project has an email address that relates to a legacy
testing account. This is recognised as being sub-optimal and will be changed in the future when additional environments
are added (see )

## Tests
To run unit tests locally run pytest in the root directory:
```
$ pytest
```

To run unit tests in the airflow local environment:

```
$ docker-compose run --entrypoint bash --workdir /home/airflow/gcs/ airflow
$ python -m pytest .
```

To run integration tests (not implemented yet) locally:

```
$ docker-compose run --entrypoint bash --workdir /home/airflow/gcs/tests airflow
$ python -m pytest .
```
