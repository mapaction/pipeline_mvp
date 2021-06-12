import geopandas as gpd

from sqlalchemy.dialects.postgresql import HSTORE

from pipeline_plugin.utils.files import load_file, save_shapefiles, save_file


def transform(source: str, input_filename: str, output_filename: str, crs, schema_mapping):
    """
        :param source: "osm" is the only option
    """
    input_filename = load_file(input_filename)

    if source == "osm":
        df_rail = transform_osm(input_filename=input_filename, schema_mapping=schema_mapping)
        df_rail = postprocess(df_rail=df_rail, crs=crs)

    save_shapefiles(df_rail, output_filename, encoding='utf8')



def transform_osm(input_filename, schema_mapping):
    df_rail = gpd.read_file(input_filename)

    # GDAL converts OSM to GPKG, tags are written as hstore key-value in attribute 'other_tags'
    # method to convert hstore string to dictionary from SqlAlchemy
    hstore = HSTORE.result_processor(None, None, 'string')
    df_rail['other_tags'] = df_rail['other_tags'].apply(hstore)

    for key, value in schema_mapping.items():
        # temp dictionary for pandas rename method. Don't use original dict as want to see whether
        # each input attribute is present.
        temp_schema_dict = {key: value}
        try:
            # rename column if exists.
            df_rail = df_rail.rename(columns=temp_schema_dict, errors="raise")
        except:
            # as error raised, input attribute is not present.
            # now make sure output attribute is NOT present.  If not pull from 'other_tags'
            if value not in df_rail.columns:
                df_rail[value] = df_rail['other_tags'].apply(lambda x: x.get(key) if type(x) == dict else x)

    # now remove columns which aren't in schema:
    schema_to_keep = list(schema_mapping.values())
    # add geometry to schema
    schema_to_keep.append('geometry')
    return df_rail.filter(schema_to_keep)


def postprocess(df_rail, crs):
    # TODO need to convert from XML to GPKG rather than OSM to GPKG
    df_rail = df_rail.to_crs(crs)
    return df_rail
