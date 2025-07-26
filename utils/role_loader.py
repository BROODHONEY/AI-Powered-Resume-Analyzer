import json
import os

def load_roles(json_path = 'data/roles_keywords.json'):
    """
    Load job roles and their associated keywords from a JSON file.

    Args:
        json_path (str): Path to the JSON file containing roles and keywords.

    Returns:
        dict: A dictionary where keys are job roles and values are lists of keywords.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found at {json_path}")

    with open(json_path, 'r') as file:
        roles_keywords = json.load(file)

    return roles_keywords