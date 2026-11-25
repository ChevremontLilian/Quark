import json
import os

if __package__:
    from .config import MEMORY_FILE
else:
    from config import MEMORY_FILE


class Memory:
    def __init__(self, path=MEMORY_FILE):
        self.path = path
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_memory(self, key):
        return self.data.get(key, None)

    def set_memory(self, key, value):
        self.data[key] = value
        self._save()

    def delete_memory(self, key):
        if key in self.data:
            del self.data[key]
            self._save()

    def all_memories(self):
        return self.data.copy()
