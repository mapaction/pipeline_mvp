import geopandas as gpd


def transform_cod(input_filename, schema_mapping):
    df = gpd.read_file(f"zip://{input_filename}")

    # COD data has some NAs
    df = df[df["geometry"].notna()]
    # Rename columns using schema_mapping
    df = df.rename(columns=schema_mapping)
    return df
