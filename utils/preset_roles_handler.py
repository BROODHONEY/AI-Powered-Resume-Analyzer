
import json

def load_role_keywords(role):    
    """
    Load keywords for a specific job role from the predefined roles_keywords dictionary.

    Args:
        role (str): The job role for which to load keywords.

    Returns:
        list: A list of keywords associated with the job role.
    """
    roles_keywords = json.load(open('data/roles_keywords.json', 'r', encoding='utf-8'))
    return roles_keywords.get(role, [])

