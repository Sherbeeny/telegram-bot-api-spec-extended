import json


def merge_json_files(file1, file2, output_file):
    """
    Merges two JSON files into a single file.
    """
    with open(file1, "r") as f1:
        data1 = json.load(f1)
    with open(file2, "r") as f2:
        data2 = json.load(f2)

    merged_data = {**data1, **data2}

    with open(output_file, "w") as f:
        json.dump(merged_data, f, indent=2)

    with open(output_file.replace(".json", ".min.json"), "w") as f:
        json.dump(merged_data, f, separators=(",", ":"))


if __name__ == "__main__":
    merge_json_files("api.json", "extensions.json", "spec-extended.json")
