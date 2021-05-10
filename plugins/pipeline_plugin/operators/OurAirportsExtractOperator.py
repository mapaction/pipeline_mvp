from airflow.utils.decorators import apply_defaults

from pipeline_plugin.operators.BaseMapActionOperator import MapActionOperator
from pipeline_plugin.extract.our_airports import get_our_airports

class HDXExtractOperator(MapActionOperator):
    @apply_defaults
    def __init__(
            self,
            iso3,
            base_uri,
            *args, **kwargs) -> None:
        super().__init__(method=get_dataset_from_hdx,
                         arguments={'iso3': hdx_address,
                                    'base_uri': hdx_filename,
                         *args, **kwargs)
