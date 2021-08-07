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


@dataclass
class HDXGetOutputSchemaCase:
    datatype: str
    schema: str


@dataclass
class HDXGetCodProcessedFilePathCase:
    dataset_name: str
    processed_filepath: str


@dataclass
class GetDamnLayerCase:
    datatype: str
    layer: str


@dataclass
class GetGeoboundariesRawCase:
    datatype: str
    geoboundaries: str


@dataclass
class GetIsoCase:
    country: str
    iso_code: str


@dataclass
class GetSchemaMappingOsmSourceCase:
    dataset_name: str
    fclass: str


@dataclass
class GetSchemaMappingCodSourceCase:
    dataset_name: str
    schem_mapping: dict


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


HDX_GET_OUTPUT_SCHEMA_CASES = [
    HDXGetOutputSchemaCase("adm0", "admin0_affected_area_py.yml"),
    HDXGetOutputSchemaCase("adm1", "admin1_affected_area_py.yml"),
    HDXGetOutputSchemaCase("adm2", "admin2_affected_area_py.yml"),
    HDXGetOutputSchemaCase("adm3", "admin3_affected_area_py.yml"),
]


@pytest.mark.parametrize("case", HDX_GET_OUTPUT_SCHEMA_CASES)
def test_get_hdx_output_schema(case):
    for country in PARSED_COUNTRIES:
        assert config.get_hdx_output_schema(country, case.datatype).endswith(
            case.schema
        )


GET_COD_PROCESSED_FILEPATH_CASES = [
    HDXGetCodProcessedFilePathCase(
        "adm0", "/202_admn/{}_admn_ad0_py_s0_unocha_pp_pipeline_generated.shp"
    ),
    HDXGetCodProcessedFilePathCase(
        "adm1", "/202_admn/{}_admn_ad1_py_s1_unocha_pp_pipeline_generated.shp"
    ),
    HDXGetCodProcessedFilePathCase(
        "adm2", "/202_admn/{}_admn_ad2_py_s2_unocha_pp_pipeline_generated.shp"
    ),
    HDXGetCodProcessedFilePathCase(
        "adm3", "/202_admn/{}_admn_ad3_py_s3_unocha_pp_pipeline_generated.shp"
    ),
]


@pytest.mark.parametrize("case", GET_COD_PROCESSED_FILEPATH_CASES)
def test_get_cod_processed_filepath(case):
    for country in PARSED_COUNTRIES:
        end = case.processed_filepath.format(config.get_iso3(country)).lower()
        assert config.get_cod_processed_filepath(country, case.dataset_name).endswith(
            end
        )


def test_roads_schema():
    answer = config.get_roads_schema()
    assert answer.endswith("/configs/schemas/roads_affected_area_ln.yml")


def test_get_crs():
    assert config.get_crs() == "EPSG:4326"


GET_GADM_LAYERS_CASES = [
    GetDamnLayerCase("adm0", "gadm36_{ISO3}_0"),
    GetDamnLayerCase("adm1", "gadm36_{ISO3}_1"),
    GetDamnLayerCase("adm2", "gadm36_{ISO3}_2"),
    GetDamnLayerCase("adm3", "gadm36_{ISO3}_3"),
]


@pytest.mark.parametrize("case", GET_GADM_LAYERS_CASES)
def test_get_gadm_level(case):
    assert config.get_gadm_layer(case.datatype) == case.layer


GET_GEOBOUNDARIES_RAW_CASES = [
    GetGeoboundariesRawCase("adm0", "/{}/GIS/1_Original_Data/geobnd_adm0.zip"),
    GetGeoboundariesRawCase("adm1", "/{}/GIS/1_Original_Data/geobnd_adm1.zip"),
    GetGeoboundariesRawCase("adm2", "/{}/GIS/1_Original_Data/geobnd_adm2.zip"),
    GetGeoboundariesRawCase("adm3", "/{}/GIS/1_Original_Data/geobnd_adm3.zip"),
]


@pytest.mark.parametrize("case", GET_GEOBOUNDARIES_RAW_CASES)
def test_get_geoboundaries_raw(case):
    for country in PARSED_COUNTRIES:
        end = case.geoboundaries.format(country)
        assert config.get_geoboundaries_raw(country, case.datatype).endswith(end)


