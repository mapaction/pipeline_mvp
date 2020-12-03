from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform.road import transform


class RoadsTransformOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            country: str,
            config,
            *args, **kwargs) -> None:
        self.country = country
        super().__init__(python_callable=self.transform_roads, op_kwargs={"country": country}, *args, **kwargs)

    def transform_roads(self, country, **kwargs):
        print(f"COUNTRY v2.0: {country}")
        transform(input_filename="/opt/data/test/cod_roads.zip",
                  schema_filename="/usr/local/airflow/plugins/pipeline_plugin/schemas/roads_affected_area_py.yml",
                  output_filename="/opt/data/test/yem_tran_rds_ln_s1_ocha_pp.shp")
