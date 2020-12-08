from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.extract.hdx_load import get_dataset_from_hdx


class HDXExtractOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            config,
            hdx_address,
            hdx_filename,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=self.retrieve_hdx_data,
                         op_kwargs={"country": country, 'config': config, 'hdx_address': hdx_address,
                                    'hdx_filename': hdx_filename}, *args, **kwargs)

    def retrieve_hdx_data(self, country, config, hdx_address, hdx_filename, **kwargs):
        print(f"Country: {country}")
        get_dataset_from_hdx(hdx_address=hdx_address, dataset_name=hdx_filename, save_directory="test")