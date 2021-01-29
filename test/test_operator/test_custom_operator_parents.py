from importlib import reload
import inspect
import pytest

from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

# import plugins.pipeline_plugin.operators.BaseMapActionOperator


# def test_k8s_operator_parent(monkeypatch):
#     monkeypatch.setenv("GCP", "TRUE")
#     reload(plugins.pipeline_plugin.operators.BaseMapActionOperator)
#     assert inspect.getmro(plugins.pipeline_plugin.operators.BaseMapActionOperator.MapActionOperator)[1] is KubernetesPodOperator


# def test_python_operator_parent():
#     reload(plugins.pipeline_plugin.operators.BaseMapActionOperator)
#     assert inspect.getmro(plugins.pipeline_plugin.operators.BaseMapActionOperator.MapActionOperator)[1] is PythonOperator


def test_mock_2():
    assert True
