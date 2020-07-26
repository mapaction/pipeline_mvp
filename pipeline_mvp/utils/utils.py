import shutil
import logging
from pathlib import Path

from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

HDX_SITE = 'prod'
USER_AGENT = 'MapAction'


Configuration.create(hdx_site=HDX_SITE, user_agent=USER_AGENT, hdx_read_only=True)
logger = logging.getLogger(__name__)


def config_logger():
    """
    Setup the logger
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def mkdir(path: str):
    """
    Create a direcotry if it doesn't exist
    :param path: path of directory to create
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def get_dataset_from_hdx(hdx_address: str, dataset_name: str, save_filepath: str):
    """
    Use the HDX API to download a daset based on the address and dataset ID
    :param hdx_address: The HDX address of the dataset
    :param dataset_name: The name of the dataset
    :param save_filepath: The desired full filepath of the downloaded file
    """
    logger.info(f'Querying HDX API for dataset {hdx_address}')
    resources = Dataset.read_from_hdx(hdx_address).get_resources()
    for resource in resources:
        if resource['name'] == dataset_name:
            _, download_filepath = resource.download()
            #mkdir(save_filepath)
            shutil.move(download_filepath, save_filepath)
            logging.info(f'Saved \"{resource["name"]}\" to {save_filepath}')
            return
    logger.error(f'Dataset with name {dataset_name} not found')
