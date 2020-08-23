import logging

from geopandas import GeoDataFrame
from dagster import (
    DagsterType,
    PythonObjectDagsterType,
    TypeCheck,
    EventMetadataEntry
)

from pipeline_mvp.utils import utils

logger = logging.getLogger(__name__)


DagsterGeoDataFrame = PythonObjectDagsterType(GeoDataFrame,
                                              loader=None,
                                              materializer=None)


####################
# Admin boundaries #
####################

def admin_boundaries_type_check(_, df_adm):
    # Check that it's a GeoDataFrame
    if not isinstance(df_adm, GeoDataFrame):
        return TypeCheck(
            success=False,
            description=f'Was expecting GeoDataFrame, got {type(df_adm)}'
        )
    # Check columns
    metis_config = utils.get_metis_config()
    for column_type in ['name', 'pcode']:
        for level in range(df_adm.attrs['admin_level'] + 1):
            expected_column = metis_config['admin_boundaries'][column_type].format(level=level)
            if expected_column not in df_adm.columns:
                return TypeCheck(
                    success=False,
                    description=f'Missing column {expected_column}'
                )
    # Check metadata
    # TODO: check type in addition to existence
    for metadata in ['crs',
                     'iso3',
                     'iso3',
                     'publisher',
                     'source_date',
                     'create_date',
                     'geometry_type']:
        if metadata not in df_adm.attrs:
            return TypeCheck(
                success=False,
                description=f'Missing metadata {metadata}'
            )
    # Check geometry type
    if not all(['Polygon' in geometry_type for geometry_type in df_adm['geometry'].geom_type]):
        return TypeCheck(
            success=False,
            description=f'Found non-polygon geometry'
        )
    # All successful
    # TODO: can add more relevant metadata to output
    return TypeCheck(success=True,
                     description='AdminBoundaries summary statistics',
                     metadata_entries=[
                         EventMetadataEntry.text(f'{", ".join(df_adm.columns)}',
                                                 'column_names',
                                                 'Keys of columns seen in the data frame')
                     ])


AdminBoundaries = DagsterType(
    name='AdminBoundaries',
    type_check_fn=admin_boundaries_type_check,
    description='A GeoDataFrame containing administrative boundaries'
)
