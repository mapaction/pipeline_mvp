import json
import os

import pytest

from .requests_api import download_url


URLS = (
    "https://file-examples-com.github.io/uploads/2017/02/file_example_XML_24kb.xml",
    "https://file-examples-com.github.io/uploads/2017/02/file_example_CSV_5000.csv",
    "https://file-examples-com.github.io/uploads/2017/02/file_example_JSON_1kb.json",
    "https://file-examples-com.github.io/uploads/2017/02/zip_2MB.zip",
)


@pytest.mark.parametrize("url", URLS)
def test_downloaded_files_are_not_empty(tmp_path, url):
    tmp_file_name = tmp_path / "file_example"
    download_url(url, tmp_file_name)
    assert os.path.exists(tmp_file_name)
    assert os.path.isfile(tmp_file_name)


JSON_EXAMPLE_DICT_ITEMS = (
    {"name": "Afghanistan", "isoCode": "AF"},
    {"name": "Gibraltar", "isoCode": "GI"},
    {"name": "United Kingdom", "isoCode": "GB"},
    {"name": "Vietnam", "isoCode": "VN"},
    {"name": "Zimbabwe", "isoCode": "ZW"},
)


def test_downloaded_file_is_correct(tmp_path):
    url = URLS[2]
    tmp_file_name = tmp_path / "json_file_example"
    download_url(url, tmp_file_name)
    with open(tmp_file_name, "r") as file:
        data = json.load(file)["countries"]
        for item in JSON_EXAMPLE_DICT_ITEMS:
            assert item in data
