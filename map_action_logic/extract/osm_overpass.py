from api_access.requests_api import download_url
from map_action_logic.extract.extract_utils.osm import convert_osm2gpkg
from storage_access.files import create_download_folder, save_file
from storage_access.yaml_api import parse_yaml


def extract_osm_query(
    osm_url,
    country_iso2,
    overpass_query_schema_filename,
    osm_output_filename,
    gpkg_output_filename,
):
    osm_schema = parse_yaml(overpass_query_schema_filename)
    geom_type = osm_schema["geom_type"]

    create_download_folder(osm_output_filename, gpkg_output_filename)

    get_osm_xml(osm_url, osm_query(osm_schema, country_iso2), osm_output_filename)
    convert_osm2gpkg(osm_output_filename, gpkg_output_filename, geom_type)

    save_file(osm_output_filename)
    save_file(gpkg_output_filename)



def osm_query(  # noqa: C901 - see Jira issue DATAPIPE-89 for more information
    osm_yml: dict, iso2_country: str
):
    """Country based query using Overpass Query Language.  Using key value pairs,
    contructs a simple OSM query on relations, ways & nodes.

    Input osm_tags should be a dictionary, where:
    (1) it has exactly two elements, which are:
        (a) osm_types - a list of geometry OSM data types (relation, way, node)
        (b) tags - a list of one or more dictionaries where the key values are those tag-name & tag-values requested

    For example {osm_types: [values], tags: {['highway': ['motorway', 'trunk']}]}

    Input iso2_country is the two letter ISO country code for a specific country

    The query will be built around requesting all matched osm data types where the
    property (key) matches one of the related values.
    """

    # Define output type. Default is XML
    # Area filter part of query
    area_filter = f'(area["ISO3166-1"="{iso2_country}"]["admin_level"="2"];)->.a; \n'
    # Main part of query is the union of sets returned with key-value tags.
    # this is perhaps overcomplicated but tries to accept different tag values in yaml file,
    # will work whether yaml tag value is list, string or dict.
    main_query = "( \n"
    for osm_type in osm_yml["osm_types"]:
        if osm_yml["flag"] == "AND":
            main_query += f"{osm_type}"
            for tags in osm_yml["tags"]:
                for tag, value in tags.items():
                    if type(value) == list:
                        for tag_value in value:
                            main_query += f"[{tag}={tag_value}]"
                    elif type(value) == str:
                        main_query += f"[{tag}={value}]"
                    elif value is None:
                        main_query += f"[{tag}]"
            main_query += "(area.a); \n"
        else:
            for tags in osm_yml["tags"]:
                for tag, value in tags.items():
                    if type(value) == list:
                        for tag_value in value:
                            main_query += f"{osm_type}[{tag}={tag_value}](area.a); \n"
                    elif type(value) == str:
                        main_query += f"{osm_type}[{tag}={value}](area.a); \n"
                    elif value is None:
                        main_query += f"{osm_type}[{tag}](area.a); \n"
    main_query += "); \n"
    # Check geom_type output in osm_yml (will be used to create temp shapefile)
    # catch errors in case geom_type missing from osm_yml
    try:
        geom_type = osm_yml["geom_type"]
    except Exception as e:
        print(e)
        geom_type = None
    if geom_type == "points":
        # don't recurse nodes, instead return centroid of feature, not line/poly, return final set.
        recurse_out = "out center qt;"
    else:
        # recurse through previous set to return all nodes & full geometry, then return final set
        recurse_out = "(._;>;); \n" "out body qt;"
    # Combine all parts of query into full query to send to Overpass
    final_query = area_filter + main_query + recurse_out
    return final_query


def get_osm_xml(api_url, osm_query, output_file):
    """
    # Commented out as using requests wrapped in method in utils/requests_api.py
    response  = requests.get(api_url,
                                params={'data': osm_query})
    data = response.text
    if response.status_code == 200:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(response.text)
    else:
        pass
    """
    download_url(api_url, output_file, parameters={"data": osm_query})
