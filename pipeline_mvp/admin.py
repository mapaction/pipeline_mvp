import os
import logging
from datetime import datetime

from dagster import (
    solid,
    Output,
    AssetMaterialization,
    EventMetadataEntry,
    Field,
    OutputDefinition,
)
import geopandas as gpd
from hdx.location.country import Country

from pipeline_mvp.utils import utils
from pipeline_mvp.utils.hdx import get_dataset_from_hdx
from pipeline_mvp.types import DagsterGeoDataFrame, AdminBoundaries

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
    output_defs=[OutputDefinition(DagsterGeoDataFrame, name=f'df_adm{i}', is_required=False) for i in range(4)]
)
def read_in_admin_cod(context, raw_filepath: str) :
    for admin_level in range(context.solid_config['max_admin_level'] + 1):
        logger.info(f'Running admin level {admin_level}')
        layer_name = utils.get_layer_by_name_contains_and_geometry(raw_filepath,
                                                                   f'adm{admin_level}',
                                                                   geometry='Polygon')
        df_adm = gpd.read_file(f'zip://{raw_filepath}', layer=layer_name)
        df_adm.attrs['admin_level'] = admin_level
        yield Output(df_adm, f'df_adm{admin_level}')


@solid(required_resource_keys={'cmf'})
def transform_admin_cod(context, df_adm: DagsterGeoDataFrame) -> AdminBoundaries:
    logger.info('Transforming COD admin boundaries')
    # Admin level is stored in metadata
    admin_level = df_adm.attrs['admin_level']
    # Change CRS
    if df_adm.crs != CRS:
        df_adm.to_crs(CRS, inplace=True)
    # Modify the column names to suit the schema
    # TODO: refactor the keys out to e.g. config file
    metis_config = utils.get_metis_config()
    admin_level_names = {f'admin{level}Name_en': metis_config['admin_boundaries']['name'].format(level=level)
                         for level in range(admin_level+1)}
    pcode_names = {f'admin{level}Pcode': metis_config['admin_boundaries']['pcode'].format(level=level)
                   for level in range(admin_level+1)}
    schema_mapping = {**admin_level_names, **pcode_names}
    df_adm.rename(columns=schema_mapping, inplace=True)
    # Add metadata
    # TODO: Some stuff here is COD / Yemen specific
    df_adm.attrs['crs'] = df_adm.crs
    df_adm.attrs['iso3'] = context.resources.cmf.iso3
    df_adm.attrs['iso2'] = Country.get_iso2_from_iso3(context.resources.cmf.iso3)
    df_adm.attrs['publisher'] = 'OCHA'
    df_adm.attrs['source_date'] = df_adm.iloc[0]['validOn']
    df_adm.attrs['create_date'] = datetime.now().strftime('%Y-%m-%d')
    df_adm.attrs['geometry_type'] = df_adm.iloc[0]['geometry']
    # TODO this is a quick hack, should be fixed (break down the metadata, have a method for forming the filename)
    df_adm.attrs['output_filename'] = os.path.join('202_adm', f'yem_admn_ad{admin_level}_py_s0_unocha_pp.shp')
    df_adm.attrs['asset_key'] =f'admin_cod_lvl{admin_level}'
    df_adm.attrs['description'] = f'Processed COD admin boundaries level {admin_level}',
    #  Because of output type will materialize to shapefile
    yield Output(df_adm)
