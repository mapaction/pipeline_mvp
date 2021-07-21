import os
from pathlib import Path
from typing import List

import yaml

from utils.fallback_dict import FallbackDict


class Config:
    def __init__(self, path=None):
        if os.environ.get("GCP") == "TRUE":
            self._MAIN_AIRFLOW_FOLDER = Path(os.getcwd()) / "gcs"
            self._DATA_FOLDER = Path("data")
            self._SCHEMAS_FOLDER = (
                Path("/") / "usr" / "src" / "pipeline_plugin" / "schemas"
            )
        else:
            self._MAIN_AIRFLOW_FOLDER = Path(os.getcwd())
            self._DATA_FOLDER = Path("/") / "opt" / "data"
            self._SCHEMAS_FOLDER = (
                self._MAIN_AIRFLOW_FOLDER / "plugins" / "pipeline_plugin" / "schemas"
            )
        if not path:
            path = self._MAIN_AIRFLOW_FOLDER / "dags" / "country_config"
        with open(path / "config.yaml") as f:
            self.raw_config = yaml.safe_load(f)
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

    def _get_name_output_file_generic(
        self, country: str, filename_field: FallbackDict
    ) -> str:
        geo_extent = self.get_iso3(country).lower()
        file_name = self._name_output_file_generic(
            geo_extent=geo_extent,
            category=filename_field["category"],
            theme=filename_field["theme"],
            geometry=filename_field["geometry"],
            scale=filename_field["scale"],
            source=filename_field["source"],
            suffix=filename_field["suffix"],
        )
        return file_name

    def _name_output_file_generic(
        self,
        geo_extent: str,
        category: str,
        theme: str,
        geometry: str,
        scale: str,
        source: str,
        suffix: str,
        permission: str = "pp",
        free_text: str = "pipeline_generated",
    ) -> str:
        file_name = (
            f"{geo_extent}_{category}_{theme}_{geometry}_{scale}_{source}_{permission}"
        )
        if free_text is not None:
            file_name += f"_{free_text}"
        file_name += f".{suffix}"
        return file_name

    def _get_processed_filename(
        self, country: str, filename_field: FallbackDict
    ) -> Path:
        filename = self._get_name_output_file_generic(country, filename_field)
        return Path(filename)

    def _get_processed_directory(self, country: str, artefact: str) -> Path:
        return Path(self._get_processed_data_directory(country)) / Path(
            self._get_country(country)["cmf"]["processed"][artefact]
        )

    def _get_schema_mapping(
        self, column_name_map: FallbackDict, column_names: list
    ) -> dict:
        return {
            column_name_map[column_name]: column_name
            for column_name in column_names
            if column_name_map[column_name] is not None
        }

    # HDX COD
    def _get_hdx(self, country: str, hdx_type) -> FallbackDict:
        return self._get_country(country=country)["hdx_cod"][hdx_type]

    def get_hdx_address(self, country: str, hdx_type: str):
        return self._get_hdx(country=country, hdx_type=hdx_type)["address"]

    def get_hdx_dataset_name(self, country: str, hdx_type: str):
        return self._get_hdx(country=country, hdx_type=hdx_type)["filename"]

    def get_hdx_dataset_type(self, country: str, hdx_type: str):
        return self._get_hdx(country=country, hdx_type=hdx_type)["file_type"]

    def get_hdx_adm_dataset_layer_name(self, country: str, adm_level: str):
        return self._get_hdx(country=country, hdx_type="adm")["layer_name"][adm_level]

    def should_process_hdx_roads(self, country: str):
        return self._get_hdx(country=country, hdx_type="roads")["include"]

    def get_cod_raw_filename(self, country: str, datatype: str) -> str:
        return os.path.join(
            self._get_raw_data_directory(country),
            self._get_country(country=country)[datatype].format(
                iso3=self.get_iso3(country=country).lower()
            ),
        )

    # OSM
    def _get_osm(self, country: str):
        return self._get_country(country=country)["osm"]

    def get_osm_url(self, country: str):
        return self._get_osm(country=country)["url"]

    def get_raw_osm_data_path(
        self, country: str, dataset_name: str, format: str = "raw_osm"
    ):
        """
        Get filename of osm raw datafile.
        :param country: desired country.
        :param dataset_name: desired data artefact: 'rail', 'roads', 'seaports', etc.
        :param format: 'raw_osm' or 'raw_gpkg'
        :return:
        """
        return os.path.join(
            self._get_raw_data_directory(country),
            self._get_osm(country=country)[dataset_name][format].format(
                iso3=self.get_iso3(country=country).lower()
            ),
        )

    def get_osm_processed_filepath(self, country: str, dataset_name: str) -> str:
        filename_field = self._get_osm(country=country)[dataset_name]["filename"]
        filename = self._get_processed_filename(country, filename_field)
        directory = self._get_processed_directory(country, dataset_name)
        return str(directory / filename)

    def get_osm_query_schema(self, country: str, dataset_name: str):
        return os.path.join(
            self._get_overpass_query_schema_directory(),
            self._get_osm(country=country)[dataset_name]["osm_tags"],
        )

    # adm
    def get_hdx_output_schema(self, country: str, datatype: str):
        return os.path.join(
            self._get_hdx_output_schema_directory(),
            self._get_country(country=country)[datatype]["schema"],
        )

    def get_cod_processed_filepath(self, country: str, datatype: str) -> str:
        filename_field = self._get_country(country=country)[datatype]["cod"]["filename"]
        filename = self._get_processed_filename(country, filename_field)
        directory = self._get_processed_directory(country=country, artefact=datatype)
        return str(directory / filename)

    # General
    def get_roads_schema(self):
        return os.path.join(
            self._get_schema_directory(), self.raw_config["roads"]["schema"]
        )

    # def _get_roads_cod(self):
    #     return self.raw_config["roads"]["cod"]

    def get_crs(self):
        return self.raw_config["constants"]["crs"]

    def get_gadm_layer(self, datatype: str):
        return self.raw_config["gadm_layer"][datatype]

    def get_geoboundaries_raw(self, country: str, datatype: str):
        return os.path.join(
            self._get_raw_data_directory(country),
            self.raw_config["geoboundaries"][datatype]["raw"],
        )

    def get_iso3(self, country: str):
        return self._get_country(country)["constants"]["ISO3"]

    def get_iso2(self, country: str):
        return self._get_country(country)["constants"]["ISO2"]

    # Directories
    def _get_raw_data_directory(self, country):
        return (
            self._DATA_FOLDER
            / country
            / Path(self._get_country(country)["cmf"]["top-level"])
            / Path(self._get_country(country)["cmf"]["original"]["top-level"])
        )

    def _get_processed_data_directory(self, country):
        return (
            self._DATA_FOLDER
            / country
            / Path(self._get_country(country)["cmf"]["top-level"])
            / Path(self._get_country(country)["cmf"]["processed"]["top-level"])
        )

    def _get_schema_directory(self):
        return self._SCHEMAS_FOLDER

    def _get_hdx_output_schema_directory(self):
        return self._get_schema_directory() / "hdx_output_format"

    def _get_overpass_query_schema_directory(self):
        return self._get_schema_directory() / "overpass_queries"

    # Schema mappings
    def get_schema_mapping(self, source: str, country: str, dataset_name: str) -> dict:
        if source == "osm":
            column_name_map = self._get_osm(country=country)[dataset_name][
                "column_names"
            ]
            column_names = ["name_en", "name_loc", "fclass"]
        elif source == "cod":
            if dataset_name in ("roads",):
                column_name_map = self.raw_config[dataset_name]["cod"][
                    "column_names"
                ]  # TODO: use fallback dict
                column_names = ["name_en", "name_loc", "fclass"]
            elif dataset_name == "adm0":
                column_name_map = self._get_country(country=country)["adm0"][source][
                    "column_names"
                ]
                column_names = ["ADM0_EN", "ADM0_PCODE"]
            elif dataset_name == "adm1":
                column_name_map = self._get_country(country=country)["adm1"][source][
                    "column_names"
                ]
                column_names = ["ADM1_EN", "ADM1_PCODE", "par_pcode"]
            elif dataset_name == "adm2":
                column_name_map = self._get_country(country=country)["adm2"][source][
                    "column_names"
                ]
                column_names = ["ADM2_EN", "ADM2_PCODE", "par_pcode"]
            elif dataset_name == "adm3":
                column_name_map = self._get_country(country=country)["adm3"][source][
                    "column_names"
                ]
                column_names = ["ADM3_EN", "ADM3_PCODE", "par_pcode"]
        return self._get_schema_mapping(
            column_name_map=column_name_map, column_names=column_names
        )


config = Config()
