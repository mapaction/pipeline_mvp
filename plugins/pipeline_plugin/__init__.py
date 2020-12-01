from airflow.plugins_manager import AirflowPlugin
from pipeline_plugin.operators.HDXExtractOperator import HDXExtractOperator
from pipeline_plugin.operators.Adm0Operator import Adm0Operator


class PipelinePlugin(AirflowPlugin):
    name = "pipeline_plugin"  # does not need to match the package name
    operators = [HDXExtractOperator, Adm0Operator]
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