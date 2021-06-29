from airflow.plugins_manager import AirflowPlugin

from pipeline_plugin.operators.HDXAdm0TransformOperator import HDXAdm0TransformOperator
from pipeline_plugin.operators.HDXAdm1TransformOperator import HDXAdm1TransformOperator
from pipeline_plugin.operators.HDXExtractOperator import HDXExtractOperator
from pipeline_plugin.operators.HDXRoadsTransformOperator import (
    HDXRoadsTransformOperator,
)
from pipeline_plugin.operators.OSMExtractOperator import OSMExtractOperator
from pipeline_plugin.operators.OSMRailTransformOperator import OSMRailTransformOperator
from pipeline_plugin.operators.OSMRoadsTransformOperator import (
    OSMRoadsTransformOperator,
)


class PipelinePlugin(AirflowPlugin):
    name = "pipeline_plugin"  # does not need to match the package name
    operators = [
        HDXExtractOperator,
        HDXAdm0TransformOperator,
        HDXAdm1TransformOperator,
        HDXRoadsTransformOperator,
        OSMExtractOperator,
        OSMRoadsTransformOperator,
        OSMRailTransformOperator,
    ]
    sensors = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
    appbuilder_views = []
    appbuilder_menu_items = []
    global_operator_extra_links = []
    operator_extra_links = []
