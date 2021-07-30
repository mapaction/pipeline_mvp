from airflow.utils.decorators import apply_defaults
from airflow_logic.operators.BaseMapActionOperator import MapActionOperator
from map_action_logic.extract.hdx_load import get_dataset_from_hdx


class HDXExtractOperator(MapActionOperator):
    @apply_defaults
    def __init__(
        self, hdx_address, hdx_filename, output_filename, *args, **kwargs
    ) -> None:
        super().__init__(
            method=get_dataset_from_hdx,
            arguments={
                "hdx_address": hdx_address,
                "dataset_name": hdx_filename,
                "output_filename": output_filename,
            },
            *args,
            **kwargs
        )
