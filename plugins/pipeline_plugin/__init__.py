# from airflow.plugins_manager import AirflowPlugin
#
# from airflow_logic.operators.DefaultTransformOperator import DefaultTransformOperator
# from airflow_logic.operators.HDXAdmTransformOperator import HDXAdmTransformOperator
# from airflow_logic.operators.HDXExtractOperator import HDXExtractOperator
# from airflow_logic.operators.OSMExtractOperator import OSMExtractOperator
#
#
# class PipelinePlugin(AirflowPlugin):
#     name = "pipeline_plugin"  # does not need to match the package name
#     operators = [
#         HDXExtractOperator,
#         HDXAdmTransformOperator,
#         OSMExtractOperator,
#         DefaultTransformOperator,
#     ]
#     sensors = []
#     hooks = []
#     executors = []
#     macros = []
#     admin_views = []
#     flask_blueprints = []
#     menu_links = []
#     appbuilder_views = []
#     appbuilder_menu_items = []
#     global_operator_extra_links = []
#     operator_extra_links = []
