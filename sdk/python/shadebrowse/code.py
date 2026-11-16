import json


def to_code(action, selector):
    target = f"page.locator({json.dumps(selector)})"
    if action["action"] == "click":
        return f"{target}.click()"
    return f"{target}.{action['action']}({json.dumps(action['value'])})"
