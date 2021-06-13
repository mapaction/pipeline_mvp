import geopandas as gpd

from sqlalchemy.dialects.postgresql import HSTORE

from pipeline_plugin.utils.files import load_file, save_shapefiles


def transform(source: str, input_filename: str, output_filename: str, crs, schema_mapping):
    input_filename = load_file(input_filename)

    if source == "osm":
        df_roads = transform_osm(input_filename=input_filename, schema_mapping=schema_mapping)
        df_roads = postprocess(df_roads=df_roads, crs=crs)

    elif source == "cod":
        df_roads = transform_cod(input_filename=input_filename, schema_mapping=schema_mapping)
        df_roads = postprocess(df_roads=df_roads, crs=crs)

    save_shapefiles(df_roads, output_filename, encoding='utf8')


def transform_osm(input_filename, schema_mapping):
    df_roads = gpd.read_file(input_filename)
    # df_roads = convert_osm_to_gpkg(input_filename, 'osm_roads.gpkg', 'lines')

    # GDAL converts OSM to GPKG, tags are written as hstore key-value in attribute 'other_tags'
    # method to convert hstore string to dictionary from SqlAlchemy
    hstore = HSTORE.result_processor(None, None, 'string')
    df_roads['other_tags'] = df_roads['other_tags'].apply(hstore)

    for key, value in schema_mapping.items():
        # temp dictionary for pandas rename method. Don't use original dict as want to see whether
        # each input attribute is present.
        temp_schema_dict = {key: value}
        try:
            # rename column if exists.
            df_roads = df_roads.rename(columns=temp_schema_dict, errors="raise")
        except:
            # as error raised, input attribute is not present.
            # now make sure output attribute is NOT present.  If not pull from 'other_tags'
            if value not in df_roads.columns:
                df_roads[value] = df_roads['other_tags'].apply(lambda x: x.get(key) if type(x) == dict else x)

    # now remove columns which aren't in schema:
    schema_to_keep = list(schema_mapping.values())
    # add geometry to schema
    schema_to_keep.append('geometry')
    return df_roads.filter(schema_to_keep)


def transform_cod(input_filename, schema_mapping):
    df_roads = gpd.read_file(f'zip://{input_filename}')

    # COD data has some NAs
    df_roads = df_roads[df_roads['geometry'].notna()]
    # Rename columns using schema_mapping
    df_roads = df_roads.rename(columns=schema_mapping)
    return df_roads


def postprocess(df_roads, crs):
    # TODO need to convert from XML to GPKG rather than OSM to GPKG
    # Change CRS
    # Make columns needed for validation
    # # df_roads['geometry_type'] = df_roads['geometry'].apply(lambda x: x.geom_type)
    # # df_roads['crs'] = df_roads.crs
    # Validate
    # # validate(instance=df_roads.to_dict('list'), schema=parse_yaml(schema_filename))
    # Write to output
    df_roads = df_roads.to_crs(crs)
    return df_roads
