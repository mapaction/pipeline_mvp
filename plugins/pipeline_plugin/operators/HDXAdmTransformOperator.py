from airflow.utils.decorators import apply_defaults

from pipeline_plugin.operators.BaseMapActionOperator import MapActionOperator
from pipeline_plugin.transform.admn_transform import transform


class HDXAdmTransformOperator(MapActionOperator):
    @apply_defaults
    def __init__(
        self,
        source,
        adm_level,
        input_filename,
        input_file_type,
        input_layer_name,
        output_schema_filename,
        output_filename,
        iso3,
        source_geoboundaries,
        schema_mapping,
        crs,
        gadm_layer,
        *args,
        **kwargs
    ) -> None:
        super().__init__(
            method=transform,
            arguments={
                "source": source,
                "adm_level": adm_level,
                "input_filename": input_filename,
                "input_file_type": input_file_type,
                "input_layer_name": input_layer_name,
                "output_schema_filename": output_schema_filename,
                "output_filename": output_filename,
                "iso3": iso3,
                "source_geoboundaries": source_geoboundaries,
                "schema_mapping": schema_mapping,
                "crs": crs,
                "gadm_layer": gadm_layer,
            },
            *args,
            **kwargs
        )
