from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.transform import hdx_adm_transform


class HDXAdm1Operator(PythonOperator):
    @apply_defaults
    def __init__(self,
                 source,
                 adm_level,
                 input_filename,
                 schema_filename,
                 output_filename,
                 iso3,
                 raw_data_dir,
                 geoboundaries_adm1_raw,
                 schema_mapping,
                 crs,
                 gadm_layer,
                 *args, **kwargs) -> None:
        super().__init__(python_callable=self.transform_adm1,
                         op_kwargs={"source": source,
                                    "adm_level": adm_level,
                                    "input_filename": input_filename,
                                    "schema_filename": schema_filename,
                                    "output_filename": output_filename,
                                    "iso3": iso3,
                                    "raw_data_dir": raw_data_dir,
                                    "geoboundaries_adm1_raw": geoboundaries_adm1_raw,
                                    "schema_mapping": schema_mapping,
                                    "crs": crs,
                                    "gadm_layer": gadm_layer},
                         *args, **kwargs)

    def transform_adm1(self,
                       source,
                       adm_level,
                       input_filename,
                       schema_filename,
                       output_filename,
                       iso3,
                       raw_data_dir,
                       geoboundaries_adm1_raw,
                       schema_mapping,
                       crs,
                       gadm_layer,
                       *args, **kwargs):
        hdx_adm_transform.transform(source=source,
                                    adm_level=adm_level,
                                    input_filename=input_filename,
                                    schema_filename=schema_filename,
                                    output_filename=output_filename,
                                    iso3=iso3,
                                    raw_data_dir=raw_data_dir,
                                    geoboundaries_adm_raw=geoboundaries_adm1_raw,
                                    schema_mapping=schema_mapping,
                                    crs=crs,
                                    gadm_layer=gadm_layer)
