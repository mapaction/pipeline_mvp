from airflow.utils.decorators import apply_defaults
from airflow_logic.operators.BaseMapActionOperator import MapActionOperator


class DefaultTransformOperator(MapActionOperator):
    @apply_defaults
    def __init__(
        self,
        source,
        input_filename,
        output_filename,
        crs,
        schema_mapping,
        transform_method,
        *args,
        **kwargs
    ) -> None:
        super().__init__(
            method=transform_method,
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
