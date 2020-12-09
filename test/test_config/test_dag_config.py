import pytest


def test_get_hdx_adm_address(config):
    address = config.get_hdx_adm_address(country="yemen")
    assert address == "yemen-admin-boundaries"

