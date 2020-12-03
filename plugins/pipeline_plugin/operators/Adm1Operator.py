from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform.adm0 import transform


def print_custom(country, **kwargs):
    print(f"COUNTRY v2.0: {country}")
    transform(source="cod",
              input_filename="/opt/data/test/yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip",
              schema_filename="/usr/local/airflow/plugins/pipeline_plugin/schemas/admin1_affected_area_py.yml",
              output_filename="/opt/data/test/yem_adm1_processed.zip")


class Adm1Operator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            config,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=print_custom, op_kwargs={"country": country}, *args, **kwargs)
