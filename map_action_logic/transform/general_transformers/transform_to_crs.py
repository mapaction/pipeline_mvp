def transform_to_crs(df, crs):
    # TODO need to convert from XML to GPKG rather than OSM to GPKG
    # Change CRS
    # Make columns needed for validation
    # # df_roads['geometry_type'] = df_roads['geometry'].apply(lambda x: x.geom_type)
    # # df_roads['crs'] = df_roads.crs
    # Validate
    # # validate(instance=df_roads.to_dict('list'), schema=parse_yaml(schema_filename))
    # Write to output
    df = df.to_crs(crs)
    return df
