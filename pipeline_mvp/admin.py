import os
import logging

from dagster import solid
import geopandas as gpd

from pipeline_mvp.utils.utils import get_dataset_from_hdx, get_layer_by_name_contains_and_geometry

# TODO: move this somewhere
CRS = 'EPSG:4326'
logger = logging.getLogger(__name__)


@solid(required_resource_keys={'cmf'})
def extract_admin_cod(context, hdx_address, hdx_filename):
    context.log.info('Downloading COD admin boundaries')
    # TODO: For CODS - refactor this out somewhere
    CODS_raw_data_dir = '101_OCHA'
    save_filepath = os.path.join(context.resources.cmf.get_raw_data_dir(), CODS_raw_data_dir, hdx_filename)
    get_dataset_from_hdx(hdx_address, hdx_filename, save_filepath)
    return save_filepath


@solid(required_resource_keys={'cmf'})
def transform_admin_cod(context, raw_filepath, admin_level=0):
    context.log.info('Transforming COD admin boundaries')
    layer_name = get_layer_by_name_contains_and_geometry(raw_filepath, f'adm{admin_level}', geometry='Polygon')
    df_adm = gpd.read_file(f'zip://{raw_filepath}', layer=layer_name)
    # TODO move this, only works for COD Yemen
    schema_mapping = {
        'admin0Name_en': 'name_en'
    }
    # Change CRS
    if df_adm.crs != CRS:
        df_adm.to_crs(CRS)
    # Modify the column names to suit the schema
    df_adm = df_adm.rename(columns=schema_mapping)
    # Write out
    output_filename = 'yem_admn_ad0_py_s0_unocha_pp.shp'
    df_adm.to_file(os.path.join(context.resources.cmf.get_final_data_dir(), '202_admn',
                                output_filename))