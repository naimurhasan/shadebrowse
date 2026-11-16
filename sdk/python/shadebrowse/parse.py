import json
import re

ACTIONS = {"click", "fill", "press"}


def parse_action(text):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(f"No JSON in model reply: {text!r}")
    action = json.loads(match.group(0))
    if action.get("action") not in ACTIONS or not isinstance(action.get("index"), int):
        raise ValueError(f"Unusable action: {action}")
    return action
