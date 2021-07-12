from airflow import DAG

from airflow.operators.pipeline_plugin import (
    HDXAdm0TransformOperator,
    HDXAdm1TransformOperator,
    HDXExtractOperator,
)
from utils.config_parser import config
from utils.dag_configuration import (
    get_catchup,
    get_default_arguments,
    get_schedule_interval,
)

countries = config.get_countries()

# Defaults which can be overridden if needed
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

with DAG(
    "hdx_adm",
    schedule_interval=schedule_interval,
    catchup=catchup,
    default_args=default_args,
) as dag:
    for country in countries:
        hdx_extract = HDXExtractOperator(
            task_id=f"{country}_hdx_adm_extract",
            hdx_address=config.get_hdx_address(country=country, hdx_type="adm"),
            hdx_filename=config.get_hdx_dataset_name(country=country, hdx_type="adm"),
            output_filename=config.get_cod_raw_filename(
                country=country, datatype="adm_cod_raw"
            ),
            dag=dag,
        )

        source = "cod"
        adm0_transform = HDXAdm0TransformOperator(
            task_id=f"{country}_hdx_adm0_transform",
            source=source,
            adm_level="adm0",
            input_filename=config.get_cod_raw_filename(
                country=country, datatype="adm_cod_raw"
            ),
            input_file_type=config.get_hdx_dataset_type(
                country=country, hdx_type="adm"
            ),
            input_layer_name=config.get_hdx_adm_dataset_layer_name(
                country=country, adm_level="adm0"
            ),
            output_schema_filename=config.get_hdx_output_schema(
                country=country, datatype="adm0"
            ),
            output_filename=config.get_cod_processed_filepath(
                country=country, datatype="adm0"
            ),
            iso3=config.get_iso3(country=country),
            source_geoboundaries=config.get_geoboundaries_raw(
                country=country, datatype="adm0"
            ),
            schema_mapping=config.get_schema_mapping(
                source=source, country=country, dataset_name="adm0"
            ),
            crs=config.get_crs(),
            gadm_layer=config.get_gadm_layer(datatype="adm0"),
            dag=dag,
        )

        adm1_transform = HDXAdm1TransformOperator(
            task_id=f"{country}_hdx_adm1_transform",
            source=source,
            adm_level="adm1",
            input_filename=config.get_cod_raw_filename(
                country=country, datatype="adm_cod_raw"
            ),
            input_file_type=config.get_hdx_dataset_type(
                country=country, hdx_type="adm"
            ),
            input_layer_name=config.get_hdx_adm_dataset_layer_name(
                country=country, adm_level="adm1"
            ),
            output_schema_filename=config.get_hdx_output_schema(
                country=country, datatype="adm0"
            ),
            output_filename=config.get_cod_processed_filepath(
                country=country, datatype="adm1"
            ),
            iso3=config.get_iso3(country=country),
            source_geoboundaries=config.get_geoboundaries_raw(
                country=country, datatype="adm1"
            ),
            schema_mapping=config.get_schema_mapping(
                source=source, country=country, dataset_name="adm1"
            ),
            crs=config.get_crs(),
            gadm_layer=config.get_gadm_layer(datatype="adm1"),
            dag=dag,
        )

        hdx_extract >> [adm0_transform, adm1_transform]
