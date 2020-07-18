import logging

from dagster import pipeline, execute_pipeline

from pipeline_mvp.utils.utils import config_logger
from pipeline_mvp.admin import extract_admin_cod

config_logger()
logger = logging.getLogger(__name__)


@pipeline
def pipeline_admin_cod():
    extract_admin_cod()


#if __name__ == '__main__':
#    execute_pipeline(pipeline_admin_cod)
