import json

import yaml


def load_yaml_file(file_address) -> dict:
    with open(file_address, "r") as yaml_file:
        try:
            yaml_dict = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    return yaml_dict


def compare(old_version: dict, new_version: dict, path=""):
    if type(old_version) == type(new_version):
        if isinstance(old_version, dict):
            for key, value in old_version.items():
                path = path + f" -> {key}"
                compare(value, new_version.get(key), path=(path))
        elif isinstance(old_version, list):
            old_version.sort()
            new_version.sort()
            if len(old_version) == len(new_version):
                for i in range(len(old_version)):
                    compare(old_version[i], new_version[i], path=path)
            else:
                print(f"{old_version} \n changed to \n{new_version}\nin [{path}]\n\n")
        else:
            if old_version != new_version:
                print(f"{old_version} \n changed to \n{new_version}\nin [{path}]\n\n")
    else:
        print(f"{old_version} \n changed to \n{new_version}\nin [{path}]\n\n")

old_version = load_yaml_file("./new_and_old_swagger_files/old.yaml")
new_version = load_yaml_file("./new_and_old_swagger_files/new.yaml")
changes = compare(old_version, new_version)
