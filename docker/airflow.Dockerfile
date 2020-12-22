FROM puckel/docker-airflow:1.10.9

# # Install Cubonacci code as python package
# RUN /usr/venv/bin/pip install /usr/src

# # Install Cubonacci code requirements
# RUN /usr/venv/bin/pip install -r docker_image/requirements.txt

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/usr/local/airflow
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

USER airflow
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
