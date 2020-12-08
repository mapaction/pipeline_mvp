import os
import yaml
from pycountry import countries


class Config:
    def __init__(self):
        with open(os.path.join(os.getcwd(), "dags", "config", "config.yaml")) as f:
            self.raw_config = yaml.safe_load(f)

        self.hdx_adm = 'adm'
        self.hdx_roads = 'roads'
        self.hdx_river = 'river'
        self.hdx_seaport = 'seaport'

    def name_output_file_generic(self, geo_extent, category, theme, geometry, scale, source, permission, free_text=None):
        file_name = f"{geo_extent}_{category}_{theme}_{geometry}_{scale}_{source}_{permission}"
        if free_text:
            file_name += f"_{free_text}"
        return file_name

    def _get_country(self, country: str):
        return self.raw_config['countries'][countries.lookup(country).name.lower()]

    def get_hdx(self, country: str, hdx_type):
        return self._get_country(country)['hdx_cod'][hdx_type]

    def get_crs(self):
        return self.raw_config['constants']['crs']

