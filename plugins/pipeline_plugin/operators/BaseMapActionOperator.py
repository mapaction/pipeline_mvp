import json

from pipeline_plugin.utils.deep_inspection import get_function_information

from airflow.operators.python_operator import PythonOperator
from airflow.operators import BaseOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

from airflow.utils.decorators import apply_defaults


class MapActionKubernetesPodOperator(KubernetesPodOperator):
    @apply_defaults
    def __init__(self, method, arguments: dict, *args, **kwargs):
        function_name, function_module = get_function_information(method)
        arguments_json = json.dumps(arguments)
        environment_variables = {"FUNCTION_NAME": function_name,
                                 "FUNCTION_MODULE": function_module,
                                 "FUNCTION_ARGUMENTS": arguments_json}
        super().__init__(image="map-action-task",
                         env_vars=environment_variables,
                         *args,
                         **kwargs)


class MapActionPythonOperator(PythonOperator):
    @apply_defaults
    def __init__(self, method, arguments: dict, *args, **kwargs):
        super().__init__(python_callable=method,
                         op_kwargs=arguments,
                         *args,
                         **kwargs)

if False:
    MapActionOperator = MapActionKubernetesPodOperator
else:
    MapActionOperator = MapActionPythonOperator
