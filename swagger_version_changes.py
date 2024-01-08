import yaml


def load_yaml_file(file_address) -> dict:
    with open(file_address, "r") as yaml_file:
        try:
            yaml_dict = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    return yaml_dict

def compare(old_version: dict, new_version: dict):
    ...


old_version = load_yaml_file("./new_and_old_swagger_files/old.yaml")
new_version = load_yaml_file("./new_and_old_swagger_files/new.yaml")
compare(old_version, new_version)
