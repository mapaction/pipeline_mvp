from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults
from pathlib import Path
from pipeline_plugin.utils.CloudStorageClient import GoogleCloudStorageClient
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
        client = GoogleCloudStorageClient()
        client.get_file_from_gcs(
            bucket_name="europe-west2-mapaction-deve-8c266b1d-bucket",
            gcs_filename=f"data/source_folder/{Path(input_filename).name}",
            output_filename=input_filename
        )
        transform(source=source,
                  input_filename=input_filename,
                  output_filename=output_filename,
                  schema_mapping=schema_mapping,
                  crs=crs)
