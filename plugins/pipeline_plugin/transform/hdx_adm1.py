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
GADM_LAYER = 'gadm36_{ISO3}_1'


def transform(source: str, input_filename: str, schema_filename: str, output_filename: str):
    """
    :param source: "cod" or "gadm"
    """
    # config = parse_yaml('config.yml')

    if source == "cod":
        layerlist = fiona.listlayers(f'zip://{input_filename}')
        search = 'adm1'
        for sublist in layerlist:
            if search in sublist:
                with fiona.open(f'zip://{input_filename}', layer=sublist) as layer:
                    for feature in layer:
                        if feature['geometry']['type'] == 'MultiPolygon':
                            # print(feature['geometry']['type'],sublist)
                            adm1 = sublist
        # print(adm1)

        index = layerlist.index(adm1)
        adm1_name = layerlist[index]

        df_adm1 = gpd.read_file(f'zip://{input_filename}', layer=adm1_name)
        schema_mapping = {
            'admin1Name_en': 'name_en'
        }
    elif source == "gadm":
        df_adm1 = gpd.read_file(f'zip://{input_filename}!{GADM_FILENAME.format(ISO3=config["constants"]["ISO3"])}',
                                layer=GADM_LAYER.format(ISO3=config['constants']['ISO3']))
        schema_mapping = {
            'NAME_1': 'name_en',
            'GID_1': 'pcode',
            'GID_0': 'par_pcode'
        }
    elif source == "geoboundaries":
        rawdir = config['dirs']['raw_data']
        source_geob = os.path.join(rawdir, config['geoboundaries']['adm1']['raw'])
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
        else:
            df_adm1 = gpd.read_file(geojson[0])
        schema_mapping = {'shapeName': 'name_en'}
    # Change CRS
    # TODO: Add back configuration
    # df_adm1 = df_adm1.to_crs(config['constants']['crs'])
    df_adm1 = df_adm1.to_crs("EPSG:2090")
    # Modify the column names to suit the schema
    df_adm1 = df_adm1.rename(columns=schema_mapping)
    # Make columns needed for validation
    df_adm1['geometry_type'] = df_adm1['geometry'].apply(lambda x: x.geom_type)
    df_adm1['crs'] = df_adm1.crs
    # Validate
    validate(instance=df_adm1.to_dict('list'), schema=parse_yaml(schema_filename))
    # Write to output
    with open(os.path.join(tempfile.tempdir, output_filename), "wb") as f:
        # with tempfile.NamedTemporaryFile(dir="/opt/data") as fp:
        df_adm1.to_file(f)
        print(f.name, output_filename)
        copy_file(f.name, output_filename)
