import pytest
import os
from pathlib import Path

from dags.utils.config_parser import Config


def test_get_hdx_input_filename():
    config = Config(path=Path(os.getcwd()) / "dags" / "config")
    assert config.get_hdx_input_filename(country="yemen") == "bla"
