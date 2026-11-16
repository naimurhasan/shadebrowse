import json
import os
import urllib.request

PROVIDERS = {
    "OPENROUTER_API_KEY": ("https://openrouter.ai/api/v1/chat/completions", "google/"),
    "GEMINI_API_KEY": ("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", ""),
}


def provider():
    for variable, (url, prefix) in PROVIDERS.items():
        if os.environ.get(variable):
            return url, prefix, os.environ[variable]
    raise RuntimeError("Set OPENROUTER_API_KEY or GEMINI_API_KEY")


def complete(messages, model):
    url, prefix, key = provider()
    body = json.dumps({"model": prefix + model, "messages": messages, "temperature": 0}).encode()
    request = urllib.request.Request(
        url, body, {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)["choices"][0]["message"]["content"]
