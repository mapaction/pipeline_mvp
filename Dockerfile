FROM puckel/docker-airflow:1.10.9

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/home/airflow/gcs
ARG AIRFLOW_DEPS="gcp"
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

USER root

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING
RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:ubuntugis/ppa \
    && apt-get install gdal-bin -yqq \
    && apt-get install libgdal-dev -yqq \
    && export CPLUS_INCLUDE_PATH=/usr/include/gdal \
    && export C_INCLUDE_PATH=/usr/include/gdal \
    && ogrinfo --version \
    && pip install GDAL==2.4.0

RUN pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION}

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

# Required to workaround https://github.com/apache/airflow/issues/12924
RUN pip install attrs==20.3.0

RUN mkdir -p ${AIRFLOW_USER_HOME}
RUN mkdir -p /opt/data
RUN chown -R airflow: ${AIRFLOW_USER_HOME}

ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/dags_utils"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/airflow_logic"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/map_action_logic"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/api_access/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/gcp_settings/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/config_access/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/storage_access/"
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/gcs/configs/"


USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
