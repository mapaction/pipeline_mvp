import os
import logging

from dagster import (
    solid,
    Output,
    AssetMaterialization,
    EventMetadataEntry,
    Field,
    OutputDefinition,
    DagsterType
)
from dagster_pandas import DataFrame
import geopandas as gpd

from pipeline_mvp.utils.utils import get_layer_by_name_contains_and_geometry
from pipeline_mvp.utils.hdx import get_dataset_from_hdx
from pipeline_mvp.types import GeoDataFrame

# TODO: move this somewhere
CRS = 'EPSG:4326'
logger = logging.getLogger(__name__)


@solid(required_resource_keys = {'cmf'})
def extract_admin_cod(context, hdx_address: str, hdx_filename: str) -> str:
    logger.info('Downloading COD admin boundaries')
    # TODO: For CODS - refactor this out somewhere
    CODS_raw_data_dir = '101_OCHA'
    save_directory = os.path.join(context.resources.cmf.get_raw_data_dir(), CODS_raw_data_dir)
    save_filepath = get_dataset_from_hdx(hdx_address, hdx_filename, save_directory)
    # Confirm that the file was saved
    yield AssetMaterialization(
        asset_key='admin_cod_raw',
        description='Raw COD admin boundaries',
        metadata_entries=[
            EventMetadataEntry.path(
                save_filepath, 'save_filepath'
            )
        ],
    )
    # Yield final output as a filename
    yield Output(save_filepath)


@solid(
    config_schema={
        'max_admin_level': Field(int, is_required=False, default_value=2)
    },
    output_defs=[OutputDefinition(GeoDataFrame, name=f'df_adm{i}', is_required=False) for i in range(4)]
)
def read_in_admin_cod(context, raw_filepath: str) :
    for admin_level in range(context.solid_config['max_admin_level'] + 1):
        logger.info(f'Running admin level {admin_level}')
        layer_name = get_layer_by_name_contains_and_geometry(raw_filepath, f'adm{admin_level}', geometry='Polygon')
        df_adm = gpd.read_file(f'zip://{raw_filepath}', layer=layer_name)
        df_adm.attrs['admin_level'] = admin_level
        yield Output(df_adm, f'df_adm{admin_level}')


@solid(required_resource_keys={'cmf'})
def transform_admin_cod(context, df_adm: GeoDataFrame) -> GeoDataFrame:
    logger.info('Transforming COD admin boundaries')
    # Admin level is stored in metadata
    admin_level = df_adm.attrs['admin_level']
    # Change CRS
    if df_adm.crs != CRS:
        df_adm.to_crs(CRS)
    # Modify the column names to suit the schema
    # TODO move this, only works for COD Yemen
    schema_mapping = {f'admin{admin_level}Name_en': 'name_en'}
    df_adm = df_adm.rename(columns=schema_mapping)
    # Write out
    output_filename = f'yem_admn_ad{admin_level}_py_s0_unocha_pp.shp'
    output_filepath = os.path.join(context.resources.cmf.get_final_data_dir(), '202_admn', output_filename)
    df_adm.to_file(output_filepath, encoding='utf-8')
    # Confirm that the file was saved
    yield AssetMaterialization(
        asset_key=f'admin_cod_lvl{admin_level}',
        description=f'Processed COD admin boundaries level {admin_level}',
        metadata_entries=[
            EventMetadataEntry.path(
                output_filepath, 'output_filepath'
            )
        ],
    )
    yield Output(df_adm)
