from airflow_logic.operators.DefaultTransformOperator import DefaultTransformOperator
from airflow_logic.operators.HDXAdmTransformOperator import  HDXAdmTransformOperator
from airflow_logic.operators.HDXExtractOperator import HDXExtractOperator

from map_action_logic.transform.default_transform import default_transform


def fill_hdx_roads_dag(dag, config, country):
    if config.should_process_hdx_roads(country):
        hdx_roads_extract = HDXExtractOperator(
            task_id=f"{country}_hdx_roads_extract",
            hdx_address=config.get_hdx_address(country=country, hdx_type="roads"),
            hdx_filename=config.get_hdx_dataset_name(country=country, hdx_type="roads"),
            output_filename=config.get_cod_raw_filename(
                country=country, datatype="roads_cod_raw"
            ),
            dag=dag,
        )
        source = "cod"
        roads_transform = DefaultTransformOperator(
            task_id=f"{country}_hdx_roads_transform",
            source=source,
            input_filename=config.get_cod_raw_filename(
                country=country, datatype="roads_cod_raw"
            ),
            output_filename=config.get_cod_processed_filepath(
                country=country, datatype="roads"
            ),
            crs=config.get_crs(),
            schema_mapping=config.get_schema_mapping(
                source=source, country=country, dataset_name="roads"
            ),
            transform_method=default_transform,
            dag=dag,
        )

        hdx_roads_extract >> roads_transform


def fill_hdx_adm_dag(dag, config, country):
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
    adm0_transform = HDXAdmTransformOperator(
        task_id=f"{country}_hdx_adm0_transform",
        source=source,
        adm_level="adm0",
        input_filename=config.get_cod_raw_filename(
            country=country, datatype="adm_cod_raw"
        ),
        input_file_type=config.get_hdx_dataset_type(country=country, hdx_type="adm"),
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

    adm1_transform = HDXAdmTransformOperator(
        task_id=f"{country}_hdx_adm1_transform",
        source=source,
        adm_level="adm1",
        input_filename=config.get_cod_raw_filename(
            country=country, datatype="adm_cod_raw"
        ),
        input_file_type=config.get_hdx_dataset_type(country=country, hdx_type="adm"),
        input_layer_name=config.get_hdx_adm_dataset_layer_name(
            country=country, adm_level="adm1"
        ),
        output_schema_filename=config.get_hdx_output_schema(
            country=country, datatype="adm1"
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

    adm2_transform = HDXAdmTransformOperator(
        task_id=f"{country}_hdx_adm2_transform",
        source=source,
        adm_level="adm2",
        input_filename=config.get_cod_raw_filename(
            country=country, datatype="adm_cod_raw"
        ),
        input_file_type=config.get_hdx_dataset_type(country=country, hdx_type="adm"),
        input_layer_name=config.get_hdx_adm_dataset_layer_name(
            country=country, adm_level="adm2"
        ),
        output_schema_filename=config.get_hdx_output_schema(
            country=country, datatype="adm2"
        ),
        output_filename=config.get_cod_processed_filepath(
            country=country, datatype="adm2"
        ),
        iso3=config.get_iso3(country=country),
        source_geoboundaries=config.get_geoboundaries_raw(
            country=country, datatype="adm2"
        ),
        schema_mapping=config.get_schema_mapping(
            source=source, country=country, dataset_name="adm2"
        ),
        crs=config.get_crs(),
        gadm_layer=config.get_gadm_layer(datatype="adm2"),
        dag=dag,
    )

    adm3_transform = HDXAdmTransformOperator(
        task_id=f"{country}_hdx_adm3_transform",
        source=source,
        adm_level="adm3",
        input_filename=config.get_cod_raw_filename(
            country=country, datatype="adm_cod_raw"
        ),
        input_file_type=config.get_hdx_dataset_type(country=country, hdx_type="adm"),
        input_layer_name=config.get_hdx_adm_dataset_layer_name(
            country=country, adm_level="adm3"
        ),
        output_schema_filename=config.get_hdx_output_schema(
            country=country, datatype="adm3"
        ),
        output_filename=config.get_cod_processed_filepath(
            country=country, datatype="adm3"
        ),
        iso3=config.get_iso3(country=country),
        source_geoboundaries=config.get_geoboundaries_raw(
            country=country, datatype="adm3"
        ),
        schema_mapping=config.get_schema_mapping(
            source=source, country=country, dataset_name="adm3"
        ),
        crs=config.get_crs(),
        gadm_layer=config.get_gadm_layer(datatype="adm3"),
        dag=dag,
    )

    hdx_extract >> [adm0_transform, adm1_transform, adm2_transform, adm3_transform]
