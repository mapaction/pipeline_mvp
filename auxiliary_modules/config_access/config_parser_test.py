from dataclasses import dataclass

import pytest

from .config_parser import config


@dataclass
class HDXInfoTestCase:
    country: str
    hdx_type: str
    result: str


@dataclass
class HDXAdminLayerNameTestCase:
    country: str
    adm_level: str
    layer_name: str


@dataclass
class HDXGetRawCODFilenameCase:
    country: str
    datatype: str
    filename: str


@dataclass
class OSMGetRawDataPathCase:
    country: str
    dataset_name: str
    format: str
    path: str


@dataclass
class OSMGetRawProcessedPathCase:
    country: str
    dataset_name: str
    processed_path: str


# TESTS FOR PUBLIC METHODS


# The list of parsed countries must be updated when including new countries to the pipeline.
PARSED_COUNTRIES = [
    "bangladesh",
    "cameroon",
    "dominica",
    "dominican_republic",
    "fiji",
    "haiti",
    "malawi",
    "nepal",
    "pakistan",
    "philippines",
    "south_sudan",
    "vanuatu",
    "yemen",
]


def test_parsed_countries():
    countries = config.get_countries()
    assert sorted(countries) == sorted(PARSED_COUNTRIES)


# HDX CODS


HDX_ADDRESS_TEST_CASES = [
    HDXInfoTestCase("yemen", "adm", "yemen-admin-boundaries"),
    HDXInfoTestCase("malawi", "adm", "malawi-administrative-level-0-3-boundaries"),
    HDXInfoTestCase("haiti", "adm", "hti-polbndl-adm1-cnigs-zip"),
    HDXInfoTestCase("fiji", "adm", "null"),
    HDXInfoTestCase("yemen", "roads", "yemen-roads"),
    HDXInfoTestCase("dominica", "roads", "null"),
]


@pytest.mark.parametrize("case", HDX_ADDRESS_TEST_CASES)
def test_get_hdx_address(case):
    assert case.result == config.get_hdx_address(case.country, case.hdx_type)


HDX_DATASET_NAME_CASES = [
    HDXInfoTestCase("yemen", "adm", "yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip"),
    HDXInfoTestCase("yemen", "roads", "ymn-roads.zip"),
    HDXInfoTestCase("fiji", "adm", "null"),
    HDXInfoTestCase("pakistan", "roads", "null"),
]


@pytest.mark.parametrize("case", HDX_DATASET_NAME_CASES)
def test_get_hdx_dataset_name(case):
    assert case.result == config.get_hdx_dataset_name(case.country, case.hdx_type)


HDX_DATASET_TYPE_CASES = [
    HDXInfoTestCase("philippines", "adm", "shp"),
    HDXInfoTestCase("fiji", "adm", "null"),
]


@pytest.mark.parametrize("case", HDX_DATASET_TYPE_CASES)
def test_get_hdx_dataset_type(case):
    assert case.result == config.get_hdx_dataset_type(case.country, case.hdx_type)


HDX_DATASET_LAYER_NAME_CASES = [
    HDXAdminLayerNameTestCase("yemen", "adm0", "null"),
    HDXAdminLayerNameTestCase(
        "philippines", "adm0", "phl_admbnda_adm0_psa_namria_itos_20200529.shp"
    ),
]


@pytest.mark.parametrize("case", HDX_DATASET_LAYER_NAME_CASES)
def test_get_hdx_layer_name(case):
    assert case.layer_name == config.get_hdx_dataset_type(case.country, case.adm_level)


SHOULD_PROCESS_HDX_ROADS = [
    "yemen",
]


def test_should_process_hdx_roads():
    for country in PARSED_COUNTRIES:
        should_process_hdx_roads = country in SHOULD_PROCESS_HDX_ROADS
        assert should_process_hdx_roads == config.should_process_hdx_roads(country)


HDX_GET_RAW_COD_FILENAME_CASES = [
    HDXGetRawCODFilenameCase("yemen", "adm_cod_raw", "yem_cod_adm.zip"),
    HDXGetRawCODFilenameCase("vanuatu", "adm_cod_raw", "vut_cod_adm.zip"),
    HDXGetRawCODFilenameCase("yemen", "roads_cod_raw", "yem_cod_roads.zip"),
    HDXGetRawCODFilenameCase("vanuatu", "roads_cod_raw", "vut_cod_roads.zip"),
]


@pytest.mark.parametrize("case", HDX_GET_RAW_COD_FILENAME_CASES)
def test_get_raw_cod_filename(case):
    assert config.get_cod_raw_filename(case.country, case.datatype).endswith(
        case.filename
    )


def test_get_osm_url():
    for country in PARSED_COUNTRIES:
        assert config.get_osm_url(country).startswith("http://overpass-api.de/")


RAW_OSM_DATA_PATH_CASES = [
    OSMGetRawDataPathCase("fiji", "roads", "raw_xml", "fji_osm_roads.xml"),
    OSMGetRawDataPathCase("yemen", "rail", "raw_xml", "yem_osm_rail.xml"),
    OSMGetRawDataPathCase(
        "bangladesh", "airports", "raw_gpkg", "bgd_osm_airports.gpkg"
    ),
    OSMGetRawDataPathCase("dominica", "seaports", "raw_gpkg", "dma_osm_seaports.gpkg"),
]


@pytest.mark.parametrize("case", RAW_OSM_DATA_PATH_CASES)
def test_get_raw_osm_data_path(case):
    country = case.country
    dataformat = case.format
    dataset_name = case.dataset_name
    path = case.path
    assert config.get_raw_osm_data_path(country, dataset_name, dataformat).endswith(
        path
    )


GET_RAW_OSM_PROCESSED_PATH_CASES = [
    OSMGetRawProcessedPathCase(
        "yemen", "roads", "/232_tran/yem_tran_rds_ln_s1_osm_pp_pipeline_generated.shp"
    ),
    OSMGetRawProcessedPathCase(
        "bangladesh",
        "rail",
        "/232_tran/bgd_tran_rrd_ln_s1_osm_pp_pipeline_generated.shp",
    ),
    OSMGetRawProcessedPathCase(
        "fiji", "lakes", "/221_phys/fji_phys_lak_py_s1_osm_pp_pipeline_generated.shp"
    ),
    OSMGetRawProcessedPathCase(
        "cameroon",
        "rivers",
        "/221_phys/cmr_phys_riv_ln_s1_osm_pp_pipeline_generated.shp",
    ),
]


@pytest.mark.parametrize("case", GET_RAW_OSM_PROCESSED_PATH_CASES)
def test_get_raw_osm_processed_filepath(case):
    assert config.get_osm_processed_filepath(case.country, case.dataset_name).endswith(
        case.processed_path
    )


# The list of osm data types must be updated when including new countries to the pipeline.
OSM_DATA_TYPES = (
    "roads",
    "rail",
    "seaports",
    "airports",
    "places",
    "rivers",
    "lakes",
    "seas",
)
OSM_QUERY_CORRECT_PATH = "/configs/schemas/overpass_queries/osm_tags_{}.yml"


def test_get_osm_query_schema():
    for country in PARSED_COUNTRIES:
        for dataset_name in OSM_DATA_TYPES:
            postfix = OSM_QUERY_CORRECT_PATH.format(dataset_name)
            assert config.get_osm_query_schema(country, dataset_name).endswith(postfix)
