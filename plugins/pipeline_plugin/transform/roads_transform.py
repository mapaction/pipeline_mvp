from pipeline_plugin.utils.files import load_file, save_shapefiles

from pipeline_plugin.transform.general_transformers.osm_transform import transform_osm
from pipeline_plugin.transform.general_transformers.cod_transform import transform_cod
from pipeline_plugin.transform.general_transformers.postprocess import postprocess

def transform(
    source: str, input_filename: str, output_filename: str, crs, schema_mapping
):
    input_filename = load_file(input_filename)

    if source == "osm":
        df_roads = transform_osm(
            input_filename=input_filename, schema_mapping=schema_mapping
        )
        df_roads = postprocess(df=df_roads, crs=crs)

    elif source == "cod":
        df_roads = transform_cod(
            input_filename=input_filename, schema_mapping=schema_mapping
        )
        df_roads = postprocess(df=df_roads, crs=crs)

    save_shapefiles(df_roads, output_filename, encoding="utf8")
