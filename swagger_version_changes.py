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
    components_changes_dict = {}

    for old_schema, old_schema_detail in old_version["components"]["schemas"].items():
        if old_version["components"]["schemas"].get(old_schema):
            old_api_sorted_detail = json.dumps(old_schema_detail, sort_keys=True)
            new_api_sorted_detail = json.dumps(new_version["components"]["schemas"][old_schema], sort_keys=True)
            if old_api_sorted_detail != new_api_sorted_detail:
                components_changes_dict[f"#/components/schemas/{old_schema}"] = (
                    f"schema changed! -> #/components/schemas/{old_schema}\n")
            if any(component_change_dict_key in str(new_version["components"]["schemas"][old_schema]) for
                   component_change_dict_key in components_changes_dict.keys()):
                components_changes_dict[f"#/components/schemas/{old_schema}"] = (
                    f"schema changed! -> #/components/schemas/{old_schema}\n")
        else:
            components_changes_dict[f"#/components/schemas/{old_schema}"] = (
                f"schema deleted! -> #/components/schemas/{old_schema}\n")



    for old_api, old_api_detail in old_version["paths"].items():
        if new_version["paths"].get(old_api):
            old_api_sorted_detail = json.dumps(old_api_detail, sort_keys=True)
            new_api_sorted_detail = json.dumps(new_version["paths"][old_api], sort_keys=True)
            if old_api_sorted_detail != new_api_sorted_detail:
                changes.append(f"PATH CHANGED! api -> {old_api}\n")
            if any(component_change_dict_key in str(new_api_sorted_detail) for
                   component_change_dict_key in components_changes_dict.keys()):
                changes.append(f"PATH Component CHANGED! api -> {old_api}\n")
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
