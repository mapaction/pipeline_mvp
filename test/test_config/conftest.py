import pytest
import os
from pathlib import Path

from dags.utils.config_parser import Config


@pytest.fixture
def config():
    config_instance = Config(path=Path(os.getcwd()) / "test" / "test_config")
    return config_instance
