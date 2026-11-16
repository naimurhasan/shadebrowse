SYSTEM = (
    "You turn one plain-English browser step into one action on one element. "
    "Reply with JSON only: {\"action\": \"click\" | \"fill\" | \"press\", \"index\": <element index>, \"value\": <text or key, or null>}. "
    "Use fill to type text into a field and press for a key such as Enter."
)


def describe(element):
    kind = f"{element['tag']}[{element['type']}]" if element["type"] else element["tag"]
    return f"{element['index']}: {kind} \"{element['label']}\""


def build_messages(instruction, elements):
    listing = "\n".join(describe(element) for element in elements)
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Elements:\n{listing}\n\nStep: {instruction}"},
    ]
