"""
Module: utils.py

Contains helper functions for parsing and cleaning string outputs from the LLM,
specifically tailored to extract JSON blocks enclosed in markdown ticks.
"""

import re
import json


def extract_json(text: str) -> dict | None:
    """
    Searches a given text for a JSON payload structured inside markdown code blocks
    (```json ... ```) and attempts to parse it into a Python dictionary.

    Args:
        text (str): The raw text output from the language model.

    Returns:
        dict | None: The parsed dictionary if successful, or None if no valid
                     JSON block is found or parsing fails.
    """
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def clean_response(text: str) -> str:
    """
    Strips out any embedded JSON markdown blocks from a string, leaving only
    the conversational text. 

    Args:
        text (str): The raw text output from the language model.

    Returns:
        str: The cleaned text suitable for displaying to the user.
    """
    return re.sub(r"```json.*?```", "", text, flags=re.DOTALL).strip()
