import logging
import os
import zipfile

from airflow.exceptions import AirflowFailException
import fiona
import geopandas as gpd
from jsonschema import validate
from storage_access.files import load_file, save_shapefiles
from storage_access.yaml_api import parse_yaml

GADM_FILENAME = "gadm36_{ISO3}.gpkg"

logger = logging.getLogger()


def transform(
    source: str,
    adm_level,
    input_filename: str,
    input_file_type: str,
    input_layer_name: str,
    output_schema_filename: str,
    output_filename: str,
    iso3,
    source_geoboundaries,
    schema_mapping,
    crs,
    gadm_layer,
):
    input_filename = load_file(input_filename)

    adm_df = gpd.GeoDataFrame()
    logger.info(f"Source = {source}")
    if source == "cod":
        logger.info(f"Input file type = {input_file_type}")
        if input_file_type == "gpkg":
            adm_df = transform_cod_gpkg(input_filename, adm_level)
        elif input_file_type == "shp":
            adm_df = transform_cod_shp(
                input_filename, adm_level, layer_name=input_layer_name
            )

    elif source == "gadm":
        adm_df = gpd.read_file(
            f"zip://{input_filename}!{GADM_FILENAME.format(ISO3=iso3)}",
            layer=gadm_layer.format(ISO3=iso3),
        )

    elif source == "geoboundaries":
        adm_df = transform_geoboundaries(source_geoboundaries)
    logger.info("Admin DataFrame successfully created.")
    adm_df = postprocess(
        adm_df=adm_df,
        schema_mapping=schema_mapping,
        output_schema_filename=output_schema_filename,
        crs=crs,
    )
    logger.info("Postprocessing was successful.")
    save_shapefiles(geopandas_df=adm_df, output_filename=output_filename)
    logger.info("Saved shapefiles.")


def transform_cod_gpkg(input_filename, adm_level) -> gpd.GeoDataFrame:
    layerlist = fiona.listlayers(f"zip://{input_filename}")
    search = adm_level
    for sublist in layerlist:
        if search in sublist:
            with fiona.open(f"zip://{input_filename}", layer=sublist) as layer:
                for feature in layer:
                    if feature["geometry"]["type"] == "MultiPolygon":
                        # print(feature['geometry']['type'],sublist)
                        adm = sublist

    index = layerlist.index(adm)
    adm_name = layerlist[index]

    return gpd.read_file(f"zip://{input_filename}", layer=adm_name)


def transform_cod_shp(input_filename, adm_level, layer_name=None) -> gpd.GeoDataFrame:
    logger.info(
        f"Transform Cod Shp Arguments:\n"
        f"Input Filename = {input_filename}"
        f"Admin Level = {adm_level}"
        f"Layer Name = {layer_name}"
    )
    if layer_name is None:
        with zipfile.ZipFile(input_filename) as z:
            for filename in z.namelist():
                if adm_level in filename.lower() and filename.lower().endswith(".shp"):
                    layer_name = filename
    if layer_name is None:
        raise AirflowFailException(
            f"There is no {adm_level} layer in the input dataset!"
        )
    return gpd.read_file(f"zip://{input_filename}!{layer_name}")


def transform_geoboundaries(source_geob):
    unzipped, ext = os.path.splitext(source_geob)
    # Unzip
    geobndzip = zipfile.ZipFile(source_geob, "r")
    geobndzip.extractall(unzipped)
    geobndzip.close()
    # Find geojson
    geojson = []
    for (
        root,
        dirs,  # noqa: B007 - see Jira issue DATAPIPE-89 for more information
        files,
    ) in os.walk(unzipped):
        for filename in files:
            if filename.endswith(".geojson"):
                geojson.append(os.path.join(root, filename))
    if len(geojson) > 1:
        print("Found more than one geojson file in {0}".format(unzipped))
    elif len(geojson) == 0:
        print("Found no geojson files in {0}".format(unzipped))

    return gpd.read_file(geojson[0])


def postprocess(adm_df: gpd.GeoDataFrame, schema_mapping, output_schema_filename, crs):
    # Change CRS
    adm_df = adm_df.to_crs(crs=crs)
    # Modify the column names to suit the schema
    adm_df = adm_df.rename(columns=schema_mapping)
    # Make columns needed for validation
    adm_df["geometry_type"] = adm_df["geometry"].apply(lambda x: x.geom_type)
    adm_df["crs"] = adm_df.crs
    # Validate
    validate(instance=adm_df.to_dict("list"), schema=parse_yaml(output_schema_filename))
    # Write to outpu
    # with open("/opt/data/")
    return adm_df
