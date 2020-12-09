from airflow.plugins_manager import AirflowPlugin

from pipeline_plugin.operators.HDXExtractOperator import HDXExtractOperator
from pipeline_plugin.operators.HDXAdm0Operator import HDXAdm0Operator
from pipeline_plugin.operators.HDXAdm1Operator import HDXAdm1Operator
from pipeline_plugin.operators.HDXRoadsTransformOperator import HDXRoadsTransformOperator
from pipeline_plugin.operators.OSMExtractOperator import OSMExtractOperator


class PipelinePlugin(AirflowPlugin):
    name = "pipeline_plugin"  # does not need to match the package name
    operators = [HDXExtractOperator, HDXAdm0Operator, HDXAdm1Operator, HDXRoadsTransformOperator, OSMExtractOperator]
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