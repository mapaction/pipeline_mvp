from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.extract.hdx_load import get_dataset_from_hdx


class HDXExtractOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            config,
            hdx_type,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=self.retrieve_hdx_data,
                         op_kwargs={"country": country, 'config': config, 'hdx_type': hdx_type}, *args, **kwargs)

    def retrieve_hdx_data(self, country, config, hdx_type, **kwargs):
        hdx_adm_config = config.get_hdx(country=country, hdx_type=hdx_type)
        print(f"Country: {country}")
        print('hdx address from config', hdx_adm_config)
        get_dataset_from_hdx(hdx_address=hdx_adm_config['address'],
                             dataset_name=hdx_adm_config['filename'],
                             save_directory="test")
