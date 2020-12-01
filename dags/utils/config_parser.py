import os
import yaml


class Config:
    def __init__(self):
        with open(os.path.join(os.getcwd(), "dags", "config", "config.yaml")) as f:
            self.raw_config = yaml.safe_load(f)

    def get_adm_url(self):
        return self.raw_config["adm0"]["gadm"]["url"]

    def name_adm_output_file(self, geo_extent, category, theme, geometry, scale, source, permission, free_text=None):
        file_name = f"{geo_extent}_{category}_{theme}_{geometry}_{scale}_{source}_{permission}"
        if free_text:
            file_name += f"_{free_text}"
        return file_name
