from .yaml_api import parse_yaml

YAML_CONTENT = """
dirs:
  raw_data: raw_data
  processed_data: processed_data
  schemas: schemas
    """


def test_yaml_api(tmp_path):
    filepath = tmp_path / "yaml_sample.yaml"
    with open(filepath, "w") as file:
        file.write(YAML_CONTENT)
    yaml_dict = parse_yaml(filepath)
    assert "dirs" in yaml_dict
    for elem in ("raw_data", "processed_data", "schemas"):
        assert elem in yaml_dict["dirs"]
        assert yaml_dict["dirs"][elem] == elem
