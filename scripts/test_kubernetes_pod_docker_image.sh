# docker run  -e FUNCTION_MODULE="extract.hdx_load" \
#             -e FUNCTION_NAME="get_dataset_from_hdx" \
#             -e FUNCTION_ARGUMENTS="{\"hdx_address\":\"yemen-admin-boundaries\", \"dataset_name\":\"yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip\", \"output_filename\":\"/opt/data/cod_roads.zip\"}" \
#             -e GCP="TRUE" \
#             -e ENVIRONMENT="DEVELOP" \
#             eu.gcr.io/datapipeline-295515/mapaction-cloudcomposer-kubernetes-image

docker run  -e FUNCTION_MODULE="extract.osm_overpass" \
            -e FUNCTION_NAME="extract_osm_query" \
            -e FUNCTION_ARGUMENTS="{\"\
            osm_url\":\"http://overpass-api.de/api/interpreter?\", \"\
            country_iso2\":\"YE\", \"\
            schema_filename\":\"/usr/src/pipeline_plugin/schemas/osm_tags_roads.yml\", \"\
            osm_output_filename\":\"/opt/data/osm_roads.xml\", \"\
            gpkg_output_filename\":\"/opt/data/osm_roads.gpkg\"}" \
            -e GCP="TRUE" \
            -e ENVIRONMENT="DEVELOP" \
            eu.gcr.io/datapipeline-295515/mapaction-cloudcomposer-kubernetes-image
