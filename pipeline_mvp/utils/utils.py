import os
import time
import logging
from pathlib import Path

import fiona


logger = logging.getLogger(__name__)


def mkdir(path: str):
    """
    Create a direcotry if it doesn't exist
    :param path: path of directory to create
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def get_file_age_days(filepath: str):
    try:
        file_age_days = (time.time() - os.path.getatime(filepath)) / 60 / 60
    except FileNotFoundError:
        file_age_days = -1
    return file_age_days


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
