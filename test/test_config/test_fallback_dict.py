import pytest

# from dags.utils.fallback_dict import FallbackDict


def test_random():
    assert True


# def test_get_from_custom_values():
#     default = {"a": {"b": 1}}
#     custom = {"a": {"b": 2}}
#     fallback_dict = FallbackDict(default_values=default, custom_values=custom)
#     assert fallback_dict["a"]["b"] == 2


# def test_get_from_default_values():
#     default = {"a": {"b": 1}}
#     custom = {"a": {"c": 2}}
#     fallback_dict = FallbackDict(default_values=default, custom_values=custom)
#     assert fallback_dict["a"]["b"] == 1
