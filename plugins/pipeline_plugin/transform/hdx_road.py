import sys

import geopandas as gpd
from jsonschema import validate

from pipeline_plugin.utils.yaml_api import parse_yaml


def transform(input_filename: str, schema_filename: str, output_filename: str, schema_mapping, crs):
    """
    :param source: "cod" or "gadm"
    """

    df_roads = gpd.read_file(f'zip://{input_filename}')
    # COD data has some NAs
    df_roads = df_roads[df_roads['geometry'].notna()]
    # TODO need to convert from XML to GPKG rather than OSM to GPKG

    # Change CRS
    df_roads = df_roads.to_crs(crs)
    # Rename columns
    df_roads = df_roads.rename(columns=schema_mapping)
    # Make columns needed for validation
    df_roads['geometry_type'] = df_roads['geometry'].apply(lambda x: x.geom_type)
    df_roads['crs'] = df_roads.crs
    # Validate
    validate(instance=df_roads.to_dict('list'), schema=parse_yaml(schema_filename))
    # Write to output
    df_roads.to_file(output_filename)
