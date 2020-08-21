import os
import time
import shutil
import logging

from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

from pipeline_mvp.utils import utils

HDX_SITE = 'prod'
USER_AGENT = 'MapAction'

Configuration.create(hdx_site=HDX_SITE, user_agent=USER_AGENT, hdx_read_only=True)
logger = logging.getLogger(__name__)


def get_dataset_from_hdx(hdx_address: str, dataset_name: str, save_directory: str, cache_days: int = 10):
    """
    Use the HDX API to download a daset based on the address and dataset ID
    :param hdx_address: The HDX address of the dataset
    :param dataset_name: The name of the dataset
    :param save_filepath: The desired full filepath of the downloaded file
    :param cache_days: How many days to cache the file (temporary for development)
    """
    save_filepath = os.path.join(save_directory, dataset_name)
    # TODO: make more generic caching ability
    file_age_days = utils.get_file_age_days(save_filepath)
    if 0 < file_age_days < cache_days:
        return save_filepath
    logger.info(f'Querying HDX API for dataset {hdx_address}')
    resources = Dataset.read_from_hdx(hdx_address).get_resources()
    for resource in resources:
        if resource['name'] == dataset_name:
            _, download_filepath = resource.download()
            shutil.move(download_filepath, save_filepath)
            logger.info(f'Saved to {save_filepath}')
            return save_filepath
    raise HDXDatasetNotFound(f'HDX dataset with address "{hdx_address}" and name "{dataset_name}" not found')


class HDXDatasetNotFound(Exception):
    pass
