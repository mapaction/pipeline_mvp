from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.extract.hdx_load import get_dataset_from_hdx


def retrieve_hdx_data(country, **kwargs):
    print(f"Country: {country}")
    get_dataset_from_hdx('yemen-admin-boundaries',
                         'yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip',
                         "test")

class HDXExtractOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=retrieve_hdx_data, op_kwargs={"country": country}, *args, **kwargs)
