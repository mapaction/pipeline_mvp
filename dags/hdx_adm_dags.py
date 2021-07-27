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
            hdx_address=config.get_hdx_adm_address(country=country),
            hdx_filename=config.get_hdx_adm_dataset_name(country=country),
            output_filename=config.get_adm_cod_raw_filename(country=country),
            dag=dag,
        )

        source = "cod"
        adm0_transform = HDXAdm0TransformOperator(
            task_id=f"{country}_hdx_adm0_transform",
            source=source,
            adm_level="adm0",
            input_filename=config.get_adm_cod_raw_filename(country=country),
            input_file_type=config.get_hdx_adm_dataset_type(country=country),
            input_layer_name=config.get_hdx_adm0_dataset_layer_name(country=country),
            schema_filename=config.get_adm0_schema(country=country),
            output_filename=config.get_adm0_cod_processed_filepath(country=country),
            iso3=config.get_iso3(country=country),
            source_geoboundaries=config.get_geoboundaries_adm0_raw(country=country),
            schema_mapping=config.get_adm0_schema_mapping(
                source=source, country=country
            ),
            crs=config.get_crs(),
            gadm_layer=config.get_gadm_layer_adm0(),
            dag=dag,
        )

        adm1_transform = HDXAdm1TransformOperator(
            task_id=f"{country}_hdx_adm1_transform",
            source=source,
            adm_level="adm1",
            input_filename=config.get_adm_cod_raw_filename(country=country),
            input_file_type=config.get_hdx_adm_dataset_type(country=country),
            input_layer_name=config.get_hdx_adm1_dataset_layer_name(country=country),
            schema_filename=config.get_adm1_schema(country=country),
            output_filename=config.get_adm1_cod_processed_filepath(country=country),
            iso3=config.get_iso3(country=country),
            source_geoboundaries=config.get_geoboundaries_adm1_raw(country=country),
            schema_mapping=config.get_adm1_schema_mapping(
                source=source, country=country
            ),
            crs=config.get_crs(),
            gadm_layer=config.get_gadm_layer_adm1(),
            dag=dag,
        )

        hdx_extract >> [adm0_transform, adm1_transform]
