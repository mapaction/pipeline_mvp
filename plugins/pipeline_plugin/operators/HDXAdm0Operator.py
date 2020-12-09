from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform import hdx_adm0


def transform_adm0(source: str, input_filename, schema_filename, output_filename, iso3, raw_data_dir,
                   geoboundaries_adm0_raw, schema_mapping, crs, *args, **kwargs):
    hdx_adm0.transform(source=source, input_filename=input_filename, schema_filename=schema_filename,
                       output_filename=output_filename, iso3=iso3, raw_data_dir=raw_data_dir,
                       geoboundaries_adm0_raw=geoboundaries_adm0_raw, schema_mapping=schema_mapping, crs=crs)


class HDXAdm0Operator(PythonOperator):
    @apply_defaults
    def __init__(self, source: str, input_filename, schema_filename, output_filename, iso3, raw_data_dir,
                 geoboundaries_adm0_raw, schema_mapping, crs, *args, **kwargs) -> None:
        super().__init__(python_callable=transform_adm0,
                         op_kwargs={"source": source, "input_filename": input_filename,
                                    "schema_filename": schema_filename,
                                    "output_filename": output_filename, "iso3": iso3,
                                    "raw_data_dir": raw_data_dir,
                                    "geoboundaries_adm0_raw": geoboundaries_adm0_raw,
                                    "schema_mapping": schema_mapping, "crs": crs, },
                         *args, **kwargs)

