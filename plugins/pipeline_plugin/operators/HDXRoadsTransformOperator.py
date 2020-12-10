from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform.roads_transform import transform


class HDXRoadsTransformOperator(PythonOperator):
    @apply_defaults
    def __init__(self, source, input_filename, output_filename, schema_mapping, crs, *args, **kwargs) -> None:
        super().__init__(python_callable=self.transform_roads,
                         op_kwargs={"source": source,
                                    "input_filename": input_filename,
                                    "output_filename": output_filename,
                                    "schema_mapping": schema_mapping,
                                    "crs": crs},
                         *args, **kwargs)

    def transform_roads(self, source, input_filename, output_filename, schema_mapping, crs):
        transform(source=source,
                  input_filename=input_filename,
                  output_filename=output_filename,
                  schema_mapping=schema_mapping,
                  crs=crs)
