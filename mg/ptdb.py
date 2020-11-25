import os
import json

class Database(dict):
    def __init__(self, filename="ptdb.json"):
        super().__init__()
        self.filename = filename
        # load (TODO: Allow live reloading)
        if os.path.lexists(self.filename):
            with open(self.filename, 'r') as f:
                self.update(json.load(f))
    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self, f, indent=2)
    def __missing__(self, key):
        empty = {}
        self[key] = empty
        return empty
