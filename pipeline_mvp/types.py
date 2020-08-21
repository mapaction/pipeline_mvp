from dagster import (
    usable_as_dagster_type
)
from dagster_pandas import (
    create_dagster_pandas_dataframe_type,
    PandasColumn
)

@usable_as_dagster_type(
    name='LessSimpleDataFrame',
    description='A more sophisticated data frame that type checks its structure.',
    #loader=less_simple_data_frame_loader,
    #materializer=less_simple_data_frame_materializer,
)
class LessSimpleDataFrame(list):
    pass


GeoDataFrame = create_dagster_pandas_dataframe_type(
    name='GeoDataFrame',
    columns=[PandasColumn.exists('geometry')],
)