"""
Module: database.py

Handles basic data persistence operations to save extracted candidate records
to a local JSON file designated in the config.
"""

import json
from datetime import datetime

from config import DB_PATH


def _read_file() -> list:
    """
    Internal helper to read the contents of the database file.

    Returns:
        list: A list of dictionaries representing existing candidates, 
              or an empty list if the file does not exist or fails to parse.
    """
    if not DB_PATH.exists():
        return []
    try:
        with DB_PATH.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return []


def _write_file(records: list) -> None:
    """
    Internal helper to write the list of candidate records back to the database file.

    Args:
        records (list): The list of dictionaries to persist.
    """
    with DB_PATH.open("w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=4, ensure_ascii=False)


def load_candidates() -> list:
    """
    Public method to retrieve all candidate records from storage.

    Returns:
        list: All saved candidate records.
    """
    return _read_file()


def save_candidate(candidate_info: dict) -> bool:
    """
    Appends a new candidate record to the existing JSON database, injecting
    a current timestamp into the payload.

    Args:
        candidate_info (dict): The extracted candidate data from the LLM.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    records = _read_file()
    # Inject current timestamp when saving the record
    candidate_info = {**candidate_info, "timestamp": datetime.now().isoformat()}
    records.append(candidate_info)
    try:
        _write_file(records)
        return True
    except OSError:
        return False


def clear_candidates() -> None:
    """
    Wipes the database file entirely. Useful for testing or resetting state.
    """
    _write_file([])
