from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.extract.hdx_load import get_dataset_from_hdx


class HDXExtractOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            hdx_address,
            hdx_filename,
            save_directory,
            *args, **kwargs) -> None:
        super().__init__(python_callable=self.retrieve_hdx_data,
                         op_kwargs={'hdx_address': hdx_address,
                                    'hdx_filename': hdx_filename,
                                    "save_directory": save_directory},
                         *args, **kwargs)

    def retrieve_hdx_data(self, hdx_address, hdx_filename, save_directory, **kwargs):
        get_dataset_from_hdx(hdx_address=hdx_address, dataset_name=hdx_filename, save_directory=save_directory)
