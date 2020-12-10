import sys
import os
import zipfile
import geopandas as gpd
import fiona
import tempfile
from jsonschema import validate

from pipeline_plugin.utils.yaml_api import parse_yaml
from pipeline_plugin.utils.copy_file import copy_file


GADM_FILENAME = 'gadm36_{ISO3}.gpkg'


def transform(source: str,
              adm_level,
              input_filename: str,
              schema_filename: str,
              output_filename: str,
              iso3,
              source_geoboundaries,
              schema_mapping,
              crs,
              gadm_layer):

    adm_df = gpd.GeoDataFrame()

    if source == "cod":
        adm_df = transform_cod(input_filename, adm_level)

    elif source == "gadm":
        adm_df = gpd.read_file(f'zip://{input_filename}!{GADM_FILENAME.format(ISO3=iso3)}',
                               layer=gadm_layer.format(ISO3=iso3))

    elif source == "geoboundaries":
        adm_df = transform_geoboundaries(source_geoboundaries)

    adm_df = postprocess(adm_df=adm_df, schema_mapping=schema_mapping, schema_filename=schema_filename, crs=crs)

    with open(os.path.join(tempfile.tempdir, output_filename), "wb") as f:
        adm_df.to_file(f)
        print(f.name, output_filename)
        copy_file(f.name, output_filename)


def transform_cod(input_filename, adm_level) -> gpd.GeoDataFrame:
    layerlist = fiona.listlayers(f'zip://{input_filename}')
    search = adm_level
    for sublist in layerlist:
        if search in sublist:
            with fiona.open(f'zip://{input_filename}', layer=sublist) as layer:
                for feature in layer:
                    if feature['geometry']['type'] == 'MultiPolygon':
                        # print(feature['geometry']['type'],sublist)
                        adm = sublist

    index = layerlist.index(adm)
    adm_name = layerlist[index]

    return gpd.read_file(f'zip://{input_filename}', layer=adm_name)


def transform_geoboundaries(source_geob):
    unzipped, ext = os.path.splitext(source_geob)
    # Unzip
    geobndzip = zipfile.ZipFile(source_geob, 'r')
    geobndzip.extractall(unzipped)
    geobndzip.close()
    # Find geojson
    geojson = []
    for root, dirs, files in os.walk(unzipped):
        for filename in files:
            if filename.endswith(".geojson"):
                geojson.append(os.path.join(root, filename))
    if len(geojson) > 1:
        print('Found more than one geojson file in {0}'.format(unzipped))
    elif len(geojson) == 0:
        print('Found no geojson files in {0}'.format(unzipped))

    return gpd.read_file(geojson[0])


def postprocess(adm_df: gpd.GeoDataFrame, schema_mapping, schema_filename, crs):
    # Change CRS
    adm_df = adm_df.to_crs(crs=crs)
    # Modify the column names to suit the schema
    adm_df = adm_df.rename(columns=schema_mapping)
    # Make columns needed for validation
    adm_df['geometry_type'] = adm_df['geometry'].apply(lambda x: x.geom_type)
    adm_df['crs'] = adm_df.crs
    # Validate
    validate(instance=adm_df.to_dict('list'), schema=parse_yaml(schema_filename))
    # Write to outpu
    # with open("/opt/data/")
    return adm_df