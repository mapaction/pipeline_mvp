from importlib import reload
import inspect
import pytest
import json

from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

import plugins.pipeline_plugin.operators.BaseMapActionOperator

from test.test_operator.method_passed_to_operator import operator_method


def test_python_operator():
    reload(plugins.pipeline_plugin.operators.BaseMapActionOperator)
    arguments = {"argument_1": 2, "argument_2": "two"}
    operator = plugins.pipeline_plugin.operators.BaseMapActionOperator.MapActionOperator(task_id="test_mapaction_operator",
                                                                                         method=operator_method,
                                                                                         arguments=arguments,
                                                                                         base_folder="test/")
    assert operator.python_callable is operator_method
    assert operator.op_kwargs == arguments


def test_k8s_operator(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "GCP")
    reload(plugins.pipeline_plugin.operators.BaseMapActionOperator)
    arguments = {"argument_1": 2, "argument_2": "two"}
    operator = plugins.pipeline_plugin.operators.BaseMapActionOperator.MapActionOperator(task_id="test_mapaction_operator",
                                                                                         method=operator_method,
                                                                                         arguments=arguments,
                                                                                         base_folder="test/")
    k8s_arguments = operator.env_vars["FUNCTION_ARGUMENTS"]
    k8s_function_name = operator.env_vars["FUNCTION_NAME"]
    k8s_function_module = operator.env_vars["FUNCTION_MODULE"]
    assert k8s_arguments == json.dumps(arguments)
    assert k8s_function_name == "operator_method"
    assert k8s_function_module == "test_operator.method_passed_to_operator"
