import os
import yaml
from pycountry import countries


class Config:
    def __init__(self, path=None):
        if not path:
            path = os.path.join(os.getcwd(), "dags", "config")
        with open(os.path.join(path, "config.yaml")) as f:
            self.raw_config = yaml.safe_load(f)

    def name_output_file_generic(self, geo_extent, category, theme, geometry, scale, source, permission,
                                 free_text=None):
        file_name = f"{geo_extent}_{category}_{theme}_{geometry}_{scale}_{source}_{permission}"
        if free_text:
            file_name += f"_{free_text}"
        return file_name

    def _get_country_config(self, country: str) -> dict:
        return self.raw_config['countries'][countries.lookup(country).name.lower()]

    # HDX COD
    def _get_hdx(self, country: str, hdx_type) -> dict:
        return self._get_country_config(country)['hdx_cod'][hdx_type]

    def get_hdx_adm_address(self, country: str):
        return self._get_hdx(country, hdx_type='adm')['address']

    def get_hdx_adm_filename(self, country: str):
        return self._get_hdx(country, hdx_type='adm')['filename']

    def get_hdx_roads_address(self, country: str):
        return self._get_hdx(country, hdx_type='roads')['address']

    def get_hdx_roads_filename(self, country: str):
        return self._get_hdx(country, hdx_type='roads')['filename']

    # OSM
    def _get_osm(self, country: str):
        return self._get_country_config(country)['osm']

    def get_osm_url(self, country: str):
        return self._get_osm(country)['url']

    def get_osm_roads_raw_osm(self, country: str):
        return os.path.join(self.get_dir_raw_data(),
                            self._get_osm(country)['roads']['raw_osm'])

    def get_osm_roads_raw_gpkg(self, country: str):
        return os.path.join(self.get_schema_directory(),
                            self._get_osm(country)['roads']['raw_gpkg'])

    def get_osm_roads_processed_filename(self, country: str):
        return os.path.join(self.get_dir_processed_data(),
                            self._get_osm(country)['roads']['processed'])

    def get_osm_roads_tags_schema(self, country: str):
        return os.path.join(self.get_schema_directory(),
                            self._get_osm(country)['roads']['osm_tags'])

    def get_roads_schema(self):
        return os.path.join(self.get_schema_directory(),
                            self.raw_config['roads']['schema'])

    def get_crs(self):
        return self.raw_config['constants']['crs']

    def get_gadm_layer_adm0(self):
        return 'gadm36_{ISO3}_0'

    def get_gadm_layer_adm1(self):
        return 'gadm36_{ISO3}_1'

    def get_geoboundaries_adm0_raw(self):
        return self.raw_config['geoboundaries']['adm0']['raw']

    def get_geoboundaries_adm1_raw(self):
        return self.raw_config['geoboundaries']['adm1']['raw']

    def get_iso3(self, country: str):
        return countries.lookup(country).alpha_3

    def get_iso2(self, country: str):
        return countries.lookup(country).alpha_2

    # Directories
    def get_dir_raw_data(self):
        return "/opt/data/test"

    def get_dir_processed_data(self):
        return "/opt/data/test/"

    def get_schema_directory(self):
        return "/usr/local/airflow/plugins/pipeline_plugin/schemas/"

    # Schemas
    # Schema mapping from adm0 transform
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

    # Schema mapping from adm1 transform
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
