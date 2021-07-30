from airflow.utils.decorators import apply_defaults
from airflow_logic.operators.BaseMapActionOperator import MapActionOperator

from pipeline_plugin.extract.osm_overpass import extract_osm_query


class OSMExtractOperator(MapActionOperator):
    @apply_defaults
    def __init__(
        self,
        osm_url,
        country_iso2,
        overpass_query_schema_filename,
        osm_output_filename,
        gpkg_output_filename,
        *args,
        **kwargs
    ) -> None:
        super().__init__(
            method=extract_osm_query,
            arguments={
                "osm_url": osm_url,
                "country_iso2": country_iso2,
                "overpass_query_schema_filename": overpass_query_schema_filename,
                "osm_output_filename": osm_output_filename,
                "gpkg_output_filename": gpkg_output_filename,
            },
            *args,
            **kwargs
        )
