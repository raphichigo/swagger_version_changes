import json

import yaml


def load_yaml_file(file_address) -> dict:
    with open(file_address, "r") as yaml_file:
        try:
            yaml_dict = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    return yaml_dict


def compare(old_version: dict, new_version: dict):
    changes = []
    for old_api, old_api_detail in old_version["paths"].items():
        if new_version["paths"].get(old_api):
            old_api_sorted_detail = json.dumps(old_api_detail, sort_keys=True)
            new_api_sorted_detail = json.dumps(new_version["paths"][old_api], sort_keys=True)
            if old_api_sorted_detail != new_api_sorted_detail:
                changes.append(f"PATH CHANGED! api -> {old_api}\n")
        else:
            changes.append(f"PATH DELETED! api -> {old_api}\n")

    new_paths = [path for path in new_version["paths"].keys() if path not in old_version["paths"].keys()]
    if new_paths:
        for new_path in new_paths:
            changes.append(f"NEW PATH ADDED! {new_path}\n")
    return changes


old_version = load_yaml_file("./new_and_old_swagger_files/old.yaml")
new_version = load_yaml_file("./new_and_old_swagger_files/new.yaml")
changes = compare(old_version, new_version)
for change in changes:
    print(change)
