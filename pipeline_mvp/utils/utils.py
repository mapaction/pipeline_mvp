import shutil
import logging
from pathlib import Path

import fiona
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

HDX_SITE = 'prod'
USER_AGENT = 'MapAction'


Configuration.create(hdx_site=HDX_SITE, user_agent=USER_AGENT, hdx_read_only=True)
logger = logging.getLogger(__name__)


def mkdir(path: str):
    """
    Create a direcotry if it doesn't exist
    :param path: path of directory to create
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def get_layer_by_name_contains_and_geometry(filepath: str, layer_name_contains: str , geometry: str=None):
    """

    :param filepath:
    :param layer_name_contains: Case insensitive
    :param geometry: Should be a valid geometry. Will handle the case if you e.g. provide 'Polygon' and
    it's actually a MultiPolygon.
    :return:
    """
    for layer_name in fiona.listlayers(f'zip://{filepath}'):
        if layer_name_contains.lower() in layer_name.lower():
            if geometry is None:
                logger.debug(f'Found layer {layer_name}')
                return layer_name
            with fiona.open(f'zip://{filepath}', layer=layer_name) as layer:
                if geometry in layer.schema['geometry']:
                    logger.debug(f'Found layer "{layer_name}" with geometry "{layer.schema["geometry"]}"')
                    return layer_name
    # TODO: should raise a custom error
    error_string = f'In file {filepath}, no layer with name containing "{layer_name_contains}"'
    if geometry is not None:
        error_string += f' and geometry "{geometry}"'
    logger.error(error_string)


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
