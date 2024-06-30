import logging
import json
from collections import defaultdict


def read_json(file_path: str) -> dict:
    """
    Reads a JSON file and returns its content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        logging.error(f"File not found error: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")
        raise
    except Exception as e:
        logging.error(f"Error reading JSON file: {e}")
        raise


def analyze_structure(data, parent_key='', key_structure=None):
    """
    Analyzes the structure of the JSON data recursively, capturing the key structure.
    """
    if key_structure is None:
        key_structure = defaultdict(set)

    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            key_structure[parent_key].add(key)
            analyze_structure(value, full_key, key_structure)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            analyze_structure(item, parent_key, key_structure)

    return key_structure


def print_structure(key_structure):
    """
    Prints the key structure in a readable format.
    """
    for parent_key, keys in key_structure.items():
        indent = parent_key.count('.') * '  '
        print(f"{indent}{parent_key if parent_key else 'root'}: {sorted(keys)}")


if __name__ == "__main__":
    # Replace 'path_to_your_json_file.json' with the actual path to your JSON file.
    json_data = read_json('theme/static/data/drug-label-0001-of-0012.json')

    if json_data:
        key_structure = analyze_structure(json_data)
        print_structure(key_structure)
