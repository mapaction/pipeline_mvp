from pipeline_plugin.transform.general_transformers.osm_transform import \
    transform_osm
from pipeline_plugin.transform.general_transformers.postprocess import \
    postprocess
from pipeline_plugin.utils.files import load_file, save_shapefiles


def transform(
    source: str, input_filename: str, output_filename: str, crs, schema_mapping
):
    """
    :param source: "osm" is the only option
    """
    input_filename = load_file(input_filename)

    if source == "osm":
        df_airports = transform_osm(
            input_filename=input_filename, schema_mapping=schema_mapping
        )
        df_airports = postprocess(df=df_airports, crs=crs)

    save_shapefiles(df_airports, output_filename, encoding="utf8")
