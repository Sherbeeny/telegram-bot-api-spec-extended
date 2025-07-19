"""
This module contains a function for merging two JSON files.
"""

import json


def merge_json_files(file1, file2, output_file):
    """
    Merges two JSON files into a single file.

    The contents of the second file are merged into the first file.
    If there are any duplicate keys, the values from the second file
    will overwrite the values from the first file.

    Args:
        file1 (str): The path to the first JSON file.
        file2 (str): The path to the second JSON file.
        output_file (str): The path to the output JSON file.
    """
    # Open and load the two JSON files
    with open(file1, "r") as f1:
        data1 = json.load(f1)
    with open(file2, "r") as f2:
        data2 = json.load(f2)

    # Merge the two dictionaries
    merged_data = {**data1, **data2}

    # Write the merged data to the output file
    with open(output_file, "w") as f:
        json.dump(merged_data, f, indent=2)

    # Write the merged data to a minified output file
    with open(output_file.replace(".json", ".min.json"), "w") as f:
        json.dump(merged_data, f, separators=(",", ":"))


if __name__ == "__main__":
    # Merge the api.json and extensions.json files into spec-extended.json
    merge_json_files("api.json", "extensions.json", "spec-extended.json")
