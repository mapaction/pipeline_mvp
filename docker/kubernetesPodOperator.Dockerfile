FROM python:3.7.9
WORKDIR /usr/src

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:ubuntugis/ppa \
    && apt-get install gdal-bin -yqq \
    && apt-get install libgdal-dev -yqq \
    && export CPLUS_INCLUDE_PATH=/usr/include/gdal \
    && export C_INCLUDE_PATH=/usr/include/gdal \
    && ogrinfo --version \
    && pip install GDAL==2.4.0 \


# Copy requirements
COPY requirements.txt /usr/src/requirements.txt

# Install Airflow code requirements
RUN pip install -r /usr/src/requirements.txt

# Copy code into container
COPY plugins/pipeline_plugin /usr/src/pipeline_plugin

# Run Kubernetes main script
CMD ["python", "pipeline_plugin/kubernetes_main.py"]
