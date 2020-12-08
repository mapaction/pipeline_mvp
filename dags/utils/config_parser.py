import os
import yaml
from pycountry import countries


class Config:
    def __init__(self):
        with open(os.path.join(os.getcwd(), "dags", "config", "config.yaml")) as f:
            self.raw_config = yaml.safe_load(f)

    def name_output_file_generic(self, geo_extent, category, theme, geometry, scale, source, permission,
                                 free_text=None):
        file_name = f"{geo_extent}_{category}_{theme}_{geometry}_{scale}_{source}_{permission}"
        if free_text:
            file_name += f"_{free_text}"
        return file_name

    def _get_country_config(self, country: str) -> dict:
        return self.raw_config['countries'][countries.lookup(country).name.lower()]

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

    def get_crs(self):
        return self.raw_config['constants']['crs']

    def get_dir_raw_data(self):
        return self.raw_config['dirs']['raw_data']

    def get_geoboundaries_adm0_raw(self):
        return self.raw_config['geoboundaries']['adm0']['raw']

    def get_iso3(self, country: str):
        return countries.lookup(country).alpha_3

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
