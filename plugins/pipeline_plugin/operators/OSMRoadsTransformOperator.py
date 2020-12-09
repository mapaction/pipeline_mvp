from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform.osm_roads import transform


class OSMRoadsTransformOperator(PythonOperator):
    @apply_defaults
    def __init__(
            self,
            source,
            input_filename,
            schema_filename,
            output_filename,
            crs,
            *args, **kwargs) -> None:
        super().__init__(python_callable=self.transform_roads,
                         op_kwargs={"source": source, "input_filename": input_filename,
                                    "schema_filename": schema_filename, "output_filename": output_filename, "crs": crs},
                         *args, **kwargs)

    def transform_roads(self, source, input_filename, schema_filename, output_filename, crs, **kwargs):
        transform(
            source=source,
            input_filename=input_filename,
            schema_filename=schema_filename,
            output_filename=output_filename,
            crs=crs
        )
