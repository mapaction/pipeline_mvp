import os
import yaml
from pathlib import Path

from pycountry import countries

from utils.fallback_dict import FallbackDict


class Config:
    def __init__(self, path=None):
        if os.environ.get("GCP") == "TRUE":
            self._MAIN_AIRFLOW_FOLDER = Path(os.getcwd()) / "gcs"
            self._DATA_FOLDER = Path(self._MAIN_AIRFLOW_FOLDER) / "data"
            self._SCHEMAS_FOLDER = Path("/") / "usr" / "src" / "pipeline_plugin" / "schemas"
        else:
            self._MAIN_AIRFLOW_FOLDER = Path(os.getcwd())
            self._DATA_FOLDER = Path("/") / "opt" / "data"
            self._SCHEMAS_FOLDER = self._MAIN_AIRFLOW_FOLDER / "plugins" / "pipeline_plugin" / "schemas"
        if not path:
            path = self._MAIN_AIRFLOW_FOLDER / "dags" / "config"
        with open(path / "config.yaml") as f:
            self.raw_config = yaml.safe_load(f)
        self.country_config = dict()
        for country_config in os.listdir(path / "countries"):
            with open(path / "countries" / country_config) as f:
                self.country_config[country_config.split(".")[0]] = yaml.safe_load(f)

    def _get_country(self, country) -> FallbackDict:
        return FallbackDict(self.raw_config, self.country_config[self._country_lower(country)])

    def _get_name_output_file_generic(self, country: str, filename_field: FallbackDict) -> str:
        geo_extent = self.get_iso3(country).lower()
        file_name = self._name_output_file_generic(geo_extent, filename_field['category'], filename_field['theme'],
                                                   filename_field['geometry'], filename_field['scale'],
                                                   filename_field['source'], filename_field['suffix'])
        return file_name

    def _name_output_file_generic(self, geo_extent: str, category: str, theme: str, geometry: str, scale: str,
                                  source: str, suffix: str, permission: str = 'pp', free_text: str = None) -> str:
        file_name = f"{geo_extent}_{category}_{theme}_{geometry}_{scale}_{source}_{permission}"
        if free_text is not None:
            file_name += f"_{free_text}"
        file_name += suffix
        return file_name

    def _country_lower(self, country: str) -> str:
        return countries.lookup(country).name.lower()

    def _get_adm(self, country: str, adm_number: int):
        return self._get_country(country=country)[f'adm{adm_number}']

    # HDX COD
    def _get_hdx(self, country: str, hdx_type) -> FallbackDict:
        return self._get_country(country=country)['hdx_cod'][hdx_type]

    def get_hdx_adm_address(self, country: str):
        return self._get_hdx(country=country, hdx_type='adm')['address']

    def get_hdx_adm_dataset_name(self, country: str):
        return self._get_hdx(country=country, hdx_type='adm')['filename']

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
        return os.path.join(self._get_raw_data_directory(),
                            self._get_osm(country=country)['roads']['raw_osm'])

    def get_osm_roads_raw_gpkg(self, country: str):
        return os.path.join(self._get_raw_data_directory(),
                            self._get_osm(country=country)['roads']['raw_gpkg'])

    def get_osm_roads_processed_filename(self, country: str):
        return os.path.join(self._get_processed_data_directory(),
                            self._get_osm(country=country)['roads']['processed'])

    def get_osm_roads_tags_schema(self, country: str):
        return os.path.join(self._get_schema_directory(),
                            self._get_osm(country=country)['roads']['osm_tags'])

    # adm
    def get_adm0_schema(self, country: str):
        return os.path.join(self._get_schema_directory(),
                            self._get_adm(country=country, adm_number=0)['schema'])

    def get_adm1_schema(self, country: str):
        return os.path.join(self._get_schema_directory(),
                            self._get_adm(country=country, adm_number=1)['schema'])

    def get_adm_cod_raw_filename(self, country: str):
        return os.path.join(self._get_raw_data_directory(),
                            self._get_country(country=country)['adm_cod_raw'])

    def get_adm0_cod_processed_filename(self, country: str):
        filename_field = self._get_adm(country=country, adm_number=0)['cod']['filename']
        filename = self._get_name_output_file_generic(country, filename_field)
        return os.path.join(self._get_processed_data_directory(), filename)

    def get_adm1_cod_processed_filename(self, country: str):
        return os.path.join(self._get_processed_data_directory(),
                            self._get_adm(country=country, adm_number=1)['cod']['processed'])

    # General
    def get_roads_schema(self):
        return os.path.join(self._get_schema_directory(),
                            self.raw_config['roads']['schema'])

    def _get_roads_cod(self):
        return self.raw_config['roads']['cod']

    def get_roads_cod_raw_filename(self):
        return os.path.join(self._get_raw_data_directory(),
                            self._get_roads_cod()['raw'])

    def get_roads_cod_processed_filename(self):
        return os.path.join(self._get_processed_data_directory(),
                            self._get_roads_cod()['processed'])

    def get_crs(self):
        return self.raw_config['constants']['crs']

    def get_gadm_layer_adm0(self):
        return 'gadm36_{ISO3}_0'

    def get_gadm_layer_adm1(self):
        return 'gadm36_{ISO3}_1'

    def get_geoboundaries_adm0_raw(self):
        return os.path.join(self._get_raw_data_directory(),
                            self.raw_config['geoboundaries']['adm0']['raw'])

    def get_geoboundaries_adm1_raw(self):
        return os.path.join(self._get_raw_data_directory(),
                            self.raw_config['geoboundaries']['adm1']['raw'])

    def get_iso3(self, country: str):
        return countries.lookup(country).alpha_3

    def get_iso2(self, country: str):
        return countries.lookup(country).alpha_2

    # Directories
    def _get_raw_data_directory(self):
        return self._DATA_FOLDER

    def _get_processed_data_directory(self):
        return self._DATA_FOLDER

    def _get_schema_directory(self):
        return self._SCHEMAS_FOLDER

    # Schema mappings
    def get_adm0_schema_mapping(self, source: str):
        schema_mapping = {}
        if source == 'cod':
            schema_mapping = {'admin0Name_en': 'name_en'}
        elif source == 'gadm':
            schema_mapping = {
                'NAME_0': 'name_en',
                'GID_0': 'pcode'
            }
        elif source == 'geoboundaries':
            schema_mapping = {'shapeName': 'name_en'}
        return schema_mapping

    def get_adm1_schema_mapping(self, source: str):
        schema_mapping = {}
        if source == 'cod':
            schema_mapping = {'admin1Name_en': 'name_en'}
        elif source == 'gadm':
            schema_mapping = {
                'NAME_1': 'name_en',
                'GID_1': 'pcode',
                'GID_0': 'par_pcode'
            }
        elif source == 'geoboundaries':
            schema_mapping = {'shapeName': 'name_en'}
        return schema_mapping

    def get_roads_schema_mapping(self, source: str):
        schema_mapping = {}
        if source == "hdx" or source == "cod":
            schema_mapping = {'TYPE': 'fclass'}
        elif source == "osm":
            schema_mapping = {
                'name:en': 'name_en',
                'name': 'name_loc',
                'highway': 'fclass'
            }
        return schema_mapping


config = Config()