GET_ISO3_CASES = [
    GetIsoCase("bangladesh", "BGD"),
    GetIsoCase("cameroon", "CMR"),
    GetIsoCase("dominica", "DMA"),
    GetIsoCase("dominican_republic", "DOM"),
    GetIsoCase("haiti", "HTI"),
    GetIsoCase("fiji", "FJI"),
    GetIsoCase("malawi", "MWI"),
    GetIsoCase("nepal", "NPL"),
    GetIsoCase("pakistan", "PAK"),
    GetIsoCase("philippines", "PHL"),
    GetIsoCase("south_sudan", "SSD"),
    GetIsoCase("vanuatu", "VUT"),
    GetIsoCase("yemen", "YEM"),
]


@pytest.mark.parametrize("case", GET_ISO3_CASES)
def test_get_iso3(case):
    assert config.get_iso3(case.country) == case.iso_code


GET_ISO2_CASES = [
    GetIsoCase("bangladesh", "BD"),
    GetIsoCase("cameroon", "CM"),
    GetIsoCase("dominica", "DM"),
    GetIsoCase("dominican_republic", "DO"),
    GetIsoCase("haiti", "HT"),
    GetIsoCase("fiji", "FJ"),
    GetIsoCase("malawi", "MW"),
    GetIsoCase("nepal", "NP"),
    GetIsoCase("pakistan", "PK"),
    GetIsoCase("philippines", "PH"),
    GetIsoCase("south_sudan", "SS"),
    GetIsoCase("vanuatu", "VU"),
    GetIsoCase("yemen", "YE"),
]


@pytest.mark.parametrize("case", GET_ISO2_CASES)
def test_get_iso2(case):
    assert config.get_iso2(case.country) == case.iso_code


GET_SCHEMA_MAPPING_OSM_SOURCE_CASES = [
    GetSchemaMappingOsmSourceCase("roads", "highway"),
    GetSchemaMappingOsmSourceCase("rail", "railway"),
    GetSchemaMappingOsmSourceCase("airports", "aerodrome:type"),
    GetSchemaMappingOsmSourceCase("seaports", "port:type"),
    GetSchemaMappingOsmSourceCase("rivers", "waterway"),
    GetSchemaMappingOsmSourceCase("lakes", "water"),
    GetSchemaMappingOsmSourceCase("seas", "water"),
    GetSchemaMappingOsmSourceCase("places", "place"),
]


@pytest.mark.parametrize("case", GET_SCHEMA_MAPPING_OSM_SOURCE_CASES)
def test_get_schema_mapping_osm_source(case):
    for country in PARSED_COUNTRIES:
        answer = {"name:en": "name_en", "name": "name_loc", case.fclass: "fclass"}
        assert config.get_schema_mapping("osm", country, case.dataset_name) == answer


# TODO: Set the correct schema mappings in tests and fix the code
GET_SCHEMA_MAPPING_COD_SOURCE_CASES = [
    GetSchemaMappingCodSourceCase(
        "roads", {"name:en": "name_en", "name": "name_loc", "highway": "fclass"}
    ),
    GetSchemaMappingCodSourceCase(
        "adm0", {"admin0Name_en": "ADM0_EN", "pcode": "ADM0_PCODE"}
    ),
    GetSchemaMappingCodSourceCase(
        "adm1",
        {"admin1Name_en": "ADM1_EN", "pcode": "ADM1_PCODE", "par_pcode": "par_pcode"},
    ),
    GetSchemaMappingCodSourceCase(
        "adm2",
        {"ADM2_EN": "ADM2_EN", "ADM2_PCODE": "ADM2_PCODE", "ADM1_PCODE": "par_pcode"},
    ),
    GetSchemaMappingCodSourceCase(
        "adm3",
        {"ADM3_EN": "ADM3_EN", "ADM3_PCODE": "ADM3_PCODE", "ADM2_PCODE": "par_pcode"},
    ),
]


@pytest.mark.parametrize("case", GET_SCHEMA_MAPPING_COD_SOURCE_CASES)
def test_get_schema_mapping_cod_source(case):
    for country in PARSED_COUNTRIES:
        assert (
            config.get_schema_mapping("cod", country, case.dataset_name)
            == case.schem_mapping
        )
