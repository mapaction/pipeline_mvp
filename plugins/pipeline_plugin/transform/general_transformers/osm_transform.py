from sqlalchemy.dialects.postgresql import HSTORE

import geopandas as gpd


def transform_osm(input_filename, schema_mapping):
    df = gpd.read_file(input_filename)
    # df_roads = convert_osm_to_gpkg(input_filename, 'osm_roads.gpkg', 'lines')

    # GDAL converts OSM to GPKG, tags are written as hstore key-value in attribute 'other_tags'
    # method to convert hstore string to dictionary from SqlAlchemy
    hstore = HSTORE.result_processor(None, None, "string")
    df["other_tags"] = df["other_tags"].apply(hstore)

    for key, value in schema_mapping.items():
        # temp dictionary for pandas rename method. Don't use original dict as want to see whether
        # each input attribute is present.
        temp_schema_dict = {key: value}
        try:
            # rename column if exists.
            df = df.rename(columns=temp_schema_dict, errors="raise")
        except:  # noqa: E722, B001 - see Jira issue DATAPIPE-89 for more information
            # as error raised, input attribute is not present.
            # now make sure output attribute is NOT present.  If not pull from 'other_tags'
            if value not in df.columns:
                df[value] = df["other_tags"].apply(
                    lambda x: x.get(key) if type(x) == dict else x
                )

    # now remove columns which aren't in schema:
    schema_to_keep = list(schema_mapping.values())
    # add geometry to schema
    schema_to_keep.append("geometry")
    return df.filter(schema_to_keep)
