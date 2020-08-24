import os
import logging

from dagster import (
    dagster_type_materializer,
    AssetMaterialization,
    EventMetadataEntry,
)

logger = logging.getLogger(__name__)


@dagster_type_materializer({}, required_resource_keys = {'cmf'})
def shapefile_materializer(context, config, df):
    output_filepath = os.path.join(context.resources.cmf.get_final_data_dir(),
                                   df.attrs['output_filename'])
    df.to_file(output_filepath, encoding='utf-8')
    logger.debug(f'Wrote dataframe to {output_filepath}')
    yield AssetMaterialization(
        asset_key=df.attrs['asset_key'],
        description=df.attrs['description'],
        metadata_entries=[
            EventMetadataEntry.path(
                output_filepath, 'output_filepath')
        ])
    # TODO: can materialize metadata as JSON
