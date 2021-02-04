import os
import json
import runpy


def load_graph(source_path):
    if os.path.lexists(source_path):
        return runpy.run_path(source_path)['graph']()
    else:
        raise Exception(f"No such graph file {source_path!r}")


class Database(dict):
    def __init__(self, path):
        super().__init__()
        self.path = path
        # load (TODO: Allow live reloading)
        if os.path.lexists(self.path):
            with open(self.path, 'r') as f:
                self.update(json.load(f))
    def save(self):
        _ensure(self.path)
        with open(self.path, 'w') as f:
            json.dump(self, f, indent=2)
    def __missing__(self, key):
        empty = {}
        self[key] = empty
        return empty


class Log:
    def __init__(self, path, load=False):
        self.path = path
        self.load = load
        self.new_lines = []
        if self.load:
            with open(self.path, 'r') as file:
                self.old_lines = [json.loads(line) for line in file]
        else:
            self.old_lines = []
    def lines(self):
        return self.old_lines + self.new_lines
    def log(self, id, time, event, data):
        self.new_lines.append({
            'id': id,
            'time': time,
            'event': event,
            'data': data,
        })
    def save(self):
        _ensure(self.path)
        with open(self.path, 'a') as file:
            for line in self.new_lines:
                print(line, file=file)


def _ensure(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

