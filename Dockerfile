FROM apache/airflow:2.3.4

# Airflow
ARG AIRFLOW_VERSION=2.3.4
ARG AIRFLOW_USER_HOME=/home/airflow/gcs
ARG AIRFLOW_DATA_MOUNT=/opt/airflow/data
ARG AIRFLOW_DEPS="gcp"
ARG PYTHON_DEPS=""
ARG POSTGRES_PASS="airflow"
ARG POSTGRES_HOST"127.0.0.1"
ARG POSTGRES_PORT="5432"
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ENV POSTGRES_USER=${POSTGRES_PASS}
ENV POSTGRES_PASSWORD=${POSTGRES_PASS}
ENV POSTGRES_DB=${POSTGRES_PASS}
ENV POSTGRES_DB_HOST=${POSTGRES_HOST}
ENV POSTGRES_DB_PORT=${POSTGRES_PORT}

USER root

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING
RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -y software-properties-common \
    && apt install g++ -yqq \
    && apt install libsasl2-dev \
    && apt-get install gdal-bin -yqq \
    && apt-get install libgdal-dev -yqq \
    && export CPLUS_INCLUDE_PATH=/usr/include/gdal \
    && export C_INCLUDE_PATH=/usr/include/gdal \
    && ogrinfo --version \

RUN useradd -U -u 1000 airflow
USER airflow

RUN pip install GDAL==3.2.2
RUN pip install ogr


RUN pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION}

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

# Required to workaround https://github.com/apache/airflow/issues/12924
RUN pip install attrs==20.3.0

RUN mkdir -p ${AIRFLOW_USER_HOME}

RUN mkdir ${AIRFLOW_DATA_MOUNT}
USER root
RUN chown airflow: ${AIRFLOW_DATA_MOUNT}

ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/airflow_logic"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/map_action_logic"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/api_access/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/gcp_settings/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/config_access/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/storage_access/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/configs/"

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
