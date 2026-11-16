import json
import os
import urllib.request

MODEL = "gemini-decision-1"
PROVIDERS = {
    "OPENROUTER_API_KEY": ("https://openrouter.ai/api/alpha/decisions", "google/", "state", "Authorization", "Bearer "),
    "GEMINI_API_KEY": ("https://generativelanguage.googleapis.com/v1beta/decisions", "", "input", "x-goog-api-key", ""),
}
ACTIONS = {
    "click": "Click or open an element such as a button or link.",
    "fill": "Type text into a field.",
    "press": "Press a key such as Enter in a field.",
}


def describe(element):
    kind = f"{element['tag']}[{element['type']}]" if element["type"] else element["tag"]
    return f"{kind} \"{element['label']}\""


def build_questions(elements):
    return {
        "action": {"type": "choice", "instructions": "Which action does the step ask for?", "criteria": ACTIONS},
        "element": {
            "type": "choice",
            "instructions": "Which page element should the step act on?",
            "criteria": {f"e{element['index']}": describe(element) for element in elements},
        },
    }


def read_answer(response):
    answers = response["answers"]
    return answers["action"]["choice"], int(answers["element"]["choice"][1:]), answers["element"]["confidence"]


def provider():
    for variable, settings in PROVIDERS.items():
        if os.environ.get(variable):
            return settings, os.environ[variable]
    raise RuntimeError("Set OPENROUTER_API_KEY or GEMINI_API_KEY")


def decide(instruction, elements, model=MODEL):
    (url, prefix, field, header, scheme), key = provider()
    body = {"model": prefix + model, field: f"Browser step: {instruction}", "questions": build_questions(elements)}
    request = urllib.request.Request(
        url, json.dumps(body).encode(), {header: scheme + key, "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return read_answer(json.load(response))
