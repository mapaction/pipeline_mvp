from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform.roads_transform import transform


class OSMRoadsTransformOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            source,
            input_filename,
            output_filename,
            crs,
            schema_mapping,
            *args, **kwargs) -> None:
        super().__init__(python_callable=self.transform_roads,
                         op_kwargs={"source": source,
                                    "input_filename": input_filename,
                                    "output_filename": output_filename,
                                    "crs": crs,
                                    "schema_mapping": schema_mapping},
                         *args, **kwargs)

    def transform_roads(self, source, input_filename, output_filename, crs, schema_mapping):
        transform(
            source=source,
            input_filename=input_filename,
            output_filename=output_filename,
            crs=crs,
            schema_mapping=schema_mapping
        )
