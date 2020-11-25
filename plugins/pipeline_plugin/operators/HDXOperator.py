from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.extract.hdx_load import get_dataset_from_hdx


def print_custom(country, **kwargs):
    print(f"COUNTRY v2.0: {country}")
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
        super().__init__(python_callable=print_custom, op_kwargs={"country": country}, *args, **kwargs)
