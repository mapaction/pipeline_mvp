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
GADM_LAYER = 'gadm36_{ISO3}_0'


def transform_cod(input_filename) -> gpd.GeoDataFrame:
    layerlist = fiona.listlayers(f'zip://{input_filename}')
    search = 'adm0'
    for sublist in layerlist:
        if search in sublist:
            with fiona.open(f'zip://{input_filename}', layer=sublist) as layer:
                for feature in layer:
                    if feature['geometry']['type'] == 'MultiPolygon':
                        # print(feature['geometry']['type'],sublist)
                        adm0 = sublist
    # print(adm0)

    index = layerlist.index(adm0)
    adm0_name = layerlist[index]

    return gpd.read_file(f'zip://{input_filename}', layer=adm0_name)


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
        print('Found more than one geojson file in {0}'.format(zippedshpdir))
    elif len(geojson) == 0:
        print('Found no geojson files in {0}'.format(zippedshpdir))

    return gpd.read_file(geojson[0])


def postprocess(adm0_df: gpd.GeoDataFrame, schema_mapping, schema_filename, crs):
    # Change CRS
    # TODO: Add back configuration
    # df_adm0 = df_adm0.to_crs(config['constants']['crs'])
    adm0_df = adm0_df.to_crs(crs=crs)
    # Modify the column names to suit the schema
    adm0_df = adm0_df.rename(columns=schema_mapping)
    # Make columns needed for validation
    adm0_df['geometry_type'] = adm0_df['geometry'].apply(lambda x: x.geom_type)
    adm0_df['crs'] = adm0_df.crs
    # Validate
    validate(instance=adm0_df.to_dict('list'), schema=parse_yaml(schema_filename))
    # Write to output
    # with open("/opt/data/")
    return adm0_df


def transform(source: str, input_filename: str, schema_filename: str, output_filename: str, iso3, raw_data_dir,
              geoboundaries_adm0_raw, schema_mapping, crs):
    """
    :param source: "cod" or "gadm"
    """
    # config = parse_yaml('config.yaml')

    adm0_df = gpd.GeoDataFrame()

    if source == "cod":
        adm0_df = transform_cod(input_filename)

    elif source == "gadm":
        adm0_df = gpd.read_file(f'zip://{input_filename}!{GADM_FILENAME.format(ISO3=iso3)}',
                                layer=GADM_LAYER.format(ISO3=iso3))

    elif source == "geoboundaries":
        source_geob = os.path.join(raw_data_dir, geoboundaries_adm0_raw)
        adm0_df = transform_geoboundaries(source_geob)

    adm0_df = postprocess(adm0_df=adm0_df, schema_mapping=schema_mapping, schema_filename=schema_filename, crs=crs)

    with open(os.path.join(tempfile.tempdir, output_filename), "wb") as f:
        adm0_df.to_file(f)
        print(f.name, output_filename)
        copy_file(f.name, output_filename)


