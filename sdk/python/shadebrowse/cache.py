import json
from pathlib import Path


class Cache:
    def __init__(self, path):
        self.path = Path(path)
        self.entries = json.loads(self.path.read_text()) if self.path.exists() else {}

    def get(self, key):
        return self.entries.get(key)

    def put(self, key, value):
        self.entries[key] = value
        self.path.write_text(json.dumps(self.entries, indent=2) + "\n")
