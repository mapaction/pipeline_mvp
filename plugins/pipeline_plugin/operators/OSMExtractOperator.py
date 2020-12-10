from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.extract.osm_overpass import extract_osm_query


class OSMExtractOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            osm_url,
            country_iso2,
            schema_filename,
            osm_output_filename,
            gpkg_output_filename,
            *args, **kwargs) -> None:
        super().__init__(python_callable=self.retrieve_osm_data,
                         op_kwargs={"osm_url": osm_url,
                                    "country_iso2": country_iso2,
                                    "schema_filename": schema_filename,
                                    "osm_output_filename": osm_output_filename,
                                    "gpkg_output_filename": gpkg_output_filename},
                         *args, **kwargs)

    def retrieve_osm_data(self,
                          osm_url,
                          country_iso2,
                          schema_filename,
                          osm_output_filename,
                          gpkg_output_filename):
        extract_osm_query(
            osm_url=osm_url,
            country_iso2=country_iso2,
            schema_filename=schema_filename,
            osm_output_filename=osm_output_filename,
            gpkg_output_filename=gpkg_output_filename,
        )
