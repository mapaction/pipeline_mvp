from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.extract.osm_overpass import extract_osm_query


class OSMExtractOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            config,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=self.retrieve_osm_data,
                         op_kwargs={"country": country, 'config': config}, *args, **kwargs)

    def retrieve_osm_data(self, country, config, **kwargs):
        print(f"Country: {country}")
        extract_osm_query(
            country=country,
            config=config,
            osm_url=config.get_osm_url(country=country),
            country_iso2=config.get_iso2(country=country),
            schema_directory=config.get_schema_directory(),
            schema_filename=config.get_osm_roads_tags(country=country),
            osm_output_filename=config.get_osm_roads_raw_osm(country=country),
            gpkg_output_filename=config.get_osm_roads_raw_gpkg(country=country),
            save_directory="/opt/data/test"
        )
