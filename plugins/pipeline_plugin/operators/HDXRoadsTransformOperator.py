from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform.hdx_road import transform


class HDXRoadsTransformOperator(PythonOperator):
    @apply_defaults
    def __init__(self, input_filename, schema_filename, output_filename, schema_mapping, crs, *args, **kwargs) -> None:
        super().__init__(python_callable=self.transform_roads,
                         op_kwargs={"input_filename": input_filename,
                                    "schema_filename": schema_filename,
                                    "output_filename": output_filename,
                                    "schema_mapping": schema_mapping,
                                    "crs": crs},
                         *args, **kwargs)

    def transform_roads(self, input_filename, schema_filename, output_filename, schema_mapping, crs):
        transform(input_filename=input_filename,
                  schema_filename=schema_filename,
                  output_filename=output_filename,
                  schema_mapping=schema_mapping,
                  crs=crs)
