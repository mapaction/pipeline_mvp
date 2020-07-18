import os
import logging

from dagster import solid

from pipeline_mvp.utils.utils import get_dataset_from_hdx, config_logger

logger = logging.getLogger(__name__)


@solid
def extract_admin_cod(_):
    # TODO: all these should go to config files
    # HDX params
    hdx_address = 'yemen-admin-boundaries'
    hdx_filename = 'yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip'
    # Path for raw data
    cmf = '/home/turnerm/data/yemen_cmf'
    event_id = '2020yem01'
    raw_data_dir = os.path.join(cmf, event_id, 'GIS', '1_Original_Data')
    # For CODS
    CODS_raw_data_dir = '101_OCHA'
    save_directory = os.path.join(raw_data_dir, CODS_raw_data_dir)
    save_filepath = os.path.join(save_directory, hdx_filename)
    get_dataset_from_hdx(hdx_address, hdx_filename, save_filepath)
    return save_filepath
