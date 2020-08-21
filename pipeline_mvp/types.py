import logging

from geopandas import GeoDataFrame
from dagster import (
    DagsterType,
    PythonObjectDagsterType,
    TypeCheck,
    EventMetadataEntry
)

logger = logging.getLogger(__name__)


DagsterGeoDataFrame = PythonObjectDagsterType(GeoDataFrame,
                                              loader=None,
                                              materializer=None)


def admin_boundaries_type_check(_, df_adm):
    if not isinstance(df_adm, GeoDataFrame):
            return TypeCheck(
            success=False,
            description=f'Was expecting GeoDataFrame, got {type(df_adm)}'
        )
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


