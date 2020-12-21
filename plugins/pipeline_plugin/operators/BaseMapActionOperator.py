import json
import os
from typing import Callable

from pipeline_plugin.utils.deep_inspection import get_function_information

from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

from airflow.utils.decorators import apply_defaults


class MapActionKubernetesPodOperator(KubernetesPodOperator):
    @apply_defaults
    def __init__(self, method: Callable, arguments: dict, *args, **kwargs):
        function_name, function_module = get_function_information(method, **kwargs)
        arguments_json = json.dumps(arguments)
        environment_variables = {"FUNCTION_NAME": function_name,
                                 "FUNCTION_MODULE": function_module,
                                 "FUNCTION_ARGUMENTS": arguments_json}
        super().__init__(image="mapaction-task-image",
                         name=kwargs["task_id"],
                         env_vars=environment_variables,
                         *args,
                         **kwargs)


class MapActionPythonOperator(PythonOperator):
    @apply_defaults
    def __init__(self, method: Callable, arguments: dict, *args, **kwargs):
        super().__init__(python_callable=method,
                         op_kwargs=arguments,
                         *args,
                         **kwargs)


if os.getenv("ENVIRONMENT") == "GCP":
    MapActionOperator = MapActionKubernetesPodOperator
else:
    MapActionOperator = MapActionPythonOperator