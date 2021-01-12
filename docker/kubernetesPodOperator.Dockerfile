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
    && pip install GDAL==$(ogrinfo --version | cut -d ',' -f1 | sed 's/[^0-9\.]//g')

# Copy requirements
COPY requirements.txt /usr/src/requirements.txt

# Install Airflow code requirements
RUN pip install -r /usr/src/requirements.txt

# Copy code into container
COPY plugins/pipeline_plugin /usr/src/pipeline_plugin

# Add /usr/src to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/usr/src"

RUN mkdir /usr/src/data

# Run Kubernetes main script
CMD ["python", "pipeline_plugin/kubernetes_main.py"]
