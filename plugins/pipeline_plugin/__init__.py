from airflow.plugins_manager import AirflowPlugin

from pipeline_plugin.operators.HDXExtractOperator import HDXExtractOperator
from pipeline_plugin.operators.Adm0Operator import Adm0Operator
from pipeline_plugin.operators.Adm1Operator import Adm1Operator
from pipeline_plugin.operators.RoadsTransformOperator import RoadsTransformOperator


class PipelinePlugin(AirflowPlugin):
    name = "pipeline_plugin"  # does not need to match the package name
    operators = [HDXExtractOperator, Adm0Operator, Adm1Operator, RoadsTransformOperator]
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