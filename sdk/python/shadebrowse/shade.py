from dataclasses import dataclass
from urllib.parse import urlsplit

from .cache import Cache
from .code import to_code
from .elements import collect
from .decision import MODEL, decide
from .value import extract_value


@dataclass
class Step:
    instruction: str
    action: dict
    selector: str
    code: str
    cached: bool


def cache_key(url, instruction):
    parts = urlsplit(url)
    return f"{parts.netloc}{parts.path} :: {instruction}"


class Shade:
    def __init__(self, page, cache="shade-steps.json", model=MODEL):
        self.page = page
        self.cache = Cache(cache)
        self.model = model

    def choose(self, instruction, elements):
        action, index, _ = decide(instruction, elements, self.model)
        return {"action": action, "index": index, "value": extract_value(instruction, action)}

    def plan(self, instruction):
        key = cache_key(self.page.url, instruction)
        saved = self.cache.get(key)
        if saved and self.page.locator(saved["selector"]).count():
            return Step(instruction, saved["action"], saved["selector"], saved["code"], True)
        elements = collect(self.page)
        action = self.choose(instruction, elements)
        selector = elements[action["index"]]["selector"]
        code = to_code(action, selector)
        self.cache.put(key, {"action": action, "selector": selector, "code": code})
        return Step(instruction, action, selector, code, False)

    def run(self, step):
        target = self.page.locator(step.selector).first
        if step.action["action"] == "click":
            target.click()
        else:
            getattr(target, step.action["action"])(step.action["value"])
        return step

    def do(self, instruction):
        return self.run(self.plan(instruction))
