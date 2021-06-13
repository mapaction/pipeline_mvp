from airflow.utils.decorators import apply_defaults

from pipeline_plugin.operators.BaseMapActionOperator import MapActionOperator
from pipeline_plugin.transform.rail_transform import transform


class OSMRailTransformOperator(MapActionOperator):
    @apply_defaults
    def __init__(
        self,
        source,
        input_filename,
        output_filename,
        crs,
        schema_mapping,
        *args,
        **kwargs
    ) -> None:
        super().__init__(
            method=transform,
            arguments={
                "source": source,
                "input_filename": input_filename,
                "output_filename": output_filename,
                "crs": crs,
                "schema_mapping": schema_mapping,
            },
            *args,
            **kwargs
        )
