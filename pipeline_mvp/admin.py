import os
import logging

from dagster import solid

from pipeline_mvp.utils.utils import get_dataset_from_hdx

logger = logging.getLogger(__name__)


@solid(required_resource_keys={'cmf'})
def extract_admin_cod(context, hdx_address, hdx_filename):
    context.log.info('Downloading COD admin boundaries')
    # For CODS - refactor this out somewhere
    CODS_raw_data_dir = '101_OCHA'
    save_directory = os.path.join(context.resources.cmf.get_raw_data_dir(), CODS_raw_data_dir)
    save_filepath = os.path.join(save_directory, hdx_filename)
    get_dataset_from_hdx(hdx_address, hdx_filename, save_filepath)
    return save_filepath
