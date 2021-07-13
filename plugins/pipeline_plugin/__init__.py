from airflow.plugins_manager import AirflowPlugin

from pipeline_plugin.operators.DefaultTransformOperator import DefaultTransformOperator
from pipeline_plugin.operators.HDXAdmTransformOperator import HDXAdmTransformOperator
from pipeline_plugin.operators.HDXExtractOperator import HDXExtractOperator
from pipeline_plugin.operators.OSMExtractOperator import OSMExtractOperator


class PipelinePlugin(AirflowPlugin):
    name = "pipeline_plugin"  # does not need to match the package name
    operators = [
        HDXExtractOperator,
        HDXAdmTransformOperator,
        OSMExtractOperator,
        DefaultTransformOperator,
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
