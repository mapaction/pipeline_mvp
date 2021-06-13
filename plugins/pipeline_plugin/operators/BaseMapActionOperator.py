import json
from typing import Callable

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from pipeline_plugin.pipeline_config.config_parser import config
from pipeline_plugin.utils.deep_inspection import get_function_information


class MapActionKubernetesPodOperator(KubernetesPodOperator):
    @apply_defaults
    def __init__(self, method: Callable, arguments: dict, *args, **kwargs):
        function_name, function_module = get_function_information(method, **kwargs)
        arguments_json = json.dumps(arguments)
        environment_variables = {
            "FUNCTION_NAME": function_name,
            "FUNCTION_MODULE": function_module,
            "FUNCTION_ARGUMENTS": arguments_json,
            "GCP": "TRUE",
            "INSIDE_KUBERNETES_POD": "TRUE",
            "ENVIRONMENT": "PRODUCTION",
        }
        super().__init__(
            namespace="default",
            image=config.get_docker_image(),
            name=kwargs["task_id"],
            env_vars=environment_variables,
            *args,
            **kwargs
        )


class MapActionPythonOperator(PythonOperator):
    @apply_defaults
    def __init__(self, method: Callable, arguments: dict, *args, **kwargs):
        super().__init__(python_callable=method, op_kwargs=arguments, *args, **kwargs)


if config.use_kubernetes():
    MapActionOperator = MapActionKubernetesPodOperator
else:
    MapActionOperator = MapActionPythonOperator
