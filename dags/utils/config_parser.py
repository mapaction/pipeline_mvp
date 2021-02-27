import os
import yaml
from pathlib import Path
import json
import logging

from typing import List

from utils.fallback_dict import FallbackDict

CMF_LOC = Path("default-crash-move-folder/20YYiso3nn/GIS")
CMF_SCHEMA_LOC = CMF_LOC / "5_Data_schemas"
CMF_LAYER_PROPERTIES_FILE = CMF_LOC / "3_Mapping/31_Resources/316_Automation/layerProperties.json"

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, path=None):
        if os.environ.get("GCP") == "TRUE":
            self._MAIN_AIRFLOW_FOLDER = Path(os.getcwd()) / "gcs"
            self._DATA_FOLDER = Path("data")
            self._SCHEMAS_FOLDER = Path("/") / "usr" / "src" / "pipeline_plugin" / CMF_SCHEMA_LOC
            layer_properties_file = Path("/") / "usr" / "src" / "pipeline_plugin" / CMF_LAYER_PROPERTIES_FILE
        else:
            self._MAIN_AIRFLOW_FOLDER = Path(os.getcwd())
            self._DATA_FOLDER = Path("/") / "opt" / "data"
            self._SCHEMAS_FOLDER = self._MAIN_AIRFLOW_FOLDER / "plugins" / "pipeline_plugin" / CMF_SCHEMA_LOC
            layer_properties_file = self._MAIN_AIRFLOW_FOLDER / "plugins" / "pipeline_plugin" / CMF_LAYER_PROPERTIES_FILE
        if not path:
            path = self._MAIN_AIRFLOW_FOLDER / "dags" / "config"
        with open(path / "config.yaml") as f:
            self.raw_config = yaml.safe_load(f)
        with open(layer_properties_file) as f:
            self.layer_properties = json.load(f)['layerProperties']
        self.country_config = dict()
        self.countries = []
        for country_config in os.listdir(path / "countries"):
            with open(path / "countries" / country_config) as f:
                country = country_config.split(".")[0]
                self.country_config[country] = yaml.safe_load(f)
                self.countries.append(country)

    def get_countries(self) -> List[str]:
        return self.countries

    def _get_country(self, country) -> FallbackDict:
        return FallbackDict(self.raw_config, self.country_config[country])

    def _get_name_output_file_generic(self, country: str, filename_field: FallbackDict) -> str:
        geo_extent = self.get_iso3(country).lower()
        file_name = self._name_output_file_generic(geo_extent=geo_extent, category=filename_field['category'],
                                                   theme=filename_field['theme'], geometry=filename_field['geometry'],
                                                   scale=filename_field['scale'], source=filename_field['source'],
                                                   suffix=filename_field['suffix'])
        return file_name

    def _name_output_file_generic(self, geo_extent: str, category: str, theme: str, geometry: str, scale: str,
                                  source: str, suffix: str, permission: str = 'pp',
                                  free_text: str = 'pipeline_generated') -> str:
        file_name = f"{geo_extent}_{category}_{theme}_{geometry}_{scale}_{source}_{permission}"
        if free_text is not None:
            file_name += f"_{free_text}"
        file_name += f'.{suffix}'
        return file_name

    def _get_processed_filename(self, country: str, filename_field: FallbackDict) -> Path:
        filename = self._get_name_output_file_generic(country, filename_field)
        return Path(filename)

    def _get_processed_directory(self, country: str, artefact: str) -> Path:
        return Path(self._get_processed_data_directory(country)) / \
               Path(self._get_country(country)['cmf']['processed'][artefact])

    def _get_schema_mapping(self, column_name_map: FallbackDict, column_names: list) -> dict:
        return {column_name_map[column_name]: column_name
                for column_name in column_names
                if column_name_map[column_name] is not None}

    def _get_layer_property(self, filename_dict):
        matching_items = [item for item in self.layer_properties if
                          f"{filename_dict['category']}-{filename_dict['theme']}-" \
                          f"{filename_dict['geometry']}-{filename_dict['scale']}"
                          in item['name']]
        if len(matching_items) > 1:
            logger.warning(f"Multiple matching items in layer property for {filename_dict}: {matching_items}."
                           f"Taking the first one")
        return matching_items[0]

    def _get_schema_filename(self, filename_dict):
        return self._get_layer_property(filename_dict)["schema_definition"]

    def _get_adm(self, country: str, adm_number: int):
        return self._get_country(country=country)[f'adm{adm_number}']

    # HDX COD
    def _get_hdx(self, country: str, hdx_type) -> FallbackDict:
        return self._get_country(country=country)['hdx_cod'][hdx_type]

    def get_hdx_adm_address(self, country: str):
        return self._get_hdx(country=country, hdx_type='adm')['address']

    def get_hdx_adm_dataset_name(self, country: str):
        return self._get_hdx(country=country, hdx_type='adm')['filename']

    def get_hdx_adm_dataset_type(self, country: str):
        return self._get_hdx(country=country, hdx_type='adm')['file_type']

    def get_hdx_adm0_dataset_layer_name(self, country: str):
        return self._get_hdx(country=country, hdx_type='adm')['layer_name']['adm0']

    def get_hdx_adm1_dataset_layer_name(self, country: str):
        return self._get_hdx(country=country, hdx_type='adm')['layer_name']['adm1']

    def should_process_hdx_roads(self, country: str):
        return self._get_hdx(country=country, hdx_type="roads")["include"]

    def get_hdx_roads_address(self, country: str):
        return self._get_hdx(country=country, hdx_type='roads')['address']

    def get_hdx_roads_dataset_name(self, country: str):
        return self._get_hdx(country=country, hdx_type='roads')['filename']

    # OSM
    def _get_osm(self, country: str):
        return self._get_country(country=country)['osm']

    def get_osm_url(self, country: str):
        return self._get_osm(country=country)['url']

    def get_osm_roads_raw_osm(self, country: str):
        return os.path.join(self._get_raw_data_directory(country),
                            self._get_osm(country=country)['roads']['raw_osm']
                            .format(iso3=self.get_iso3(country=country).lower()))

    def get_osm_roads_raw_gpkg(self, country: str):
        return os.path.join(self._get_raw_data_directory(country),
                            self._get_osm(country=country)['roads']['raw_gpkg']
                            .format(iso3=self.get_iso3(country=country).lower()))

    def get_osm_roads_processed_filepath(self, country: str) -> str:
        filename_field = self._get_osm(country=country)['roads']['filename']
        filename = self._get_processed_filename(country, filename_field)
        directory = self._get_processed_directory(country, 'roads')
        return str(directory / filename)

    def get_osm_roads_tags_schema(self, country: str):
        # TODO: Not sure what this is
        return os.path.join(self._get_schema_directory(),
                            self._get_osm(country=country)['roads']['osm_tags'])

    # adm
    def get_adm0_schema(self, country: str):
        return os.path.join(self._get_schema_directory(),
                            self._get_schema_filename(
                                filename_dict=self._get_adm(country=country, adm_number=0)['cod']['filename']))

    def get_adm1_schema(self, country: str):
        return os.path.join(self._get_schema_directory(),
                            self._get_schema_filename(
                                filename_dict=self._get_adm(country=country, adm_number=1)['cod']['filename']))

    def get_adm_cod_raw_filename(self, country: str) -> str:
        return os.path.join(self._get_raw_data_directory(country),
                            self._get_country(country=country)['adm_cod_raw']
                            .format(iso3=self.get_iso3(country=country).lower()))

    def get_adm0_cod_processed_filepath(self, country: str) -> str:
        filename_field = self._get_adm(country=country, adm_number=0)['cod']['filename']
        filename = self._get_processed_filename(country, filename_field)
        directory = self._get_processed_directory(country=country, artefact='admin')
        return str(directory / filename)

    def get_adm1_cod_processed_filepath(self, country: str) -> str:
        filename_field = self._get_adm(country=country, adm_number=1)['cod']['filename']
        filename = self._get_processed_filename(country, filename_field)
        directory = self._get_processed_directory(country=country, artefact='admin')
        return str(directory / filename)

    # General
    def get_roads_schema(self):
        # TODO: This method is for roads in general but currently uses road COD filename
        return os.path.join(self._get_schema_directory(),
                            self._get_schema_filename(self._get_roads_cod()['filename']))

    def _get_roads_cod(self):
        return self.raw_config['roads']['cod']

    def get_roads_cod_raw_filename(self, country) -> str:
        return os.path.join(self._get_raw_data_directory(country),
                            self._get_roads_cod()['raw']
                            .format(iso3=self.get_iso3(country=country).lower()))

    def get_roads_cod_processed_filepath(self, country: str) -> str:
        filename_field = self._get_roads_cod()['filename']
        filename = self._get_processed_filename(country, filename_field)
        directory = self._get_processed_directory(country, 'roads')
        return str(directory / filename)

    def get_crs(self):
        return self.raw_config['constants']['crs']

    def get_gadm_layer_adm0(self):
        return 'gadm36_{ISO3}_0'

    def get_gadm_layer_adm1(self):
        return 'gadm36_{ISO3}_1'

    def get_geoboundaries_adm0_raw(self, country):
        return os.path.join(self._get_raw_data_directory(country),
                            self.raw_config['geoboundaries']['adm0']['raw'])

    def get_geoboundaries_adm1_raw(self, country):
        return os.path.join(self._get_raw_data_directory(country),
                            self.raw_config['geoboundaries']['adm1']['raw'])

    def get_iso3(self, country: str):
        return self._get_country(country)['constants']['ISO3']

    def get_iso2(self, country: str):
        return self._get_country(country)['constants']['ISO2']

    # Directories
    def _get_raw_data_directory(self, country):
        return self._DATA_FOLDER / country / \
            Path(self._get_country(country)['cmf']['top-level']) / \
            Path(self._get_country(country)['cmf']['original']['top-level'])

    def _get_processed_data_directory(self, country):
        return self._DATA_FOLDER / country / \
           Path(self._get_country(country)['cmf']['top-level']) / \
           Path(self._get_country(country)['cmf']['processed']['top-level'])

    def _get_schema_directory(self):
        return self._SCHEMAS_FOLDER

    # Schema mappings
    def get_adm0_schema_mapping(self, source: str, country: str) -> dict:
        return self._get_schema_mapping(
            column_name_map=self._get_adm(country=country, adm_number=0)[source]['column_names'],
            column_names=['name_en', 'pcode'])

    def get_adm1_schema_mapping(self, source: str, country: str) -> dict:
        return self._get_schema_mapping(
            column_name_map=self._get_adm(country=country, adm_number=1)[source]['column_names'],
            column_names=['name_en', 'pcode', 'par_pcode'])

    def get_roads_schema_mapping(self, source: str, country: str) -> dict:
        if source == 'osm':
            column_name_map = self._get_osm(country=country)['roads']['column_names']
        elif source == 'cod':
            column_name_map = self._get_roads_cod()['column_names']
        return self._get_schema_mapping(column_name_map=column_name_map,
                                        column_names=['name_en', 'name_loc', 'fclass'])


config = Config()