import re

PATTERNS = {
    "fill": [r"[\"'](.+?)[\"']", r"^(?:type|enter|fill in|fill|write|input)\s+(.+?)\s+(?:into|in|on)\s+"],
    "press": [r"^press\s+(?:the\s+)?(\S+)"],
}


def extract_value(instruction, action):
    for pattern in PATTERNS.get(action, []):
        match = re.search(pattern, instruction.strip(), re.I)
        if match:
            return match.group(1)
    return None
